try:
    import matplotlib.pyplot as plt
    import pandas as pd
    VISUALIZATION_AVAILABLE = True
except ImportError:
    VISUALIZATION_AVAILABLE = False
    print("Warning: matplotlib or pandas not found. Visualization will be skipped.")

from strategies import AlwaysCooperate, AlwaysDefect, TitForTat, GrimTrigger, RandomStrategy
from experiment import Tournament

def main():
    print("Initializing Prisoner's Dilemma Tournament...")
    
    # 1. Setup Strategies
    strategies = [
        AlwaysCooperate(),
        AlwaysDefect(),
        TitForTat(),
        GrimTrigger(),
        RandomStrategy()
    ]
    
    # 2. Run Tournament
    rounds = 100
    tournament = Tournament(strategies, rounds_per_match=rounds)
    print(f"Running round-robin tournament with {rounds} rounds per match...")
    tournament.run()
    
    # 3. Process Results
    summary = tournament.get_summary()
    
    print("\n--- Tournament Results ---")
    print(f"{'Strategy':<20} | {'Avg Score/Match':<15} | {'Avg Score/Round':<15} | {'Coop Rate':<10}")
    print("-" * 70)
    for s in summary:
        print(f"{s['strategy']:<20} | {s['avg_score_per_match']:<15.2f} | {s['avg_score_per_round']:<15.2f} | {s['cooperation_rate']:<10.2%}")

    # 4. Visualization
    if VISUALIZATION_AVAILABLE:
        create_visualizations(summary, tournament)
    else:
        print("\nSkipping visualization (dependencies missing).")

def create_visualizations(summary, tournament):
    """Generates plots for the tournament results."""
    # Convert summary to DataFrame for easier plotting
    df = pd.DataFrame(summary)
    
    # Plot 1: Average Score per Strategy
    try:
        plt.figure(figsize=(10, 6))
        plt.bar(df['strategy'], df['avg_score_per_match'], color='steelblue')
        plt.title('Average Score per Match by Strategy')
        plt.xlabel('Strategy')
        plt.ylabel('Average Score')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.savefig('avg_score.png')
        print("\nVisualization saved: avg_score.png")
        
        # Plot 2: Cooperation Rate per Strategy
        plt.figure(figsize=(10, 6))
        plt.bar(df['strategy'], df['cooperation_rate'], color='forestgreen')
        plt.title('Cooperation Rate by Strategy')
        plt.xlabel('Strategy')
        plt.ylabel('Cooperation Rate')
        plt.ylim(0, 1)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.savefig('coop_rate.png')
        print("Visualization saved: coop_rate.png")

        # Plot 3: Score Evolution for a specific interesting match (e.g., TitForTat vs Random)
        match_data = next((r for r in tournament.results if r["p1_name"] == "TitForTat" and r["p2_name"] == "RandomStrategy"), None)
        
        if match_data:
            cum_p1 = [sum(match_data["p1_scores"][:i+1]) for i in range(len(match_data["p1_scores"]))]
            cum_p2 = [sum(match_data["p2_scores"][:i+1]) for i in range(len(match_data["p2_scores"]))]
            
            plt.figure(figsize=(10, 6))
            plt.plot(cum_p1, label='TitForTat')
            plt.plot(cum_p2, label='RandomStrategy')
            plt.title('Score Evolution: TitForTat vs Random')
            plt.xlabel('Round')
            plt.ylabel('Cumulative Score')
            plt.legend()
            plt.grid(True, linestyle='--', alpha=0.5)
            plt.savefig('match_evolution.png')
            print("Visualization saved: match_evolution.png")
    except Exception as e:
        print(f"Error generating visualizations: {e}")

if __name__ == "__main__":
    main()
