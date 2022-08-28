from ast import arg
import nltk
import torch
import torch.nn as nn
import json
import numpy as np
import uuid
import random
import csv
import os

from pickle import NONE
from datetime import datetime
from argparse import ArgumentParser
from torch.utils.data import Dataset, DataLoader
from HanTa import HanoverTagger as ht


# CPUGPU = 'cuda:0'
CPUGPU = 'cpu'

SRC_FILE = 'intents.json'
OUT_FILE = 'data.pth'
OPEN_QUESTIONS_FILE = 'to_answer.csv'
DIALOG_LOG_FILE = 'dialog_log.csv'
MIN_PROB = 0.95

# nltk.download('punkt')  # run only once (uncomment once, to init a new system)
tagger = ht.HanoverTagger('morphmodel_ger.pgz')    

class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(NeuralNet, self).__init__()

        self.l1 = nn.Linear(input_size, hidden_size).to(CPUGPU)
        self.l2 = nn.Linear(hidden_size, hidden_size).to(CPUGPU)
        self.l3 = nn.Linear(hidden_size, num_classes).to(CPUGPU)

        self.relu = nn.ReLU().to(CPUGPU)

    def forward(self, x):
        out = self.l1(x)
        out = self.relu(out)
        out = self.l2(out)
        out = self.relu(out)
        out = self.l3(out)

        return out

def singlechat(conversation_uuid, text_input):

    device = torch.device(CPUGPU)
    data = torch.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), OUT_FILE), map_location=torch.device(CPUGPU))

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

    log_uuid = conversation_uuid

    log_dialog(log_uuid, 200)


    # sentence
    sentence = text_input

    log_dialog(log_uuid, 400, sentence)

    #sentence = tokenize(sentence)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1).to(CPUGPU)
    prob = probs[0][predicted.item()]

    if prob.item() > MIN_PROB:

        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), SRC_FILE), 'r', encoding='utf-8') as json_data:
            intents = json.load(json_data)

        for intent in intents['intents']:
            if tag == intent["tag"]:
                answer = random.choice(intent['responses'])
                log_dialog(log_uuid, 600, answer, prob.item())
                return json.JSONEncoder().encode({
                    'probability' : float(prob.item()), 
                    'understood' : bool(True), 
                    'output' : str(answer),
                    })
    else:
        log_dialog(log_uuid, 650, "", prob.item())

        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), OPEN_QUESTIONS_FILE), 'a', encoding='utf-8') as f:
            f.write("\"" + str(datetime.now()) +
                    "\";\"" + sentence + "\"\n")
        return json.JSONEncoder().encode({
            'probability' : float(prob.item()), 
            'understood' : bool(False), 
            'output' : str("Das habe ich nicht verstanden...")
            })



def chat():

    device = torch.device(CPUGPU)
    data = torch.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), OUT_FILE), map_location=torch.device(CPUGPU))

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

    log_uuid = get_new_uuid()

    log_dialog(log_uuid, 200)

    while True:
        # sentence
        sentence = input("            Du: ")

        log_dialog(log_uuid, 400, sentence)

        if sentence == "ende":
            log_dialog(log_uuid, 900)
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

            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), SRC_FILE), 'r', encoding='utf-8') as json_data:
                intents = json.load(json_data)

            for intent in intents['intents']:
                if tag == intent["tag"]:
                    answer = random.choice(intent['responses'])
                    print(f"{bot_name} [{probstr}]: {answer}")
                    log_dialog(log_uuid, 600, answer, prob.item())
        else:
            print(f"{bot_name} [{probstr}]: Das habe ich nicht verstanden...")
            log_dialog(log_uuid, 650, "", prob.item())

            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), OPEN_QUESTIONS_FILE), 'a', encoding='utf-8') as f:
                f.write("\"" + str(datetime.now()) +
                        "\";\"" + sentence + "\"\n")


def log_dialog(log_uuid, type, log_str="", prob=None):
    '''
     50 = uuid created
     51 = uuid created, no log file present
    200 = start chat session
    400 = user input
    600 = chatbot answer, understood
    650 = chatbot answer, unshure
    900 = end chat session with keyword
    '''

    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), DIALOG_LOG_FILE), 'a', encoding='utf-8') as f:
        if prob:
            f.write(str(log_uuid) + ";" + str(datetime.now()) + ";" +
                    str(type) + ";\"" + log_str + "\";" + str(prob) + "\n")
        else:
            f.write(str(log_uuid) + ";" + str(datetime.now()) +
                    ";" + str(type) + ";\"" + log_str + "\";\n")


def get_new_uuid():
    while True:
        new_uuid = str(uuid.uuid4())
        found = False
        try:
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), DIALOG_LOG_FILE), 'r') as f:
                my_content = csv.reader(f, delimiter=';')
                for row in my_content:
                    if new_uuid == row[0]:
                        found = True
                        break
            if not found:
                log_dialog(new_uuid, 50)
                return new_uuid
        except FileNotFoundError:
                log_dialog(new_uuid, 51)
                return new_uuid
            


def token_and_stem(text):
    text = str(text)
    bag_of_words = []
    delimiters = ('.')
    split_char = '+'

    tokenized_sentence = nltk.tokenize.word_tokenize(text, language='german')

    for word in tokenized_sentence:
        stemmed_words = tagger.analyze(word, taglevel=2)
        stemmed_words = stemmed_words[0]

        for char in delimiters:
            stemmed_words = stemmed_words.replace(char, split_char)

        seperated_stemmed_words = stemmed_words.split(split_char)
        for single_stemmed_word in seperated_stemmed_words:
            if len(single_stemmed_word) > 1 and single_stemmed_word not in bag_of_words:
                bag_of_words.append(single_stemmed_word)

    return bag_of_words


def token_and_stem_array(text):
    #text = str(text)
    new_text = ""
    for word in text:
        new_text = new_text + str(word) + " "
    text = new_text
    bag_of_words = []
    delimiters = ('.')
    split_char = '+'

    tokenized_sentence = nltk.tokenize.word_tokenize(text, language='german')

    for word in tokenized_sentence:
        stemmed_words = tagger.analyze(word, taglevel=2)
        stemmed_words = stemmed_words[0]

        for char in delimiters:
            stemmed_words = stemmed_words.replace(char, split_char)

        seperated_stemmed_words = stemmed_words.split(split_char)

        for single_stemmed_word in seperated_stemmed_words:
            if len(single_stemmed_word) > 1 and single_stemmed_word not in bag_of_words:
                bag_of_words.append(single_stemmed_word)
    return bag_of_words


def bag_of_words(tokenized_sentence, all_words):

    tokenized_sentence = token_and_stem(tokenized_sentence)
    bag = np.zeros(len(all_words), dtype=np.float32)

    for idx, w in enumerate(all_words):
        if w in tokenized_sentence:
            bag[idx] = 1

    return bag


def bag_of_words_array(tokenized_sentence, all_words):
    tokenized_sentence = token_and_stem_array(tokenized_sentence)
    bag = np.zeros(len(all_words), dtype=np.float32)

    for idx, w in enumerate(all_words):
        if w in tokenized_sentence:
            bag[idx] = 1

    return bag


def train():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), SRC_FILE), 'r', encoding='utf-8') as f:
        dialogus = json.load(f)
    print(f'training starts with contents from file {SRC_FILE}')

    all_words = []
    tags = []
    xy = []

    for intent in dialogus['intents']:
        tag = intent['tag']
        tags.append(tag)
        for pattern in intent['patterns']:
            words = token_and_stem(pattern)
            all_words.extend(words)
            xy.append((words, tag))

    # input()
    x_train = []
    y_train = []

    for (patten_sentence, tag) in xy:
        bag = bag_of_words_array(patten_sentence, all_words)
        x_train.append(bag)

        label = tags.index(tag)
        y_train.append(label)

    # input()
    x_train = np.array(x_train)
    y_train = np.array(y_train)

    class ChatDataset(Dataset):
        def __init__(self):
            self.n_samples = len(x_train)
            self.x_data = x_train
            self.y_data = y_train

        # dataset[idx]
        def __getitem__(self, index):
            return self.x_data[index], self.y_data[index]

        def __len__(self):
            return self.n_samples

    # Hyperparmeters
    batch_size = 8
    hidden_size = 8
    output_size = len(tags)
    input_size = len(x_train[0])  # 1st is all_words
    learning_rate = 0.001
    num_epochs = 2000

    dataset = ChatDataset()
    train_loader = DataLoader(
        dataset=dataset, batch_size=batch_size, shuffle=True, num_workers=0)

    device = torch.device(CPUGPU)
    print("device: %s" % device)
    model = NeuralNet(input_size, hidden_size, output_size)

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    for epoch in range(num_epochs):
        for (words, labels) in train_loader:
            words = words.to(device)
            labels = labels.to(dtype=torch.long).to(device)

            # forward
            outputs = model(words)
            loss = criterion(outputs, labels)

            # backward
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        if (epoch + 1) % 100 == 0:
            print(f'epoch {epoch+1}/{num_epochs}, loss={loss.item():.4f}')

    print(f'final loss, loss={loss.item():.4f}')

    # save nn
    data = {
        "model_state": model.state_dict(),
        "input_size": input_size,
        "hidden_size": hidden_size,
        "output_size": output_size,
        "all_words": all_words,
        "tags": tags
    }

    torch.save(data, os.path.join(os.path.dirname(os.path.abspath(__file__)), OUT_FILE))

    print(f'training complete. file saved to {OUT_FILE}')


def main():
    parser = ArgumentParser(description='Allows the use of a chatbot with PyTorch.')

    parser.add_argument('-u', '--newuuid',  action='store_true',
                        help='Get a new, unique id for a conversation.')

    parser.add_argument('-t', '--train',  action='store_true',
                        help='Trains the NN model based on current data.')

    parser.add_argument('-c', '--chat',  action='store_true',
                        help='Chat with the chatbot.')

    parser.add_argument('-i', '--textinput',  type=str,
                        help='Give an text input to the chatbot and recive a answer. \
                            Provide a UUID for the conversation with -cu or --conversationuuid \
                                followed by the UUID.')

    parser.add_argument('-cu', '--conversationuuid',  type=str,
                        help='Needed when using -i, --textinput. Provide a UUID to a conversation.')

    args = parser.parse_args()

    
    if vars(args)['newuuid']:
        print(str(get_new_uuid()))
        quit()

    if vars(args)['train']:
        train()
        quit()    

    if vars(args)['chat']:
        chat()
        quit()
    
    # check for complete input for a 'singlechat' call
    complete_text_input = 0
    if vars(args)['textinput']:
        complete_text_input += 1 
    if vars(args)['conversationuuid']:       
        complete_text_input += 1 

    if complete_text_input == 1:
        parser.error("Too few arguments: -cu/--conversationuuid and -i/--textinput are both needed.")
    
    if complete_text_input == 2:
        print(str(singlechat(str(args.conversationuuid), str(args.textinput))))
        quit()

    parser.print_help()


if __name__ == '__main__':
    main()
