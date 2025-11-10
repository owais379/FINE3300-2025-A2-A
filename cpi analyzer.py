import pandas as pd
import os

def part_b_analysis():  
    # Question 1: combine the 11 data frames into one data frame
    print("Loading and combining CPI data")
    
    all_data = []
    cpi_files = [f for f in os.listdir('A2_Data') if f.endswith('.csv') and 'CPI' in f]
    
    for file in cpi_files:
        province = file.split('.')[0]  # get province from filename (ON, BC, etc.)
        file_path = os.path.join('A2_Data', file)
        df = pd.read_csv(file_path)
        
        # reshape the data from wide to long format
        melted_df = df.melt(id_vars=['Item'], var_name='Month', value_name='CPI')
        melted_df['Jurisdiction'] = province
        
        all_data.append(melted_df)
    
    # combine all data frames into one
    combined_df = pd.concat(all_data, ignore_index=True)
    
    print("First 12 lines of combined data:")
    print(combined_df.head(12))
    print()
    
    # Question 2 & 3: month-to-month changes and highest average changes
    print("Average monthly changes by province and category:")
    
    categories = ['Food', 'Shelter', 'All-items excluding food and energy']
    category_data = combined_df[combined_df['Item'].isin(categories)]
    
    # sort by province, category, and month to calculate changes 
    category_data = category_data.sort_values(['Jurisdiction', 'Item', 'Month'])
    
    # calculate monthly percentage changes
    category_data['Monthly_Change'] = category_data.groupby(['Jurisdiction', 'Item'])['CPI'].pct_change() * 100
    
    # get average changes by province and category
    avg_changes = category_data.groupby(['Jurisdiction', 'Item'])['Monthly_Change'].mean().reset_index()
    avg_changes['Monthly_Change'] = avg_changes['Monthly_Change'].round(1)
    
    # find highest for each category
    for category in categories:
        category_avg = avg_changes[avg_changes['Item'] == category]
        if not category_avg.empty:
            highest = category_avg.loc[category_avg['Monthly_Change'].idxmax()]
            print(f"   {category}: {highest['Jurisdiction']} ({highest['Monthly_Change']}%)")
    print()
    
    #Question 4: equivalent salary calculation
    print("Equivalent salaries to $100,000 in Ontario:")
    
    # get december cpi values
    dec_cpi = combined_df[
        (combined_df['Item'] == 'All-items') & 
        (combined_df['Month'] == '24-Dec')
    ]
    
    # get ontario cpi
    ontario_cpi = dec_cpi[dec_cpi['Jurisdiction'] == 'ON']['CPI'].values[0]
    
    # calculate equivalent salaries
    for _, row in dec_cpi.iterrows():
        province = row['Jurisdiction']
        province_cpi = row['CPI']
        equivalent = (province_cpi / ontario_cpi) * 100000
        print(f"   {province}: ${equivalent:,.2f}")
    print()
    
    # Question 5: minimum wage analysis
    print("Minimum wage analysis:")
    
    # load minimum wages
    wages_path = os.path.join('A2_Data', 'MinimumWages.csv')
    wages = pd.read_csv(wages_path)
    
    # nominal analysis
    highest_nominal = wages.loc[wages['Minimum Wage'].idxmax()]
    lowest_nominal = wages.loc[wages['Minimum Wage'].idxmin()]
    
    print(f"   Highest nominal: {highest_nominal['Province']} (${highest_nominal['Minimum Wage']})")
    print(f"   Lowest nominal: {lowest_nominal['Province']} (${lowest_nominal['Minimum Wage']})")
    
    # real wage analysis (simplified)
    wage_with_cpi = pd.merge(wages, dec_cpi[['Jurisdiction', 'CPI']], 
                            left_on='Province', right_on='Jurisdiction')
    wage_with_cpi['Real_Wage'] = (wage_with_cpi['Minimum Wage'] / wage_with_cpi['CPI']) * 100
    highest_real = wage_with_cpi.loc[wage_with_cpi['Real_Wage'].idxmax()]
    
    print(f"   Highest real: {highest_real['Province']} (${highest_real['Real_Wage']:.2f})")
    print()
    
    # Question 6 & 7: services inflation analysis
    print("Annual change in Services CPI:")
    
    # get services data for January and December
    services_data = combined_df[
        (combined_df['Item'] == 'Services') & 
        (combined_df['Month'].isin(['24-Jan', '24-Dec']))
    ]
    
    # calculate annual changes
    jan_data = services_data[services_data['Month'] == '24-Jan'][['Jurisdiction', 'CPI']]
    dec_data = services_data[services_data['Month'] == '24-Dec'][['Jurisdiction', 'CPI']]
    
    merged = pd.merge(jan_data, dec_data, on='Jurisdiction', suffixes=('_Jan', '_Dec'))
    merged['Annual_Change'] = ((merged['CPI_Dec'] - merged['CPI_Jan']) / merged['CPI_Jan']) * 100
    merged['Annual_Change'] = merged['Annual_Change'].round(1)
    
    for _, row in merged.iterrows():
        print(f"   {row['Jurisdiction']}: {row['Annual_Change']}%")
    
    # Question 8: find highest services inflation
    highest_services = merged.loc[merged['Annual_Change'].idxmax()]
    print(f"   Highest services inflation: {highest_services['Jurisdiction']} ({highest_services['Annual_Change']}%)")

if __name__ == "__main__":
    part_b_analysis()