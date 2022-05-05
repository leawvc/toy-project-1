import jwt
from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

# localhost에 연결하지 않고 최종적으로 배포할 서버에 있는 mongodb에 연결
client = MongoClient('52.79.226.1', 27017, username="test", password="test")

# client = MongoClient('localhost', 27017) #내 로컬에서 실행할 때는 얘 살리기
# 테스트 - 내 로컬

db = client.toy_project

# 맛집리스트 불러오기
@app.route('/matjip', methods=['GET'])
def get_matjips():
    matjip_list = list(db.matjip.find({}, {"_id": False}))
    return jsonify({'result': 'success', 'matjip_list': matjip_list})


# 좋아요 버튼 클릭하면
# 포스트 DB 쌓기 (이름, 주소, 이미지, 리뷰(null))
@app.route('/post/create', methods=['GET'])
def create_post():
    title_receive = request.form['title']
    address_receive = request.form['address']

    doc = {
        "title": title_receive,
        "address": address_receive,
        "review": ""
    }

    db.posts.insert_one(doc)

    # 테스트하려고 작성한 코드
    # postings = list(db.posts.find({}, {"_id": False}))
    # return jsonify({'result': 'success', 'postings': postings})

# 리뷰 저장
@app.route('/post/update', methods=['POST'])
def update_post():
    title_receive = request.form['title_give']
    review_receive = request.form['review_give']
    doc = {
        "title": title_receive,
        "review": review_receive
    }
    db.posts.update_one({'title': title_receive}, {'$set': {'review': review_receive}})
    return jsonify({'result': 'success', 'msg': '포스팅 완료'})


# 게시물 삭제 api
@app.route('/post/delete', methods=['POST'])
def delete_post():
    title_receive = request.form['title_give']
    post = list(db.posts.find({"title": title_receive}))["review"]
    print(title_receive, post)
    db.posts.delete_one({"title":title_receive, "post":post})
    return jsonify({'result': 'success', 'msg': f'"{title_receive}"에 대한 포스팅 삭제 완료!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
