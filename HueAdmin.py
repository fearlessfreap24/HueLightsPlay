from dotenv import load_dotenv
from os import getenv
import requests as req
import json

from requests.api import get

load_dotenv()
HK = getenv('HUEKEY')
HIP = getenv('HUEIP')
HUEADDRESS = f"http://{HIP}/api/{HK}/"


def get_lights(light=0):
    lights_call = "lights"
    if light:
        lights_call += f"/{light}"

    get_lights = req.get(HUEADDRESS + lights_call)
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
    if not scan_for_new_lights():
        return
    get_new_lights = req.get(HUEADDRESS + "lights/new")
    if get_new_lights.status_code >= 400:
        return
    else:
        return get_new_lights.json()


def add_light_to_group(light: int, group: int):
    light_group = f"groups/{group}"
    get_group_info = get_groups()
    if not get_group_info:
        return
    group_lights = get_group_info.json()['lights']
    print(group_lights)
    group_lights.append(str(light))
    send_group_update = req.put(HUEADDRESS + light_group, json={'lights': group_lights})
    
    return send_group_update.status_code < 400


def remove_light_from_group(light: int, group: int):
    light_group = f"groups/{group}"
    get_group_info = get_groups()
    if not get_group_info:
        return
    group_lights = get_group_info.json()['lights']
    if str(light) not in group_lights:
        return
    
    light_index = group_lights.index(str(light))
    del group_lights[light_index]

    send_group_update = req.put(HUEADDRESS + light_group, json={'lights': group_lights})

    return send_group_update.status_code < 400


def scan_for_new_lights():
    scan_call = "lights"
    scan = req.post(HUEADDRESS + scan_call)

    return scan.status_code < 400


def edit_light(light: int, attribs: dict):
    light_call = f"lights/{light}"
    send_edits = req.put(HUEADDRESS + light_call, json=attribs)

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
            print(f"{item}, {groups[item]['name']}, {groups[item]['lights']}")


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
                print(f"{item}, {lights[item]['name']}, on = {lights[item]['state']['on']}")


def print_sensors(number=0):
    if number:
        sensors = get_sensors(number)
        if not sensors:
            return
        print(f"{sensors['name']}, enabled = {sensors['config']['on']}, state = {sensors['state']['flag']}")

    else:
        sensors = get_sensors()
        if not sensors:
            return
        for item in sensors:
            print_statement = f"{item}, {sensors[item]['name']}, enabled = {sensors[item]['config']['on']}"
            if 'flag' in sensors[item]['state']:
                print_statement += f", state = {sensors[item]['state']['flag']}"
            print(print_statement)
        

def toggle_sensor7():
    sensor7 = get_sensors(7)
    sensor7_state = sensor7['state']['flag']
    
    update_sensor7 = req.put(HUEADDRESS + "sensors/7", json={'state': {'flag': not sensor7_state}})
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


if __name__ == "__main__":
    # print(f"{add_light_to_group(16, 4)}")
    # print(f"{remove_light_from_group(5, 4)}")
    # print(json.dumps(get_new_lights(), indent=2))
    # print(json.dumps(get_light_info(16), indent=2))
    # new_light_info = { 'name': "Purple Lamp" }
    # print(f"{edit_light(16, new_light_info)}")
    # print_groups(5)
    print_lights()
    # print(json.dumps(get_schedules(2), indent=2))
    light1_name = {'name': "Paige Bedside"}
    light12_name = {'name': "Dylan Bedside"}
    edit_light(1, light1_name)
    edit_light(12, light12_name)
    print_lights()
    # print(json.dumps(get_rules(2), indent=2))
    # rule2 = get_rules(2)
    # rule2_actions = rule2['actions']
    # index = None
    # for i in range(len(rule2_actions)):
    #     if "groups/5" in rule2_actions[i]['address']:
    #         del rule2_actions[i]

    # add_group4 = { 'address': "/groups/4/action",
    #                 'method': "PUT",
    #                 'body': {
    #                     'on': True
    #                 }
    #             }

    # rule2_actions.append(add_group4)

    # update_rule2 = req.put(HUEADDRESS + "rules/2", json={'actions': rule2_actions})
    # print(json.dumps(update_rule2.json(), indent=2))

    # toggle_sensor7()
    # print_sensors()
    # print(f"{change_group_state(4, {'on': False})}")
    # print(f"{change_light_state(16, {'on': False})}")
