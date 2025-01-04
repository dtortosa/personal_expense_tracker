#!/usr/bin/env python3.10
# coding: utf-8
    #to run this script: chmod +x script.py; ./script.py
    #if you are using "$" to paste the path of the executable, you do not need to use "./" for running the executable.
    #you can save the output and the errors
        #./script.py > script.out #only output
        #./script.py 2> error.out #only error
        #./script.py > script.out 2> error.out #both in different files
        #./script.py > script.out 2>&1 #both in the same file


##function to input expenses
import random
from datetime import datetime, timedelta
import numpy as np

#define the function
def input_expenses(demo=False, n_entries=None):
    '''
    Function to input the expenses. \n 
    Expenses can be added manually or they can be created as a synthetic dataset (demo=True) \n
    Returns a list of dicts being each one an expense.
    '''

    #set the random seed for reproducibility when creating demo data
    random.seed(34)

    #if interactive is true, request to introcute the inputs manually
    if(demo==False):
        exp_date = input("Enter the date of the expense in the format YYYY-MM-DD: ")
        exp_category = input("Enter the category of the expense: ")
        exp_amount = float(input("Enter the amount of the expense: "))
        exp_description = input("Enter the description of the expense: ")

        #create a list with a dictionary including the inputs
        list_expenses = [{ \
            "date": exp_date, \
            "category": exp_category, \
            "amount_usd": exp_amount, \
            "description": exp_description \
        }]
    #create a dummy list of inputs from scratch
    elif(demo==True):
        #number of data entries
        n_entries=n_entries

        #create random dates within 2024
        #first the days within the range 
        start_date = datetime(2020, 1, 1)
        end_date = datetime(2024, 12, 31)
        delta = end_date - start_date
        #create 500 random dates from the start and convert to the required format
        example_dates = [ \
            (start_date + timedelta(days=random.randint(0, delta.days))).strftime("%Y-%m-%d") for _ in range(n_entries) \
        ]

        #create random expenses categories including missing data
        example_categories = [ \
            random.choice(["Groceries", "Clothing", "Entertaiment"]) for _ in range(n_entries) \
        ]

        #create random amounts based on the categories
        example_amounts = []
        for i in example_categories:
            if(i=="Groceries"):
                example_amounts.append(random.randint(5,200))
            elif(i=="Clothing"):
                example_amounts.append(random.randint(5,100))
            elif(i=="Entertaiment"):
                example_amounts.append(random.randint(5,20))

        #create random descriptions based on the categories
        example_descriptions = []
        for i in example_categories:
            if(i=="Groceries"):
                example_descriptions.append( \
                    "Doing groceries in " + random.choice(["Aldi", "Lidl", "Tesco", "Dunnes"]) \
                )
            elif(i=="Clothing"):
                example_descriptions.append( \
                    "Buying clothes in " + random.choice(["Penneys", "H&M", "Zara", "Dunnes"]) \
                )
            elif(i=="Entertaiment"):
                example_descriptions.append( \
                    "Going to the cinema to watch " + random.choice( \
                        ["The Avengers", "Star Wars", "The Lord of the Rings"] \
                    ) \
                )

        #create a list of dictionaries with the inputs
        list_expenses = [ \
            { \
                "date": date, \
                "category": category, \
                "amount_usd": amount_usd, \
                "description": description \
            } for date, category, amount_usd, description in zip(example_dates, example_categories, example_amounts, example_descriptions) \
        ]
    
    #return only the dict
    return list_expenses


##function to see expenses
import pandas as pd

#list_expenses=input_expenses(demo=True)
def visual_exp(list_expenses):
    '''
    Function to visualize the expenses. \n
    This function expects as input a list of dicts being each dict a expense. \n
    It returns a pandas DF without missing data. One row per expense.
    '''

    #convert the list to a pandas DF
    pd_expenses = pd.DataFrame(list_expenses)

    #remove missing 
    pd_expenses_no_nan = pd_expenses.dropna()

    #convert date column to datatime format for filtering in future steps
    pd_expenses_no_nan["date"] = pd.to_datetime( \
        pd_expenses_no_nan["date"], \
        format="%Y-%m-%d" \
    )

    #sort by date and return
    pd_expenses_no_nan_sorted = pd_expenses_no_nan.sort_values(by="date")
    return pd_expenses_no_nan_sorted


##function to track the budget
#pd_expenses=visual_exp(list_expenses = input_expenses(demo=True))
#monthly_budget=1000
#month=4; year=2024
def budget_tracking(pd_expenses, month, year, monthly_budget):
    '''
    Function to calculate the expenditure in a given month and compare it with the monthly budget. \n
    It takes as input a pandas DF with the expenditure (one row per expense), the month, year and budget. \n
    The function will check whether the user is under or above the monthly limit.
    '''

    #ensure "deate" is in datetime format
    pd_expenses["date"] = pd.to_datetime( \
        pd_expenses["date"], \
        format= "%Y-%m-%d" \
    )

    #calculate the current expenditure
    current_expending = pd_expenses.loc[ \
        (pd_expenses["date"].dt.month == month) & (pd_expenses["date"].dt.year == year), \
        "amount_usd" \
    ].sum()
        #select those expenses of the selected month and year
        #extract the amount in USD and sum all of them

    #calculate the difference between budget and current expenditure
    remaining_budget = monthly_budget - current_expending


    #check the user is above or below
    if(remaining_budget < 0):
        status = f"WARNING: You have already exceeded you budget in {remaining_budget} USD"
    else:
        status = f"Remaining budget for {year}-{month}: {remaining_budget} USD"
    
    #return the results
    return status


##function to save the expenses
import os

#pd_expenses=visual_exp(list_expenses = input_expenses(demo=True))
#user_name="dsalazar"
def save_expenses(pd_expenses, user_name):
    '''
    Function to save expenses taking as arguments a pandas DF with the expenses and the user name. \n
    It saves the expenses as a CSV file
    '''

    #create a folder to save the results
    os.makedirs("../expenses/", exist_ok=True)
        #not raise error if the folder exists

    #save the expenses as a CSV file
    pd_expenses.to_csv(\
        "../expenses/expenses_" + user_name + ".csv", \
        sep=",", \
        index=False \
    )


#function to load the expenses
#user_name="dsalazar"
def load_expenses(user_name):
    '''
    Function to load previously generated expenses data for a given user.
    '''

    #add the file path
    file_path = "../expenses/expenses_" + user_name + ".csv"

    #if the file exists
    if(os.path.exists(file_path)):
        
        #load it and return it
        loaded_expenses = pd.read_csv(\
            file_path, \
            sep=",", \
            header=0 \
        )
        return loaded_expenses
    else:
        return None


#function to display a menu for the user
def main_function():
    '''
    Function to run the main program. \n
    It displays a menu to the user to select the desired action. \n
    '''

    #ask for hte user name
    user_name = input("Type your user name: ")

    #print user name
    print("STARTING SESSION OF " + user_name, flush=True)

    #ask for the menu choice
    menu_choice = input("Select one of the following: Add expense (1); Add demo data (2); View expenses (3); Track budget (4); Save expenses (5); Exit (6): ")

    #load previously generated expenses datafile
    current_expenses = load_expenses(user_name=user_name)
        #this will return None if the file does not exists, instead of a pandas DF

    #run loop until the user selects the exit option
    while menu_choice != "6":

        #add data
        if(menu_choice=="1") | (menu_choice=="2"):

            #manually
            if(menu_choice=="1"):

                #if the user has a previous datafile
                if (type(current_expenses)==pd.core.frame.DataFrame):

                    #add the new expenses to the existing data
                    current_expenses = pd.concat( \
                        [current_expenses, pd.DataFrame(input_expenses(demo=False))], \
                        ignore_index=True \
                    )
                        #use "input_expenses" to add a new entry manually (i.e., demo=False)
                        #concatenate and ignore the index to avoid duplicated indexes
                else: #the user does not have a previous datafile
                    
                    #just create a pandas DF with the new entry
                    current_expenses = pd.DataFrame(input_expenses(demo=False))
            
                #print message
                print("\nENTRY ADDED", flush=True)
                print(current_expenses, flush=True)
                    #the flush=True parameter is added to the print statements to ensure that the output is displayed immediately 

            #create demo data
            elif(menu_choice=="2"):

                #ask the number of entries to be created
                n_entries = int(input("Enter the number of entries to be created: "))

                #if the user has a previous datafile
                if(type(current_expenses)==pd.core.frame.DataFrame):
                    
                    #add the new demo data to the existing data
                    current_expenses = pd.concat( \
                        [current_expenses, pd.DataFrame(input_expenses( \
                            demo=True, \
                            n_entries=n_entries))], \
                        ignore_index=True \
                    )
                else: #the user does not have a previous datafile
                    
                    #just create a pandas DF with the new entry
                    current_expenses = pd.DataFrame(input_expenses(demo=True, n_entries=n_entries))

                #print message
                print("\nDEMO DATA ADDED: " + str(n_entries) + " ENTRIES", flush=True)

            #remove nan
            current_expenses.dropna(inplace=True)

            #convert the date column to datetime format
            current_expenses["date"] = pd.to_datetime( \
                current_expenses["date"], \
                format= "%Y-%m-%d" \
            )
            
            #sort by the date column
            current_expenses = current_expenses.sort_values(by="date")
        
        #visualize the data
        elif(menu_choice=="3"):
            
            #print message
            print("\nVISUALIZE THE EXPENSES", flush=True)

            #print only if the user has a previous datafile
            if (type(current_expenses)==pd.core.frame.DataFrame):
                print(current_expenses, flush=True)
            else:
                print("ERROR: THERE IS NO EXPENSES DATA", flush=True) 
        
        #track budget
        elif(menu_choice=="4"):

            #print message
            print("\nTRACKING BUDGET", flush=True)

            #do budget check if the user has a previous datafile
            if (type(current_expenses)==pd.core.frame.DataFrame):

                #ask for the year, month and budget
                selected_year = int(input("Type the year (as numeric): "))
                selected_month = int(input("Type the month (as numeric): "))
                selected_budget = float(input("Type the monthly budget: "))
                    #only the amount in USD can be float

                #print message
                print(f"YEAR:{selected_year}; MONTH:{selected_month}; BUDGET:{selected_budget}", flush=True)

                #run the function to check the budget
                check_budget = budget_tracking( \
                    pd_expenses=current_expenses, \
                    year=selected_year, \
                    month=selected_month, \
                    monthly_budget=selected_budget \
                )

                #print the output
                print(check_budget, flush=True)
            else:
                print("ERROR: THERE IS NO EXPENSES DATA", flush=True) 
        
        #save expenses
        elif(menu_choice=="5"):
            
            #print message
            print("\nSAVE EXPENSES", flush=True)

            #save if the user has a previous datafile
            if (type(current_expenses)==pd.core.frame.DataFrame):
                
                #run the function to save the expenses
                save_expenses( \
                    pd_expenses=current_expenses, \
                    user_name=user_name \
                )
            else:
                print("ERROR: THERE IS NO EXPENSES DATA", flush=True) 

        #ask for the menu choice again
        menu_choice = input("Select one of the following: Add expense (1); Add demo data (2); View expenses (3); Track budget (4); Save expenses (5); Exit (6): ")
    
    #exit the program when (6) has been selected
    print("\nENDING SESSION OF " + user_name, flush=True)


if __name__ == "__main__":
    main_function()

