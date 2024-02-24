from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import re
import time
import random

#Linkedin's main page
LINKEDIN_MAIN = 'https://www.linkedin.com/'

#Token constant (will be used to train the model and defines a blank space)
NULL = '[NONE]'

#Useful constants (for easy changes of language)
with open('lang.txt', 'r') as l:
    LAN = l.read().replace(' ', '')

if LAN == 'EN':
    LINKEDIN_BANNER = 'helpedmegetthisjob'
    SKILLS = 'Skills: '
if LAN == 'ES':
    LINKEDIN_BANNER = 'meayudóaconseguiresteempleo'
    SKILLS = 'Aptitudes: '

class Scraper():
    def __init__(self)->None:
        #The web driver is instantiated
        self.options = Options()
        self.options.add_experimental_option('detach', True)

        self.driver =  webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)

        #Access Linkedin's main page
        self.driver.get(LINKEDIN_MAIN)
        self.driver.maximize_window()

    def scrape_job(self, url:str)->str|list:
        #Retrieve the HTML of past jobs
        self.driver.get(url+'details/experience/')

        #Pause script to avoid being detected
        wait = random.randint(8, 15)
        time.sleep(wait)

        body = self.driver.find_elements(By.TAG_NAME, "body")[0]
        jobs_content = body.get_attribute('innerHTML')

        #Parse HTML content with BeautifulSoup
        jobs_soup = BeautifulSoup(jobs_content, 'html.parser')

        #This is the div class of a job in Linkedin
        jobs_class = "pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column"
        
        jobs = jobs_soup.find_all('li', class_ = jobs_class)

        #This lists will be returned to the main app to save in a csv. They contain the profiles full data
        Companies = []
        Roles = []
        Times = []
        Types = []
        Descriptions = []
        Skills = []

        for job in jobs:
            print("-"*50)
            ####Select general div####
            #Go into deep nested structures
            embeded_class = "display-flex flex-column full-width align-self-center"
            general = job.find('div', class_=embeded_class)

            ####Find the roles####
            #Some profiles have different roles in the same company, and that will be considered here
            roles_class = "pvs-list__paged-list-item pvs-list__item--one-column"
            try:
                roles = general.find_all('li', class_=roles_class)

                #List used to store previous roles in a certain company
                comp_roles = []
                for role in roles:
                    comp_roles.append(role.find('span', attrs={'aria-hidden': 'true'}).text.strip())

            except AttributeError:
                return 'error'
                 
            #Definition of classes that will be used later
            comp_role_class = "display-flex flex-row justify-space-between"
            time_class = "pvs-entity__caption-wrapper"
            job_skill_class = "pvs-list__outer-container pvs-entity__sub-components"
            desc_class = "display-flex align-items-center t-14 t-normal t-black"
            skill_class = "display-flex align-items-center t-14 t-normal t-black"

            if len(comp_roles): #The candidate has worked in multiple roles inside the company
                ####Find the company####
                company_div = general.find('div', class_ = comp_role_class)
                company = company_div.find('span', attrs={'aria-hidden': 'true'}).text.strip()

                ##Iterate over roles##
                times = []
                types = []
                descriptions = []
                skills = []
                type_class = "t-14 t-normal"
                for role in roles:
                    ####Find time####
                    times.append(role.find('span', class_=time_class).text.strip())

                    ####Find the type of role####
                    type_span = role.find('span', class_=type_class)
                    #The person may have not specified his job type
                    try:
                        types.append(type_span.find('span', attrs={'aria-hidden': 'true'}).text.strip())

                    except:
                        types.append(NULL)

                    ####Find job description and skills related####
                    job_description, job_skills = self.find_jobs_skills(role, job_skill_class, desc_class, skill_class)

                    descriptions.append(job_description)
                    skills.append(job_skills)


                print(f"Company's name is: {company}")
                print(f"Roles developed: {comp_roles}")
                print(f"Time in each role: {times}")
                print(f"Type of each role: {types}")
                print(f"Description of each role: {descriptions}")
                print(f"Skills related to each role: {skills}")

                Companies += [company]*len(comp_roles)
                Roles += comp_roles
                Times += times
                Types += types
                Descriptions += descriptions
                Skills += skills

            else: #The candidate has not developed different roles in the same company
                ####Find the role####
                role_div = general.find('div', class_ = comp_role_class)
                role = role_div.find('span', attrs={'aria-hidden': 'true'}).text.strip()

                ####Find the company####
                company_class = "t-14 t-normal"
                company_div = role_div.find('span', class_ = company_class)
                company_info = company_div.find('span', attrs={'aria-hidden': 'true'}).text
                company = company_info.split("·")[0].strip()

                ####Find job type####
                job_type = company_info.split("·")[1].strip() if len(company_info.split("·")) != 1 else NULL

                ####Find time in the role####
                job_time = role_div.find('span', class_=time_class).text.strip()

                ####Find job description and skills related####
                job_description, job_skills = self.find_jobs_skills(general, job_skill_class, desc_class, skill_class)

                print(f"Company's name is: {company}")
                print(f"Role developed: {role}")
                print(f"Time in the role: {job_time}")
                print(f"Job type: {job_type}")
                print(f"Role's description: {job_description}")
                print(f"Role's skills: {job_skills}")

                Companies.append(company)
                Roles.append(role)
                Times.append(job_time)
                Types.append(job_type)
                Descriptions.append(job_description)
                Skills.append(job_skills)

        print("-"*20+"Experience fully scraped!"+"-"*20)

        return [Companies, Roles, Times, Types, Descriptions, Skills]


    def scrape_skills(self, url:str)->str|list:
        #Retrieve the HTML of listed skills
        self.driver.get(url+'details/skills/')

        #Pause script to avoid being detected
        wait = random.uniform(3.0, 5.0)
        time.sleep(wait)

        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight/2)")
        time.sleep(random.uniform(1.4, 1.6))

        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight*9/10)")
        time.sleep(random.uniform(1, 1.6))

        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight*9/10)")

        body = self.driver.find_elements(By.TAG_NAME, "body")[0]
        skills_content = body.get_attribute('innerHTML')

        #Parse HTML content with BeautifulSoup
        skills_soup = BeautifulSoup(skills_content, 'html.parser')

        skills_class = "pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column"

        skills_div = skills_soup.find('div', class_ = re.compile(r'\bartdeco-tabs artdeco-tabs--size-t-48 ember-view\b'))

        try:
            skills_list = skills_div.find('ul', class_ = re.compile(r'\bpvs-list\b'))
        
        except AttributeError:
            return 'void'
        
        skills = skills_list.find_all('li', class_ = skills_class)

        person_skills = []

        for i in skills:
            person_skills.append(i.find('span', attrs={'aria-hidden':'true'}).text.strip())

        print(f"Skills: {person_skills}")

        print("-"*20+"Skills fully scraped!"+"-"*20)

        return person_skills

    #This function checks whether the given div corresponds to a description or skill (useful in the scrape function)
    def is_desc(self, div):
        try:
            return not(div.find('strong').text == "Skills:")
        except AttributeError:
            return True
        
    #Helper function to find the skills and jobs of a profile (works both on single role and multi role profiles)
    def find_jobs_skills(self, general_div, job_skill_class, desc_class, skill_class):
        job_skills = []
        job_apt_div = general_div.find('div', class_=job_skill_class)

        #Detect the Linkedin's banner of 'Helped me get this job'
        try:
            linkedin_div = job_apt_div.find('div', class_= desc_class)
            text = linkedin_div.find('span', attrs={'aria-hidden': 'true'}).text.replace(' ', '').split()
            if text[0] == LINKEDIN_BANNER:
                banner = True
            else:
                banner =  False
        except AttributeError:
            banner =  False

        #People may not specify any job description nor skills related to the job
        try:
            description_div = job_apt_div.find('div', class_= desc_class)
            if self.is_desc(description_div):
                if banner:
                    description_div = job_apt_div.find_all('div', class_= desc_class)[1]
                    job_description = description_div.find('span', attrs={'aria-hidden': 'true'}).text.strip()
                else:
                    job_description = description_div.find('span', attrs={'aria-hidden': 'true'}).text.strip()
            else:
                job_description = [NULL]

        except AttributeError:
            return NULL, [NULL] #If there is no li with this class, there isn't any job description nor skills

        try: 
            #The skills div comes after the description div and carries the same class name
            if not(self.is_desc(description_div)):
                skills_div = job_apt_div.find('div', class_=skill_class)

                if banner:
                    skills_div = job_apt_div.find_all('div', class_= desc_class)[1]
                    job_description = skills_div.find('span', attrs={'aria-hidden': 'true'}).text.strip()
                else:
                    job_skills = skills_div.find('span', attrs={'aria-hidden': 'true'}).text.replace(SKILLS, '').split("·")
                
                #Just delete the blank spaces
                for i in range(len(job_skills)):
                    job_skills[i] = job_skills[i].strip()

            else:
                if banner:
                    skills_div = job_apt_div.find_all('div', class_= desc_class)[2]
                    job_skills = skills_div.find('span', attrs={'aria-hidden': 'true'}).text.replace(SKILLS, '').split("·")
                else:
                    skills_div = job_apt_div.find_all('div', class_= desc_class)[1]
                    job_skills = skills_div.find('span', attrs={'aria-hidden': 'true'}).text.replace(SKILLS, '').split("·")

                #Just delete the blank spaces
                for i in range(len(job_skills)):
                    job_skills[i] = job_skills[i].strip()
                    
        except IndexError:
            job_skills = [NULL]
        except AttributeError:
            job_skills = [NULL]
        
        return job_description, job_skills
    

