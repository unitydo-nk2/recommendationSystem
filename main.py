from flask import Flask
from recommendationSystem import get_recommend

app = Flask(__name__)

@app.route('/api/recommendActivities/<int:user_id>', methods=['GET'])
def getRecommendActivity(user_id):
    return get_recommend(user_id)
@app.route('/', methods=['GET'])
def run():
    return "{\"message\": \"Hello World!\""

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("3000"), debug=True)
