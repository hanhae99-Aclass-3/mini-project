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

site_list = ['https://www.goal.com/kr/%ED%8C%80/%EB%A7%A8%EC%B2%B4%EC%8A%A4%ED%84%B0-%EC%8B%9C%ED%8B%B0/a3nyxabgsqlnqfkeg41m6tnpp',
             'https://www.goal.com/kr/%ED%8C%80/%EC%B2%BC%EC%8B%9C/9q0arba2kbnywth8bkxlhgmdr',
             'https://www.goal.com/kr/%ED%8C%80/%EB%A6%AC%EB%B2%84%ED%92%80/c8h9bw1l82s06h77xxrelzhur',
             'https://www.goal.com/kr/%ED%8C%80/%EC%95%84%EC%8A%A4%EB%84%90/4dsgumo7d4zupm2ugsvm4zm4d',
             'https://www.goal.com/kr/%ED%8C%80/%EC%9B%A8%EC%8A%A4%ED%8A%B8%ED%96%84-%EC%9C%A0%EB%82%98%EC%9D%B4%ED%8B%B0%EB%93%9C/4txjdaqveermfryvbfrr4taf7',
             'https://www.goal.com/kr/%ED%8C%80/%ED%86%A0%ED%8A%B8%EB%84%98-%ED%99%8B%EC%8A%A4%ED%8D%BC/22doj4sgsocqpxw45h607udje',
             'https://www.goal.com/kr/%ED%8C%80/%EB%A7%A8%EC%B2%B4%EC%8A%A4%ED%84%B0-%EC%9C%A0%EB%82%98%EC%9D%B4%ED%8B%B0%EB%93%9C/6eqit8ye8aomdsrrq0hk3v7gh',
             'https://www.goal.com/kr/%ED%8C%80/%EC%9A%B8%EB%B2%84%ED%96%84%ED%8A%BC-%EC%9B%90%EB%8D%94%EB%9F%AC%EC%8A%A4/b9si1jn1lfxfund69e9ogcu2n',
             'https://www.goal.com/kr/%ED%8C%80/%EB%B8%8C%EB%9D%BC%EC%9D%B4%ED%8A%BC-%EC%95%A4-%ED%98%B8%EB%B8%8C/e5p0ehyguld7egzhiedpdnc3w',
             'https://www.goal.com/kr/%ED%8C%80/%EB%A0%88%EC%8A%A4%ED%84%B0-%EC%8B%9C%ED%8B%B0/avxknfz4f6ob0rv9dbnxdzde0',
             'https://www.goal.com/kr/%ED%8C%80/%ED%81%AC%EB%A6%AC%EC%8A%A4%ED%84%B8-%ED%8C%B0%EB%A6%AC%EC%8A%A4/1c8m2ko0wxq1asfkuykurdr0y',
             'https://www.goal.com/kr/%ED%8C%80/%EB%B8%8C%EB%A0%8C%ED%8A%B8%ED%8F%AC%EB%93%9C/7yx5dqhhphyvfisohikodajhv',
             'https://www.goal.com/kr/%ED%8C%80/%EC%95%84%EC%8A%A4%ED%86%A4-%EB%B9%8C%EB%9D%BC/b496gs285it6bheuikox6z9mj',
             'https://www.goal.com/kr/%ED%8C%80/%EC%82%AC%EC%9A%B0%EC%83%98%ED%94%84%ED%84%B4/d5ydtvt96bv7fq04yqm2w2632',
             'https://www.goal.com/kr/%ED%8C%80/%EC%97%90%EB%B2%84%ED%8A%BC/ehd2iemqmschhj2ec0vayztzz',
             'https://www.goal.com/kr/%ED%8C%80/%EB%A6%AC%EC%A6%88-%EC%9C%A0%EB%82%98%EC%9D%B4%ED%8B%B0%EB%93%9C/48gk2hpqtsl6p9sx9kjhaydq4',
             'https://www.goal.com/kr/%ED%8C%80/%EC%99%93%ED%8D%BC%EB%93%9C/4t83rqbdbekinxl5fz2ygsyta',
             'https://www.goal.com/kr/%ED%8C%80/%EB%B2%88%EB%A6%AC/64bxxwu2mv2qqlv0monbkj1om',
             'https://www.goal.com/kr/%ED%8C%80/%EB%89%B4%EC%BA%90%EC%8A%AC-%EC%9C%A0%EB%82%98%EC%9D%B4%ED%8B%B0%EB%93%9C/7vn2i2kd35zuetw6b38gw9jsz',
             'https://www.goal.com/kr/%ED%8C%80/%EB%85%B8%EB%A6%AC%EC%B9%98-%EC%8B%9C%ED%8B%B0/suz80crpy3anixyzccmu6jzp',]



site = ''
@app.route('/detail/<int:detail_id>')
def team_detail(detail_id, site = ''):
    # detail/id 별로 site url 다르게 하기
    detailid = detail_id
    if detailid == 1:
        site = site_list[0]
    elif detailid == 2:
        site = site_list[1]
    elif detailid == 3:
        site = site_list[2]   
    elif detailid == 4:
        site = site_list[3]   
    elif detailid == 5:
        site = site_list[4]   
    elif detailid == 6:
        site = site_list[5]   
    elif detailid == 7:
        site = site_list[6]   
    elif detailid == 8:
        site = site_list[7]   
    elif detailid == 9:
        site = site_list[8]   
    elif detailid == 10:
        site = site_list[9]   
    elif detailid == 11:
        site = site_list[10]   
    elif detailid == 12:
        site = site_list[11]   
    elif detailid == 13:
        site = site_list[12]   
    elif detailid == 14:
        site = site_list[13]   
    elif detailid == 15:
        site = site_list[14]   
    elif detailid == 16:
        site = site_list[15]   
    elif detailid == 17:
        site = site_list[16]   
    elif detailid == 18:
        site = site_list[17]   
    elif detailid == 19:
        site = site_list[18]   
    elif detailid == 20:
        site = site_list[19]

    # 토큰값 받아옴
    token_receive = request.cookies.get('mytoken')

    # token 값, 시크릿키, 사용알고리즘?확인
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
        # '골닷컴' 크롤링
        data = requests.get(
            site,
            headers=headers)
        soup = BeautifulSoup(data.text, 'html.parser')
        trs = soup.select(
            'body > div.page-container > div.page-container-bg > div > div > div > div.p0c-team-squad__body > ul > li > a')

        # 크롤링한 데이터를 담을 리스트 준비하기
        players = []
        numbers = []
        for tr in trs:
            name = tr.select_one('div > span.p0c-team-squad__member-name').text.strip()
            number = tr.select_one('span.p0c-team-squad__member-number').text.strip()
            players.append(name)
            numbers.append(number)

        # 팀 이름 크롤링
        data2 = requests.get(site, headers=headers)

        soup2 = BeautifulSoup(data2.text, 'html.parser')

        
        teams = soup2.select(
            'body > div.page-container > div.page-container-bg > div.page-header.tag-header.tag-header-team')
        # 팀 목록 리스트
        team_list = []
        for team in teams:
            teamname = team.select_one('span').text   
            team_list.append(teamname)

        return render_template('detail.html', players=players, numbers=numbers, team_list = team_list, zip=zip)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))




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


@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


@app.route('/sign_in', methods=['POST'])
def sign_in():
    # id, pw를 받아서 맞춰보고, 토큰을 만들어 발급한다.
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    # 회원가입 때와 같은 방법으로 pw를 암호화한다.
    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()

    # id, 암호화된 pw를 가지고 해당 유저를 찾는다.
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})

    # 찾으면 JWT 토큰을 만들어 발급합니다.
    if result is not None:
        # JWT 토큰에는, payload와 시크릿키가 필요하다.
        # 시크릿키가 있어야 토큰을 복호화해서 payload 값을 볼 수 있다.
        # id와 exp를 담는다. JWT 토큰을 풀면 유저ID 값을 알 수 있다.
        # exp에는 만료시간을 넣어준다.(seconds,hours등으로 형식은 seconds=60*60*24)는 24시간.
        # 만료시간이 지나면, 시크릿키로 토큰을 풀때 만료되었다고 에러가 난다.
        payload = {
            'id': username_receive, # 로그인 10초 유지
            'exp': datetime.utcnow() + timedelta(seconds=30)  # 로그인 30초 유지
        }
        # 찾으면 토큰을 준다.
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        # .decode('utf-8') 왜 에러가 나는건지..

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


# ------------크롤링
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
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        return render_template('index.html', result=team_list, zip = zip)

    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))



# -----------즐겨찾기 페이지
@app.route('/like')
def like():
    token_receive = request.cookies.get('mytoken')
    try:

# -------------사용한 payload가져오기

        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        return render_template('index2.html')
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

#-----------즐겨찾기 기능
@app.route('/api/like', methods=['POST'])
def save_like():
    token_receive = request.cookies.get('mytoken')
    try:
#-------------사용한 payload가져오기
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        userid = payload['id']
# ----------저장에 필요한 값 받아오기
        teamlogo_receive = request.form['teamlogo_give']
        teamname_receive = request.form['teamname_give']
#---------db에 입력된 값을 찾아 존재하는지 확인하여 중복 방지
        team = db.teamlike.find_one({'teamname': teamname_receive, 'userID': payload['id']}, {'_id': False})
        if (team is not None):
            return jsonify({'msg': '이미 등록된 팀입니다!'})
        else:
            doc = {
                "userID": userid,
                "teamlogo": teamlogo_receive,
                "teamname": teamname_receive
            }
#---------즐겨찾기 저장
            db.teamlike.insert_one(doc)
        return jsonify({'result': 'success', 'msg': '즐찾!!'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("login"))

#----------즐겨찾기 보기
@app.route('/api/like', methods=['GET'])
def get_like():
    token_receive = request.cookies.get('mytoken')
    try:
# -------------사용한 payload가져오기
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
# ---------------팀당 1개씩만 저장, userid값만 불러오면 됨
        mylike = list(db.teamlike.find({'userID': payload['id']},{'_id':False}))
        return jsonify({'my_like': mylike})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("login"))

#---------즐겨찾기 삭제
@app.route('/api/deletelike', methods=['POST'])
def delete_like():
    token_receive = request.cookies.get('mytoken')
    try:
# -------------사용한 payload가져오기
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
#---------------팀명 가져오기
        teamname_receive = request.form['teamname_give']
#------------------팀명과 payload의 id값만 찾아와서 삭제
        db.teamlike.delete_one({'teamname': teamname_receive, 'userID': payload['id']})
        return jsonify({'result': 'success', 'msg': '삭제'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("login"))




if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
