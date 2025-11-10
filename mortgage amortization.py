import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class MortgagePayments:
    # class created to calculate various mortgage payment options for canadian fixed-rate mortgages
    
    # fixed rate mortgages in Canada are quoted as semiannually compounded rates
    def __init__(self, interest_rate, amortization_period, term_years):
        self.quoted_interest = interest_rate / 100 #convert to a decimal
        self.amortizations_years = amortization_period
        self.term_years = term_years  # NEW: mortgage term

    def pva(self, r, n):
        # PVA Formula
        if r == 0:
            return n
        else:
            return (1 - (1 + r) ** -n) / r
        
    def calculate_periodic_rate(self, compounding_frequency, payment_frequency):
        # find the appropriate periodic interest rate for mortgage payments

        # convert semiannually compounded rate to effective annual rate
        effective_annual_rate = (1 + self.quoted_interest / compounding_frequency) ** compounding_frequency - 1

        periodic_rate = (1 + effective_annual_rate) ** (1 / payment_frequency) - 1

        total_periods = self.amortizations_years * payment_frequency
        
        return periodic_rate, total_periods
    
    def payments(self, principal):
        # all payment options from the instructions
        # returns Tuple

        # monthly payments (compounded semiannually, paid monthly)
        monthly_rate, monthly_periods = self.calculate_periodic_rate(2, 12)
        monthly_payment = principal / self.pva(monthly_rate, monthly_periods)
        
        # semi-monthly payments 24 payments per year
        semi_monthly_rate, semi_monthly_periods = self.calculate_periodic_rate(2, 24)
        semi_monthly_payment = principal / self.pva(semi_monthly_rate, semi_monthly_periods)
        
        # bi-weekly payments 26 payments per year
        bi_weekly_rate, bi_weekly_periods = self.calculate_periodic_rate(2, 26)
        bi_weekly_payment = principal / self.pva(bi_weekly_rate, bi_weekly_periods)
        
        # weekly payments 52 payments per year
        weekly_rate, weekly_periods = self.calculate_periodic_rate(2, 52)
        weekly_payment = principal / self.pva(weekly_rate, weekly_periods)
        
        # bi-weekly half of monthly payment
        rapid_bi_weekly_payment = monthly_payment / 2
        
        # weekly quarter of monthly payment
        rapid_weekly_payment = monthly_payment / 4
        
        # Round all payments to nearest penny
        payments_tuple = (
            round(monthly_payment, 2),
            round(semi_monthly_payment, 2),
            round(bi_weekly_payment, 2),
            round(weekly_payment, 2),
            round(rapid_bi_weekly_payment, 2),
            round(rapid_weekly_payment, 2)
        )
        
        return payments_tuple

    # new parts added for assignment #2
    def generate_amortization_schedule(self, principal, payment_frequency, payment_amount, schedule_name):
        """
        generate amortization schedule for a specific payment option

            principal (float): Initial loan amount
            payment_frequency (int): Number of payments per year
            payment_amount (float): Periodic payment amount
            schedule_name (str): Name of the payment schedule
            
        returns: pd.DataFrame: Amortization schedule
        """
        # calculate periodic interest rate
        periodic_rate, total_periods = self.calculate_periodic_rate(2, payment_frequency)
        
        # only generate schedule for the term period, not full amortization
        term_periods = self.term_years * payment_frequency
        
        schedule = []
        balance = principal
        
        for period in range(1, term_periods + 1):
            interest_payment = balance * periodic_rate
            principal_payment = payment_amount - interest_payment
            ending_balance = balance - principal_payment
            
            # ending balance doesn't go negative
            if ending_balance < 0:
                principal_payment = balance
                payment_amount = principal_payment + interest_payment
                ending_balance = 0
            
            schedule.append({
                'Period': period,
                'Starting Balance': round(balance, 2),
                'Interest Amount': round(interest_payment, 2),
                'Payment': round(payment_amount, 2),
                'Ending Balance': round(ending_balance, 2)
            })
            
            balance = ending_balance
            if balance <= 0:
                break
        
        df = pd.DataFrame(schedule)
        return df

    def generate_all_schedules(self, principal):
        """
        Generate amortization schedules for all 6 payment options
        
            principal (float): mortgage principal amount
            
        returns: dcionary of dataframes for each payment option
        """
        payment_amounts = self.payments(principal)
        frequencies = [12, 24, 26, 52, 26, 52]  # Corresponding frequencies
        schedule_names = [
            'Monthly', 'Semi-Monthly', 'Bi-Weekly', 
            'Weekly', 'Rapid Bi-Weekly', 'Rapid Weekly'
        ]
        
        schedules = {}
        
        for i, (payment, freq, name) in enumerate(zip(payment_amounts, frequencies, schedule_names)):
            schedules[name] = self.generate_amortization_schedule(
                principal, freq, payment, name
            )
        
        return schedules

    def save_schedules_to_excel(self, schedules, filename='mortgage_schedules.xlsx'):
        """
        save all amortization schedules to an Excel file with multiple worksheets
            schedules (dict): dictionary of DataFrames
            filename (str): output Excel filename
        """
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            for schedule_name, df in schedules.items():
                df.to_excel(writer, sheet_name=schedule_name, index=False)
        print(f"All schedules saved to {filename}")

    def plot_loan_balance_decline(self, schedules, filename='loan_balance_decline.png'):
        """
        Create a graph showing loan balance decline for all payment options
            schedules (dict): Dictionary of DataFrames
            filename (str): Output PNG filename
        """
        plt.figure(figsize=(12, 8))
        
        for schedule_name, df in schedules.items():
            # convert periods to years for x-axis
            periods = df['Period']
            if schedule_name == 'Monthly':
                years = periods / 12
            elif schedule_name == 'Semi-Monthly':
                years = periods / 24
            elif schedule_name == 'Bi-Weekly' or schedule_name == 'Rapid Bi-Weekly':
                years = periods / 26
            else:  # weekly and rapid Weekly
                years = periods / 52
                
            plt.plot(years, df['Ending Balance'], label=schedule_name, linewidth=2)
        
        plt.xlabel('Years')
        plt.ylabel('Loan Balance ($)')
        plt.title('Loan Balance Decline Over Time - All Payment Options')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"Graph saved as {filename}")
        plt.show()


# main execution for Part A
def run_part_a():
    print("FINE 3300: Assignment #2 - Part A: Loan Amortization Schedules")
    print("-" * 60)
    
    # get user input
    print("\nEnter mortgage details:")
    principal = float(input("Enter the principal amount: $"))
    interest_rate = float(input("Enter the quoted interest rate (e.g., 4.85): "))
    amortization_years = int(input("Enter the amortization period in years: "))
    term_years = int(input("Enter the mortgage term in years: "))
    
    # create mortgage object
    mortgage = MortgagePayments(interest_rate, amortization_years, term_years)
    
    # calculate payment amounts
    payment_amounts = mortgage.payments(principal)
    
    # display payment amounts
    print(f"\nPayment Amounts:")
    payment_names = ['Monthly', 'Semi-Monthly', 'Bi-Weekly', 'Weekly', 'Rapid Bi-Weekly', 'Rapid Weekly']
    for name, amount in zip(payment_names, payment_amounts):
        print(f"{name}: ${amount:,.2f}")
    
    # generate all amortization schedules
    print("\nGenerating amortization schedules...")
    schedules = mortgage.generate_all_schedules(principal)
    
    # save to Excel
    mortgage.save_schedules_to_excel(schedules, 'mortgage_amortization_schedules.xlsx')
    
    # create and save graph
    print("Creating loan balance decline graph...")
    mortgage.plot_loan_balance_decli5000ne(schedules, 'loan_balance_decline.png')
    
    print("\nPart A completed successfully!")


if __name__ == "__main__":
    run_part_a()