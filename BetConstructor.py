
import random
from attr import dataclass
import math

SPREAD = 0.16
SACRIFICE = 10000
POWER = 1
BIAS = 0.5


@dataclass
class Bet():
    id: str
    option: str
    promisedRate: float
    amount: float


def calculatePromisedRate(coefficient):
    return (1 - SPREAD) / coefficient


def calculateCoefficient(proportion):
    x = proportion**(0.25)
    m = 1 - (1/(POWER+1))
    b = 1 / (2 * (POWER + 1))
    return m * x + b
    # a = 1 - math.exp(-1 * POWER * (proportion + POWER))
    # b = 1 + math.exp(-1 * POWER * (proportion - BIAS))
    # return a / b


class BetConstructor():
    def __init__(self, options=["1", "X", "2"]):
        self.options = options  # list of options
        self.bets = []  # list of bets
        self.collected = 0  # amount of money collected
        self.coefficients = [1/len(options)] * \
            len(options)  # list of coefficients

    def updateCoefficients(self):
        # What if analysis to find how much of sacrifice we can have
        collected = self.collected
        total_amount_bet = sum(
            [math.log1p(bet.amount*bet.promisedRate) for bet in self.bets])
        amount_bet_on_each_option = [0] * len(self.options)

        for bet in self.bets:
            option_index = self.options.index(bet.option)
            amount_bet_on_each_option[option_index] += math.log1p(bet.amount *
                                                                  bet.promisedRate)

        for i, option in enumerate(self.options):
            percentage_of_total_bet_on_option = amount_bet_on_each_option[i] / \
                total_amount_bet
            new_coefficient = calculateCoefficient(
                percentage_of_total_bet_on_option)
            self.coefficients[i] = new_coefficient

        # normalize coefficients
        total_coefficient = sum(self.coefficients)
        self.coefficients = [coefficient /
                             total_coefficient for coefficient in self.coefficients]

        for index, option in enumerate(self.options):
            winningBets = [bet for bet in self.bets if bet.option == option]
            payout = sum(
                [bet.amount * bet.promisedRate for bet in winningBets])
            print(f"Total payout for {option} is {payout}", end=": ")
            print(
                f"Balance after payout is {SACRIFICE - payout + collected}")

    def printPayouts(self):
        for index, option in enumerate(self.options):
            print(option, ":", calculatePromisedRate(self.coefficients[index]))

    def placeBet(self, id, option, amount):

        optionIndex = self.options.index(option)
        promisedRate = calculatePromisedRate(self.coefficients[optionIndex])
        newBet = Bet(id, option, promisedRate, amount)
        self.bets.append(newBet)
        self.collected += amount
        global POWER
        POWER += 1
        self.updateCoefficients()
        return self.bets


if __name__ == "__main__":
    bet_constructor = BetConstructor(options=["1", "2"])
    bet_constructor.printPayouts()
    for i in range(10):
        option = random.choice(["1", "2"])
        amount = random.randrange(1, 1200)
        print(f"Placing bet {i} on {option} for {amount}")
        bet_constructor.placeBet(f"id_{i}", option, amount)
        bet_constructor.printPayouts()
