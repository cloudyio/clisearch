import click
import webbrowser
import json 
import re
import os
import datetime
import urllib

path = os.path.join(os.path.expanduser("~"), ".searchcli/bang.json")
if not os.path.exists(path):
    url = "https://raw.githubusercontent.com/cloudyio/clisearch/refs/heads/main/search/config/bang.json"
    bang_path = os.path.join(os.path.expanduser("~"), ".searchcli/bang.json")
    os.makedirs(os.path.dirname(bang_path), exist_ok=True)
    urllib.request.urlretrieve(url, bang_path)

    config_path = os.path.join(os.path.expanduser("~"), ".searchcli/config.json")
    config_data = {"default": "g"}
    with open(config_path, "w") as config_file:
        json.dump(config_data, config_file, indent=4)
bangs = json.loads(open(path).read())

config_path = os.path.join(os.path.expanduser("~"), ".searchcli/config.json")
config = json.loads(open(config_path).read())

history_path = os.path.join(os.path.expanduser("~"), ".searchcli/history.json")
if not os.path.exists(history_path):
    with open(history_path, "w") as file:
        json.dump([], file)
history = json.loads(open(history_path).read())



@click.command()
@click.option('--default', help='default bang, if not sure set to g')
@click.argument('query', nargs=-1)
def search(default, query):
    link = None

    if default:
        for i in bangs:
            if i["t"] == default:
                link = "pass"
                break
        
        if link == None:
            click.echo("This bang is invalid, make your you are setting it correctly! Example: search --default 'g'")
            return
             
        config["default"] = default
        with open(config_path, "w") as file:
            json.dump(config, file, indent=4) 
            file.close()

        click.echo(f"Set bang to {default}")
        return
    else:
        default = config["default"]
    
    
    query = ' '.join(query)
    match = re.search(r"!(\w+)", query)
    if match: 
        bang = match.group(1)
    else:
        bang = default

    query = re.sub(r"!\w+", "", query, count=1).strip()

    for i in bangs:
        if i["t"] == bang:
            link = i["u"]
            break
    if link == None:
        click.echo("Invalid bang!, bang can be reset with search --default = 'g' if needed")
        return

    link = link.replace("{{{s}}}", query)

    history.append({"date": datetime.datetime.now().isoformat(), "link": link})
    with open(history_path, "w") as file:
        json.dump(history, file, indent=4)
        file.close()

    webbrowser.open(link, new=2)

if __name__ == "__main__":
    search()