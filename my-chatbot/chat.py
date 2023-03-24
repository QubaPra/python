import json
import random
from difflib import get_close_matches

# Wczytaj plik JSON
with open('ans.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Zdefiniuj funkcję, która znajduje najlepiej pasujący wzorzec
def get_best_matching_pattern(input_str):
    # Konwertuj wprowadzony ciąg znaków na małe litery
    input_str = input_str.lower()
    # Zdefiniuj listę, w której będą przechowywane możliwe dopasowania
    possible_matches = []
    # Przejdź przez każdy wzorzec w danych
    for item in data:
        # Przejdź przez każdy ciąg znaków w wzorcu
        for pattern in item['pattern']:
            # Konwertuj wzorzec na małe litery
            pattern = pattern.lower()
            # Użyj funkcji get_close_matches, aby znaleźć najlepsze dopasowanie
            match = get_close_matches(input_str, [pattern])
            # Jeśli jest dopasowanie, dodaj je do listy możliwych dopasowań
            if match:
                possible_matches.append((item['tag'], match[0]))
    # Jeśli nie ma dopasowań, zwróć None
    if not possible_matches:
        return None
    # Posortuj możliwe dopasowania według wyniku podobieństwa malejąco
    possible_matches.sort(key=lambda x: get_close_matches(input_str, [x[1]])[0], reverse=True)
    # Zwróć tag najlepiej pasującego wzorca
    return possible_matches[0][0]

# Zdefiniuj funkcję, która zwraca losową odpowiedź na podstawie wprowadzonego ciągu znaków
def get_response(input_str):
    # Znajdź tag najlepiej pasującego wzorca
    tag = get_best_matching_pattern(input_str)
    # Jeśli nie ma pasującego wzorca, zwróć None
    if not tag:
        return None
    # Znajdź odpowiedź związana z tagiem
    responses = [r for item in data for r in item['responses'] if item['tag'] == tag]
    response = random.choice(responses)
    return response

# Pobierz dane od użytkownika i uzyskaj odpowiedź
while True:
    input_str = input("Ty: ")
    response = get_response(input_str)
    if response:
        print("Bot: " + response)
    else:
        print("Bot: Przepraszam, nie zrozumiałem.")
