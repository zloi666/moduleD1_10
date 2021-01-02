import requests
import sys

USER = "zloi666"

BOARD_ID = "5fcb8a4cbcd3b125d6c9c269"

auth = {
    "key": "654febea302c9ad2dd3cd24099454674",
    "token": "8e2f78ff7fc353b5ad7f0b0d1f3fb7d9fa5aca36ada45e895afa6a096a5cfd54"
}

base_url = "https://api.trello.com/1/{}"

def read():
    column_data = requests.get(base_url.format('boards') + '/' + BOARD_ID + '/lists', params=auth).json() 

    for column in column_data:      
        print(column['name'])

        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth).json()
        print("{} tasks".format(len(task_data)))
        if not task_data:
            print('\t' + 'Нет задач!')      
            continue      
        for task in task_data:      
            print('\t' + task['name'])  


def create_card(name, column_name):
    column_id = check_name(column_name)
    if column_id is None:
        column = create_column(column_name)
        column_id = column["id"]

    requests.post(base_url.format('cards'), data={'name': name, 'idList': column_id, **auth})


def move_card(name, column_name):
    duplicates = get_duplicates(name)

    if len(duplicates) > 0:
        print("tasks > 0")
        for index, task in enumerate(duplicates):
            column_name = requests.get(base_url.format('lists') + '/' + task['idList'], params=auth).json()['name']
            print("task #{}\tid: {}\tin column: {}\t ".format(index, task['id'], column_name))
        task_id = input("enter task ID for move")
    else:
        task_id = duplicates[0]["id"]

    column = check_name(column_name)
    if column is None:
        response = create_column(column_name)
        column = response["id"]

    requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column, **auth})


def create_column(name):
    response = requests.post(base_url.format("lists"), data={"name": name, "idBoard": BOARD_ID, **auth})
    return response


def check_name(name):
    id = None
    data = requests.get(base_url.format('boards') + '/' + BOARD_ID + '/lists', params=auth).json()
    for d in data:
        if d["name"] == name:
            id = d["id"]
            return id
    return


def get_duplicates(task_name):
    data = requests.get(base_url.format('boards') + '/' + BOARD_ID + '/lists', params=auth).json()

    duplicate_tasks = []
    for d in data:
        tasks = requests.get(base_url.format('lists') + '/' + d['id'] + '/cards', params=auth).json()
        for task in tasks:
            if task['name'] == task_name:
                duplicate_tasks.append(task)
    return duplicate_tasks


if __name__ == "__main__":
    if len(sys.argv) < 2:
        read()
    elif sys.argv[1] == "create":
        create_card(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == "move":
        move_card(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == "create_column":
        create_column(sys.argv[2])
