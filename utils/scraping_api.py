import requests
import json

base_url = "https://api.jikan.moe/v4/anime"
current_page = 0
has_next_page = True
temp = []

while has_next_page:
    current_page += 1
    res = requests.get(base_url+"?page={}".format(current_page)).json()
    has_next_page = res['pagination']['has_next_page']
    temp += res['data']
    print("Fetching page: {}".format(current_page))
    print("Temp range: {}".format(len(temp)))

json_object = json.dumps(temp, indent=4)

# Writing to anime.json
with open("anime.json", "w") as outfile:
    outfile.write(json_object)