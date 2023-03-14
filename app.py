from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:sparta@cluster0.ahs6lya.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta


from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

@app.route('/')
def content2():
    return render_template('index.html')

@app.route('/content2')
def home():
   return render_template('content2.html')

@app.route('/content3')
def content3():
    return render_template('content3.html')


@app.route("/ruff_info", methods=["POST"])
def _post():
    name_receive = request.form['name_give']
    url_receive = request.form['url_give']

    doc = {
        'name': name_receive,
        'url': url_receive,
    }
    db.ruff_info.insert_one(doc)
    return jsonify({'msg': '주문 완료!'})


@app.route("/members", methods=["POST"])
def members_post():

    name_receive = request.form['name_give']
    image_receive = request.form['image_give']
    mbti_receive = request.form['mbti_give']
    book_receive = request.form['book_give']
    blog_receive = request.form['blog_give']

    doc = {
        'name': name_receive,
        'image': image_receive,
        'mbti': mbti_receive,
        'book': book_receive,
        'blog': blog_receive
    }
    db.members.insert_one(doc)
    return jsonify({'msg': '작성 완료!'})

@app.route("/show", methods=["GET"])
def members_get():
    all_members = list(db.members.find({},{'_id':False}))
    return jsonify({'result':all_members})


if __name__ == '__main__':
   app.run('0.0.0.0', port=5003, debug=True)