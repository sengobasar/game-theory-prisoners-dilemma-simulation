import random
from abc import ABC, abstractmethod

class Strategy(ABC):
    """Abstract base class for a Prisoner's Dilemma strategy."""

    def __init__(self):
        self.name = self.__class__.__name__

    @abstractmethod
    def move(self, my_history: list[str], opponent_history: list[str], my_score: int) -> str:
        """
        Decide on the next move based on history.
        
        Args:
            my_history: List of my past moves.
            opponent_history: List of opponent's past moves.
            my_score: Current total score.
            
        Returns:
            "C" for Cooperate, "D" for Defect.
        """
        pass

    def reset(self):
        """Reset any internal state if necessary."""
        pass


class AlwaysCooperate(Strategy):
    """Always chooses Cooperate."""
    def move(self, my_history: list[str], opponent_history: list[str], my_score: int) -> str:
        return "C"


class AlwaysDefect(Strategy):
    """Always chooses Defect."""
    def move(self, my_history: list[str], opponent_history: list[str], my_score: int) -> str:
        return "D"


class TitForTat(Strategy):
    """Cooperates on the first move, then copies the opponent's last move."""
    def move(self, my_history: list[str], opponent_history: list[str], my_score: int) -> str:
        if not opponent_history:
            return "C"
        return opponent_history[-1]


class GrimTrigger(Strategy):
    """Cooperates until the opponent defects once, then defects forever."""
    def __init__(self):
        super().__init__()
        self.triggered = False

    def move(self, my_history: list[str], opponent_history: list[str], my_score: int) -> str:
        if not opponent_history:
            return "C"
        
        if self.triggered:
            return "D"
        
        if opponent_history[-1] == "D":
            self.triggered = True
            return "D"
            
        return "C"

    def reset(self):
        self.triggered = False


class RandomStrategy(Strategy):
    """Randomly chooses Cooperate or Defect with equal probability."""
    def move(self, my_history: list[str], opponent_history: list[str], my_score: int) -> str:
        return "C" if random.random() < 0.5 else "D"
