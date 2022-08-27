import json
import numpy as np

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

from model import NeuralNet
from bow import token_and_stem, bag_of_words_array
from config import CPUGPU, NUM_EPOCHS, SRC_FILE, OUT_FILE


with open(SRC_FILE, 'r', encoding='utf-8') as f:
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
num_epochs = NUM_EPOCHS

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

# save stuff
data = {
    "model_state": model.state_dict(),
    "input_size": input_size,
    "hidden_size": hidden_size,
    "output_size": output_size,
    "all_words": all_words,
    "tags": tags
}

torch.save(data, OUT_FILE)

print(f'training complete. file saved to {OUT_FILE}')
