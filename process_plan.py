import re
from helpful_functions import save_lines_to_file, read_file, write_file

def extract_pddl_files(path_to_gpt_domain_output, path_to_gpt_problem_output, path_to_unprocessed_gpt_domain_problem_output):
    domain_pattern = re.compile(r'\(define \(domain', re.IGNORECASE)
    problem_pattern = re.compile(r'\(define \(problem', re.IGNORECASE)
    define_pattern = re.compile(r'\(define \(', re.IGNORECASE)
    domain_line_span = []
    problem_line_span = []
    domain_lines = []
    problem_lines = []
    define_pattern_matched_counter = 0
    line_counter = 0
    lines = read_file(path_to_unprocessed_gpt_domain_problem_output, 'rl') 
    for line in lines:
        if define_pattern.search(line):
            if define_pattern_matched_counter == 0:
                domain_line_span.append(line_counter)
            else:
                domain_line_span.append(line_counter)
                problem_line_span.append(line_counter)
            define_pattern_matched_counter += 1
        line_counter += 1
    problem_line_span.append(line_counter)
    domain_lines = lines[domain_line_span[0]:domain_line_span[1]]
    problem_lines = lines[problem_line_span[0]:problem_line_span[1]]
    
    # Extraction of domain definition based on placement of the opening
    # and closing parentheses
    domain_file_first_line = 0
    domain_file_last_line = len(domain_lines)
    first_left_parentheses_found = False
    last_right_parentheses_found = False
    
    for line in domain_lines:
        if not first_left_parentheses_found:
            if line.find('(') >= 0:
                first_left_parentheses_found = True
            else:
                domain_file_first_line += 1
        else:
            break
        
    for line in reversed(domain_lines):
        if not last_right_parentheses_found:
            if line.rfind(')') >= 0:
                last_right_parentheses_found = True
            else:
                domain_file_last_line -= 1
        else:
            break
        
    # Extraction of domain definition based on placement of the opening
    # and closing parentheses
    problem_file_first_line = 0
    problem_file_last_line = len(problem_lines)
    first_left_parentheses_found = False
    last_right_parentheses_found = False
    
    for line in problem_lines:
        if not first_left_parentheses_found:
            if line.find('(') >= 0:
                first_left_parentheses_found = True
            else:
                problem_file_first_line += 1
        else:
            break
        
    for line in reversed(problem_lines):
        if not last_right_parentheses_found:
            if line.rfind(')') >= 0:
                last_right_parentheses_found = True
            else:
                problem_file_last_line -= 1
        else:
            break
    
    domain_lines = domain_lines[domain_file_first_line:domain_file_last_line]
    problem_lines = problem_lines[problem_file_first_line:problem_file_last_line]
    
    # counting parenthesis to make sure that only domain and problem definitions 
    # are extracted
    left_pth_counter = 0
    right_pth_counter = 0
    line_counter = 0
    for line in domain_lines:
        indexes = [
            match.start() for match in re.finditer(r'\(', line)
        ]
        left_pth_counter += len(indexes)
        indexes = [
            match.start() for match in re.finditer(r'\)', line)
        ]
        right_pth_counter += len(indexes)
        line_counter += 1
        if left_pth_counter > 0 and left_pth_counter == right_pth_counter:
            break
    domain_lines = domain_lines[:line_counter]
    
    left_pth_counter = 0
    right_pth_counter = 0
    line_counter = 0
    for line in problem_lines:
        indexes = [
            match.start() for match in re.finditer(r'\(', line)
        ]
        left_pth_counter += len(indexes)
        indexes = [
            match.start() for match in re.finditer(r'\)', line)
        ]
        right_pth_counter += len(indexes)
        line_counter += 1
        if left_pth_counter > 0 and left_pth_counter == right_pth_counter:
            break
    problem_lines = problem_lines[:line_counter]
    
    # Saving extracted planning domain and problem definition to pddl files
    save_lines_to_file(domain_lines, path_to_gpt_domain_output)
    save_lines_to_file(problem_lines, path_to_gpt_problem_output)
    

def extract_pddl_problem(path_to_gpt_problem_output, path_to_unprocessed_gpt_domain_problem_output):
    problem_pattern = re.compile(r'\(define \(problem', re.IGNORECASE)
    define_pattern = re.compile(r'\(define \(', re.IGNORECASE)
    problem_line_span = []
    problem_lines = []
    define_pattern_matched_counter = 0
    line_counter = 0
    lines = read_file(path_to_unprocessed_gpt_domain_problem_output, 'rl')
    for line in lines:
        if define_pattern.search(line):
            problem_line_span.append(line_counter)
        line_counter += 1
    problem_line_span.append(line_counter)
    problem_lines = lines[problem_line_span[0]:]
        
    # Extraction of domain definition based on placement of the opening
    # and closing parentheses
    problem_file_first_line = 0
    problem_file_last_line = len(problem_lines)
    first_left_parentheses_found = False
    last_right_parentheses_found = False
    
    for line in problem_lines:
        if not first_left_parentheses_found:
            if line.find('(') >= 0:
                first_left_parentheses_found = True
            else:
                problem_file_first_line += 1
        else:
            break
        
    for line in reversed(problem_lines):
        if not last_right_parentheses_found:
            if line.rfind(')') >= 0:
                last_right_parentheses_found = True
            else:
                problem_file_last_line -= 1
        else:
            break
    
    problem_lines = problem_lines[problem_file_first_line:problem_file_last_line]
    
    # counting parenthesis to make sure that only domain and problem definitions 
    # are extracted    
    left_pth_counter = 0
    right_pth_counter = 0
    line_counter = 0
    for line in problem_lines:
        indexes = [
            match.start() for match in re.finditer(r'\(', line)
        ]
        left_pth_counter += len(indexes)
        indexes = [
            match.start() for match in re.finditer(r'\)', line)
        ]
        right_pth_counter += len(indexes)
        line_counter += 1
        if left_pth_counter > 0 and left_pth_counter == right_pth_counter:
            break
    problem_lines = problem_lines[:line_counter]
    
    # Saving extracted planning domain and problem definition to pddl files
    save_lines_to_file(problem_lines, path_to_gpt_problem_output)



def check_if_planner_succeeded(path_to_planner_output, planner_type):
    timestamp_pattern = r'\b\d+\.+\d+:+.*'
    lines = read_file(path_to_planner_output, 'rl')
    for line in lines:
        matches = re.findall(timestamp_pattern, line)
        if len(matches):
            return True
    return False

def extract_plan_from_planner_output(path_to_planner_output, path_to_plan):
    timestamp_pattern = r'\b\d+.+\d+:.'
    plan_lines = []
    lines = read_file(path_to_planner_output, 'rl')
    for line in lines:
        matches = re.findall(timestamp_pattern, line)
        if len(matches):
            plan_lines.append(line) 
    write_file(path_to_plan, plan_lines, 'wl')
        
def extract_actions_from_domain(path_to_domain_file):
    timestamp_pattern = r':\baction.*'
    actions = []
    lines = read_file(path_to_domain_file, 'rl')
    for line in lines:
        matches = re.findall(timestamp_pattern, line)
        if matches:
            action = matches[0][8:]
            actions.append(action)
    return actions

def rate_plan(path_to_plan_file, capabilities_importances):
    pattern = r'\(.*\)'
    actions_definitions = []
    used_actions = []
    lines = read_file(path_to_plan_file, 'rl')
    for line in lines:
        matches = re.search(pattern, line)
        print(matches)
        try:
            actions_definitions.append(line[matches.span()[0]+1:matches.span()[1]])
        except AttributeError as e:
            print(e)
    for action_definition in actions_definitions:
        used_actions.append(action_definition.split(" ")[0])
            
    plan_rate = 0
    single_action_usage_cost = 2
    for used_action in used_actions:
        plan_rate += int(capabilities_importances[used_action])
        plan_rate -= single_action_usage_cost
    return plan_rate
            
# print(extract_actions_from_domain('pddl_files/domain.pddl'))
            
        
# extract_plan_from_planner_output('gpt_generated_files/planner_output.pddl', 'gpt_generated_files/plan.pddl')
    