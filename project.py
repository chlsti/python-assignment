from dataclasses import dataclass
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# read in an excel sheet (partially filled for visualization but could also be empty)
productivity_df = pd.read_excel("productivity.xlsx")

# create an empty array of activities to be filled during each run of the program
activities = np.array([])

# Define a dataclass for the activities
@dataclass
class Activity:
    name: str # name of the activity
    time: datetime # time of input
    duration: float # time spent doing the activity (in hours)

# Define a function to add activities
def add_activity(activities):
    name = input("Type of acitivity: ")
    duration = float(input("Time spent on acitivity (in hours): "))
    activity = Activity(name, datetime.today().date(), duration)
    activities =  np.append(activities,activity)
    return activities

# Look at the activities already added
def show_activities():
    for activity in activities:
        print(f'Type of activity: {activity.name}')
        print(f'Date: {activity.time}')
        print(f'Time spent doing: {activity.duration}')

def save_to_excel(df):
    data = {'Activity': [activity.name for activity in activities],
            'Date': [activity.time for activity in activities],
            'Hours': [activity.duration for activity in activities]}
    data = pd.DataFrame(data)
    
    # set data type for date to only get the current date without hours and minutes
    data['Date'] = data['Date'].astype(str)
    
    if df.empty:
        # If the input DataFrame is empty, use the new_data directly
        new_df = data
    else:
        # Concatenate the DataFrames
        new_df = pd.concat([df, data], ignore_index=True)

    # Save the updated DataFrame to the Excel file
    new_df.to_excel('productivity.xlsx', index=False)
    print("Successfully appended the activities to 'productivity.xlsx'!")

def visualize_productivity():
    productivity_df = pd.read_excel("productivity.xlsx")

    # Group activities by name and sum the time spent
    total_time = productivity_df.groupby('Activity')['Hours'].sum()

    # Plotting
    plt.figure(figsize=(5, 3))
    total_time.sort_values().plot(kind='bar', color='green')
    plt.title('Total Time Spent on the Activities')
    plt.xlabel('Activities')
    plt.ylabel('Hours')
    plt.show()

finished = False
while not finished:
    print("""
          1. Add an activity
          2. Show all activities added during the current run
          3. Save progress to Excel (only choose if no further inputs in the current run)
          4. Look at the the complete activity log
          5. Visualize my productivity
          6. Finished for now 
          """)
    option = input("What would you like to do: ")

    if option == "1":
        activities = add_activity(activities)
    elif option == "2":
        show_activities()
    elif option == "3":
        productivity_df = save_to_excel(productivity_df)
    elif option == "4":
        productivity_df = pd.read_excel("productivity.xlsx")
        print(productivity_df)
    elif option == "5":
        visualize_productivity()
    elif option == "6":
        finished = True
    else:
        print("Invalid input. Please choose from the presented options.")