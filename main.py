import re
from scraping import search_salary
import numpy as np
import pandas as pd


def calculate_montly(data_frame):
    """
    Returns the montly salary regardless of if data collected by montly or annualy.
    """
    yearly = data_frame[data_frame["Payment Interval"] == "yr"]
    montly = data_frame[data_frame["Payment Interval"] == "mo"]
    if len(yearly) == 0:
        return np.mean(montly["Salary"])
    elif len(montly) == 0:
        return np.mean(yearly["Salary"])/12
    return (np.mean(yearly["Salary"])/12 + np.mean(montly["Salary"]))/2

def read_list_of_jobs(country):
    with open("Jobs.txt","r") as file:
        list_of_jobs = file.readlines()
    for job in list_of_jobs:
        df = search_salary(job,country)
        try:
            print(df)
            print(calculate_montly(df))
        except:
            print("Couldn't find anything about " + job)

read_list_of_jobs("Turkey")