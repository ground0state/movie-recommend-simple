import json

from flask import Flask, jsonify

app = Flask(__name__)

with open('recommend_by_user.json', 'r') as f:
    movie_recommendations = json.load(f)


@app.route('/api/v1/recommendations/<string:user_id>', methods=['GET'])
def get_recommendations(user_id):
    # 指定したユーザーIDの映画のリストを取得
    movie_list = movie_recommendations.get(user_id)

    # ユーザーIDが存在しない場合、404エラーを返す
    if movie_list is None:
        # コールドケース
        return jsonify({'recommendations': []})

    return jsonify({'recommendations': movie_list})


@app.route('/api/v1/recommendations', methods=['GET'])
def get_all_ecommendations():
    return jsonify({'all_recommendations': movie_recommendations})


if __name__ == "__main__":
    app.run()
