"""
Provides CRUD operations for authenticated gspread clients

This authentication is required to use gspread library, which authenticates the app
and allows access to your Google Drive and Sheets through a service account O.auth2.
Details can be found here:

https://docs.gspread.org/en/latest/oauth2.html#enable-api-access

GoogleSheetService wraps the gspread library and includes a repeated Thread to constantly
update the sheet, so data can be queued without the requirement of an API call.

"""

import gspread

"""
Authorize Gspread
Authorization requires service account credentials absolute path
"""
credentials_path = 'C:/Users/cnuen/PycharmProjects/NBot/credentials.json'
manager = gspread.service_account(filename=credentials_path)

worksheet = manager.open("N-Fam 2023").get_worksheet(0)

"""
Provides easy access sheet data from the NuenthelFamily Budget sheet
Current sheet data coupling limitations with assumed data:
    Expense Budgets: A,B,C * 80:87
    Expense Cumulative: A-G * 93:198
    Cody Income: C59
    Sam Income: C60
    Other Income: C61
    Total Budget: C64
    Total Used: C89
"""

expense_categories = ['Dining', 'Grocery', 'Transportation', 'Recreation', 'Personal', 'JL', 'Other']
income_categories = ['Sam', 'Cody', 'Other']

column_dict = {
    1: "A",
    2: "B",
    3: "C",
    4: "D",
    5: "E",
    6: "F",
    7: "G"
}


def get_expense_percent(category: str) -> int:
    """ Return percent cell value of a given expense category
    :param category Category of expense
    """
    if category not in expense_categories:
        raise ValueError(f"Invalid category passed to function: {category} not found. Valid arguments: "
                         f"Cody, Sam, Other")
    match category:
        case "Dining":
            return worksheet.acell("B81").value
        case "Grocery":
            return worksheet.acell("B82").value
        case "Transportation":
            return worksheet.acell("B83").value
        case "Recreation":
            return worksheet.acell("B84").value
        case "Personal":
            return worksheet.acell("B85").value
        case "JL":
            return worksheet.acell("B86").value
        case "Other":
            return worksheet.acell("B87").value


def get_expense_total(category: str) -> int:
    """ Return cell value of a given expense category
    :param category Category of expense
    """
    if category not in expense_categories:
        raise ValueError(f"Invalid category passed to function: {category} not found. Valid arguments: "
                         f"Cody, Sam, Other")
    match category:
        case "Dining":
            return worksheet.acell("C81").value
        case "Grocery":
            return worksheet.acell("C82").value
        case "Transportation":
            return worksheet.acell("C83").value
        case "Recreation":
            return worksheet.acell("C84").value
        case "Personal":
            return worksheet.acell("C85").value
        case "JL":
            return worksheet.acell("C86").value
        case "Other":
            return worksheet.acell("C87").value


def get_income_total(category: str) -> str:
    """ Returns income cell value for Cody, Sam or Other
    :param category Category of income, Cody, Sam or Other
    """
    if category not in income_categories:
        raise ValueError(f"Invalid category passed to function: {category} not found. Valid arguments: "
                         f"Cody, Sam, Other")
    match category:
        case "Cody":
            return worksheet.acell("C59").value
        case "Sam":
            return worksheet.acell("C60").value
        case "Other":
            return worksheet.acell("C61").value


def get_budget_expense_used_total() -> str:
    """ Returns value of total monthly budget used """
    return str(worksheet.acell("C89").value)


def get_budget_amount_total() -> str:
    """ Returns value of total monthly bugdet funding """
    return worksheet.acell("C64").value


def get_cell_dollar_data(alphanum_cell_coord: str) -> str:
    """ Gets cell data from a dollar formatted cell, returns $0.00 if empty cell
    :param alphanum_cell_coord Dollar formatted cell alphanumeric coordinate
    """
    cell_value = worksheet.acell(alphanum_cell_coord).value
    if not cell_value:
        cell_value = "$0.00"
    return cell_value


def get_cell_value(alphanum_cell_cord: str):
    return worksheet.acell(alphanum_cell_cord).value


def add_expense(category: str, expense: float, note: str = None) -> int:
    """
    Adds expense to desired expense column on sheet, will return 1 on successful update
    :param category Name of expense column
    :param expense Value of expense to be inserted
    :param note: A note to add to the spreadsheet cell, defaults to nothing
    """
    expense_columns = {category: i+1 for i, category in enumerate(expense_categories)}
    column_values = worksheet.col_values(expense_columns[category])
    row = 1 + len(column_values)
    alphanum_coord = column_dict[expense_columns[category]] + str(row)

    if note:
        worksheet.update_note(alphanum_coord, note)

    return worksheet.update_cell(row, expense_columns[category], expense)['updatedCells']


def get_all_expense_data():
    """
    Returns a dictionary of all expense data for percentage used, amount used and total allowance
    for each expense category
    """
    expense_list = []
    for i, item in enumerate(expense_categories):
        row_data = worksheet.row_values(80+i) # ["Expense Category", "Percent", "Used"]
        row_data.append(worksheet.acell(f"C{67+i}").value) # Add expense allowance to list
        expense_list.append(row_data)
    return expense_list


def update_income(category: str, amount: float):
    """
    Changes income cell for given category
    :return:
    """
    if category not in income_categories:
        raise ValueError(f"Invalid category passed to function: {category} not found. Valid arguments: "
                         f"Cody, Sam, Other")
    match category:
        case "Cody":
            return worksheet.update("C59", amount)['updatedCells']
        case "Sam":
            return worksheet.update("C60", amount)['updatedCells']
        case "Other":
            return worksheet.update("C61", amount)['updatedCells']


def update_note(alphanumeric_coord: str, text: str):
    """
    Adds given text as a note to a Google spreadsheet cell
    :param alphanumeric_coord: Alphanumeric coord, such as "A1" to describe a cell
    :param text: Value to include as the note
    :return:
    """
    return worksheet.update_note(alphanumeric_coord, text)


def reformat_dollar_string(dollar_string: str) -> float:
    """
    Refactor a dollar formatted sheet cell and returns value as float
    :param dollar_string Dollar formatted sheet string, i.e. '$5,322.60'
    """
    list_value = [char for char in dollar_string if char not in [",", "$"]]
    return float("".join(list_value))


def cumulate_dollar_format_cell(additional_value: float or int, alphanum_cell_coord: str) -> dict:
    """
    Updates cell, increments data to current value if true
    :param additional_value Data to increment or update in income cell
    :param alphanum_cell_coord alpha numeric coordinate of sheet cell
    """
    current_value = get_cell_dollar_data(alphanum_cell_coord)
    additional_value = float(additional_value) + reformat_dollar_string(current_value)
    return worksheet.update(alphanum_cell_coord, additional_value)['updatedCells']