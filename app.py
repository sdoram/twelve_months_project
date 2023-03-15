from pymongo import MongoClient

client = MongoClient('mongodb+srv://sparta:sparta@cluster0.ahs6lya.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import time

app = Flask(__name__)

# 책 리뷰 작성 페이지
@app.route('/review')
def content2():
    return render_template('review.html')

# 메인 페이지
@app.route('/')
def home():
    return render_template('main.html')

# 팀원 정보 입력 페이지
@app.route('/record')
def content3():
    return render_template('record.html')

# 책 정보 저장하기
@app.route("/books", methods=["POST"])
def movie_post():
    url_receive = request.form['url_give']
    star_receive = request.form['star_give']
    reviewer_receive = request.form['reviewer_give']
    comment_receive = request.form['comment_give']

    data = requests.get(url_receive)
    soup = BeautifulSoup(data.text, "html.parser")

    img_tag = soup.select_one("img[src^='https://contents.kyobobook.co.kr/sih/fit-in/']")
    img_url = img_tag.get("src")

    title_tag = soup.select_one(
        "#contents > div.prod_detail_header > div > div.prod_detail_title_wrap > div > div.prod_title_box.auto_overflow_wrap > div.auto_overflow_contents > div > h1 > span")
    title_name = title_tag.text

    author_tag = soup.select_one(
        "#contents > div.prod_detail_header > div > div.prod_detail_view_wrap > div.prod_detail_view_area > div:nth-child(1) > div > div.prod_author_box.auto_overflow_wrap > div.auto_overflow_contents > div > div > a:nth-child(1)")
    author_name = author_tag.text

    doc = {
        'image': img_url,
        'title': title_name,
        'author': author_name,
        'star': star_receive,
        'reviewer': reviewer_receive,
        'comment': comment_receive
    }

    db.books.insert_one(doc)
    return jsonify({'msg': '저장 완료!'})

# 책 정보 가져오기
@app.route("/books", methods=["GET"])
def movie_get():
    book_list = list(db.books.find({}, {'_id': False}))
    return jsonify({'books': book_list})

# 팀원 정보 저장하기 
@app.route("/members", methods=["POST"])
def members_post():
    img_receive = request.form['img_give']
    name_receive = request.form['name_give']
    mbti_receive = request.form['mbti_give']
    book_receive = request.form['book_give']
    blog_receive = request.form['blog_give']
    #입력 시간 체크 함수
    time_receive = (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

    doc = {
        'img': img_receive,
        'name': name_receive,
        'mbti': mbti_receive,
        'book': book_receive,
        'blog': blog_receive,
        'time': time_receive
    }
    db.members.insert_one(doc)
    return jsonify({'msg': '작성 완료!'})

# 팀원 정보 가져오기
@app.route("/show", methods=["GET"])
def members_get():
    all_members = list(db.members.find({}, {'_id': False}))
    return jsonify({'result': all_members})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5003, debug=True)
