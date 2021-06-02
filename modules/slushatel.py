import json

from modules.constants import *

class Slushatel:

    def __init__(self, login):
        """
        Init

        Args:
            login ([str]): login
        """
        file = open(USERS_FILE, 'r', encoding='utf-8')
        data = json.loads(file.read())[login]
        file.close()

        self.login = login
        self.fullname = data['fullname']
        self.group = data['group']
        

    def get_queue_data(self):
        """
        Generate for web -view

        Returns:
            [list] : sample : [
                {
                    'fullname' : Имя преподавателя,
                    'group'    : 1111,
                    'queue_index' : номер в очереди
                },
                ...
            ] 
        """
        file = open(USERS_FILE, 'r', encoding='utf-8')
        user_file = json.loads(file.read())
        file.close()

        file = open(QUEUE_FILE, 'r', encoding='utf-8')
        queue_data = json.loads(file.read())
        file.close()

        self.queue_data = []

        for k, v in queue_data.items():
            if self.login in [d['login'] for d in v]:
                self.queue_data.append({
                    'fullname'    : user_file[k]['fullname'],
                    'group'       : user_file[k]['group'],
                    'queue_index' : [d['login'] for d in v].index(self.login) + 1
                })

        return self.queue_data

    def get_in_line(self, prepod_login):
        """
        Set in queue

        Args:
            prepod_login ([str]): prepod string

        Returns:
            [int]: position queue
        """
        file = open(QUEUE_FILE, 'r', encoding='utf-8')
        queue_data = json.loads(file.read())
        file.close()

        if prepod_login not in queue_data:
            queue_data[prepod_login] = []

        if self.login in [el['login'] for el in queue_data[prepod_login]]:
            return

        queue_data[prepod_login].append({
            'name' : self.fullname,
            'group' : self.group,
            'status' : 'wait',
            'login' : self.login
        })

        file = open(QUEUE_FILE, 'w', encoding='utf-8')
        file.write(json.dumps(queue_data, ensure_ascii=False))
        file.close()

        return len(queue_data)
        