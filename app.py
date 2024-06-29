from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from dateutil.relativedelta import relativedelta

app = Flask(__name__)

def get_days_in_month(date):
    next_month = date + relativedelta(months=1)
    return (next_month - date).days

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    client = request.form['client']
    channel = request.form['channel']
    product = request.form['product']
    date_str = request.form['date']
    budget = float(request.form['budget'])
    goal_1 = request.form['goal_1']
    goal_2 = request.form['goal_2']

    # Convert goal inputs to floats if they are provided, else set them to None
    goal_1 = float(goal_1) if goal_1 else None
    goal_2 = float(goal_2) if goal_2 else None

    # Convert the date string to a proper date format
    date = pd.to_datetime(date_str, format="%B, %Y")

    # Calculate the number of days in the corresponding month
    days_in_month = get_days_in_month(date)

    # Handle missing budget values by replacing NaN with 0
    budget = budget if budget is not None else 0

    # Calculate daily budget
    daily_budget = budget / days_in_month

    # Calculate daily goal_1 and goal_2
    daily_goal_1 = goal_1 / days_in_month if goal_1 is not None else None
    daily_goal_2 = goal_2 / days_in_month if goal_2 is not None else None

    # Create a new DataFrame to store daily values
    daily_df = pd.DataFrame(columns=['Client', 'Date', 'Channel', 'Product', 'Budget', 'Goal_1', 'Goal_2'])

    # Generate daily entries for the month and append to the daily_df DataFrame
    daily_entries = [
        [client, date.replace(day=day), channel, product, daily_budget, daily_goal_1, daily_goal_2]
        for day in range(1, days_in_month + 1)
    ]
    daily_df = pd.concat([daily_df, pd.DataFrame(daily_entries, columns=daily_df.columns)], ignore_index=True)

    # Save the resulting DataFrame to a new CSV file
    daily_df.to_csv('daily_data.csv', index=False)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
