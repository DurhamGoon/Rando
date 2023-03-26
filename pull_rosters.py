from bs4 import BeautifulSoup
import requests
import json 
import re
import pandas as pd

xfl_teams = [
    'arlington',
    'washington-dc',
    'houston',
    'orlando',
    'san-antonio',
    'seattle',
    'st-louis',
    'las-vegas'
]

def pull_roster():

    for team in xfl_teams:

        url = f'https://www.xfl.com/teams/{team}/roster'

        webpage = requests.get(url)
        soup = BeautifulSoup(webpage.content, 'html.parser')
        roster_location = soup.html.body.div.main.section

        js_roster_script = roster_location.find_all('script')[1].text

        pattern = r'{(.*)}'

        match = re.search(pattern, js_roster_script)

        json_text = match.group()
        data = json.loads(json_text)
        html_data = data["content"][1]["text"]
        soup = BeautifulSoup(html_data, "html.parser")

        table = soup.find('table')
        df = pd.read_html(str(table), header=0)[0].iloc[:,1:]
        df["No."] = df["No."].fillna(-1).astype("int")
        df.rename(columns={"No.":"number","Name":"name","Position":"position","College":"college"}, inplace=True)
        df = df.reindex(columns=['number','name','position','college'])
        df.to_csv(f'{team}-roster.csv', index=False)
        