from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///notices.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ------------------ MODELS ------------------
class Notice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date_posted = db.Column(db.String(20), default=datetime.now().strftime("%Y-%m-%d"))

# ------------------ ROUTES ------------------
@app.route("/")
def home():
    return jsonify({"message": "College Notice Board API is running!"})

@app.route("/add_notice", methods=["POST"])
def add_notice():
    data = request.get_json()
    title = data.get("title")
    content = data.get("content")
    category = data.get("category")

    if not title or not content or not category:
        return jsonify({"error": "All fields are required"}), 400

    notice = Notice(title=title, content=content, category=category)
    db.session.add(notice)
    db.session.commit()

    return jsonify({"message": "Notice added successfully!"})

@app.route("/get_notices", methods=["GET"])
def get_notices():
    category = request.args.get("category")
    if category:
        notices = Notice.query.filter_by(category=category).all()
    else:
        notices = Notice.query.all()
    data = [
        {
            "id": n.id,
            "title": n.title,
            "content": n.content,
            "category": n.category,
            "date": n.date_posted,
        }
        for n in notices
    ]
    return jsonify(data)

@app.route("/delete_notice/<int:id>", methods=["DELETE"])
def delete_notice(id):
    notice = Notice.query.get(id)
    if not notice:
        return jsonify({"error": "Notice not found"}), 404
    db.session.delete(notice)
    db.session.commit()
    return jsonify({"message": "Notice deleted successfully"})

# ------------------ MAIN ------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000)
