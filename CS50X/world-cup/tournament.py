# Simulate a sports tournament

import csv
import sys
import random

# Number of simluations to run
N = 1000


def main():

    # Ensure correct usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python tournament.py FILENAME")

    teams = []

    with open(sys.argv[1]) as file:  # Open csv in file variable
        reader = csv.DictReader(file)  # Read it as a dictionary in object reader
        for row in reader:  # For every row in object reader
            teams.append({"team": row["team"], "rating": int(row["rating"])})
            # Create a dictionary in teams list, so for every value in list, I get a team and rating

    counts = {}

    for i in range(N):  # Run a 1000 simulations
        winner = simulate_tournament(teams)  # I only sent the name of the team, no worries about list and dict keys
        if winner in counts:  # If winner is already present in counts dictionary, add 1 to the count in that place
            counts[winner] += 1
        else:  # Otherwise create the key and make it 1
            counts[winner] = 1

    # Print each team's chances of winning, according to simulation
    for team in sorted(counts, key=lambda team: counts[team], reverse=True):
        print(f"{team}: {counts[team] * 100 / N:.1f}% chance of winning")


def simulate_game(team1, team2):
    """Simulate a game. Return True if team1 wins, False otherwise."""
    rating1 = team1["rating"]
    rating2 = team2["rating"]
    probability = 1 / (1 + 10 ** ((rating2 - rating1) / 600))
    return random.random() < probability


def simulate_round(teams):
    """Simulate a round. Return a list of winning teams."""
    winners = []

    # Simulate games for all pairs of teams
    for i in range(0, len(teams), 2):
        if simulate_game(teams[i], teams[i + 1]):
            winners.append(teams[i])
        else:
            winners.append(teams[i + 1])

    return winners


def simulate_tournament(teams):
    """Simulate a tournament. Return name of winning team."""

    while True:  # Create a loop to iterate through the rounds in a tournament
        teams = simulate_round(teams)  # Send it to the round simulation
        if len(teams) < 2:  # If I only get one team, the winner
            return teams[0]["team"]
            # Send only the name of the team, present in the first place of the list, with a key of team


if __name__ == "__main__":
    main()