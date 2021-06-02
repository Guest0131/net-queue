import json

from modules.constants import *

def check_login(form_data):
    """
    Check login form data

    Args:
        form_data ([type]): requst.form from login page

    Returns:
        [string | boolean]: 
    """
    file = open(USERS_FILE, 'r', encoding='utf-8') 
    users_dict = json.loads(file.read())
    file.close()

    if 'login' in form_data and form_data['login'] in users_dict:
        return users_dict[form_data['login']]['type'] if 'password' in form_data and form_data['password'] == users_dict[form_data['login']]['password'] else False

    return False

def check_register(form_data):
    """
    Register new user

    Args:
        form_data ([type]): requst.form from login page

    Returns:
        [boolean]: Correct register or not?
    """

    file = open(USERS_FILE, 'r', encoding='utf-8') 
    users_dict = json.loads(file.read())
    file.close()

    if 'login' in form_data and form_data['login'] not in users_dict:
        try:
            users_dict[form_data['login']] = {
                'type'     : form_data['type'],
                'fullname' : form_data['fullname'],
                'password' : form_data['password'],
                'group'    : form_data['group']
            }

            file = open(USERS_FILE, 'w', encoding='utf-8')
            file.write(json.dumps(users_dict, ensure_ascii=False))
            file.close()

            return True

        except:
            return False

    return False
