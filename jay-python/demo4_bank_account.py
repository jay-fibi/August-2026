# Jay - Demo 4: Object Oriented Programming (Bank Account)

class InsufficientFundsError(Exception):
    """Raised when a withdrawal is larger than the available balance."""


class BankAccount:
    """A simple bank account with deposit, withdraw and history support."""

    def __init__(self, owner, balance=0.0):
        self.owner = owner
        self.balance = float(balance)
        self.history = []
        if self.balance:
            self.history.append(("open", self.balance))

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        self.history.append(("deposit", amount))
        return self.balance

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise InsufficientFundsError(
                f"Balance {self.balance:.2f} is less than requested {amount:.2f}."
            )
        self.balance -= amount
        self.history.append(("withdraw", amount))
        return self.balance

    def statement(self):
        lines = [f"Statement for {self.owner}"]
        for action, amount in self.history:
            lines.append(f"  {action:<10} {amount:>10.2f}")
        lines.append(f"  {'balance':<10} {self.balance:>10.2f}")
        return "\n".join(lines)

    def __str__(self):
        return f"{self.owner}: {self.balance:.2f}"


class SavingsAccount(BankAccount):
    """A bank account that can add yearly interest."""

    def __init__(self, owner, balance=0.0, interest_rate=0.05):
        super().__init__(owner, balance)
        self.interest_rate = interest_rate

    def add_interest(self):
        interest = self.balance * self.interest_rate
        self.balance += interest
        self.history.append(("interest", interest))
        return interest

    def __str__(self):
        return f"{self.owner} (savings @ {self.interest_rate:.0%}): {self.balance:.2f}"


def main():
    print("=" * 40)
    print("  Jay - Demo 4: Bank Accounts (OOP)")
    print("=" * 40)

    checking = BankAccount("Jay", 500)
    checking.deposit(250)
    checking.withdraw(120)
    print(checking.statement())

    try:
        checking.withdraw(10_000)
    except InsufficientFundsError as error:
        print(f"\nExpected error: {error}")

    savings = SavingsAccount("Jay", 1000, interest_rate=0.07)
    earned = savings.add_interest()
    print(f"\nInterest earned: {earned:.2f}")
    print(savings.statement())

    print("\nAll accounts:")
    for account in (checking, savings):
        print(f"  {account}")


if __name__ == "__main__":
    main()
