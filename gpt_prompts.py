from process_plan import extract_actions_from_domain
from helpful_functions import read_file
import os

class GPTPrompts:
    def __init__(self, args):
        self.initial_conversation_prompt = ''
        self.followup_conversation_prompt = ''
        self.ask_for_capabilities_importances_for_commanded_task_prompt = ''
        self.check_if_robot_can_perform_requested_task_prompt = ''
        self.args = args
        self.tasks_system_can_perform = args['tasks_system_can_perform']
        self.task_request = args['task_request']
        self.pddl_version = args['pddl_version']
    
    def create_initial_conversation_prompt(self, args):
        # with open('pddl_files/domain.pddl', 'r') as domain_file:
        #     domain_file = domain_file.read()  
        domain_file = read_file(args['domain_path'], 'r')
        system_capabilities = extract_actions_from_domain(args['domain_path'])
        system_capabilities_str = ', '.join(system_capability for system_capability in system_capabilities)
        messages = [
        # description to the system, what it is gonna perform 
        {   
            'role': 'system',
            'content': 'You are a helpful system, that will help me generate planning problems \
            in PDDL 1.2 language. You work on a service robot named Rico serving in a house. \
            You have a set of tasks that you can perform. You can hear what people ask you to do \
            and also you can talk to them too. You are a wheel robot with no manipulators (hands), \
            but you have a little platform on you that can be used to transport something. \
            There are people in the house and you are interacting with them.',
        },
        
        # description about what the conversation topic is
        {   
            'role': 'user',
            'content': 'Here is the planning domain in PDDL 1.2 language. \
            ' + domain_file,
        },
        
        # description of what the robot's abilities are
        {   
            'role': 'user',
            'content': 'Based on the domain file, the actions that the \
            system can perform are: ' + system_capabilities_str,
        },
        ]
        return messages
    
    def give_examples_of_problem_files_prompt(self, args):
        messages = [
            {
            'role':'user',
            'content': 'In the following messages I will give you the \
            definitions of example PDDL problem files for the PDDL domain file \
            I gave you in the previous message.'
            },   
        ]
        for problem_file_path in os.listdir(args['example_problems_path']):
            problem_file = read_file(os.path.join(args['example_problems_path'], problem_file_path), 'r')
            messages.append({
                'role':'user',
                'content': problem_file
            })
        return messages

    def provide_gpt_with_the_task_request_prompt(self, args):
        messages = [
        {
            'role': 'user',
            'content': 'You are requested to ' + self.task_request + 'Give a list \
            of actions that you should do to perform this task. Use only the actions that you can perform.'
        },
        ]
        return messages
    def ask_to_create_problem_pddl_file(self, requested_task_in_gpt_interpretation):
        # request to the chat to produce pddl plan of commanded ability 
        messages = [
        {
            'role': 'user',
            'content': 'In the previous messages I gave you the definition \
            of correctly defined PDDL domain file. Generate a PDDL problem for the , \
            requested task (' + self.task_request + '), based on the domain file that I gave you, \
            and the set of actions that the system can perform. The plan should only consist \
            of those actions. Remember to use the correct syntax for PDDL \
            language. Call the problem as system_problem. In the output, give me \
            the problem file only, without any comments.'
        },
        ]  
        return messages
    
    def create_info_about_wrong_pddl_problem_definition_prompt(self, planner_output):
        messages = [
        {
            'role': 'user',
            'content': 'Sorry. But the PDDL problem definition for the \
            planning problem we talked about is incorrect. Please correct it according \
            to PDDL rules. Planner returned this error as an output: ' + planner_output
            # Remember to only use the actions \
            # included in the PDDL domain file that I gave you.'
        },
        # {
        #     'role': 'user',
        #     'content': 'Planner returned this error as an output. ' + planner_output
        # }
        ]
        return messages
            
    def create_ask_for_capabilities_importances_for_commanded_task_prompt(self, args):
        system_capabilities = extract_actions_from_domain(args['domain_path'])
        system_capabilities_str = ', '.join(system_capability for system_capability in system_capabilities)
        messages = [
        # description to the system, what it is gonna perform 
        {   
            'role': 'system',
            'content': 'You are a helpful assistant, that will tell me \
            if some ability that the system has is important to perform \
            a given task',
        },
        
        {   
            'role': 'user',
            'content': 'There is an autonomic system',
        },
        
        {   
            'role': 'user',
            'content': 'This system has the following set of capabilities: \
            ' + system_capabilities_str,
        },
        
        {
            'role': 'user',
            'content': 'The system was requested to ' + self.task_request 
        },
        
        {
            'role': 'user',
            'content': 'Take under considearation only the capabilities, that \
            I told you, that the robot has. These are ' + system_capabilities_str + '\
            As the output, give me a json-like struct \
            with capability on the left-hand side and grade on the right-hand side. \
            This grade should mean, how important this capability will be in performing \
            the task ' + self.task_request + '. Grade the capabilities importance from 0 to 9. \
            Emphasize the ones that will be the most important in completing the commanded \
            task. Name the json-like struct that you will return as "capabilities_importances" \
            the output should only be: \
            capabilities_importances = {"ability_id": grade, "ability_id": grade ...}'
        },
        ]
        return messages
        
    def create_check_if_robot_can_perform_requested_task_prompt(self):
        tasks_system_can_perform = self.args['tasks_system_can_perform']
        tasks_system_can_perform_str = ', '.join(task for task in tasks_system_can_perform)
        messages = [
        # description to the system, what it is gonna perform 
        {   
            'role': 'system',
            'content': 'You are a helpful assistant that will \
            tell me if a system can perform some commanded task'
        },
        
        # description about what the robot system can do
        {   
            'role': 'user',
            'content': 'This is a set of tasks that the system \
            can perform: ' + tasks_system_can_perform_str
        },
        # keep those capabilities in mind when i will ask \
        # you if a robot can perform some action'
        
        # question to the gpt if the described robot system can perform the commanded task
        {   
            'role': 'user',
            'content': 'The system is requested to ' + self.task_request +  '.\
            does the robot system already know how to do it? Answer yes or no only'
        },
        ]
        return messages