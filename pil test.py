import requests
from bs4 import BeautifulSoup

url = "https://baseballsavant.mlb.com/statcast_search?hfPT=&hfAB=&hfGT=R%7C&hfPR=&hfZ=&hfStadium=&hfBBL=&hfNewZones=&hfPull=&hfC=&hfSea=2022%7C&hfSit=&player_type=pitcher&hfOuts=&hfOpponent=&pitcher_throws=&batter_stands=&hfSA=&game_date_gt=&game_date_lt=&hfMo=&hfTeam=&home_road=&hfRO=&position=&hfInfield=&hfOutfield=&hfInn=&hfBBT=fly%5C.%5C.ball%7Cpopup%7C&hfFlag=&metric_1=&group_by=name&min_pitches=0&min_results=0&min_pas=0&sort_col=pitches&player_event_sort=api_p_release_speed&sort_order=desc&chk_stats_ba=on#results"

r = requests.get(url)

soup = BeautifulSoup(r.content, "lxml")

table = soup.find("table", {"id": "search_results"}).find("tbody")
amount = 0
for row in table.findAll("tr", {"class": "search_row"}):
    amount += int([i.text for i in row.findAll("td")][3])

print(amount)
