from pymongo import MongoClient
from bs4 import BeautifulSoup
from flask import Flask, render_template, jsonify, request, redirect, url_for
import requests
import jwt
import datetime
import hashlib
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'SPARTA'


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
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        return render_template('index.html', result=team_list)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))
@app.route('/like')
def like():
    return render_template('index2.html')

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}


# '골닷컴' 크롤링
data = requests.get('https://www.goal.com/kr/%ED%8C%80/%ED%86%A0%ED%8A%B8%EB%84%98%ED%99%8B%EC%8A%A4%ED%8D%BC/22doj4sgsocqpxw45h607udje', headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')
trs = soup.select('body > div.page-container > div.page-container-bg > div > div > div > div.p0c-team-squad__body > ul > li > a')

# 크롤링한 데이터를 담을 리스트 준비하기
images = []
players = []
numbers = []
for tr in trs:
    img = tr.select_one('span.p0c-team-squad__member-photo > img')['src']
    name = tr.select_one('div > span.p0c-team-squad__member-name').text.strip()
    number = tr.select_one('span.p0c-team-squad__member-number').text.strip()
    players.append(name)
    numbers.append(number)

# 상세 페이지 API
@app.route('/detail')
def detail_page():
    # site_list = ['https://www.goal.com/kr/%ED%8C%80/%EB%A7%A8%EC%B2%B4%EC%8A%A4%ED%84%B0-%EC%8B%9C%ED%8B%B0/a3nyxabgsqlnqfkeg41m6tnpp',
    #          'https://www.goal.com/kr/%ED%8C%80/%EC%B2%BC%EC%8B%9C/9q0arba2kbnywth8bkxlhgmdr',
    #          'https://www.goal.com/kr/%ED%8C%80/%EB%A6%AC%EB%B2%84%ED%92%80/c8h9bw1l82s06h77xxrelzhur',
    #          'https://www.goal.com/kr/%ED%8C%80/%EC%95%84%EC%8A%A4%EB%84%90/4dsgumo7d4zupm2ugsvm4zm4d',
    #          'https://www.goal.com/kr/%ED%8C%80/%EC%9B%A8%EC%8A%A4%ED%8A%B8%ED%96%84-%EC%9C%A0%EB%82%98%EC%9D%B4%ED%8B%B0%EB%93%9C/4txjdaqveermfryvbfrr4taf7',
    #          'https://www.goal.com/kr/%ED%8C%80/%ED%86%A0%ED%8A%B8%EB%84%98-%ED%99%8B%EC%8A%A4%ED%8D%BC/22doj4sgsocqpxw45h607udje',
    #          'https://www.goal.com/kr/%ED%8C%80/%EB%A7%A8%EC%B2%B4%EC%8A%A4%ED%84%B0-%EC%9C%A0%EB%82%98%EC%9D%B4%ED%8B%B0%EB%93%9C/6eqit8ye8aomdsrrq0hk3v7gh',
    #          'https://www.goal.com/kr/%ED%8C%80/%EC%9A%B8%EB%B2%84%ED%96%84%ED%8A%BC-%EC%9B%90%EB%8D%94%EB%9F%AC%EC%8A%A4/b9si1jn1lfxfund69e9ogcu2n',
    #          'https://www.goal.com/kr/%ED%8C%80/%EB%B8%8C%EB%9D%BC%EC%9D%B4%ED%8A%BC-%EC%95%A4-%ED%98%B8%EB%B8%8C/e5p0ehyguld7egzhiedpdnc3w',
    #          'https://www.goal.com/kr/%ED%8C%80/%EB%A0%88%EC%8A%A4%ED%84%B0-%EC%8B%9C%ED%8B%B0/avxknfz4f6ob0rv9dbnxdzde0',
    #          'https://www.goal.com/kr/%ED%8C%80/%ED%81%AC%EB%A6%AC%EC%8A%A4%ED%84%B8-%ED%8C%B0%EB%A6%AC%EC%8A%A4/1c8m2ko0wxq1asfkuykurdr0y',
    #          'https://www.goal.com/kr/%ED%8C%80/%EB%B8%8C%EB%A0%8C%ED%8A%B8%ED%8F%AC%EB%93%9C/7yx5dqhhphyvfisohikodajhv',
    #          'https://www.goal.com/kr/%ED%8C%80/%EC%95%84%EC%8A%A4%ED%86%A4-%EB%B9%8C%EB%9D%BC/b496gs285it6bheuikox6z9mj',
    #          'https://www.goal.com/kr/%ED%8C%80/%EC%82%AC%EC%9A%B0%EC%83%98%ED%94%84%ED%84%B4/d5ydtvt96bv7fq04yqm2w2632',
    #          'https://www.goal.com/kr/%ED%8C%80/%EC%97%90%EB%B2%84%ED%8A%BC/ehd2iemqmschhj2ec0vayztzz',
    #          'https://www.goal.com/kr/%ED%8C%80/%EB%A6%AC%EC%A6%88-%EC%9C%A0%EB%82%98%EC%9D%B4%ED%8B%B0%EB%93%9C/48gk2hpqtsl6p9sx9kjhaydq4',
    #          'https://www.goal.com/kr/%ED%8C%80/%EC%99%93%ED%8D%BC%EB%93%9C/4t83rqbdbekinxl5fz2ygsyta',
    #          'https://www.goal.com/kr/%ED%8C%80/%EB%B2%88%EB%A6%AC/64bxxwu2mv2qqlv0monbkj1om',
    #          'https://www.goal.com/kr/%ED%8C%80/%EB%89%B4%EC%BA%90%EC%8A%AC-%EC%9C%A0%EB%82%98%EC%9D%B4%ED%8B%B0%EB%93%9C/7vn2i2kd35zuetw6b38gw9jsz',
    #          'https://www.goal.com/kr/%ED%8C%80/%EB%85%B8%EB%A6%AC%EC%B9%98-%EC%8B%9C%ED%8B%B0/suz80crpy3anixyzccmu6jzp',]

    # for site in site_list:
    #     data = requests.get(site, headers=headers)

    #     soup = BeautifulSoup(data.text, 'html.parser')

    #     trs = soup.select('body > div.page-container > div.page-container-bg > div > div > div > div.p0c-team-squad__body > ul > li > a')
    #     for tr in trs:
    #         img = tr.select_one('span.p0c-team-squad__member-photo > img')
    #         name = tr.select_one('div > span.p0c-team-squad__member-name').text.strip()
    #         number = tr.select_one('span.p0c-team-squad__member-number').text.strip()

    #         print(img, name, number)
    
    
    team_name = '토트넘 홋스퍼 FC'
    hometown = '잉글랜드 런던 북부 토트넘'
    home_stadium = '토트넘 홋스퍼 스타디움'
    team_manager = '안토니오 콘테'
    return render_template('detail.html', team_name = team_name, hometown = hometown, home_stadium = home_stadium, team_manager = team_manager, players = players, numbers = numbers, zip = zip)

# 상세 페이지 코멘트 업로드하기 API
@app.route('/api/comment', methods=['POST'])
def upload_comment():
    # nickname_receive = request.form['nickname_give']
    comment_receive = request.form['comment_give']

    doc = {
        # 'nickname': nickname_receive,
        'comment': comment_receive
    }

    db.comments.insert_one(doc)

    return jsonify({'result': 'success', 'msg': '작성 완료!'})

# 상세 페이지 코멘트 삭제하기 API
@app.route('/api/comment/delete', methods=['POST'])
def delete_post():
    comment_receive = request.form['comment_give']
    db.comments.delete_one({'comment': comment_receive})

    return jsonify({'result': 'success', 'msg': '삭제 완료!'})

# 상세 페이지 코멘트 보여주기 API
@app.route('/api/comment/list', methods=['GET'])
def view_comment():
    comments = list(db.comments.find({}, {'_id': False}))

    return jsonify({'result': 'success', 'all_comments': comments})

# client = MongoClient('내AWS아이피', 27017, username="아이디", password="비밀번호")
db = client.football_tonight


# @app.route('/')
# def home():
#     token_receive = request.cookies.get('mytoken')
#     try:
#         payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

#         return render_template('index.html')
#     except jwt.ExpiredSignatureError:
#         return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
#     except jwt.exceptions.DecodeError:
#         return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
            'id': username_receive,
            'exp': datetime.utcnow() + timedelta(seconds=10)  # 로그인 10초 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')  #.decode('utf-8') 왜 에러가 나는건지..

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    nickname_receive = request.form['nickname_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,  # 아이디
        "password": password_hash,  # 비밀번호
        "nickname": nickname_receive,
        "profile_name": username_receive,  # 프로필 이름 기본값은 아이디
        "profile_pic": "",  # 프로필 사진 파일 이름
        "profile_pic_real": "profile_pics/profile_placeholder.png",  # 프로필 사진 기본 이미지
        "profile_info": ""  # 프로필 한 마디
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})


@app.route('/update_profile', methods=['POST'])
def save_img():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # 프로필 업데이트
        return jsonify({"result": "success", 'msg': '프로필을 업데이트했습니다.'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@app.route('/posting', methods=['POST'])
def posting():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # 포스팅하기
        return jsonify({"result": "success", 'msg': '포스팅 성공'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@app.route("/get_posts", methods=['GET'])
def get_posts():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # 포스팅 목록 받아오기
        return jsonify({"result": "success", "msg": "포스팅을 가져왔습니다."})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@app.route('/update_like', methods=['POST'])
def update_like():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # 좋아요 수 변경
        return jsonify({"result": "success", 'msg': 'updated'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
