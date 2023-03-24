import random
import yaml

def load_data():
    with open("data.yml", "r",encoding="utf-8") as stream:
        try:
            data = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return data

def save_data(data):
    with open("data.yml", "w",encoding="utf-8") as stream:
        try:
            yaml.dump(data, stream, allow_unicode=True, default_flow_style=False)
        except yaml.YAMLError as exc:
            print(exc)

data = load_data()

if not data:
    quit()

for key in data["questions"]:
    if key not in data["answers"]:
        data["answers"][key] = []
    question = random.choice(data["questions"][key])
    answer = input(question + " ")
    found = False
    if data["answers"][key]:
        for i, entry in enumerate(data["answers"][key]):
            for k in entry.keys():
                if answer.lower() == k.lower():
                    found = True
                    data["answers"][key][i][k] += 1
                    break
            if found:
                break
    if not found:
        if data["answers"][key] is None:
            data["answers"][key] = []
        data["answers"][key].append({answer: 1})
    save_data(data)

