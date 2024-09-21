# import yaml
# import json
from liquid import Template
import time
from datetime import datetime

# with open('data.yml', 'r') as file:
#     data = yaml.safe_load(file)

# with open('imdb_result.json', 'r') as file:
#     imdb_result = json.load(file)

date_offsets = {}

last_added_pos = 0.

for i in range(2000, 2100):
    now = time.time()
    target = datetime.fromisoformat(f"{i}-01-01").timestamp()
    if target >= now:
        break
    diff = now - target
    pos = 0.9999 ** (diff / 30000)
    if pos - last_added_pos > 0.07:
        last_added_pos = pos
        date_offsets[i] = pos * 50

def generate_html():
    with open('template.liquid', 'r') as file:
        template = file.read()
    template = Template(template)
    html = template.render(data={
        "date_offsets_years": list(date_offsets.keys()),
        "date_offsets": date_offsets,
    })
    with open('dist/index.html', 'w') as file:
        file.write(html)

#check_if_imdb_is_update()
generate_html()