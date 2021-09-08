# At the beginning put in terminal: 'pip3 install gspread google-auth'

import gspread
from google.oauth2.service_account import Credentials

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
    Get sales figures imput from the user 
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

get_sales_data()