import yaml
# import json
from liquid import Template
import time
from datetime import datetime
import os

with open('data/root.yml', 'r') as file:
    data = yaml.safe_load(file)

data["terminal_data"] = {}

for terminal in data["terminals"]:
    with open(f'data/terminals/{terminal}.yml', 'r') as file:
        parsed = yaml.safe_load(file)
    data["terminal_data"][terminal] = parsed

for terminal in data["terminal_data"]:
    t = data["terminal_data"][terminal]
    for feature in t["features"]:
        f = t["features"][feature]
        for event in f["events"]:
            if not "date" in event:            
                event["date"] = t["created_date"]
            print(event)

MAX_POS = 70

def datetime_to_pos(d):
    now = time.time()
    target = d.timestamp()
    if now < target:
        raise "Can not show time in future"
    diff = now - target
    pos = 0.9999 ** (diff / 30000)
    return pos * MAX_POS

def event_segments(feature):
    events = feature["events"]
    links = feature["links"] if "links" in feature else []
    result = []
    current_event = { "name": "not_created", "pos": 0 }
    def close(pos):
        current_event["len"] = pos - current_event["pos"]
        result.append(current_event)

    for event in events:
        print("fff", event)
        pos = datetime_to_pos(datetime.combine(event["date"], datetime.min.time()))
        close(pos)
        current_event = { "name": event["status"], "pos": pos }
        if "links" in event:
            current_event["links"] = event["links"] + links
        else:
            current_event["links"] = links
    close(MAX_POS)
    return result

def current_status(events):
    e = events[-1]
    text = data["status_cases"][e["status"]]["name"]
    if "release" in e:
        text += " since " + e["release"]
    return { "status": e["status"], "text": text }

# with open('imdb_result.json', 'r') as file:
#     imdb_result = json.load(file)

date_offsets = {}

last_added_pos = 0.

for i in range(2000, 2100):
    now = time.time()
    target = datetime.fromisoformat(f"{i}-01-01").timestamp()
    if target >= now:
        break
    pos = datetime_to_pos(datetime.fromisoformat(f"{i}-01-01"))
    if pos - last_added_pos > 3.5:
        last_added_pos = pos
        date_offsets[i] = pos

def generate_html():
    with open('templates/feature.liquid', 'r') as file:
        feature_template = file.read()
    feature_template = Template(feature_template)
    with open('templates/index.liquid', 'r') as file:
        index_template = file.read()
    index_template = Template(index_template)
    os.makedirs("dist", exist_ok=True)
    os.makedirs("dist/features", exist_ok=True)
    html = index_template.render(data={
        "features": data["features"],
    })
    with open(f'dist/index.html', 'w') as file:
        file.write(html)
    for f in data["features"]:
        terminals = [t for t in data["terminals"] if f in data["terminal_data"][t]["features"]]
        html = feature_template.render(data={
            "feature": data["features"][f],
            "date_offsets_years": list(date_offsets.keys()),
            "date_offsets": date_offsets,
            "terminals": terminals,
            "terminal_data": data["terminal_data"],
            "segments": { t: event_segments(data["terminal_data"][t]["features"][f]) for t in terminals},
            "current_status": { t: current_status(data["terminal_data"][t]["features"][f]["events"]) for t in terminals},
            "status_cases": data["status_cases"],
        })
        with open(f'dist/features/{f}.html', 'w') as file:
            file.write(html)

generate_html()
