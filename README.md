# LaravelScraper

![image](https://github.com/axylisdead/LaravelScraper/assets/135433130/2784feb0-4c98-496a-9041-7cf81530d6ae)

# Description
LaravelScraper is a small script to scrape Laravel error pages using the Shodan API and extract valuable information
<br>
It is incredibly useful for gaining access to random databases and credentials for different services

Features:
- <b>Uses the Shodan API and allows you to search through pages of results</b>
- <b>Resolves IP addresses to hostnames</b>
- <b>Allows you to save all of your results to a file</b>

# Requirements
Python 3 (duh)
<br>
argparse
<br>
datetime
<br>
os
<br>
requests
<br>
re
<br>
pyfiglet
<br>
urllib3
<br>
sys
<br>
socket
<br>
bs4
<br>
contextlib

<b>You can install all of the dependencies by cloning the repository and running: ```pip install -r requirements.txt```

# Usage
Run normally: ```python laravelscraper.py -k YOUR_SHODAN_API_KEY_HERE```
Add results to sqllite3: -o laravelscraper_index.txt -d  dbname -o output.txt
Send results to telegram: -o laravelscraper_index.txt -t YOUR_BOT_TOKEN YOUR_CHAT_ID -d DB_NAME -o OUTPUT_FILENAME
<br>
Output the results to a file called output.txt: ```python laravelscraper.py -k YOUR_SHODAN_API_KEY_HERE -o output.txt```
<br>
Scroll through pages of Shodan results to page 13: ```python laravelscraper.py -k YOUR_SHODAN_API_KEY_HERE -p 13```

# Arguments
- ```-k``` or ```--api_key``` | This is required. This is where you put your Shodan API key.
- ```-p``` or ```--page``` | Shodan only prints 100 results by default per page, so if you want more results, change this parameter to go to a different page.
- ```-o``` or ```--output``` | Outputs whatever results to stdout AS WELL AS to a file of your choice.
- ```-d``` or ```--database``` | Saves the hits to a local SQLite database
- ```-t``` or ```--telegram``` | Sends the hits to your Telegram bot. Please follow -t with your Telegram Chat ID for your bot.

# To Do
- [x] Add feature to save all results to a local SQLite database or a CSV file
- [x] Add Telegram feature
- [ ] Allow --all argument to download all results from Shodan (i tried implementing this but it gave me a headache)
- [ ] Intergrate with other services (Hunter, CriminalIP, ZoomEye etc)
- [ ] Implement automatic testing of DBs, SMTP logins, AWS keys to test if they work
- [ ] Add -e argument to allow for extra queries to the dork

# Disclaimer
This is to be used for educational purposes only blah blah (insert boilerplate shite here)

# License
This code was proudly written and published under the <a href=https://plusnigger.org>+NIGGER license</a>, a modified version of Daddy Stallmans <a href="https://www.gnu.org/licenses/gpl-3.0.txt">GPL v3 license</a>

# Credits
All work was done by me, Lodzie Kotekya. You can find me on <a href="https://t.me/lodzie">Telegram</a>
Many contributions such as local database saving and the Telegram bot were done by <a href="https://github.com/nelly113113">nelly113113</a>. Many thanks to them.
