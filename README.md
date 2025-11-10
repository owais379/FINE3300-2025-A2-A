# FINE 3300 - Assignment #2

## Part A: Mortgage Amortization Calculator

This Python project extends the mortgage payment calculator I previously constructed to generate comprehensive loan amortization schedules. The program calculates six different payment options (monthly, semi-monthly, bi-weekly, weekly, rapid bi-weekly, and rapid weekly) and creates detailed amortization schedules for each.

### Features:
- Calculates periodic payments using Canadian fixed-rate mortgage conventions
- Generates amortization schedules with starting balance, interest, payment, and ending balance
- Exports all schedules to an Excel file with multiple worksheets
- Creates a matplotlib graph comparing loan balance decline across all payment options

## Libraries used
Pandas, Matplotlib, Numpy, and Openpyxl

## Part B: Consumer Price Index (CPI) Analysis

This component analyzes CPI data across Canadian provinces to examine inflation trends and cost-of-living differences. The program processes 11 CPI data files and minimum wage data to provide economic insights.

### Features
- Combines CPI data from all provinces into a unified dataset
- Calculates monthly inflation rates for key categories (Food, Shelter, All-items excluding food and energy)
- Computes equivalent salaries across provinces based on cost-of-living differences
- Analyzes nominal vs real minimum wages
- Identifies regions with highest services inflation

### Libraries used
Pandas and OS
