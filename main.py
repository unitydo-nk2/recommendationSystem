from flask import Flask
from recommendationSystem import recommender_engine

app = Flask(__name__)

@app.route('/getRecommends/<int:user_id>', methods=['GET'])
def getRecommendActivity(user_id):
    return recommender_engine(user_id)


if __name__ == '__main__':
    app.run(debug=True)