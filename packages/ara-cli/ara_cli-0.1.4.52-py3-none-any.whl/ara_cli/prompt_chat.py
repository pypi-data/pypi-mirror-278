import os
import shutil
from ara_cli.chat import Chat
from ara_cli.classifier import Classifier
from ara_cli.prompt_handler import generate_config_prompt_template_file, generate_config_prompt_givens_file
from ara_cli.update_config_prompt import update_config_prompt_files

def initialize_prompt_chat_mode(classifier, param):
    sub_directory = Classifier.get_sub_directory(classifier)
    artefact_data_path = os.path.join("ara", sub_directory, f"{param}.data") # f"ara/{sub_directory}/{parameter}.data"
    prompt_data_path = os.path.join(artefact_data_path, "prompt.data")  # f"ara/{sub_directory}/{parameter}.data/prompt.data"
    
    if not os.path.exists(prompt_data_path):
        os.makedirs(prompt_data_path)

    givens_file_name = "config_prompt_givens.md"
    givens_tmp_file_name = "config_prompt_givens_tmp.md"
    template_file_name = "config_prompt_templates.md"
    template_tmp_file_name = "config_prompt_templates_tmp.md"
    
    prompt_config_givens = os.path.join(prompt_data_path, givens_file_name)
    prompt_config_givens_tmp = os.path.join(prompt_data_path, givens_tmp_file_name)

    prompt_config_templates = os.path.join(prompt_data_path, template_file_name)
    prompt_config_templates_tmp = os.path.join(prompt_data_path, template_tmp_file_name)

    if not os.path.exists(prompt_config_givens):
        generate_config_prompt_givens_file(prompt_data_path, givens_file_name)
    else:
        # logic to ask for overwrite or update
        action = input(f"{prompt_config_givens} already exists. Do you want to overwrite (o) or update (u)? ")
        if action.lower() == 'o':
            generate_config_prompt_givens_file(prompt_data_path, givens_file_name)
        elif action.lower() == 'u':
            generate_config_prompt_givens_file(prompt_data_path, givens_tmp_file_name)
            update_config_prompt_files(prompt_config_givens, prompt_config_givens_tmp)

    if not os.path.exists(prompt_config_templates):
        generate_config_prompt_template_file(prompt_data_path, template_file_name)
    else:
        # logic to ask for overwrite or update
        action = input(f"{prompt_config_templates} already exists. Do you want to overwrite (o) or update (u)? ")
        if action.lower() == 'o':
            generate_config_prompt_template_file(prompt_data_path, template_file_name)
        elif action.lower() == 'u':
            generate_config_prompt_template_file(prompt_data_path, template_tmp_file_name)
            update_config_prompt_files(prompt_config_templates, prompt_config_templates_tmp)

    classifier_chat_file = os.path.join(artefact_data_path, f"{classifier}")
    start_chat_session(classifier_chat_file)

def start_chat_session(chat_file):
    chat = Chat(chat_file)
    chat.start()