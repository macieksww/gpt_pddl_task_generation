import os
import openai
import tarfile
import re
import signal
import inspect
from db_connector import DBConnector
from helpful_functions import save_to_file, str_to_json
from planutils_manager import copy_to_docker_container, execute_planner, copy_from_docker_container
from process_plan import extract_pddl_problem, check_if_planner_succeeded, extract_plan_from_planner_output, rate_plan
from gpt_prompts import GPTPrompts
from exceptions import TimeoutException, ExectionHandlers

pddl_version = "PDDL 1.2"
planner_type = "popf"
debug = False
openai.api_key = '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'
models = openai.Model.list()['data']
path_to_unprocessed_gpt_domain_problem_output = \
'gpt_generated_files/unprocessed_gpt_domain_problem.pddl'
path_to_gpt_domain_output = \
'gpt_generated_files/gpt_domain.pddl'
path_to_gpt_problem_output = \
'gpt_generated_files/gpt_problem.pddl'
path_to_planner_output = \
'gpt_generated_files/planner_output.pddl'
path_to_plan = \
'gpt_generated_files/plan.pddl'
planutils_container_name = \
'crazy_yalow:/'

if debug:
    for model in models:
        print(model['id'])

def process_gpt_can_robot_perform_commanded_task_response(response):
    no_pattern = re.compile(r"no", re.IGNORECASE)
    yes_pattern = re.compile(r"yes", re.IGNORECASE)
    if no_pattern.match(response):
        return False
    if yes_pattern.match(response):
        return True
    else:
        return None
        
def ask_chat(messages):
    # model="gpt-3.5-turbo-16k"
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(10)  
    try:  
        response = openai.ChatCompletion.create(model='gpt-3.5-turbo',
                                                messages=messages,
                                                max_tokens = 1024,
                                                temperature = 0.8)    
    except TimeoutException(inspect.currentframe().f_code.co_name):
        continue
    else:
        finish_reason = response['choices'][0]['finish_reason']
        return response.choices[0].message.content, messages


def ask_chat_one_by_one(messages):
    so_far_asked_questions_and_gpt_answers = []
    message_iterator = 0
    for message in messages:
        if debug:
            print(so_far_asked_questions_and_gpt_answers)
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(10)  
        try:  
            so_far_asked_questions_and_gpt_answers.append(messages[message_iterator])
            response = openai.ChatCompletion.create(model='gpt-3.5-turbo-16k',
                                                    messages=so_far_asked_questions_and_gpt_answers,
                                                    max_tokens = 1024,
                                                    temperature = 0.8)
        except TimeoutException(inspect.currentframe().f_code.co_name):
            continue
        else:
            so_far_asked_questions_and_gpt_answers.append(
                {
                    'role': 'assistant',
                    'content': response.choices[0].message.content
                }
            )
            message_iterator += 1
            if message_iterator == len(messages):
                break
    final_response = response.choices[0].message.content
    finish_reason = response['choices'][0]['finish_reason']
    return response.choices[0].message.content, so_far_asked_questions_and_gpt_answers

def check_if_robot_can_perform_requested_task(args):
    gpt_prompts = GPTPrompts(args)
    messages = gpt_prompts.create_check_if_robot_can_perform_requested_task_prompt()
    robot_can_perform_commanded_task = None
    while robot_can_perform_commanded_task is None:
        response, _ = ask_chat(messages)
        robot_can_perform_commanded_task = process_gpt_can_robot_perform_commanded_task_response(response)
    return robot_can_perform_commanded_task
    
def initial_conversation(args):
    gpt_prompts = GPTPrompts(args)
    messages = gpt_prompts.create_initial_conversation_prompt()
    response, conversation_context = ask_chat_one_by_one(messages)
    save_to_file(response, path_to_unprocessed_gpt_domain_problem_output)
    extract_pddl_problem(path_to_gpt_problem_output, path_to_unprocessed_gpt_domain_problem_output)
    return response, conversation_context

def followup_conversation(args):
    conversation_context = args['conversation_context']
    gpt_prompts = GPTPrompts(args)
    messages = gpt_prompts.create_info_about_wrong_pddl_problem_definition_prompt()
    conversation_context.append(messages)
    response, conversation_context = ask_chat_one_by_one(conversation_context)
    save_to_file(response, path_to_unprocessed_gpt_domain_problem_output)
    extract_pddl_problem(path_to_gpt_problem_output, path_to_unprocessed_gpt_domain_problem_output)
    return response, conversation_context

def ask_for_capabilities_importances_for_commanded_task(args):
    capabilities_importances_pattern = r'\bcapabilities_importances\s=\s{(\n.*)*}'
    matches = []
    max_attempts = 5
    attempts_counter = 0
    reminder_to_chat_about_desired_output_format = {
        'role': 'user',
        # 'content': ' Remembert to name the json-like struct that you will \
        # return as "capabilities_importances" the output should only be: \
        # capabilities_importances = {"ability_id": grade, "ability_id": grade ...}'
        'content':''
    },
    
    gpt_prompts = GPTPrompts(args)
    messages = gpt_prompts.create_ask_for_capabilities_importances_for_commanded_task_prompt()
    """
    we ask the chat to produce a json-like dict with rates of every skill
    the robot's system has to be later able to rate the produced plan (planning problem)
    while not len(matches) and attempts_counter < max_attempts:
    """
    
    #     response, conversation_context = ask_chat(messages)
    #     matches = re.findall(capabilities_importances_pattern, response)
    #     # if the chat didn't produce a correct response (as stated in the request)
    #     # a message is added to the previous conversation context that reminds it
    #     # about how the output should look like
    #     # if attempts_counter == 1:
    #     #     messages.append(reminder_to_chat_about_desired_output_format)
    #     attempts_counter += 1
    response, conversation_context = ask_chat(messages)
    matches = re.findall(capabilities_importances_pattern, response)
    capabilities_importances_json = str_to_json(response)
    return capabilities_importances_json


def main():
    task_request = input("What would you like the system to do: ")
    dbc = DBConnector()
    tasks_system_can_perform = dbc.get_tasks_system_can_perform()
    args = {}
    args['tasks_system_can_perform'] = tasks_system_can_perform
    args['pddl_version'] = pddl_version
    args['task_request'] = task_request
    # taking the request to learn/perform a new task
    robot_can_perform_commanded_task = check_if_robot_can_perform_requested_task(args)
    if robot_can_perform_commanded_task:
        print("Robot can perform commanded task.")
        return
    else:
        print("Robot cannot perform commanded task.")
    gpt_generated_domain_and_problem_correct = False
    first_plan_domain_and_problem_request = True
    max_attempts = 5
    attempts_so_far = 0
    while not gpt_generated_domain_and_problem_correct and attempts_so_far < max_attempts:
        if first_plan_domain_and_problem_request:
            response, conversation_context = initial_conversation(args)
            args['conversation_context'] = conversation_context
            print("GPT generated planning domain and problem.")
            print(response)
        else:
            followup_conversation(args)
        first_plan_domain_and_problem_request = False
        copy_to_docker_container(path_to_gpt_domain_output, planutils_container_name)
        copy_to_docker_container(path_to_gpt_problem_output, planutils_container_name)
        execute_planner(planutils_container_name, planner_type)
        copy_from_docker_container(planutils_container_name)
        gpt_generated_domain_and_problem_correct = check_if_planner_succeeded(path_to_planner_output, planner_type)
        if not gpt_generated_domain_and_problem_correct:
            print("GPT generated planning domain and problem are incorrectly defined. Planner could not find plan. Followup discussion will be performed.")
        else:
            print("GPT generated planning domain and problem are correctly defined. Plan found, system proceeds to real-life task testing.")
        attempts_so_far += 1
    extract_plan_from_planner_output(path_to_planner_output, path_to_plan)
    capabilities_importances = ask_for_capabilities_importances_for_commanded_task(args)
    plan_rate = rate_plan(path_to_plan, capabilities_importances)
    print("PLAN RATE")
    print(plan_rate)

 
if __name__ == "__main__":
    main()