# At the beginning put in terminal: 'pip3 install gspread google-auth'
# 'pip3 freeze' in terminal shows all packages installed
# 'pip3 freeze --local > requirements.txt' redirects the output to a file called requirements.txt.
# 'pip3 uninstal ...' uninstals package
# 'pip3 install -r requirements.txt' instals all packages listed in the file

import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint # in order to use pprint() instead of just print()

SCOPE = [ # in Python we  write constant variable names in capitals
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')

SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    """
    Get sales figures input from the user.
    Run a while loop to collect a valid string of data from the user
    via the terminal, which must be a string of 6 numbers separated
    by commas. The loop will repeatedly request data, until it is valid.
    (A Python function description goes between triple double quotes like this, and should always be inside the function, 
    right underneath the function name.)
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here: ")
        
        sales_data = data_str.split(",") 
        """
        So, we defined a new variable called sales_data and use the split() method on 
        our data string, to break it up at the commas. This will remove the commas from 
        the string. Let’s print our sales_data out to the terminal to take a look at our 
        new list. And there we can see, each value from our string has been added to the list,  
        the commas here separate the items in the list, they are not the same string commas 
        that we removed with the split method. In order to insert our data into our spreadsheet,
        our values need to be in a list like this.
        """
        if validate_data(sales_data):
            print("Data is valid!")
            break
        
    return sales_data

def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError (
                f"Exactly 6 values required, you provided {len(values)}"
            )

    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True

def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.
    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extra made when stock was sold out.
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1] # access the last row in the stock data
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row): # zip method iterates through two lists at the same time
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    return surplus_data

def update_worksheet(data, worksheet):
    """
    Receives a list of integers to be inserted into a worksheet
    Update the relevant worksheet with the data provided
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully.\n")

def get_last_5_entries_sales():
    """
    Collects columns of data from sales worksheet, collecting
    the last 5 entries for each sandwich and returns the data
    as a list of lists.
    """
    sales = SHEET.worksheet("sales")
    
    columns = []
    for ind in range(1,7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    return columns

def calculate_stock_data(data):
    """
    Calculate the average stock for each item type, adding 10%
    """
    print("Calculating stock data...\n")

    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))

    return new_stock_data

def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, "stock")

main()
