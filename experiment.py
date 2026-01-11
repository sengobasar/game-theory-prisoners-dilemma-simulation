from strategies import Strategy, AlwaysCooperate, AlwaysDefect, TitForTat, GrimTrigger, RandomStrategy
from game import Game
from itertools import combinations_with_replacement

class Tournament:
    """
    Manages a round-robin tournament between strategies.
    """
    def __init__(self, strategies: list[Strategy], rounds_per_match: int = 200,
                 payoff_matrix: dict = None, noise: float = 0.0):
        self.strategies = strategies
        self.rounds_per_match = rounds_per_match
        self.payoff_matrix = payoff_matrix
        self.noise = noise
        self.results = []
        self.strategy_scores = {s.name: 0 for s in strategies}
        self.strategy_matches = {s.name: 0 for s in strategies}
        self.strategy_coop_rates = {s.name: [] for s in strategies}

    def run(self):
        """Runs the round-robin tournament."""
        # We use combinations_with_replacement to allow a strategy to play against a copy of itself
        pairs = list(combinations_with_replacement(self.strategies, 2))
        
        for p1, p2 in pairs:
            # We need fresh instances for each match to ensure no state carries over
            # However, our strategy classes are simple enough that .reset() works.
            # But wait, python objects are references. 
            # If I pass the SAME instance to Game, and p1 is p2, it might get confused if they share state (like GrimTrigger).
            # For self-play, we MUST have two distinct instances of the same class.
            
            s1 = p1.__class__()
            s2 = p2.__class__()
            
            game = Game((s1, s2), self.rounds_per_match, 
                       payoff_matrix=self.payoff_matrix, noise=self.noise)
            game.run()
            res = game.get_results()
            
            self.results.append({
                "p1_name": s1.name,
                "p2_name": s2.name,
                "p1_score": res["p1_score"],
                "p2_score": res["p2_score"],
                "p1_history": res["p1_history"],
                "p2_history": res["p2_history"],
                "p1_scores": res["p1_scores"],
                "p2_scores": res["p2_scores"]
            })
            
            # Aggregate scores
            self.strategy_scores[s1.name] += res["p1_score"]
            self.strategy_matches[s1.name] += 1
            self.strategy_scores[s2.name] += res["p2_score"]
            self.strategy_matches[s2.name] += 1
            
            # Aggregate cooperation rates
            coop_rate_p1 = res["p1_history"].count("C") / self.rounds_per_match
            coop_rate_p2 = res["p2_history"].count("C") / self.rounds_per_match
            self.strategy_coop_rates[s1.name].append(coop_rate_p1)
            self.strategy_coop_rates[s2.name].append(coop_rate_p2)

    def get_summary(self):
        """Returns summarized stats for the tournament."""
        summary = []
        for name in self.strategy_scores:
            avg_score = self.strategy_scores[name] / self.strategy_matches[name]
            all_rates = self.strategy_coop_rates[name]
            avg_coop = sum(all_rates) / len(all_rates) if all_rates else 0
            summary.append({
                "strategy": name,
                "avg_score_per_match": avg_score,
                "avg_score_per_round": avg_score / self.rounds_per_match,
                "cooperation_rate": avg_coop
            })
        return sorted(summary, key=lambda x: x["avg_score_per_match"], reverse=True)
