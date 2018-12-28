# Save the contents of the clipboard when it changes

import os
import re
import csv
import time
import pyperclip

from datetime import datetime
from sys import getsizeof


def csv_start():
    if not os.path.isfile(save_path):
        with open(save_path, 'w', newline='') as log:
            file_writer = csv.writer(log, delimiter=',',
                                     quotechar='"', quoting=csv.QUOTE_ALL)
            file_writer.writerow(['Timestamp', 'Clipboard', 'Type'])


def csv_write(insert):
    with open(save_path, 'a', newline='') as log:
        file_writer = csv.writer(log, delimiter=',',
                                 quotechar='"', quoting=csv.QUOTE_ALL)
        file_writer.writerow(insert)


def discard_clip(clip):
    blank = ''
    social_security = re.compile('^\d{3}-\d{2}-\d{4}|\d{3}\d{2}\d{4}$')

    if clip.strip() == blank:
        # No need to save blank text
        return True
    elif social_security.match(clip):
        # We dont want to save privet information
        return True
    # TODO: Add bank account and credit card number recognition
    else:
        return False


def content_info(clip):
    # Checks the content against guidelines to make sure we want to save it
    email = re.compile('^[a-zA-Z0-9.-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]+$')
    url = re.compile('(https?:\/\/(?:www\.|(?!www))'
                     '[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]'
                     '\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]'
                     '+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))'
                     '[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9]\.[^\s]{2,})')
    tel = re.compile('^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$')

    if email.match(clip):
        return 'email'
    elif url.match(clip):
        return 'url'
    elif tel.match(clip):
        return 'phone'
    else:
        return ''


# Output file
save_dir = 'C:\\Users\\Avrohom\\Google Drive\\Clipboard-Saver\\'
save_filename = (str(datetime.now().year) + '-' +
                 str(datetime.now().month) + '_' +
                 'Clipboard-Save.csv')
save_path = os.path.join(save_dir, save_filename)
csv_start()

# Current value
recent_value = pyperclip.paste()

while True:
    tmp_value = pyperclip.paste()
    try:
        if tmp_value != recent_value:
            if discard_clip(tmp_value) == False:
                save = [datetime.now(),
                        tmp_value,
                        content_info(tmp_value)]
                csv_write(save)
            print('Clip Saved: Length = ' + str(len(tmp_value)))
            recent_value = tmp_value
    except:
        continue
        print('Something Failed')
    time.sleep(0.1)
