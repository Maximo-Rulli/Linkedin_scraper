import tkinter as tk
from tkinter import messagebox
from scraper import Scraper
import pandas as pd
from ast import literal_eval as lit

#Token constant (will be used to train the model and defines a blank space)
NULL = '[NONE]'

class Linkedin_Scraper:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Linkedin Manual Profile Scraper")
        self.root.geometry('700x400')

        self.label = tk.Label(self.root, text="Enter Linkedin link:", font=("Calibri", "24", "bold"))
        self.label.grid(pady=5, padx=50, row=0, column=0, columnspan = 4, sticky = tk.W+tk.E)

        self.entry = tk.Entry(self.root, font=("Calibri", "12", "italic"), width = 70)
        self.entry.grid(pady=10, padx=50, row=1, column=0, columnspan = 4, sticky = tk.W+tk.E)

        self.button = tk.Button(self.root, text="Scrape and save!", command=self.button_clicked)
        self.button.grid(pady=5, row=2, column=0)

        #Set list and menu with job titles
        with open('jobs_titles.txt', 'r') as f:
            options_list = f.readlines()
            f.close()
        
        self.job_var = tk.StringVar(self.root)
        self.job_var.set("Select a job")
        self.job_menu = tk.OptionMenu(self.root, self.job_var, *options_list) 
        self.job_menu.grid(pady=5, row=2, column=1)  

        #Set radiobuttons that determine if the profile matches the job or not
        self.match_var = tk.BooleanVar()
        self.match = tk.Radiobutton(self.root, text="Match", variable=self.match_var, value=1)
        self.match.grid(pady=5, row=2, column=2)
        self.no_match = tk.Radiobutton(self.root, text="No match", variable=self.match_var, value=0)
        self.no_match.grid(pady=5, row=2, column=3) 

        self.scraper = Scraper()

        #Update dataset (the old dataset will become the backup dataset)
        df_back = pd.read_csv('dataset.csv', converters={'Companies': lit, 'Roles': lit, 'Times': lit, 'Types': lit,
                                                    'Descriptions': lit, 'Roles skills': lit, 'General skills': lit})
        df_back.to_csv('backup_dataset.csv', index=False)

        #Create GUI to display the profile in the csv format

        #Titles of each column
        title_font = ("Calibri", "12", "bold")
        self.company_title = tk.Label(self.root, text='1st Company', font=title_font).grid(pady=5, row=3, column=0)
        self.role_title = tk.Label(self.root, text='1st Role', font=title_font).grid(pady=5, row=3, column=1)
        self.time_title = tk.Label(self.root, text='1st Time', font=title_font).grid(pady=5, row=3, column=2)
        self.type_title = tk.Label(self.root, text='1st Job type',font=title_font).grid(pady=5, row=3, column=3)
        self.description_title = tk.Label(self.root, text='1st Description',font=title_font).grid(pady=5, row=5, column=0, columnspan=2)
        self.role_skills_title = tk.Label(self.root, text='Skills related to 1st job',font=title_font).grid(pady=5, row=5, column=2)
        self.general_skills_title = tk.Label(self.root, text='First 5 skills',font=title_font).grid(pady=5, row=5, column=3)

        #Display the last row of the backup dataframe
        self.company_var = tk.StringVar(self.root, df_back.iloc[-1]['Companies'][-1][:30])
        self.company_content = tk.Label(self.root, textvariable=self.company_var).grid(pady=5, row=4, column=0)

        self.role_var = tk.StringVar(self.root, df_back.iloc[-1]['Roles'][-1][:30])
        self.role_content = tk.Label(self.root, textvariable=self.role_var).grid(pady=5, row=4, column=1)

        self.time_var = tk.StringVar(self.root, df_back.iloc[-1]['Times'][-1])
        self.time_content = tk.Label(self.root, textvariable=self.time_var).grid(pady=5, row=4, column=2)

        self.type_var = tk.StringVar(self.root, df_back.iloc[-1]['Types'][-1])
        self.type_content = tk.Label(self.root, textvariable=self.type_var).grid(pady=5, row=4, column=3)
        
        #The description is splitted in chunks of 55 characters
        description = df_back.iloc[-1]['Descriptions'][-1]
        chunk_size = 55
        desc_split = []
        while description:
            chunk, description = description[:chunk_size], description[chunk_size:]
            desc_split.append(chunk)

        self.description_var = tk.StringVar(self.root, '\n'.join(desc_split))
        self.description_content = tk.Label(self.root, textvariable=self.description_var).grid(pady=5, row=6, column=0, columnspan=2, sticky=tk.W)

        self.role_skill_var = tk.StringVar(self.root, '\n'.join(df_back.iloc[-1]['Roles skills'][-1][:5]))
        self.role_skill_content = tk.Label(self.root, textvariable=self.role_skill_var).grid(pady=5, row=6, column=2)
        
        self.general_skills_var = tk.StringVar(self.root, '\n'.join(df_back.iloc[-1]['General skills'][:5]))
        self.general_skills_content = tk.Label(self.root, textvariable=self.general_skills_var).grid(pady=5, row=6, column=3)

    def button_clicked(self)->None:
        url = self.entry.get()
        jobs_out = self.scraper.scrape_job(url)
        if jobs_out == 'error':
            messagebox.showerror("HTML Error AttributeError: 'NoneType'", "Error: No job experience found on profile. It will not be saved!")
        else:
            skills_out  = self.scraper.scrape_skills(url)
            
            if skills_out != 'void':
                self.save(url, jobs_out, skills_out)
            
            else:
                self.save(url, jobs_out, [NULL])

        print("-"*20+"Process finished!"+"-"*20)

    def run(self)->None:
        self.root.mainloop()

    def save(self, url:str,jobs_out:list, skills_out:list)->None:
        df = pd.read_csv('dataset.csv', converters={'Companies': lit, 'Roles': lit, 'Times': lit, 'Types': lit,
                                                    'Descriptions': lit, 'Roles skills': lit, 'General skills': lit})
        
        #Build dictionary with new data
        new_data = {'Profile': url, 'Companies':jobs_out[0], 'Roles':jobs_out[1], 'Times':jobs_out[2], 'Types':jobs_out[3], 
                    'Descriptions':jobs_out[4], 'Roles skills':jobs_out[5], 'General skills':skills_out,
                    'Job class':self.job_var.get().replace('\n', ''), 'Match':self.match_var.get()}
        
        #Add data to dataset and save
        df.loc[len(df.index)] = new_data

        df.to_csv('dataset.csv', index=False)

        #Display the inserted row
        self.company_var.set(df.iloc[-1]['Companies'][-1][:30])
        self.role_var.set(df.iloc[-1]['Roles'][-1][:30])
        self.time_var.set(df.iloc[-1]['Times'][-1])
        self.type_var.set(df.iloc[-1]['Types'][-1])
        
        #The description is splitted in chunks of 55 characters
        description = df.iloc[-1]['Descriptions'][-1]
        chunk_size = 55
        desc_split = []
        while description:
            chunk, description = description[:chunk_size], description[chunk_size:]
            desc_split.append(chunk)

        self.description_var.set('\n'.join(desc_split))
        self.role_skill_var.set('\n'.join(df.iloc[-1]['Roles skills'][-1][:5]))
        self.general_skills_var.set('\n'.join(df.iloc[-1]['General skills'][:5]))


if __name__ == "__main__":
    app = Linkedin_Scraper()
    app.run()
