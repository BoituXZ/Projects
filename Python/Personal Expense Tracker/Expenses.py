import sqlite3
import datetime
# creating a connection

def create():
    conn = sqlite3.connect("Expenses.db")

    curs = conn.cursor()
    curs.execute("""CREATE TABLE IF NOT EXISTS Expenses
             (id INTEGER PRIMARY KEY,
             Date DATE,
             Description TEXT,
             Category TEXT,
             Amount REAL)""")
    
    # committing the changes
    conn.commit()
    conn.close()

create()

conn = sqlite3.connect("Expenses.db")
curs = conn.cursor()

temp = True







while temp == True:
    print("Hey, Welcome to the expense Tracker, keeping your finances in order!")
    decision = int(input("What would you like to do today? \n1.View Expenses \n2.Add an Expense \n3.Remove an expense \nOption: "))
    if decision == 1:
        view_choice =  int(input("Select an option:\n1.View all Expenses\n2.View Monthly Expenses by category\nOption: "))
        
        if view_choice == 1:
            curs.execute("SELECT * FROM Expenses")
            expenses = curs.fetchall()
            for expense in expenses:
                print(expense)  
        elif view_choice == 2:
            month = input("Enter the month (MM)")
            year = input("Enter the year (YYYY)")
            curs.execute("""SELECT Category, SUM(Amount) FROM Expenses WHERE 
                        strftime('%m', Date) = ? 
                        and strftime('%Y', Date) = ? GROUP BY Category""", (month, year))
            expenses = curs.fetchall()
            for expense in expenses:
                print(f"Category: {expense[0]}, Total: {expense[1]}")
        
        else:
            exit("Invalid Option")  
        
        repeat = input("would you like to do something else (Y/N)? \n")
        if repeat.lower() != "y":
            break
        
        
        
    elif decision == 2:
        date = input("Enter date in the format (DD-MM-YYYY): ")
        # changing the date to DD-MM-YYYY cause that's what I'm used to
        # Parse user input into a datetime object
        user_date = datetime.datetime.strptime(date, '%d-%m-%Y')
        # formatting the date
        formatted_date = user_date.strftime('%d-%m-%Y')
        
        description = input("Enter the Description of the Expense: ")
        amount = input("Enter the cost of the expense:")
        
        
        # This ensures that even if we have 100 items with the same category we won't return that category 100 times.
        curs.execute("SELECT DISTINCT Category FROM Expenses")
        categories = curs.fetchall()
        print("Please select a category by number: ")
        
        
        # so enumerate loops over the index and value incase you was lost
        for index, category in enumerate(categories):
            print(f" {index + 1}.{category}")
        print(f" {len(categories)+1}. Create a new category")
        
        
        # Taking the choice from the user
        chosen_category = int(input())
        if chosen_category == len(categories) + 1:
            category = input("Enter the category name: ")
        else:
            category = categories[chosen_category-1][0]

        # Pushing all our values into the good ol database 
        
        curs.execute("""INSERT INTO Expenses (Date, Description, Category, Amount) VALUES (?,?,?,?)""",
                (formatted_date, description, category, amount))
        conn.commit()
    elif decision == 3:
        # Printing out the available categories from the ones in the database.
        curs.execute("SELECT id,Description,Category, Amount FROM Expenses")
        expenses = curs.fetchall()
        for expense in expenses:
            print(f"{expense}")
        choice = int(input("Enter the number of the category you wish to delete: "))
        chosen_expense = choice
        # deleting said category from database
        curs.execute("DELETE FROM Expenses WHERE id=?", (chosen_expense,))
        conn.commit()
            
    else:
        print(f"You entered an invalid option, there is no option {decision}. Please try again")
        exit()
        
conn.close()