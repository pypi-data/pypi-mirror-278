from langchain_openai import ChatOpenAI
from ara_cli.classifier import Classifier
from ara_cli.template_manager import TemplatePathManager
from ara_cli.ara_config import ConfigManager
from ara_cli.file_lister import generate_markdown_listing
from os.path import exists, join, splitext, isfile
import os
from os import makedirs, listdir, environ
from sys import exit
from subprocess import run
from re import findall
import shutil

class ChatOpenAISingleton:
    _instance = None

    def __init__(self):
        ChatOpenAISingleton._instance = ChatOpenAI(openai_api_key=environ.get("OPENAI_API_KEY"), model_name='gpt-4o')

    @staticmethod
    def get_instance():
        if ChatOpenAISingleton._instance is None:
            ChatOpenAISingleton()
        return ChatOpenAISingleton._instance    

def write_string_to_file(filename, string, mode):
    with open(filename, mode) as file:
            file.write(f"\n{string}\n")
    return file

def read_string_from_file(path):
    with open(path, 'r') as file:
            text = file.read()
    return text

def read_prompt(classifier, param):
    sub_directory = Classifier.get_sub_directory(classifier)
    prompt_path = f"ara/{sub_directory}/{param}.data/prompt.data/{classifier}.prompt"

    prompt = read_string_from_file(prompt_path)
    return prompt

def send_prompt(prompt):
    chat = ChatOpenAISingleton.get_instance()
    chat_result = chat.invoke(prompt)
    return chat_result.content

def append_headings(classifier, param, heading_name):
    sub_directory = Classifier.get_sub_directory(classifier)

    artefact_data_path = f"ara/{sub_directory}/{param}.data/{classifier}_exploration.md"
    content = read_string_from_file(artefact_data_path)
    pattern = r'## {}_(\d+)'.format(heading_name)
    matches = findall(pattern, content)

    max_number = 1
    if matches:
        max_number = max(map(int, matches)) + 1
    heading = f"## {heading_name}_{max_number}"
            
    write_string_to_file(artefact_data_path, heading, 'a')

def write_prompt_result(classifier, param, text):
    sub_directory = Classifier.get_sub_directory(classifier)

    # TODO change absolute path to relative path with directory navigator
    artefact_data_path = f"ara/{sub_directory}/{param}.data/{classifier}_exploration.md"
    write_string_to_file(artefact_data_path, text, 'a')

def prompt_data_directory_creation(classifier, parameter):
    sub_directory = Classifier.get_sub_directory(classifier)
    prompt_data_path = f"ara/{sub_directory}/{parameter}.data/prompt.data"
    if not exists(prompt_data_path):
        makedirs(prompt_data_path)
    return prompt_data_path

def default_prompt_creation(classifier, parameter):
    sub_directory = Classifier.get_sub_directory(classifier)
    
    prompt_data_path = prompt_data_directory_creation(classifier, parameter)
    
    # default templates are added to the prompt.data directory
    ensure_basic_prompt_files_exists(classifier, prompt_data_path)
    create_prompt_from_defaults(classifier, prompt_data_path)

def ensure_basic_prompt_files_exists(classifier, prompt_data_path):
    """
    Ensures that all basic prompt files for a given classifier exist within the specified directory and creates them if they don't.
    
    :param classifier: The type of artefact (e.g., 'feature', 'vision'), which determines the template used for file creation.
    :param prompt_data_path: The path to the directory where 'prompt.data' files are stored.
    :return: Returns 'False' if any file was created during the execution, indicating that the user should review these files.
             Returns 'True' if all files were already in place.

    Note: 
    - The function prints a message listing the newly created files, if any.
    - The content for 'prompt.md' and 'givens.md' requires further manual editing.
    """
    basic_prompt_files = ["rules.md", "givens.md", "prompt.md", "commands.md"]
    basic_prompt_files = set(filter(lambda file: need_to_be_created(file, prompt_data_path), basic_prompt_files))
    
    for basic_file in basic_prompt_files:
        file_path = join(prompt_data_path, basic_file)
        with open(file_path, 'w') as file:
            content = basic_prompt_file_content_creation(classifier, basic_file)
            file.write(content)

    if basic_prompt_files:
        print(f"Following File(s) were created: {basic_prompt_files}. \nCheck these files and continue by re-entering the command.")
        exit(1)

def need_to_be_created(basic_prompt_file, prompt_data_path):
    path = join(prompt_data_path, basic_prompt_file)
    return not exists(path)

def basic_prompt_file_content_creation(classifier, basic_prompt_file):
    content = ""
    if basic_prompt_file in ("commands.md", "rules.md", "prompt.md"):
        content = get_template_content(classifier, basic_prompt_file)

    if basic_prompt_file == "givens.md":                    
        command = ["ara", "list"]
        output = run(command, capture_output=True, text=True).stdout
        output = output.replace(" - .", " - [ ] ./ara")
        content = output

    return content

def get_template_content(classifier, basic_prompt_file):
    basic_prompt_template_path = join(TemplatePathManager.get_template_base_path_artefacts(), "prompt-creation")
    
    root, _ = splitext(basic_prompt_file)
    template_name = f"template_{classifier}.md"
    
    root = root.replace("prompt", "prompts")

    template_path = join(basic_prompt_template_path, root, template_name)
    content = ""
    
    if not exists(template_path):
        print(f"WARNING: {template_path} does not exist. Please create a template or {basic_prompt_file} will be empty!")
        return f"# {basic_prompt_file} \n\nNo template found, fill manually or create a template ({template_path})!"

    with open(template_path, 'r') as file:
        return file.read()
    

def create_prompt_from_defaults(classifier, prompt_data_path):
    prompt_file_path = join(prompt_data_path, f"{classifier}.prompt")
    combined_content = ""

    # Define the order of prompt chunks
    prompt_order = ["rules.md", "givens.md", "prompt.md", "commands.md"]

    for file_name in prompt_order:
        md_prompt_file_path = join(prompt_data_path, file_name)
        if file_name == "givens.md":
            combined_content += "### GIVENS\n\n"
            # Handle "givens.md" differently to dynamically load further files
            for item in extract_checked_items(md_prompt_file_path):
                # TODO this works only from the ara directory 
                given_item_path = join(item)
                combined_content += given_item_path + "\n" + "```\n"
                combined_content += get_file_content(given_item_path) + "\n"
                combined_content += "```\n\n"
        else:
            combined_content += get_file_content(md_prompt_file_path) + "\n\n"

    with open(prompt_file_path, 'w') as file:
        file.write(combined_content)

def is_prompt_file(file, prompt_data_path):
    path = join(prompt_data_path, file)
    if exists(path) and file.endswith(".md"):
        return True
    return False


def get_file_content(path):
    with open(path, 'r') as file:
        return file.read()


def get_checked_lines(line):
    return line.startswith("  - [x] ")


def get_path_only(line):
    return line.replace("  - [x] ./", "").strip()


def extract_checked_items(file_path):
    with open(file_path, 'r') as file:

        lines = filter(get_checked_lines, file)
        lines = map(get_path_only, lines)
        lines = set(lines)

    print(lines)
    return lines

def initialize_prompt_templates(classifier, parameter):
    sub_directory = Classifier.get_sub_directory(classifier)
    prompt_data_path = prompt_data_directory_creation(classifier, parameter)
    
    generate_config_prompt_template_file(prompt_data_path, "config_prompt_templates.md")

    generate_config_prompt_givens_file(prompt_data_path, "config_prompt_givens.md")

def write_template_files_to_config(template_type, config_file, base_template_path):
    template_path = os.path.join(base_template_path, template_type)
    for root, _, files in os.walk(template_path):
        for file in sorted(files):
            config_file.write(f"  - [] {template_type}/{file}\n")

def load_selected_prompt_templates(classifier, parameter):
    sub_directory = Classifier.get_sub_directory(classifier)
    prompt_data_path = f"ara/{sub_directory}/{parameter}.data/prompt.data"
    config_file_path = os.path.join(prompt_data_path, "config_prompt_templates.md")
    
    if not os.path.exists(config_file_path):
        print("WARNING: config_prompt_templates.md does not exist.")
        return
    
    with open(config_file_path, 'r') as config_file:
        content = config_file.read()
    
    global_base_template_path = TemplatePathManager.get_template_base_path_prompt_modules()
    local_base_template_path = ConfigManager.get_config().local_prompt_templates_dir
    
    is_local = False
    selected_templates = []
    
    for line in content.splitlines():
        if "# GLOBAL TEMPLATES" in line:
            is_local = False
        elif "# LOCAL TEMPLATES" in line:
            is_local = True
        elif line.strip().startswith('- [x]'):
            template_rel_path = line.split(' ')[-1].strip()
            if is_local:
                source_path = os.path.join(local_base_template_path, template_rel_path)
            else:
                source_path = os.path.join(global_base_template_path, template_rel_path)
            selected_templates.append(source_path)
    
    for template_path in selected_templates:
        if os.path.exists(template_path):
            destination_path = os.path.join(prompt_data_path, os.path.basename(template_path))
            shutil.copy(template_path, destination_path)
        else:
            print(f"WARNING: Template {template_path} not found in {source_path}")

def find_files_with_endings(directory, endings):
    # Create an empty dictionary to store files according to their endings
    files_by_ending = {ending: [] for ending in endings}

    # Walk through the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check each file to see if it ends with one of the specified endings
            for ending in endings:
                if file.endswith(ending):
                    # If it does, append the file to the corresponding list
                    files_by_ending[ending].append(file)
                    break  # Move to the next file after finding a matching ending

    # Collect and sort files by the order of their endings, flatten the dictionary values into a list
    sorted_files = []
    for ending in endings:
        sorted_files.extend(files_by_ending[ending])

    return sorted_files

def extract_and_load_markdown_files(md_prompt_file_path):
    """
    Extracts markdown files paths based on checked items and constructs proper paths respecting markdown header hierarchy.
    """
    header_stack = []
    path_accumulator = []
    with open(md_prompt_file_path, 'r') as file:
        for line in file:
            if line.strip().startswith('#'):
                level = line.count('#')
                header = line.strip().strip('#').strip()
                # Adjust the stack based on the current header level
                current_depth = len(header_stack)
                if level <= current_depth:
                    header_stack = header_stack[:level-1]
                header_stack.append(header)
            elif '[x]' in line:
                relative_path = line.split(']')[-1].strip()
                full_path = os.path.join('/'.join(header_stack), relative_path)
                path_accumulator.append(full_path)
    return path_accumulator

def create_and_send_custom_prompt(classifier, parameter):
    sub_directory = Classifier.get_sub_directory(classifier)
    prompt_data_path = f"ara/{sub_directory}/{parameter}.data/prompt.data"
    # prompt_file_path = join(prompt_data_path, f"{classifier}.prompt")
    prompt_file_path_markdown = join(prompt_data_path, f"{classifier}_prompt.md")
    # combined_content = ""
    combined_content_markdown = ""

    endings = ["_rules.md", "_prompt_givens.md", "_intention_and_context.md", "_commands.md"]
    prompt_order = find_files_with_endings(prompt_data_path, endings)

    for file_name in prompt_order:
        md_prompt_file_path = join(prompt_data_path, file_name)
        if file_name.endswith("_prompt_givens.md"):
            combined_content_markdown += "### GIVENS\n\n"
            markdown_items = extract_and_load_markdown_files(md_prompt_file_path)
            for item in markdown_items:
                combined_content_markdown += item + "\n" + "```\n"
                combined_content_markdown += get_file_content(item) + "\n"
                combined_content_markdown += "```\n\n"
        else:
            # combined_content += get_file_content(md_prompt_file_path) + "\n\n"
            combined_content_markdown += get_file_content(md_prompt_file_path) + "\n\n"

    with open(prompt_file_path_markdown, 'w') as file:
        file.write(combined_content_markdown)

    prompt = read_string_from_file(prompt_file_path_markdown)
    append_headings(classifier, parameter, "prompt")
    write_prompt_result(classifier, parameter, prompt)

    response = send_prompt(prompt)
    append_headings(classifier, parameter, "result")
    write_prompt_result(classifier, parameter, response)

def generate_config_prompt_template_file(prompt_data_path, config_prompt_templates_name):
    config_file_path = os.path.join(prompt_data_path, config_prompt_templates_name)
    with open(config_file_path, 'w') as config_file:
        config_file.write("# GLOBAL TEMPLATES\n")
        config_file.write("## RULES\n")

        write_template_files_to_config("rules", config_file, TemplatePathManager.get_template_base_path_prompt_modules())
        
        config_file.write("\n## INTENTIONS and CONTEXT:\n")
        write_template_files_to_config("prompts", config_file, TemplatePathManager.get_template_base_path_prompt_modules())
        
        config_file.write("\n## COMMANDS:\n")
        write_template_files_to_config("commands", config_file, TemplatePathManager.get_template_base_path_prompt_modules())

        config_file.write("\n# LOCAL TEMPLATES\n")
        config = ConfigManager.get_config()
        local_template_path = config.local_prompt_templates_dir
        
        if not os.path.exists(local_template_path):
            os.makedirs(local_template_path)
            print(f"Local template directory created at {local_template_path}")
        
        sub_dirs = ["rules", "prompts", "commands"]
        for sub_dir in sub_dirs:
            sub_dir_path = os.path.join(local_template_path, sub_dir)
            if not os.path.exists(sub_dir_path):
                os.makedirs(sub_dir_path)
                print(f"Sub-directory '{sub_dir}' created at {sub_dir_path}")

        config_file.write("## RULES:\n")
        write_template_files_to_config("rules", config_file, local_template_path)
        
        config_file.write("\n## INTENTIONS and CONTEXT:\n")
        write_template_files_to_config("prompts", config_file, local_template_path)
        
        config_file.write("\n## COMMANDS:\n")
        write_template_files_to_config("commands", config_file, local_template_path)


def generate_config_prompt_givens_file(prompt_data_path, config_prompt_givens_name):
    config_prompt_givens_path = os.path.join(prompt_data_path, config_prompt_givens_name)
    config = ConfigManager.get_config()
    dir_list = ["ara"] + [item for ext in config.ext_code_dirs for key, item in ext.items()] + [config.doc_dir] + [config.glossary_dir]

    print(f"used {dir_list} for prompt givens file listing\n")
    generate_markdown_listing(dir_list, config.ara_prompt_given_list_includes, config_prompt_givens_path)