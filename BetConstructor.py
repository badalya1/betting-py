
from attr import dataclass


SPREAD = 0.12
SACRIFICE = 10000
POWER = 0.10


@dataclass
class Bet():
    id: str
    option: str
    promisedRate: float
    amount: float


def calculatePromisedRate(coefficient):
    return (1 - SPREAD) / coefficient


class BetConstructor():
    def __init__(self, options=["1", "2"]):
        self.options = options  # list of options
        self.bets = []  # list of bets
        self.collected = 0  # amount of money collected
        self.coefficients = [1/len(options)] * \
            len(options)  # list of coefficients

    def updateCoefficients(self):
        # What if analysis to find how much of sacrifice we can have
        totalPayout = sum([bet.amount * bet.promisedRate for bet in self.bets])
        collected = self.collected
        balance = min(SACRIFICE, totalPayout*2)

        for index, option in enumerate(self.options):
            winningBets = [bet for bet in self.bets if bet.option == option]
            payout = sum(
                [bet.amount * bet.promisedRate for bet in winningBets])
            portion = payout / totalPayout
            otherPower = payout / balance
            power = (totalPayout-payout) / \
                (balance * (len(self.options)-1))
            self.coefficients[index] = (
                1/len(self.options)) - power + otherPower

            print(f"Total payout for {option} is {payout}")
            print(f"{portion*100}% of total payout chose this option")
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
        self.updateCoefficients()
        return self.bets


if __name__ == "__main__":
    a = BetConstructor()
    a.printPayouts()
    a.placeBet("David", "1", 200)
    a.printPayouts()
    a.placeBet("David", "1", 200)
    a.printPayouts()
    a.placeBet("David", "1", 200)
    a.printPayouts()
    a.placeBet("David", "1", 200)
    a.printPayouts()
    a.placeBet("David", "1", 200)
    a.printPayouts()
    a.placeBet("Daniel", "2", 140)
    a.printPayouts()
    a.placeBet("Daniel", "2", 140)
    a.printPayouts()
    a.placeBet("Daniel", "2", 140)
    a.printPayouts()
    a.placeBet("Daniel", "2", 140)
    a.printPayouts()
    a.placeBet("Daniel", "2", 140)
    a.printPayouts()
    a.placeBet("Daniel", "2", 140)
    a.printPayouts()
    a.placeBet("Daniel", "2", 140)
