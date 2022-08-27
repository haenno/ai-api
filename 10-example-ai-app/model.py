import torch
import torch.nn as nn
from config import CPUGPU


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
