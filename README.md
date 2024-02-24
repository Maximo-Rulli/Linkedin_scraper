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
1. 
