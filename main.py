from flask import Flask, request, jsonify
from recommendationSystem import get_recommend

app = Flask(__name__)

@app.route('/api/recommendActivities/<int:user_id>', methods=['GET'])
def getRecommendActivity(user_id):
    return get_recommend(user_id)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("5050"), debug=True)
