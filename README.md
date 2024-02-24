# Linkedin_scraper ⛏️🌐
Local Python app capable of scraping a LinkedIn profile and storing it to train an ML model

## Brief description and parts of the project
The project's main objective is to develop an automated tool to analyze LinkedIn profiles and determine whether they match a certain position. The project consists of the following main files:

* app.py: This is the main app. Once executed, the program will open LinkedIn's main page to log in with one's account. From the app's UI, the user will be able to scrape any LinkedIn profile given the profile's link.

* scraper.py: This is where the scraper is coded and where the main logic is developed.

* lang.txt: This file determines in which language the LinkedIn app will be. Write EN for English and ES for Español. Default language is Español.

* jobs.txt: In this file the positions to match are stored. The user can edit this file freely without crashing the program (restart is required) and may label his own jobs. It is mandatory that the user follows the same style of the file (one job per line).

* dataset.csv/backup_dataset.csv: In these files the scraped profiles and their labels will be stored. Each time the program is restarted, backup_dataset.csv will copy dataset.csv's data.

## How to use? 🤔
The program is pretty straightforward to use so I will not go into great depth about any tool:

1. Open the app.py file

2. Log in to your LinkedIn account once the main page is opened

3. Copy and paste the link of the LinkedIn profile that you wish to scrape

4. Select the position to which the person is going to be labeled

5. Select 'Match' or 'No match' depending on the profile's correspondence with the selected position

6. Press 'Scrape and save!' to scrape the profile and save it (only experience and aptitudes will be scraped)

7. The scraped information will be displayed on the app and saved to the dataset file


## Disclaimer and use ⚠️
This tool is not meant to make any profit out of it (as the license states) and is not intended to copy or damage LinkedIn in any way. It is just a more human-friendly way of constructing a dataset for the incoming LLM era. It is suggested to use the tool under regulation and not spam the 'Scrape and save!' button frequently to avoid being banned from the platform.
Thank you!!!
