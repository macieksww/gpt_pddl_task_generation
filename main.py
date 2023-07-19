import os
import openai
import tarfile
import re
import signal
import inspect
import sys
import copy
import json
from db_connector import DBConnector
from helpful_functions import save_to_file, str_to_json, read_file
from planutils_manager import copy_to_docker_container, execute_planner, copy_from_docker_container
from process_plan import extract_pddl_problem, check_if_planner_succeeded, extract_plan_from_planner_output, rate_plan
from gpt_prompts import GPTPrompts
from exceptions import TimeoutException, AttributeErrorException, ExectionHandlers

pddl_version = "PDDL 1.2"
planner_type = "enhsp"
debug = False
openai.api_key = os.getenv('OPENAPI_KEY')
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
path_to_ask_for_capabilities_context = \
'gpt_conversations/ask_for_capabilities.json'
path_to_ask_if_robot_can_perform_task_context = \
'gpt_conversations/ask_if_robot_can_perform_task.json'
path_to_followup_conversation_context = \
'gpt_conversations/followup_conversation.json'
path_to_initial_conversation_context = \
'gpt_conversations/init_conversation.json'
path_to_example_problem_files = \
'pddl_files/example_problem_files'
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
    function_name = copy.deepcopy(sys._getframe().f_code.co_name)
    signal.signal(signal.SIGALRM, ExectionHandlers.timeout_handler)
    max_attempts = 5
    current_attempt = 0
    response_received = False
    timeout_const = 30
    timeout = len(messages)*timeout_const
    while not response_received and current_attempt < max_attempts:
        signal.alarm(timeout)  
        function_name = copy.deepcopy(sys._getframe().f_code.co_name)
        print("Attempt to prompt GPT: " + str(current_attempt))
        try:  
            response = openai.ChatCompletion.create(model='gpt-3.5-turbo-16k',
                                                    messages=messages,
                                                    max_tokens = 1024,
                                                    temperature = 0.8)    
        except openai.error.InvalidRequestError as e:
            print(e)
            current_attempt += 1
        except TimeoutError as e:
            print(e)
            signal.alarm(0)  
            current_attempt += 1
        else:
            response_received = True
            finish_reason = response['choices'][0]['finish_reason']
            return response.choices[0].message.content, messages
    return None, None


def ask_chat_one_by_one(messages):
    function_name = copy.deepcopy(sys._getframe().f_code.co_name)
    so_far_asked_questions_and_gpt_answers = []
    message_iterator = 0
    timeout_const = 30
    for message in messages:
        if debug:
            print(so_far_asked_questions_and_gpt_answers)
        signal.signal(signal.SIGALRM, ExectionHandlers.timeout_handler)
        max_attempts = 5
        current_attempt = 0
        response_received = False
        while not response_received and current_attempt < max_attempts:
            signal.alarm(timeout_const)  
            function_name = copy.deepcopy(sys._getframe().f_code.co_name)
            print("Attempt to prompt GPT: " + str(current_attempt))
            try:  
                so_far_asked_questions_and_gpt_answers.append(messages[message_iterator])
                response = openai.ChatCompletion.create(model='gpt-3.5-turbo-16k',
                                                        messages=so_far_asked_questions_and_gpt_answers,
                                                        max_tokens = 1024,
                                                        temperature = 0.8)
            except openai.error.InvalidRequestError as e:
                print(e)
                current_attempt += 1
            except TimeoutError as e:
                print(e)
                signal.alarm(0)  
                current_attempt += 1
            else:
                response_received = True
                so_far_asked_questions_and_gpt_answers.append(
                    {
                        'role': 'assistant',
                        'content': response.choices[0].message.content
                    }
                )
                message_iterator += 1
                if message_iterator == len(messages):
                    final_response = response.choices[0].message.content
                    finish_reason = response['choices'][0]['finish_reason']
                    return response.choices[0].message.content, so_far_asked_questions_and_gpt_answers
    return None, None

def check_if_robot_can_perform_requested_task(args):
    gpt_prompts = GPTPrompts(args)
    messages = gpt_prompts.create_check_if_robot_can_perform_requested_task_prompt()
    robot_can_perform_commanded_task = None
    while robot_can_perform_commanded_task is None:
        response, conversation_context = ask_chat(messages)
        robot_can_perform_commanded_task = process_gpt_can_robot_perform_commanded_task_response(response)
    with open(path_to_ask_if_robot_can_perform_task_context, 'w') as f:
        json.dump(conversation_context, f)
    return robot_can_perform_commanded_task
    
def initial_conversation(args):
    gpt_prompts = GPTPrompts(args)
    """
    Conducting initial conversation, including telling GPT
    what it will be working on, what the system is requested to do
    Making sure that GPT understands well what the requested task is
    It may be useful in the case of any mistakes in retrieving the
    request from the user (like spelling mistakes)
    """
    messages = gpt_prompts.create_initial_conversation_prompt(args)
    response, conversation_context = ask_chat_one_by_one(messages)
    if not response:
        return None, None
    """
    Giving problem files examples to the GPT, to make LLM 
    perform "in-context" learning
    """
    messages = gpt_prompts.give_examples_of_problem_files_prompt(args)
    for message in messages:
        conversation_context.append(message)
    response, conversation_context = ask_chat(conversation_context)
    if not response:
        return None, None
    """
    Telling GPT what the task request is. Asking to give list of 
    actions (in natural language) that are needed to perform this task 
    """
    messages = gpt_prompts.provide_gpt_with_the_task_request_prompt(args)
    for message in messages:
        conversation_context.append(message)
    response, conversation_context = ask_chat(conversation_context)
    if not response:
        return None, None
    """
    Processing the output from GPT, about how it understands the 
    request to the system. Reprompting GPT, including previous 
    conversation context
    """    
    # requested_task_in_gpt_interpretation = str(conversation_context[len(conversation_context)-1]['content'])
    requested_task_in_gpt_interpretation = ''
    messages = gpt_prompts.ask_to_create_problem_pddl_file(requested_task_in_gpt_interpretation)
    for message in messages:
        conversation_context.append(message)
    """
    Using ask_chat instead ask_chat_one_by_one in order to limit the prompts
    sent to GPT. The context is loaded in conversation context. No need to 
    recreate the whole conversation
    """
    response, conversation_context = ask_chat(conversation_context)
    if not response:
        return None, None
    save_to_file(response, path_to_unprocessed_gpt_domain_problem_output)
    extract_pddl_problem(path_to_gpt_problem_output, path_to_unprocessed_gpt_domain_problem_output)
    with open(path_to_initial_conversation_context, 'w') as f:
        json.dump(conversation_context, f)
    return response, conversation_context

def followup_conversation(args):
    conversation_context = args['conversation_context']
    planner_output = args['planner_output']
    gpt_prompts = GPTPrompts(args)
    messages = gpt_prompts.create_info_about_wrong_pddl_problem_definition_prompt(planner_output)
    for message in messages:
        conversation_context.append(message)
    """
    Using ask_chat instead ask_chat_one_by_one in order to limit the prompts
    sent to GPT. The context is loaded in conversation context. No need to 
    recreate the whole conversation
    """
    response, conversation_context = ask_chat(conversation_context)
    if not response:
        return None, None
    save_to_file(response, path_to_unprocessed_gpt_domain_problem_output)
    extract_pddl_problem(path_to_gpt_problem_output, path_to_unprocessed_gpt_domain_problem_output)
    with open(path_to_followup_conversation_context, 'w') as f:
        json.dump(conversation_context, f)
    return response, conversation_context

def pddl_problem_conversation(args):
    gpt_generated_domain_and_problem_correct = False
    first_plan_domain_and_problem_request = True
    max_attempts = 5
    attempts_counter = 0
    print('Initial conversation, asking GPT to create planning problem file.')
    while not gpt_generated_domain_and_problem_correct and attempts_counter < max_attempts:
        print('Attempt: ' + str(attempts_counter) + ' of generating problem file by GPT.')
        if first_plan_domain_and_problem_request:
            response, conversation_context = initial_conversation(args)
            args['conversation_context'] = conversation_context
            print('GPT generated planning problem.')
            print(response)
        else:
            print('GPT failed while generating planning problem.')
            print('Fetching the PDDL error message.')
            # with open(path_to_planner_output) as f:
            #     planner_output = f.read()
            planner_output = read_file(path_to_planner_output, mode='r')
            args['planner_output'] = planner_output
            print('Conducting a followup conversation.')
            followup_conversation(args)
        first_plan_domain_and_problem_request = False
        print('Copying domain file to planutils container.')
        copy_to_docker_container(path_to_gpt_domain_output, planutils_container_name)
        print('Copying problem file to planutils container.')
        copy_to_docker_container(path_to_gpt_problem_output, planutils_container_name)
        print('Executing planner.')
        execute_planner(planutils_container_name, planner_type)
        print('Copying the planner output to host.')
        copy_from_docker_container(planutils_container_name)
        print('Checking if planner succeeded or failed.')
        gpt_generated_domain_and_problem_correct = check_if_planner_succeeded(path_to_planner_output, planner_type)
        if not gpt_generated_domain_and_problem_correct:
            print("GPT generated planning domain and problem are incorrectly defined. Planner could not find plan. Followup discussion will be performed.")
        else:
            print("GPT generated planning domain and problem are correctly defined. Plan found, system proceeds to real-life task testing.")
            return True
        attempts_counter += 1
    return False

def ask_for_capabilities_importances_for_commanded_task(args):
    gpt_prompts = GPTPrompts(args)
    capabilities_importances_pattern = r'\bcapabilities_importances\s=\s{(\n.*)*}'
    json_object_created = False
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
    messages = gpt_prompts.create_ask_for_capabilities_importances_for_commanded_task_prompt(args)
    """
    we ask the chat to produce a json-like dict with rates of every skill
    the robot's system has to be later able to rate the produced plan (planning problem)
    while not len(matches) and attempts_counter < max_attempts:
    """
    while attempts_counter < max_attempts and not json_object_created:
        print("Attempt to prompt GPT: " + str(attempts_counter))
        """
        Conducting a whole conversation in a one-by-one style.
        No previous conversation context is loaded.
        """
        response, conversation_context = ask_chat_one_by_one(messages)
        if not response:
            return None, None
        matches = re.findall(capabilities_importances_pattern, response)
        if len(matches):
            capabilities_importances_json = str_to_json(response)
            if capabilities_importances_json:
                with open(path_to_ask_for_capabilities_context, 'w') as f:
                    json.dump(conversation_context, f)
                return capabilities_importances_json
            else:
                attempts_counter += 1
        else:
            attempts_counter += 1

def main():
    dbc = DBConnector()
    task_request = input('What would you like the system to do: ')
    print('Fetching the tasks that the system can perform from DB.')
    tasks_system_can_perform = dbc.get_tasks_system_can_perform()
    args = {'tasks_system_can_perform': tasks_system_can_perform,
            'planner_type': planner_type,
            'pddl_version': pddl_version,
            'task_request': task_request,
            'domain_path': path_to_gpt_domain_output,
            'problem_path': path_to_gpt_problem_output,
            'example_problems_path': path_to_example_problem_files}
    # taking the request to learn/perform a new task
    print('Checking if the system already knows how to perform the commanded task.')
    robot_can_perform_commanded_task = check_if_robot_can_perform_requested_task(args)
    if robot_can_perform_commanded_task:
        print("Robot can perform commanded task.")
        return
    else:
        print('Robot cannot perform commanded task.')
    gpt_correctly_generated_problem = pddl_problem_conversation(args)
    if gpt_correctly_generated_problem:
        print('Extracting planner output.')
        extract_plan_from_planner_output(path_to_planner_output, path_to_plan, args['planner_type'])
        print('Asking GPT for robot capabilities importances.')
        capabilities_importances = ask_for_capabilities_importances_for_commanded_task(args)
        print('Rating the generated plan, based on capabilities importances.')
        plan_rate = rate_plan(path_to_plan, capabilities_importances)
        print('Plan rate:' + str(plan_rate))
        return
    else:
        print("GPT couldn't generate PDDL problem for commanded task.")
        return
 
if __name__ == "__main__":
    main()