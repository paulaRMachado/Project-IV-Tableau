import pandas as pd
import requests
from bs4 import BeautifulSoup

def acquire_data (name):
    """This function calls a locally saved CSV file to be imported as a dataframe.
    args:
    :name: string. name to save the file
    """
    # 0. Establish variables
    path = f"data/{name}.csv"
    
    # 1. We read from the path
    df = pd.read_csv(path)
    
    return df

def acquire_salaries(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")
    results = soup.find_all("table", {"class": "wikitable"})[0]
    df = pd.read_html(results.prettify())[0]
    return  df