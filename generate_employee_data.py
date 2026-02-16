import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize Faker
fake = Faker('ja_JP')  # Use Japanese locale for realism if desired, or standard. Given the user prompt was in Japanese, let's try 'ja_JP'.

def generate_data(num_employees=1000):
    """
    Generates sample data for departments, employees, and salaries.

    Args:
        num_employees (int): The number of employees to generate.

    Returns:
        tuple: A tuple containing three pandas DataFrames (departments, employees, salaries).
    """
    # 1. Departments
    departments_data = [
        {'dept_id': 1, 'dept_name': 'Human Resources', 'base_salary': 4000000},
        {'dept_id': 2, 'dept_name': 'Engineering', 'base_salary': 6000000},
        {'dept_id': 3, 'dept_name': 'Sales', 'base_salary': 5000000},
        {'dept_id': 4, 'dept_name': 'Marketing', 'base_salary': 4500000},
        {'dept_id': 5, 'dept_name': 'Finance', 'base_salary': 5500000},
        {'dept_id': 6, 'dept_name': 'Operations', 'base_salary': 4200000},
        {'dept_id': 7, 'dept_name': 'Legal', 'base_salary': 7000000},
        {'dept_id': 8, 'dept_name': 'Product', 'base_salary': 5800000},
    ]
    df_departments = pd.DataFrame(departments_data)

    # 2. Employees
    employees = []
    salaries = []

    start_date = datetime(2015, 1, 1)
    end_date = datetime(2023, 12, 31)

    for i in range(1, num_employees + 1):
        emp_id = i
        dept = random.choice(departments_data)
        dept_id = dept['dept_id']

        # Employee Data
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = f"{last_name.lower()}.{first_name.lower()}@example.com" # Simple email generation
        hire_date = fake.date_between(start_date=start_date, end_date=end_date)

        employees.append({
            'emp_id': emp_id,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'hire_date': hire_date,
            'dept_id': dept_id
        })

        # Salary Data (Simplified: current annual salary)
        # Random variation around base salary
        base = dept['base_salary']
        variation = random.uniform(0.8, 1.5) # -20% to +50%
        amount = int(base * variation)

        salaries.append({
            'salary_id': i, # Simple 1-to-1 mapping for this example
            'emp_id': emp_id,
            'amount': amount,
            'effective_date': datetime(2024, 1, 1).date()
        })

    df_employees = pd.DataFrame(employees)
    df_salaries = pd.DataFrame(salaries)

    return df_departments, df_employees, df_salaries

def analyze_data(df_departments, df_employees, df_salaries):
    """
    Performs aggregation on the employee data.

    Args:
        df_departments (pd.DataFrame): Departments data.
        df_employees (pd.DataFrame): Employees data.
        df_salaries (pd.DataFrame): Salaries data.

    Returns:
        pd.DataFrame: A summary DataFrame with aggregation results.
    """
    # Merge
    merged = df_employees.merge(df_salaries, on='emp_id').merge(df_departments, on='dept_id')

    # Aggregation
    summary = merged.groupby('dept_name').agg(
        employee_count=('emp_id', 'count'),
        average_salary=('amount', 'mean'),
        total_salary=('amount', 'sum')
    ).reset_index()

    # Format
    summary['average_salary'] = summary['average_salary'].astype(int)

    return summary

def main():
    """
    Main execution function.
    """
    print("Generating data...")
    df_departments, df_employees, df_salaries = generate_data(1000)

    print("Analyzing data...")
    df_summary = analyze_data(df_departments, df_employees, df_salaries)

    output_file = 'employee_data.xlsx'
    print(f"Saving to {output_file}...")

    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        df_departments.to_excel(writer, sheet_name='Departments', index=False)
        df_employees.to_excel(writer, sheet_name='Employees', index=False)
        df_salaries.to_excel(writer, sheet_name='Salaries', index=False)
        df_summary.to_excel(writer, sheet_name='Summary_Aggregation', index=False)

    print("Done!")

if __name__ == "__main__":
    main()
