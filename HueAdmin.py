from dotenv import load_dotenv
from os import getenv
import requests as req
import json

load_dotenv()
HK = getenv('HUEKEY')
HIP = getenv('HUEIP')
HUEADDRESS = f"http://{HIP}/api/{HK}/"


def lights_call(number:int=0, new:bool=False) -> str:
    '''
    returns a string that should be appended to HUEADDRESS to complete call to
    the lights API.\n
    Input:\n
    number - int - default is 0, the number assigned to the light by the hub. 
    This is the key value in the json output from "/api/<username>/lights"\n
    new - boolean - default is False, a boolean whether the API should append 
    "new" to the string for the API call.
    '''
    if number:
        return f"lights/{number}"
    elif new:
        return f"lights/new"
    else:
        return "lights"


def get_lights(light:int=0) -> dict:
    '''
    Calls the lights GET API.\n
    Input:\n
    lights - integer - default is 0, the number of the light assigned by the hub. 
    This is the key value in the json output from "/api/<username>/lights"\n
    Output:\n
    returns the JSON data from the API call if the status code is less than 400 
    or a None if the status code is greater than or equal to 400
    '''
    get_lights = req.get(HUEADDRESS + lights_call(light))
    if get_lights.status_code >= 400:
        return
    return get_lights.json()
    

def get_groups(number=0):
    groups_call = "groups"
    if number:
        groups_call += f"/{number}"

    get_groups = req.get(HUEADDRESS + groups_call)
    if get_groups.status_code >= 400:
        return
    return get_groups.json()


def get_schedules(number=0):
    schedule_call = "schedules"
    if number:
        schedule_call += f"/{number}"

    get_schedules = req.get(HUEADDRESS + schedule_call)
    if get_schedules.status_code >= 400:
        return
    return get_schedules.json()


def get_rules(number=0):
    rules_call = "rules"
    if number:
        rules_call += f"/{number}"

    get_rules = req.get(HUEADDRESS + rules_call)
    if get_rules.status_code >= 400:
        return
    return get_rules.json()


def get_sensors(number=0):
    sensor_call = "sensors"
    if number:
        sensor_call += f"/{number}"

    get_sensors = req.get(HUEADDRESS + sensor_call)
    if get_sensors.status_code >= 400:
        return
    return get_sensors.json()


def get_new_lights():

    get_new_lights = req.get(HUEADDRESS + "lights/new")
    if get_new_lights.status_code >= 400:
        return
    else:
        return get_new_lights.json()


def add_light_to_group(light: int, group: int):
    light_group = f"groups/{group}"
    get_group_info = get_groups(group)
    if not get_group_info:
        return
    group_lights = get_group_info['lights']
    group_lights.append(str(light))
    send_group_update = req.put(
        HUEADDRESS + light_group,
        json={'lights': group_lights}
        )
    
    return send_group_update.status_code < 400


def remove_light_from_group(light: int, group: int):
    light_group = f"groups/{group}"
    get_group_info = get_groups(group)
    if not get_group_info:
        return
    group_lights = get_group_info['lights']
    if str(light) not in group_lights:
        return
    
    light_index = group_lights.index(str(light))
    del group_lights[light_index]

    send_group_update = req.put(
        HUEADDRESS + light_group,
        json={'lights': group_lights}
        )

    return send_group_update.status_code < 400


def scan_for_new_lights():
    scan_call = "lights"
    scan = req.post(HUEADDRESS + lights_call())

    return scan.json()


def edit_light(light: int, attribs: dict):
    send_edits = req.put(HUEADDRESS + lights_call(light), json=attribs)

    return send_edits.status_code < 400


def print_groups(number=0):
    if number:
        groups = get_groups(number)
        if not groups:
            return
        print(f"{groups['name']}, {groups['lights']}")
    else:
        groups = get_groups()
        if not groups:
            return
        for item in groups:
            stmt = f"{item}, {groups[item]['name']}, type = "
            stmt += f"{groups[item]['type']}, {groups[item]['lights']}"
            print(stmt)


def print_lights(light=0):
    if light:
        lights = get_lights(light)
        if not lights:
            return
        print(f"{lights['name']}, on = {lights['state']['on']}")

    else:
        lights = get_lights()
        if not lights:
            return
        else:
            for item in lights:
                stmt = f"{item}, {lights[item]['name']}, on = "
                stmt += f"{lights[item]['state']['on']}"
                print(stmt)


def print_sensors(number=0):
    if number:
        sensors = get_sensors(number)
        if not sensors:
            return
        stmt = f"{sensors['name']}, enabled = "
        stmt += f"{sensors['config']['on']}, state = "
        stmt += f"{sensors['state']['flag']}"
        print(stmt)

    else:
        sensors = get_sensors()
        if not sensors:
            return
        for item in sensors:
            print_statement = f"{item}, {sensors[item]['name']}, enabled = "
            print_statement += f"{sensors[item]['config']['on']}"
            if 'flag' in sensors[item]['state']:
                print_statement += f", state = {sensors[item]['state']['flag']}"
            print(print_statement)


def print_rules(number=0):
    if number:
        print(json.dumps(get_rules(number), indent=2))
    else:
        print(json.dumps(get_rules(), indent=2))
        

def toggle_sensor7():
    sensor7 = get_sensors(7)
    sensor7_state = sensor7['state']['flag']
    
    update_sensor7 = req.put(
        HUEADDRESS + "sensors/7",
        json={'state': {'flag': not sensor7_state}}
        )
    print(json.dumps(get_sensors(7), indent=2))


def change_group_state(group: int, state: dict):
    group_call = f"groups/{group}/action"
    update_state = req.put(HUEADDRESS + group_call, json=state)
    
    return update_state.status_code < 400


def change_light_state(light: int, state: dict):
    light_call = f"lights/{light}/state"
    update_light = req.put(HUEADDRESS + light_call, json=state)
    
    return update_light.status_code < 400


def update_schedule(number: int, update: dict):
    schedule_call = f"schedules/{number}"
    update_schedule = req.put(HUEADDRESS + schedule_call, json=update)

    return update_schedule.status_code < 400


def create_group(attribs: dict):
    group_call = "groups"

    create_group = req.post(HUEADDRESS + group_call, json=attribs)
    if create_group.status_code >= 400:
        return
    return create_group.json()


def update_rule(number: int, attribs: dict):
    rules_call = f"rules/{number}"

    update_rule = req.put(HUEADDRESS + rules_call, json=attribs)
    if update_rule.status_code >= 400:
        return
    else:
        print(json.dumps(update_rule.json(), indent=2))


def delete_light_from_hub(light:int=0) -> bool:
    '''
    This will delete the specified light from the hub.\n
    light - integer - required - the number that is assigned to the light from 
    the hub. This is the key value in the json output from "/api/<username>/lights"\n
    The output will be a boolean if the request status code is less than 400.
    '''
    assert type(light) == int
    delete_light = req.delete(HUEADDRESS + f"lights/{light}")

    return delete_light.status_code < 400


if __name__ == "__main__":
    # print(json.dumps(get_new_lights(), indent=2))
    # light = 2
    # assert type(light) == int
    header = {'hue-application-key': HK}
    sess = req.session()
    sess.headers = header
    lights = sess.get(
        f"https://{HIP}/clip/v2/resource/light",
        verify=False
        )
    if lights.status_code == 200:
        my_light = [i for i in lights.json()['data'] if i['id_v1'] == "/lights/22"]
        print(json.dumps(my_light, indent = 4))
    else: print(lights.status_code)
