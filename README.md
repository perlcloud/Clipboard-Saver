# Clipboard Saver
###### Save the contents of your clipboard every time it changes to a csv for later reference.

## Use
Change the `save-dir` variable to the path to where you want your .csv saved.
A new .csv file will be created for each month to keep the file size manageable.

## Is this a good idea?
No, not really.
Think carefully about the sensitive and private information that you copy all the time...
If you do use this, resist the urge to make the output available on the cloud.

To make this more safe, adjust the `discard_clip()` function to only save specific types of data such as phone numbers, addresses, etc

## Commands
You can send a number of commands to be executed. If the command returns text, it will do so by resetting your clipboard.
- `#sleep30` Use this command to stop the script from working for a specified number of seconds. Useful to stop the
script from saving something during the sleep.
- `#crazy-test text` Transforms the given text after the `-` into annoying meme worthy text. `test text` becomes `tEsT tExT`. Wonderful!
- `#.command-test text` `command` is a string manipulation string 

## Why you might find this useful:
If you know that in the background everything you copy is saved, you can purposely copy things to save them for later. Addresses, phone numbers, jokes, a link to something to look at later, etc.

The 3rd column of the output csv will characterize (if recognized by the `content_info()` function) what the data type is so you can filter it later. This is a good candidate for improvement. If we know exactly what the data copied is, we can make the filtering to exclude sensitive data better, add better filtering, and treat data differently. For example, we could keep a file for just phone numbers etc.

## How to make this even better:
Share your clipboard across all your devices using an app like [Join](https://joaoapps.com/join/)!
With a single computer running the script you can save your clipboard from all your devices.
Besides, copying an address on your computer and than pasting it on your phone is useful, awesome, and the inspiration behind this project.
