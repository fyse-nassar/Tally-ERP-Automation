import os
import re
from pathlib import Path
import pandas as pd
import pyautogui


# Setting all the paths
script_folder = os.path.dirname(os.path.realpath(__file__))
alias_file = os.path.join(script_folder, "Database", "Alias List.csv")
exclude_items_file = os.path.join(
    script_folder, "Database", "Exclude Items.csv")
report_file = os.path.join(script_folder, "ITE000.CSV")


# Output Lists for Correct Item
valid_item_code = []
valid_item_name = []
valid_item_quantity = []

# Output Lists for Incorrect Item
error_item_code = []
error_item_name = []
error_item_quantity = []




def checkfiles():
    '''
    Checks if all the requied report files are present
    '''

    if not os.path.exists(alias_file):
        pyautogui.alert("Alias List file not present")
        exit(0)

    if not os.path.exists(exclude_items_file):
        pyautogui.alert("Exclude List file not present")
        exit(0)

    if not os.path.exists(report_file):
        pyautogui.alert("Report file image not present")
        exit(0)


def extract_item_code(item_name):
    '''
    Extracts the alias number from the item_code name
    '''
    item_name = item_name[:4]
    if '-' in item_name:
        item_code = item_name.split('-')[0]

    elif ' ' in item_name:
        item_code = item_name.split(' ')[0]
    else:
        item_code = ''.join((re.findall("\\d+", item_name)))

    return item_code


def add_item(item_code, item_name, item_quantity, list_name):
    '''
    Adds item to corresponding lists
    '''
    if list_name == "Valid":
        valid_item_code.append(item_code)
        valid_item_name.append(item_name)
        valid_item_quantity.append(int(item_quantity))

    elif list_name == "Invalid":
        error_item_code.append(item_code)
        error_item_name.append(item_name)
        error_item_quantity.append(int(item_quantity))

    else:
        error_item_code.append("No Item Number")
        error_item_name.append(item_name)
        error_item_quantity.append(int(item_quantity))


def process_report():
    '''
    Takes the reports file and processes over it
    '''

    # Loading Alias list file
    temp = pd.read_csv(alias_file)
    alias_list = temp["Num"].tolist()
    # print(type(alias_list[2]))

    # Reading Exclude items List
    exclude = pd.read_csv(exclude_items_file)
    exclude_item_code = exclude["Item Code"].tolist()

    # Reading Report File
    f = open(report_file, 'rb')
    for i in range(4):  # Skipping the first few lines containing date and other info
        next(f)

    report = pd.read_csv(f)
    item_name_list = report["ITEM NAME"].tolist()
    item_name_list = item_name_list[:-1]  # removing the total column

    item_quantity_list = report["HSN"].tolist()
    item_quantity_list = item_quantity_list[:-1]  # removing the total column


    # Initializing the count stats
    total_count = len(item_name_list)
    error_count = 0
    success_count = 0
    bakery_count = 0

    for i, item_name in enumerate(item_name_list):
        item_code = extract_item_code(item_name)
        # print(item_code)
        try:
            if int(item_code) not in exclude_item_code and int(item_code) in alias_list:
                # Check if item quantity is positive
                if int(item_quantity_list[i]) > 0:
                    add_item(item_code, item_name, item_quantity_list[i], "Valid")
                    success_count += 1
                else:
                    add_item(item_code, item_name,
                             item_quantity_list[i], "Invalid")
                    error_count += 1

            elif int(item_code) not in alias_list and int(item_code) not in exclude_item_code:
                add_item(item_code, item_name,
                         item_quantity_list[i], "Invalid")
                error_count += 1

            elif int(item_code) in exclude_item_code:
                bakery_count += 1

        except:
            add_item(item_code, item_name, item_quantity_list[i], "Exception")
            error_count += 1
    return total_count, success_count, error_count, bakery_count

def write_report():

    # Writing Processed File
    temp = {'Item Code': valid_item_code,
            'Item Name': valid_item_name, 'Quantity': valid_item_quantity}
    df = pd.DataFrame(temp)
    df.index += 1
    processed_file = os.path.join(
        script_folder, "Output", "Processed Items.csv")
    try:
        df.to_csv(processed_file)
    except:
        pyautogui.alert("Ouput Folder doesn't exist")

    # Writing Error File
    temp = {'Item Code': error_item_code,
            'Item Name': error_item_name, 'Quantity': error_item_quantity}
    df = pd.DataFrame(temp)
    df.index += 1
    error_file = os.path.join(script_folder, "Output", "Error Items.csv")
    try:
        df.to_csv(error_file)
    except:
        pyautogui.alert("Ouput Folder doesn't exist")


checkfiles()
total_count, success_count, error_count, bakery_count = process_report()
write_report()
pyautogui.alert("""Extraction Successful!\n
                Total Items   : {}\n
                Valid Items   : {}\n
                Invalid Items : {}\n
                Bakery Items : {}""".format(total_count, success_count, error_count, bakery_count))
