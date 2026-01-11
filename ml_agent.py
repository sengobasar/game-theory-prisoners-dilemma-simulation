import random
from strategies import Strategy

class QLearningAgent(Strategy):
    """
    Q-Learning Agent for Iterated Prisoner's Dilemma.
    State: (My Last Move, Opponent Last Move)
    Action: C or D
    Reward: Change in score from previous round.
    """
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1):
        super().__init__()
        self.alpha = alpha      # Learning Rate
        self.gamma = gamma      # Discount Factor
        self.epsilon = epsilon  # Exploration Rate
        self.q_table = {}       # Map state -> current q-values {action: value}
        self.last_state = None
        self.last_action = None
        self.last_score = 0

    def get_q(self, state, action):
        if state not in self.q_table:
            self.q_table[state] = {"C": 0.0, "D": 0.0}
        return self.q_table[state][action]

    def update_q(self, state, action, reward, next_state):
        if state is None: return
        
        current_q = self.get_q(state, action)
        
        # Max Q for next state
        if next_state not in self.q_table:
            self.q_table[next_state] = {"C": 0.0, "D": 0.0}
        max_next_q = max(self.q_table[next_state].values())
        
        # Q-Learning Update Rule
        new_q = current_q + self.alpha * (reward + self.gamma * max_next_q - current_q)
        self.q_table[state][action] = new_q

    def move(self, my_history: list[str], opponent_history: list[str], my_score: int) -> str:
        # Determine current state
        if not my_history:
            state = "START"
        else:
            state = (my_history[-1], opponent_history[-1])
            
        # Calculate Reward from *previous* action
        if self.last_state is not None:
            reward = my_score - self.last_score
            self.update_q(self.last_state, self.last_action, reward, state)
            
        # Choose Action (Epsilon-Greedy)
        if random.random() < self.epsilon:
            action = random.choice(["C", "D"])
        else:
            if state not in self.q_table:
                self.q_table[state] = {"C": 0.0, "D": 0.0}
            # Pick action with highest Q
            qs = self.q_table[state]
            if qs["C"] == qs["D"]:
                action = random.choice(["C", "D"])
            else:
                action = max(qs, key=qs.get)
        
        # Update memory
        self.last_state = state
        self.last_action = action
        self.last_score = my_score # Wait, my_score includes this round? NO. my_score is score *before* this move?
        # NO. Game loop:
        # score1 = sum(scores) -> Score from rounds 0 to t-1.
        # move() called.
        # So my_score IS the total score accumulated so far.
        # So (my_score - self.last_score) IS the reward from the round that just finished.
        
        return action

    def reset(self):
        self.last_state = None
        self.last_action = None
        self.last_score = 0
        # Note: We do NOT reset q_table to allow learning across matches if desired.
        # But if we want fresh agent, caller handles it.
