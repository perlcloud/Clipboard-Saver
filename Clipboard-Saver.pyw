"""Save the contents of the clipboard when it changes"""

import os
import re
import csv
import time
import pyperclip

from datetime import datetime


def csv_start(path):
    """Creates a .csv file if one does not exist"""
    if not os.path.isfile(path):
        with open(path, 'w', newline='') as log:
            file_writer = csv.writer(log, delimiter=',',
                                     quotechar='"', quoting=csv.QUOTE_ALL)
            file_writer.writerow(['Timestamp',
                                  'Clipboard',
                                  'Type',
                                  'Length',
                                  'Lines'])


def csv_write(insert):
    """Writes a list of strings to the .csv file"""
    with open(save_path, 'a', newline='') as log:
        file_writer = csv.writer(log, delimiter=',',
                                 quotechar='"', quoting=csv.QUOTE_ALL)
        file_writer.writerow(insert)


def discard_clip(clip):
    """
    Discards a clip if it matches the format
    of something we don't want to save
    """
    blank = ''
    social_security = re.compile(r'^\d{3}-\d{2}-\d{4}|\d{3}\d{2}\d{4}$')

    if clip.strip() == blank:
        # No need to save blank text
        print('Clip rejected: No text')
        return True
    elif social_security.match(clip):
        # We don't want to save privet information
        print('Clip rejected: Social Security')
        return True
    elif len(clip) > 40000:
        # Too much text
        print('Clip rejected: Too long')
        return True
    elif clip.count('\n') > 4000:
        # Too many lines
        print('Clip rejected: Too many lines')
        return True
    else:
        return False


def content_info(clip):
    """Checks the clip for a known value type, returns known value name"""
    email = re.compile(r'^[a-zA-Z0-9.-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]+$')
    url = re.compile(r'(https?:\/\/(?:www\.|(?!www))'
                     r'[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]'
                     r'\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]'
                     r'+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))'
                     r'[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9]\.[^\s]{2,})')
    tel = re.compile(r'^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$')
    command = re.compile(r'^#((del|sleep)[0-9]+|kill)$')
    sql = re.compile(r'^\[.+\]\.\[.+\]\.\[.+\]$')

    if email.match(clip):
        return 'email'
    elif url.match(clip):
        return 'url'
    elif tel.match(clip):
        return 'phone'
    elif sql.match(clip):
        return 'sql'
    elif command.match(clip):
        return 'CMD'
    else:
        return ''


def cmd(clip):
    """Accepts and executes a specially formatted command"""
    sleep = re.compile(r'^#sleep([0-9]+)$')

    if sleep.match(clip):
        # Ignore any copied text for the specified number of seconds
        num = re.search(r'^#sleep([0-9]+)$', clip).group(1)
        print('Sleeping:', num)
        time.sleep(int(num))
        return pyperclip.copy(clip + ': Done')


# Output file
save_dir = r'M:\Dropbox\Sandbox\Clipboard-Saver\output'
save_filename = (str(datetime.now().year) + '-' +
                 str(datetime.now().month) + '_' +
                 'Clipboard-Save.csv')
save_path = os.path.join(save_dir, save_filename)

# Current clipboard value
recent_value = pyperclip.paste()

while True:
    # Create the .csv file if it does not exist
    csv_start(save_path)

    # New clipboard value
    tmp_value = pyperclip.paste()

    try:
        if tmp_value != recent_value:
            recent_value = cmd(tmp_value)
            if not discard_clip(tmp_value):
                save_value = [datetime.now(),
                              tmp_value,
                              content_info(tmp_value),
                              len(tmp_value),
                              tmp_value.count('\n') + 1]
                csv_write(save_value)
                print('Clip Saved: Length = ' + str(len(tmp_value)))
            recent_value = tmp_value
    except Exception as e:
        print(str(e))
        recent_value = tmp_value
    time.sleep(0.1)
