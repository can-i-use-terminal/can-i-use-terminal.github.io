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

for i in range(2000, 2100):
    now = time.time()
    target = datetime.fromisoformat(f"{i}-01-01").timestamp()
    if target >= now:
        break
    diff = now - target
    pos = 0.9999 ** (diff / 30000)
    date_offsets[i] = pos

def generate_html():
    with open('template.html', 'r') as file:
        template = file.read()
    template = Template(template)
    for x in imdb_result:
        x['date'] = x['date'].split()[2]
    html = template.render(data=imdb_result)
    with open('dist/index.html', 'w') as file:
        file.write(html)

#check_if_imdb_is_update()
generate_html()