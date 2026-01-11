from strategies import Strategy

class Game:
    """
    Engine to run a single match of Iterated Prisoner's Dilemma.
    """
    
    # Payoff Matrix: (Player1, Player2)
    PAYOFFS = {
        ("C", "C"): (3, 3),
        ("C", "D"): (0, 5),
        ("D", "C"): (5, 0),
        ("D", "D"): (1, 1),
    }

    def __init__(self, strategies: tuple[Strategy, Strategy], rounds: int = 100, 
                 payoff_matrix: dict = None, noise: float = 0.0):
        self.p1 = strategies[0]
        self.p2 = strategies[1]
        self.rounds = rounds
        self.noise = noise
        
        # Default Payoff: (P1, P2)
        # C/C=(3,3), C/D=(0,5), D/C=(5,0), D/D=(1,1)
        self.payoffs = payoff_matrix if payoff_matrix else {
            ("C", "C"): (3, 3),
            ("C", "D"): (0, 5),
            ("D", "C"): (5, 0),
            ("D", "D"): (1, 1),
        }
        
        self.history_p1 = []
        self.history_p2 = []
        self.scores_p1 = []
        self.scores_p2 = []
        self.log = []

    def run(self):
        """Runs the game for the specified number of rounds."""
        import random
        
        # Reset strategies before starting
        self.p1.reset()
        self.p2.reset()
        
        self.log = []
        
        for i in range(self.rounds):
            score1 = sum(self.scores_p1)
            score2 = sum(self.scores_p2)
            move1_raw = self.p1.move(self.history_p1, self.history_p2, score1)
            move2_raw = self.p2.move(self.history_p2, self.history_p1, score2) 
            
            # Apply Noise (Trembling Hand)
            move1 = self._apply_noise(move1_raw)
            move2 = self._apply_noise(move2_raw)
            
            self.history_p1.append(move1)
            self.history_p2.append(move2)
            
            s1, s2 = self.payoffs[(move1, move2)]
            self.scores_p1.append(s1)
            self.scores_p2.append(s2)
            
            self.log.append({
                "round": i + 1,
                "p1_strategy": self.p1.name,
                "p2_strategy": self.p2.name,
                "p1_move_raw": move1_raw,
                "p2_move_raw": move2_raw,
                "p1_move": move1,
                "p2_move": move2,
                "p1_score": s1,
                "p2_score": s2,
            })

    def _apply_noise(self, move: str) -> str:
        """Flips the move with probability `self.noise`."""
        import random
        if random.random() < self.noise:
            return "D" if move == "C" else "C"
        return move

    def get_results(self):
        """Returns a summary of the game."""
        return {
            "p1_name": self.p1.name,
            "p2_name": self.p2.name,
            "p1_score": sum(self.scores_p1),
            "p2_score": sum(self.scores_p2),
            "p1_history": self.history_p1,
            "p2_history": self.history_p2,
            "p1_scores": self.scores_p1,
            "p2_scores": self.scores_p2,
            "rounds": self.rounds,
            "noise": self.noise,
            "log": self.log
        }
