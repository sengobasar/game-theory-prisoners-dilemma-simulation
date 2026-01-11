# Prisoner's Dilemma Laboratory 🧪

This is a playground to watch AI agents play the "Prisoner's Dilemma" against each other. It’s got a Python brain (backend) and a React face (frontend).

## How to Run It in 30 Seconds

You need **two** terminal windows open.

**Terminal 1: The Brain (Backend)**
```bash
python server.py
# If it says "address in use", kill any old python processes!
```

**Terminal 2: The Face (Frontend)**
```bash
cd client
npm run dev
```
Then just click the link it gives you (usually `http://localhost:5173`).

## The Agents 🤖

*   **AlwaysCooperate**: Nice guy. Always gets taken advantage of.
*   **AlwaysDefect**: Jerk. Always betrays you.
*   **TitForTat**: The fair one. Copies whatever you did last round.
*   **GrimTrigger**: Holds a grudge forever. One wrong move and he never trusts you again.
*   **Random**: Pure chaos.
*   **QLearningAgent**: The ML bot. It actually learns how to beat the others while playing.

## Cool Stuff to Try
*   Set **Noise** to `0.2` (20%) and watch `TitForTat` accidentally get into a war with itself.
*   Pit `QLearningAgent` against `TitForTat` and see if it learns to cooperate.

Enjoy the chaos!
