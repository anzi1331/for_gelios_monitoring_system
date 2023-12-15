from requests import get
import json

#Запрос токена. В функцию передаем логин и пароль учетной записи, для которой получает токен
def get_token(login: str, psw: str) -> str:
    url = 'https://admin.geliospro.com/sdk/?'
    params = {
    'login': login,
    'pass': psw,
    'svc': 'create_token',
    }
    r = get(url, params).json()
    if r.get('token'):
        return r.get('token')
    elif r.get('error'):
        return f"error: {r.get('error')}"
    else:
        return f"Unknow error"


#На вход подаем список из названия групп, на выходе получаем id групп в словаре, вида {'имя группы':id}
def get_group_id(tkn: str, groups: list) -> dict:
    url = 'https://admin.geliospro.com/sdk/?'
    params = {
    'token' : tkn,
    'svc': 'get_units_groups'
    }
    r = get(url, params)
    user_groups = r.json()
    return_groups = {}
    for gr in user_groups:
        if gr.get('name') in groups:
            return_groups[gr.get('name')] = gr.get('id')
    return return_groups

# возвращает имя и id всех доступных пользователю объектов

def get_units_id_2(token: str) -> dict:
    url = 'https://admin.geliospro.com/sdk/?'
    params = {
        'token' : token,
        'svc': 'get_units',
        }
    r = get(url, params).json()
    r_dict = {}
    for i in r:
        r_dict[i.get('name')] = i.get('id')
    return r_dict


# на вход подается список id групп и cписок id объектов. Функция добавляет объекты в группы.
#  На выходе иммем список объектов, которые были добавлены и которые не удалось добавить
def add_units_to_groups(token: str, groups: list, units: list) -> None:
    url = 'https://admin.geliospro.com/sdk/?'
    gr_lst = [int(v) for v in get_group_id(token, groups).values()]
    unit_list = [int(v) for k, v in get_units_id_2(token).items() if k in units]
    for i in gr_lst:
        params = {
            'token' : token,
            'svc': 'add_units_to_group',
            'params': json.dumps({"group_id": i, "unit_ids": unit_list})
        }
        r = get(url, params)
        print(r.text)
