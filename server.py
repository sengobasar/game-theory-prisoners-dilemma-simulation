from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn

# Import Engine Logic
from game import Game
from strategies import Strategy, AlwaysCooperate, AlwaysDefect, TitForTat, GrimTrigger, RandomStrategy
from ml_agent import QLearningAgent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development convenience
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registry of available strategies
STRATEGIES = {
    "AlwaysCooperate": AlwaysCooperate,
    "AlwaysDefect": AlwaysDefect,
    "TitForTat": TitForTat,
    "GrimTrigger": GrimTrigger,
    "RandomStrategy": RandomStrategy,
    "QLearningAgent": QLearningAgent
}

# State
current_game: Optional[Game] = None
p1_instance: Optional[Strategy] = None
p2_instance: Optional[Strategy] = None

class SimConfig(BaseModel):
    p1_strategy: str
    p2_strategy: str
    rounds: int = 100
    noise: float = 0.0
    payoff_matrix: Optional[Dict[str, tuple]] = None # Simplified for JSON

@app.get("/strategies")
def get_strategies():
    return {"strategies": list(STRATEGIES.keys())}

@app.post("/simulation/run")
def run_simulation(config: SimConfig):
    global current_game, p1_instance, p2_instance
    
    if config.p1_strategy not in STRATEGIES or config.p2_strategy not in STRATEGIES:
        raise HTTPException(status_code=400, detail="Invalid strategy")
        
    s1_cls = STRATEGIES[config.p1_strategy]
    s2_cls = STRATEGIES[config.p2_strategy]
    
    # Instantiate
    p1_instance = s1_cls()
    p2_instance = s2_cls()
    
    # Handle Payoff Matrix conversion if needed (JSON dict key is string "C,C", Game needs tuple ("C","C"))
    # For now, use default if None
    
    current_game = Game((p1_instance, p2_instance), rounds=config.rounds, noise=config.noise)
    current_game.run()
    
    return current_game.get_results()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
