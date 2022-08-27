from pickle import NONE
import random
import json
import torch
import uuid
import csv

from datetime import datetime
from model import NeuralNet
from bow import bag_of_words
from config import CPUGPU, OPEN_QUESTIONS_FILE, SRC_FILE, MIN_PROB, OUT_FILE, DIALOG_LOG_FILE

device = torch.device(CPUGPU)

with open(SRC_FILE, 'r', encoding='utf-8') as json_data:
    intents = json.load(json_data)

data = torch.load(OUT_FILE, map_location=torch.device(CPUGPU))

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Chatbot"
print("Lass quatschen -- Schreib einfach drauf los! (tippe 'ende' zum beenden)")


def log_dialog(type, log_str="", prob=None):
    '''
    200 = start chat session
    400 = user input
    600 = chatbot answer, understood
    650 = chatbot answer, unshure
    900 = end chat session with keyword
    '''

    with open(DIALOG_LOG_FILE, 'a', encoding='utf-8') as f:
        if prob:
            f.write(log_uuid + ";" + str(datetime.now()) + ";" +
                    str(type) + ";\"" + log_str + "\";" + str(prob) + "\n")
        else:
            f.write(log_uuid + ";" + str(datetime.now()) +
                    ";" + str(type) + ";\"" + log_str + "\";\n")


def get_new_uuid():
    while True:
        new_uuid = str(uuid.uuid4())
        found = False
        try:
            with open(DIALOG_LOG_FILE, 'r') as f:
                my_content = csv.reader(f, delimiter=';')
                for row in my_content:
                    if new_uuid == row[0]:
                        found = True
                        break
            if not found:
                return new_uuid
        except FileNotFoundError:
            return new_uuid


log_uuid = get_new_uuid()

log_dialog(200)

while True:
    # sentence
    sentence = input("            Du: ")

    log_dialog(400, sentence)

    if sentence == "ende":
        log_dialog(900)
        break

    #sentence = tokenize(sentence)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1).to(CPUGPU)
    prob = probs[0][predicted.item()]
    probstr = str(int(prob.item() * 100)) + " %"

    if prob.item() > MIN_PROB:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                answer = random.choice(intent['responses'])
                print(f"{bot_name} [{probstr}]: {answer}")
                log_dialog(600, answer, prob.item())
    else:
        print(f"{bot_name} [{probstr}]: Das habe ich nicht verstanden...")
        log_dialog(650, "", prob.item())

        with open(OPEN_QUESTIONS_FILE, 'a', encoding='utf-8') as f:
            f.write("\"" + str(datetime.now()) + "\";\"" + sentence + "\"\n")
