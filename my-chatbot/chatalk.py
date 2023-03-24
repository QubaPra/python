import yaml
import random
from difflib import get_close_matches

# Load the data from the YAML file
with open('data.yml', 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)

with open('other.yml', 'r', encoding='utf-8') as f2:
    other_data = yaml.safe_load(f2)

while True:
    # Get the input question from the user
    question = input("Ty: ")
    quelist = [pattern.lower() for key in data['questions'] for pattern in data['questions'][key]]

    best_match = get_close_matches(question, quelist, n=1, cutoff=0.5)

    if not best_match:
        best_match = get_close_matches(question, other_data.keys(), n=1, cutoff=0.2)
        if not best_match:
            print("Nie znam odpowiedzi na to pytanie :(")
        else:
            print(random.choice(other_data[best_match[0]]))
    else:
        for key, patterns in data['questions'].items():
            if best_match[0] in [pattern.lower() for pattern in patterns]:
                # Get the list of possible answers corresponding to the best matched question
                possible_answers = data['answers'][key]
                
                # Calculate the total count and the list of probabilities
                total_count = sum(answer.get(list(answer.keys())[0], 0) for answer in possible_answers)
                probabilities = [answer.get(list(answer.keys())[0], 0) / total_count for answer in possible_answers]

                # Choose a random answer based on the probabilities
                answer = next(iter(random.choices(possible_answers, weights=probabilities)[0]))

                print("Quba:", answer)
