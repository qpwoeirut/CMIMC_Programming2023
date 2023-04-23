from strategy import get_strategies
from typing import List
import random
import math

class AuctionHouseGrader:
    """
    AuctionHouse grading class used to locally test an auctionhouse submission.
    """

    NUM_LOSSES = 5

    def __init__(self, num_tournaments, debug) -> None:
        """
        Initializes the grader with the strategies and number of tournaments to run.

        :param dict strategies: dict of strategy ID to strategy function
        :param int num_tournaments: number of tournaments to run
        """
        strategies = get_strategies()
        self.bidders = [(f"{strategy.__name__} #{i}", strategy) for i, strategy in enumerate(strategies)]
        self.num_tournaments = num_tournaments

        self.debug = debug

        self.bidder_scores = {bidder[0]: 0 for bidder in self.bidders}

    def _run_single_tournament(self):
        curr_bidders = self.bidders[:]

        bidder_wallet = {bidder[0]: 100 for bidder in self.bidders}
        bidder_history = {bidder[0]: [] for bidder in self.bidders}
        bidder_losses = {bidder[0]: 0 for bidder in self.bidders}

        while len(curr_bidders) > 1:  # Simulates rounds
            next_bidders = []  # Keep track of bidders going to the next round
            losers = []  # Keep track of bidders who lose
            random.shuffle(curr_bidders)  # Pair up bidders randomly

            if len(curr_bidders) % 2 == 1:
                # If odd number of bidders, give the last bidder a free ticket to the next round
                next_bidders.append(curr_bidders[-1])

            for i in range(0, len(curr_bidders) - (len(curr_bidders) % 2), 2):  # Battle everyone else
                # Get the two bidders who are matched against each other (next to each other in permuted array)
                matched_bidders = [curr_bidders[i+j] for j in range(0, 2)]
                bidder_bids = []

                for j in range(0, 2):
                    bidder = matched_bidders[j]
                    opp = matched_bidders[1 - j]  # Get the other bidder
                    bidder_val = bidder[1](
                        bidder_wallet[bidder[0]], bidder_history[opp[0]])

                    if bidder_val < 0 or bidder_val > bidder_wallet[bidder[0]]:
                        # Need to add to losers to calculate scoring
                        losers.append(bidder)
                        bidder_bids.append(-1)  # Represents invalid bid
                    else:
                        bidder_bids.append(bidder_val)

                    bidder_wallet[bidder[0]] -= bidder_val

                if bidder_bids[0] == -1 or bidder_bids[1] == -1:  # Handle invalid bids
                    if bidder_bids[0] == -1 and bidder_bids[1] == -1:
                        continue  # Nothing left to do here
                    if bidder_bids[0] == -1:
                        # Automatically moves on to next round
                        next_bidders.append(matched_bidders[1])
                        bidder_history[matched_bidders[1][0]].append((bidder_bids[1], True))
                        continue
                    if bidder_bids[1] == -1:
                        next_bidders.append(matched_bidders[0])
                        bidder_history[matched_bidders[0][0]].append((bidder_bids[0], True))
                        continue

                # At this point, no bids are invalid
                winner = None
                loser = None
                if bidder_bids[0] == bidder_bids[1]:  # Coin flip
                    winner = random.randint(0, 1)
                else:
                    winner = 0 if bidder_bids[0] > bidder_bids[1] else 1
                loser = 1 - winner

                next_bidders.append(matched_bidders[winner])
                bidder_losses[matched_bidders[loser][0]] += 1
                bidder_history[matched_bidders[winner][0]].append((bidder_bids[winner], True))
                bidder_history[matched_bidders[loser][0]].append((bidder_bids[loser], False))
                if bidder_losses[matched_bidders[loser][0]] < self.NUM_LOSSES:
                    next_bidders.append(matched_bidders[loser])
                else:
                    losers.append(matched_bidders[loser])

            curr_bidders = next_bidders
            for loser in losers:
                self.bidder_scores[loser[0]] += 1/(1 + math.sqrt(len(curr_bidders)))

        if len(curr_bidders) == 1:
            self.bidder_scores[curr_bidders[0][0]] += 1
            if self.debug:
                print(f"The winner of the tournament is {curr_bidders[0][0]}")
        else:
            if self.debug:
                print("No winner")

    def grade(self) -> None:
        """
        Runs the grader by running the tournaments.
        """
        for i in range(self.num_tournaments):
            if self.debug:
                print(f"Running tournament {i+1}...")
            self._run_single_tournament()

    def print_result(self) -> dict:
        """
        Prints the result of the grading.
        """
        print("Results:")
        sorted_scores = dict(sorted(self.bidder_scores.items(), key=lambda item: item[1], reverse=True))
        i = 1
        print("{:<5} {:<20} {:<12}".format("Rank", "Strategy", "Score"))
        for bidder in sorted_scores:
            print("{:<5} {:<20} {:<12}".format(i, bidder, sorted_scores[bidder]))
            i += 1
