import json

from modules.constants import *


class Prepod:

    def __init__(self, login):
        """
        Init

        Args:
            login ([str]): user login
        """
        self.login = login

        users_file = open(USERS_FILE, 'r', encoding='utf-8')
        self.name = json.loads(users_file.read())[login]['fullname']
        users_file.close()

        queue_data = open(QUEUE_FILE, 'r', encoding='utf-8')
        file_data = json.loads(queue_data.read())
        self.data = file_data[login] if login in file_data else []
        queue_data.close()

    
    def update_index(self, old_index, new_index):
        """
        Update index in queue

        Args:
            old_index ([int]): old index
            new_index ([int]): new index
        """
        self.data[old_index], self.data[new_index] = self.data[new_index], self.data[old_index]
        self.update_file()
        

    def update_file(self):
        """
        Additionally function
        """
        file = open(QUEUE_FILE, 'r', encoding='utf-8')
        data_to_export = json.loads(file.read())
        data_to_export[self.login] = self.data
        file.close()

        file = open(QUEUE_FILE, 'w', encoding='utf-8')
        file.write(json.dumps(data_to_export, ensure_ascii=False))
        file.close()

    def drop_index(self, index):
        """
        Drop student from queu

        Args:
            index ([int]): index in queue
        """
        self.data.pop(index)
        self.update_file()
    
    def update_status(self, index, status):
        """
        Update status for indexe's student in queue

        Args:
            index ([int]): index in queue
            status ([string]): new status
        """
        self.data[int(index)]['status'] = status
        self.update_file()

    def get_query_data(self):
        """
        Get queue data

        Returns:
            [arr]: Sample => [
                {
                    "name" : "Слушак С.С.", 
                    "group": "7777", 
                    "status": "wait", 
                    "login": "slu"
                },
                ...
            ]
        """
        return self.data

    @staticmethod
    def get_prepods_name():
        """
        Get all prepods names

        Returns:
            [dict]: Sample => {
                "{prepod_login}" : {
                    ... {This data from users.json file}
                }
            }
        """
        users_file = open(USERS_FILE, 'r', encoding='utf-8')
        file_data = json.loads(users_file.read())
        users_file.close()

        return {
            k : v
            for k, v in file_data.items()
            if v['type'] == 'Преподаватель'
        }

