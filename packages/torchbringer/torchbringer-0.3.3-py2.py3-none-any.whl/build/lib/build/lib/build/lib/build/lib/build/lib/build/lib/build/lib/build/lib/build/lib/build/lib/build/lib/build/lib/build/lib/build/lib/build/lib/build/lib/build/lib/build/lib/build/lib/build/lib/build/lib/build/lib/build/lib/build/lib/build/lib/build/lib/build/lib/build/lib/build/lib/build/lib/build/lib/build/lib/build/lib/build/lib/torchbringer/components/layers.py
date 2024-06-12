import torch.nn as nn


class Normalize(nn.Module):
    def __init__(self, max):
        super(Normalize, self).__init__()
        self.max = max

    def forward(self, input):
        return input / self.max