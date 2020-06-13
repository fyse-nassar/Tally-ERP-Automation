import os
import time
from datetime import timedelta

import pandas as pd
import pyautogui

from python_imagesearch.imagesearch import imagesearch

# Typing Speed Parameters
type_speed = 0.3
enter_speed = 0.2
max_character = 5

# Setting all the paths
script_folder = os.path.dirname(os.path.realpath(__file__))

processed_file = os.path.join(
    script_folder, "Output", "Processed Items.csv")
print(processed_file)
negative_image_file = os.path.join(script_folder, "Database", "negative.PNG")

log_file = os.path.join(script_folder, "Output", "log.txt")


def checkfiles():
    '''
    Checks if all the requied report files are present
    '''

    if not os.path.exists(processed_file):
        pyautogui.alert(
            "Step 1 not executed properly OR Processed Item file not present")
        exit(0)

    if not os.path.exists(negative_image_file):
        pyautogui.alert("Negative file image not present")
        exit(0)


def delete_unknown_item():
    '''
    Deletes entered characters
    '''
    pyautogui.press('left', presses=max_character)
    pyautogui.press('delete', presses=max_character)
    # TODO: Output Negative Stock Items to CSV


def check_negative():
    '''
    Checks if entered quantity leads to negative stock
    '''
    pos = imagesearch(
        negative_image_file)  # Finds the position of the negative i
    if pos[0] != -1:  # Successfully detects negative stock pop up
        print("error")
        # pyautogui.press('backspace', presses=2, interval=enter_speed)
        # pyautogui.press('space', presses=1, interval=enter_speed)
        # pyautogui.press('down', presses=1, interval=enter_speed)
        # pyautogui.press('enter', presses=1, interval=enter_speed)
        # pyautogui.press('backspace', presses=1, interval=enter_speed)
        # pyautogui.press('enter', presses=3, interval=enter_speed)
        pyautogui.press('space')
        pyautogui.press('enter')
        pyautogui.press('backspace',presses=3,interval = enter_speed)
        time.sleep(0.5)
        pyautogui.press('space')
        

        return False
    else:
        return True


def check_test_negative():
    '''
    Test check for negative stock
    '''
    pos = imagesearch(negative_image_file)
    if pos[0] != -1:
        print("error")
        pyautogui.press('space', presses=1, interval=enter_speed)
        time.sleep(2)
        pyautogui.press('space')
        pyautogui.press('enter')
        pyautogui.press('backspace',presses=3,interval = enter_speed)
        pyautogui.press('space')
        # pyautogui.typewrite('1', interval=type_speed)
        # pyautogui.press('enter', presses=9, interval=enter_speed)
        return False
    else:
        return True

# def check_item(item_code):
#     '''
#     Checks if item exists in the database
#     '''

#     if pyautogui.locateOnScreen(PATH+"Database\\error.png" ):
#         print("Error Found")
#         print("Item Error: ",item_code)
#         delete_unknown_item()
#         return False

#     else:
#         print("Item Found",item_code)
#         return True

def enter_quantity(item_quantity):
    pyautogui.press('enter', presses=2)
    pyautogui.typewrite(item_quantity, interval=type_speed)
    pyautogui.press('enter')
    time.sleep(0.3)
    if(check_negative()):
        pyautogui.press('enter', presses=8, interval=enter_speed)


def test_item():
    '''
    Testing Negative Check for Single Item
    '''
    pyautogui.typewrite("44", interval=type_speed)
    pyautogui.press('enter', presses=2)
    pyautogui.typewrite("5000", interval=type_speed)
    pyautogui.press('enter')
    time.sleep(2)
    if(check_test_negative()):
        pyautogui.alert(
            "Tally is not in full screen mode. \n Program will exit now.")
        exit(0)


def run():
    '''
    Runs the Main Code
    '''
    pyautogui.alert("Switch To Tally and wait 10 secs")
    time.sleep(10)

    test_item()

    for i in range(len(item_code_list)):
        # time.sleep(1)
        item_code = str(item_code_list[i])
        print(i, item_code_list[i],file=log)
        pyautogui.typewrite(item_code, interval=type_speed)
        # if check_item(item_code):
        enter_quantity(str(item_quantity_list[i]))


checkfiles()

data = pd.read_csv(processed_file)
log = open(log_file,'w')

item_code_list = data["Item Code"].tolist()
item_quantity_list = data["Quantity"].tolist()


start = time.time()
run()
end = time.time()

total_time = str(timedelta(seconds=end-start))

pyautogui.alert("All Items Entered\n Time Taken = {}".format(
    total_time.split(".")[0]))
