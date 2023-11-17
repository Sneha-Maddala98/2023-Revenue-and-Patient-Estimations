import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# File paths for the data
appointments_file_path = 'C:\\Laptop data\\Documents\\Masters\\Intern_Project\\p21_bi_intern_test_appointments (1).csv'
revenues_file_path = 'C:\\Laptop data\\Documents\\Masters\\Intern_Project\\p21_bi_intern_test_revenues.csv'

# Load appointment and revenue data from CSV files
appointments_data = pd.read_csv(appointments_file_path)
revenues_data = pd.read_csv(revenues_file_path)

# Drop records with missing values to ensure data quality
revenues_data.dropna(inplace=True)
appointments_data.dropna(inplace=True)

# Merge the two datasets on 'appointment_id'
merged_data = pd.merge(appointments_data, revenues_data, on='appointment_id', how='left')

# Convert appointment dates to datetime objects for easy manipulation
merged_data['appointment_date'] = pd.to_datetime(merged_data['appointment_date'])

# Filter the data to include records up to the year 2022
data_until_2022 = merged_data[merged_data['appointment_date'].dt.year <= 2022]

# Group data by month and calculate total revenue and unique patient counts for each month in 2022
monthly_revenue_2022 = data_until_2022.groupby(data_until_2022['appointment_date'].dt.to_period('M'))['revenues'].sum()
monthly_new_patients_2022 = data_until_2022.groupby(data_until_2022['appointment_date'].dt.to_period('M'))['patient_id'].nunique()

# Print monthly revenue and unique patient counts for each month in 2022
print("\nMonthly Revenue and Unique Patients in 2022:")
for month in monthly_revenue_2022.index:
    print(f"Month: {month}, Revenue: ${monthly_revenue_2022[month]:,.2f}, Unique Patients: {monthly_new_patients_2022[month]}")

# Define the opening months of new clinics in 2023
new_clinics = [(3, 3), (4, 7)]  # Format: (clinic number, opening month)

# Initialize lists to store monthly revenue and patient projections for 2023
monthly_projections_2023 = []
monthly_patient_projections_2023 = []

# Calculate the average monthly growth rates for revenue and patient counts
revenue_growth_rate = monthly_revenue_2022.pct_change().mean()
patient_growth_rate = monthly_new_patients_2022.pct_change().mean()

# Store the last month's revenue and patient count from 2022
last_month_revenue = monthly_revenue_2022.iloc[-1]
last_month_patients = monthly_new_patients_2022.iloc[-1]

# Loop through each month of 2023 to forecast revenue and patient counts
for month in range(1, 13):
    # Apply growth rates to forecast the next month
    last_month_revenue *= (1 + revenue_growth_rate)
    last_month_patients *= (1 + patient_growth_rate)

    # Adjust forecasts for new clinics opening
    monthly_revenue = last_month_revenue * (1 + sum([1 for clinic, open_month in new_clinics if month >= open_month]))
    monthly_patients = last_month_patients * (1 + sum([1 for clinic, open_month in new_clinics if month >= open_month]))

    # Add the forecasts to the lists
    monthly_projections_2023.append(monthly_revenue)
    monthly_patient_projections_2023.append(monthly_patients)

# Print monthly revenue and unique patient projections for each month in 2023
print("\nMonthly Revenue and Patient Projections for 2023:")
for month in range(1, 13):
    print(f"Month: {month}, Projected Revenue: ${monthly_projections_2023[month-1]:,.2f}, Projected Unique Patients: {int(monthly_patient_projections_2023[month-1])}")

# Calculate the total projected revenue and unique patient count for 2023
total_revenue_2023 = sum(monthly_projections_2023)
total_unique_patients_2023 = sum(monthly_patient_projections_2023)

# Output the total projected figures for 2023
print(f"\nTotal Projected Revenue for 2023: ${total_revenue_2023:,.2f}")
print(f"Total Projected Unique Patients for 2023: {int(total_unique_patients_2023)}")

# Setting a style for the plots
sns.set_style("whitegrid")

# Visualization section
plt.figure(figsize=(18, 10))

# Months for the x-axis
months = range(1, 13)

# Convert projection lists to pandas Series for cumulative calculations
monthly_projections_2023_series = pd.Series(monthly_projections_2023)
monthly_patient_projections_2023_series = pd.Series(monthly_patient_projections_2023)

# Plot line charts with area fill for cumulative revenue
plt.subplot(2, 1, 1)  # Adjusted for better layout
plt.fill_between(months, monthly_revenue_2022.cumsum(), color="#abd9e9", alpha=0.6)  # Adjusted color
plt.plot(months, monthly_revenue_2022.cumsum(), marker='o', label='2022 Actual', color="#74add1", alpha=0.8, linewidth=2)
plt.fill_between(months, monthly_projections_2023_series.cumsum(), color="#fee08b", alpha=0.5)  # Adjusted color
plt.plot(months, monthly_projections_2023_series.cumsum(), marker='o', label='2023 Projected', color="#fdae61", alpha=0.8, linewidth=2)
plt.title('Cumulative Revenue: 2022 vs 2023', fontsize=16, fontweight='bold')
plt.xlabel('Month', fontsize=14)
plt.ylabel('Cumulative Revenue', fontsize=14)
plt.legend(loc='upper left', fontsize=12)

# Plot line charts with area fill for cumulative patients
plt.subplot(2, 1, 2)  # Adjusted for better layout
plt.fill_between(months, monthly_new_patients_2022.cumsum(), color="#e6f598", alpha=0.6)  # Adjusted color
plt.plot(months, monthly_new_patients_2022.cumsum(), marker='o', label='2022 Actual', color="#66bd63", alpha=0.8, linewidth=2)
plt.fill_between(months, monthly_patient_projections_2023_series.cumsum(), color="#f7f7f7", alpha=0.5)  # Adjusted color
plt.plot(months, monthly_patient_projections_2023_series.cumsum(), marker='o', label='2023 Projected', color="#999999", alpha=0.8, linewidth=2)
plt.title('Cumulative Unique Patients: 2022 vs 2023', fontsize=16, fontweight='bold')
plt.xlabel('Month', fontsize=14)
plt.ylabel('Cumulative Unique Patients', fontsize=14)
plt.legend(loc='upper left', fontsize=12)

plt.tight_layout()
plt.show()