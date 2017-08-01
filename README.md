# ParseBook
A program to Parse Facebook Message Data into a useable form incredibly quickly!  
we are excited to announce that the useable form is json.

Slower programs built around libraries such as BeautifulSoup can take whole minutes to run through your entire message history, but `parse.py` is optimized to run in just seconds ~

# Usage
Download your facebook data following these instructions: https://www.facebook.com/help/131112897028467

Then simply run `python parse.py path/to/facebook/html/messages.htm your/output/file.json`

`messages_1.html` is given as an example input,
run `python parse.py messages_1.html out.json` for a sample json output
