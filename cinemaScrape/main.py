import requests
from bs4 import BeautifulSoup
import schedule
import time
import tkinter as tk
from tkinter import messagebox


continue_cycle = True


def check_cinema_website(day_of_the_month_to_look: str):
    """
    Check the cinema website for a specific date.

    :param day_of_the_month_to_look: The day of the month to look for.
    :type day_of_the_month_to_look: str
    :return: None
    :rtype: None
    """
    url = 'https://www.cinegrand.bg/m/dun-cast-vtora-imdbtt15239678'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        dates = soup.find_all('h3', class_='day fs')

        for date in dates:
            date_text = date.text.strip()
            if day_of_the_month_to_look in date_text:
                show_popup_notification('New date found!',
                                        'The cinegrand has change their program. go ahead and '
                                        'make a reservation for Dune Ⅱ')
                global continue_cycle
                continue_cycle = False

    else:
        show_popup_notification('something went wrong with the response', 'Please check your connection')
        return


def show_popup_notification(title, message):
    """
    Shows a popup notification with a given title and message.

    :param title: The title of the popup notification.
    :param message: The message content of the popup notification.
    :return: None

    Example usage:

    >>> show_popup_notification("Notification", "This is a notification message.")
    """
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showinfo(title, message)


# Schedule the job to run every 30 minutes
schedule.every(30).minutes.do(check_cinema_website, '15')  # Change this to the date you are interested in

# run the script until the date is found
while continue_cycle:
    schedule.run_pending()
    time.sleep(1)
