from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbsparta
@app.route('/')
def home():
    url = 'https://www.goal.com/kr/%ED%94%84%EB%A6%AC%EB%AF%B8%EC%96%B4%EB%A6%AC%EA%B7%B8/%EC%88%9C%EC%9C%84/2kwbbcootiqqgmrzs6o5inle5'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    team_list = []
    teams = soup.select(
        'body > div.page-container > div.page-container-bg > div.mr-gutters.main-container.clearfix > div > div > div.widget-match-standings > div.widget-match-standings__table-container > table > tbody > tr')
    for team in teams:
        teamname = team.select_one('td.widget-match-standings__team > a.widget-match-standings__link > span').text
        teamrank = team.select_one('td').text
        teamlogo = team.select_one('td.widget-match-standings__team > a:nth-child(1) > img')['src']
        teamp = team.select_one('td.widget-match-standings__matches-played').text
        teamw = team.select_one('td.widget-match-standings__matches-won').text
        teamd = team.select_one('td.widget-match-standings__matches-drawn').text
        teaml = team.select_one('td.widget-match-standings__matches-lost').text
        team_list.append([teamrank, teamlogo, teamname, teamp, teamw, teamd, teaml])
    return render_template('index.html', result=team_list)
@app.route('/like')
def like():
    return render_template('index2.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)