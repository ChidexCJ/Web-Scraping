import pandas as pd
from bs4 import BeautifulSoup
import requests

url = 'https://www.espn.com/soccer/table/_/league/eng.1'

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

soup.find('h1')

soup.find_all('span', class_ = 'hide-mobile')

club_names = [i.text for i in soup.find_all('span', class_ = 'hide-mobile')]


position = [i.text for i in soup.find_all('span', class_ = 'team-position ml2 pr3')]

data = pd.DataFrame(club_names, position)
data.rename(columns= {0 : 'Club'}, inplace=True)

games_played = [i.text for i in soup.find_all('span', class_ = 'stat-cell')]

def splitter(lst, size):
    for i in range(0, len(lst), size):
        x =  lst[i:i+size]
        yield x

stats = list(splitter(games_played,8))

data1 = pd.DataFrame(stats, position)

data1
data1.rename(columns= {0: "Games Played", 1 : " Won", 2 : "Draw", 3 : "Loss", 4 : "Scored", 5 : "Conceded", 6 : "Difference", 7 : "Points"}, inplace=True)


table = pd.concat([data,data1], axis=1)

table.to_csv('PremierLeagueTable.csv', index=False)