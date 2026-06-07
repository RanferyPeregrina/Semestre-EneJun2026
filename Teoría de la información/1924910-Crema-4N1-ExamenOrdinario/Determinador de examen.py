import random
import requests
import re
from collections import Counter

TARGET_WORDS = 500

matricula = input("Introduce tu matrícula: ")

while not re.fullmatch(r"\d{7}", matricula):
    matricula = input("La matrícula debe tener exactamente siete dígitos. Introdúcela nuevamente: ")

random.seed(int(matricula))

url = "https://www.gutenberg.org/files/1342/1342-0.txt"
text = requests.get(url).text

words = re.findall(r"\b[a-zA-Z']+\b", text.lower())

freq = Counter(words)

vocabulary = list(freq.keys())
weights = list(freq.values())

phrases = []

for n in [2, 3]:
    ngrams = zip(*[words[i:] for i in range(n)])
    counts = Counter(ngrams)

    for gram, count in counts.items():
        if count > 20:
            phrases.append((" ".join(gram), count))

phrase_texts = [p[0] for p in phrases]
phrase_weights = [p[1] for p in phrases]

while True:
    generated = []
    count = 0

    while count < TARGET_WORDS:
        if phrases and random.random() < 0.15:
            phrase = random.choices(phrase_texts, weights=phrase_weights, k=1)[0]
            pw = phrase.split()

            if count + len(pw) <= TARGET_WORDS:
                generated.extend(pw)
                count += len(pw)
        else:
            word = random.choices(vocabulary, weights=weights, k=1)[0]
            generated.append(word)
            count += 1

    if any(len(word) == 10 for word in generated):
        break

sentences = []
temp = []

for word in generated:
    temp.append(word)

    if len(temp) >= random.randint(8, 16):
        sentences.append(" ".join(temp).capitalize() + ".")
        temp = []

if temp:
    sentences.append(" ".join(temp).capitalize() + ".")

final_text = " ".join(sentences)

print(final_text)