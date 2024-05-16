import json
import os

lark_card_path = '../extra/dag/buildin_awel/lark/lark_card_by_json/'


def replace_variables(data, variables):
    if isinstance(data, dict):
        for key, value in data.items():
            data[key] = replace_variables(value, variables)
    elif isinstance(data, list):
        for i in range(len(data)):
            data[i] = replace_variables(data[i], variables)
    elif isinstance(data, str):
        for variable, value in variables.items():
            if isinstance(value, str):
                data = data.replace('${' + variable + '}', value)
            elif data == '${' + variable + '}':
                data = value
                break
    return data

def disable_interactive(data, disabled_element_list):
    if isinstance(data, dict):
        if 'tag' in data:
            for element in disabled_element_list:
                if data['tag'] == element:
                    data['disabled'] = True
                    data['required'] = False

        for key, value in data.items():
            disable_interactive(value, disabled_element_list)

    if isinstance(data, list):
        for i in range(len(data)):
            data[i] = disable_interactive(data[i], disabled_element_list)

    return data

def get_lard_card_json(card_name: str = 'daily_report',
                       template_variable: dict = {},
                       disabled: bool = False):
    file_path = f'{lark_card_path}{card_name}.json'
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            card_content = json.load(file)
    else:
        raise FileNotFoundError(f'{file_path} does not exist')

    try:
        card_content = replace_variables(card_content, template_variable)
    except TypeError:
        raise TypeError(f'{card_name} template variable have something wrong')

    disabled_element_list = ['input', 'date_picker', 'button']
    if disabled:
        card_content = disable_interactive(card_content, disabled_element_list)

    return card_content
