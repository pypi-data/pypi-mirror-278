import torchbringer.components.builders as builders
import torch

# if GPU is to be used
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class TorchBringerAgent():
    def __init__(self) -> None:
        self.learner = None
    

    def initialize(self, config):
        self.learner = builders.build_learner(config)
    

    def step(self, state, reward, terminal):
        self.learner.experience(state, reward, terminal)
        self.learner.optimize()
        return torch.tensor([], device=device) if state is None else self.learner.select_action(state)
    
    # TODO: This should be returned by the step function to avoid multiple calls when dealing with remote learning
    def get_past_loss(self):
        if hasattr(self.learner, "past_loss"):
            return self.learner.past_loss
        return 0.0