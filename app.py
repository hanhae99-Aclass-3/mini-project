from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbsparta
@app.route('/')
def home():
# ------------크롤링
    url = 'https://www.goal.com/kr/%ED%94%84%EB%A6%AC%EB%AF%B8%EC%96%B4%EB%A6%AC%EA%B7%B8/%EC%88%9C%EC%9C%84/2kwbbcootiqqgmrzs6o5inle5'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    team_list = []
    teams = soup.select(
        'body > div.page-container > div.page-container-bg > div.mr-gutters.main-container.clearfix > div > div > div.widget-match-standings > div.widget-match-standings__table-container > table > tbody > tr')
    for team in teams:
        teamname = team.select_one('td.widget-match-standings__team > a.widget-match-standings__link > span').text  #팀이름
        teamrank = team.select_one('td').text                                                                       #팀순위
        teamlogo = team.select_one('td.widget-match-standings__team > a:nth-child(1) > img')['src']                 #팀로고
        teamp = team.select_one('td.widget-match-standings__matches-played').text                                   #경기수
        teamw = team.select_one('td.widget-match-standings__matches-won').text                                      #승리
        teamd = team.select_one('td.widget-match-standings__matches-drawn').text                                    #무승부
        teaml = team.select_one('td.widget-match-standings__matches-lost').text                                     #패배
        team_list.append([teamrank, teamlogo, teamname, teamp, teamw, teamd, teaml])                                #리스트로묶음
#-----------list로만들어서 index페이지로 주기
    return render_template('index.html', result=team_list)

#-----------즐겨찾기 페이지
@app.route('/like')
def like():
    return render_template('index2.html')

#-----------즐겨찾기 기능
@app.route('/api/like', methods=['POST'])
def save_like():
# ----------저장에 필요한 값 받아오기
    teamlogo_receive = request.form['teamlogo_give']
    teamname_receive = request.form['teamname_give']
#---------db에 입력된 값을 찾아 존재하는지 확인하여 중복 방지
    team = db.teamlike.find_one({'teamname': teamname_receive}, {'_id': False})
    if (team is not None):
        return jsonify({'msg': '이미 등록된 팀입니다!'})
    doc = {
        "teamlogo": teamlogo_receive,
        "teamname": teamname_receive
    }
#---------즐겨찾기 저장
    db.teamlike.insert_one(doc)
    return jsonify({'result': 'success', 'msg': '즐찾!!'})

#----------즐겨찾기 보기
@app.route('/api/like', methods=['GET'])
def get_like():
    mylike = list(db.teamlike.find({},{'_id':False}))
    return jsonify({'my_like': mylike})

#---------즐겨찾기 삭제
@app.route('/api/deletelike', methods=['POST'])
def delete_like():
    teamname_receive = request.form['teamname_give']
    db.teamlike.delete_one({'teamname': teamname_receive})
    return jsonify({'result': 'success', 'msg': '삭제'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)