import sqlite3
from datetime import datetime, timedelta
import math

class Budget:
    def __init__(self, name, total_amount, end_date):
        self.name = name
        self.total_amount = total_amount
        self.remaining_amount = total_amount
        self.end_date = end_date
        self.transations = []
        self.start_date = datetime.today().date()
        self.num_of_days = (self.end_date - self.start_date).days

        print(self.remaining_amount)

    def spend(self, amount):
        amount = float(amount)
        if amount > self.remaining_amount:
            return("Not enough funds in the budget.")
        self.remaining_amount -= amount
        self.add_transaction(-amount)

    def refund(self, amount, description=""):
        amount = float(amount)
        self.remaining_amount += amount
        self.add_transaction(amount)

    def get_spend_rate(self): # this is hard coded for 7 days rn
        todays_day = datetime.today()
        days_passed = (todays_day.date() - self.start_date).days  # Calculate days passed

        # Check if it's past lunch or dinner time
        if todays_day.hour >= 14:
            days_passed += 0.5
        elif todays_day.hour >= 20:
            days_passed += 1

        daily_rate = self.total_amount  / self.num_of_days

        if days_passed == 0:
            return f"Check again in a couple hours, your daily rate is around ${math.floor(daily_rate)}"
        else:
            # Calculate spending rate per day based on days passed
            spending_rate = (self.total_amount - self.remaining_amount) / days_passed

        spending_ratio = spending_rate / daily_rate
        spending_at_rate_over_budget = (spending_rate * self.num_of_days) - self.total_amount


        if spending_ratio >= 1.2:
            return f"Your way over budget! At this rate you be ${int(spending_at_rate_over_budget)} over budget!"
        elif 1 <= spending_ratio < 1.2:
            return f"Your roughly on budget but the rate is a little high"
        else:
            return f"Your under budget so far. Keep it up!"



    def add_transaction(self, amount):
        self.transations.append(amount)



    def get_transactions(self):
        return self.transations

    @staticmethod
    def print_variable_names_and_values(**kwargs):
        for name, value in kwargs.items():
            print(f"{name}: {value}")


#test_budget = Budget('food', 150, (datetime.now() + timedelta(days=7)).date())

#test_budget.spend(20)
#print(test_budget.get_spend_rate())
