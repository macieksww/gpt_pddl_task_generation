from process_plan import extract_actions_from_domain
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
    
    def create_initial_conversation_prompt(self):
        with open('pddl_files/domain.pddl', 'r') as domain_file:
            domain_file = domain_file.read()      
        system_capabilities = extract_actions_from_domain('pddl_files/domain.pddl')
        system_capabilities_str = ', '.join(system_capability for system_capability in system_capabilities)
        messages = [
        # description to the system, what it is gonna perform 
        {   
            'role': 'system',
            'content': 'you are a helpful system, that will help me generate planning problems \
            in PDDL 1.2 language',
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
                        
        # description of what kind of a new ability we want the robot to have 
        {
            'role': 'user',
            'content': 'The system is requested to ' + self.task_request 
        },
        
        # request to the chat to produce pddl plan of commanded ability 
        {
            'role': 'user',
            'content': 'In the previos message I gave you the definition \
            of correctly defined PDDL domain file. Generate a PDDL problem, \
            based on the domain file that I gave you, and the set of actions \
            that the system can perform. The plan should only consist \
             of those actions. Remember to use the correct syntax for PDDL \
            language. Call the problem as system_problem. In the output, give me \
            the problem file only, without any comments.'
        },
        ]  
        return messages
    
    def create_info_about_wrong_pddl_problem_definition_prompt(self):
        messages = {
        'role': 'user',
        'content': 'Sorry. But the PDDL problem definition for the \
        planning problem we talked about is incorrect. Please correct it according \
        to PDDL rules. Remember to only use the actions \
        included in the PDDL domain file that I gave you.'
        } 
        return messages
            
    def create_ask_for_capabilities_importances_for_commanded_task_prompt(self):
        system_capabilities = extract_actions_from_domain('pddl_files/domain.pddl')
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
            
            
        # robot_abilities_content = 'this is a system of a robot that can perform \
        # the following actions: '
        # for robot_ability in robot_abilities:
        #     robot_abilities_content += robot_ability
        #     robot_abilities_content += ", "
        # robot_abilities_content += 'keep those capabilities in mind while \
        #     creating plans for tasks in the future'
            
        # with open('pddl_files/domain.pddl', 'r') as domain_file:
        #     domain_file = domain_file.read()
        # with open('pddl_files/switch_domain.pddl', 'r') as domain_file:
        #     domain_file = domain_file.read()
        # with open('pddl_files/switch_problem.pddl', 'r') as problem_file:
        #     problem_file = problem_file.read()
        # domain_example_content = 'I will later ask you to generate planning domain \
        #     and problem for the task I told you about in the previous message. \
        #     In this message I show you an example of \
        #     correctly defined domain file in PDDL 1.2 language. Be careful \
        #     of the correct setting of parenthesis. \n' + domain_file
        # problem_example_content = 'In this message I show you an example of \
        #     correctly defined problem file in PDDL 1.2 language. Be careful \
        #     of the correct setting of parenthesis. \n' + problem_file
                # providing gpt with correctly defined domain and problem file as an examle
        # to follow
        # {
        #     'role': 'user',
        #     'content': domain_example_content,
        # },
        
        # {
        #     'role': 'user',
        #     'content': problem_example_content,
        # },
        # Remember to use correct syntax for \
        # PDDL language and to declare types and requirements in the domain file. \
        # Inculde ":typing" and ":negative-preconditions" in requirements in domain file. \
        # Remeber to declare all variables used in action definitions.'
