from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from models import db, Notice

app = Flask(__name__)
CORS(app)  # Allow frontend to access backend

# SQLite database (Render automatically persists it)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notices.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# ---------- ROUTES ----------

@app.route('/')
def home():
    return jsonify({"message": "College Notice Board API is running"})


@app.route('/notices', methods=['GET'])
def get_notices():
    """Fetch all notices"""
    notices = Notice.query.all()
    return jsonify([n.to_dict() for n in notices])


@app.route('/add_notice', methods=['POST'])
def add_notice():
    """Add a new notice"""
    data = request.get_json()

    if not data or not data.get("title") or not data.get("content"):
        return jsonify({"error": "Missing fields"}), 400

    new_notice = Notice(
        title=data["title"],
        content=data["content"],
        category=data.get("category", "General")
    )

    db.session.add(new_notice)
    db.session.commit()

    return jsonify({"message": "Notice added successfully!"})


@app.route('/delete_notice/<int:id>', methods=['DELETE'])
def delete_notice(id):
    """Delete a notice by ID"""
    notice = Notice.query.get(id)
    if not notice:
        return jsonify({"error": "Notice not found"}), 404

    db.session.delete(notice)
    db.session.commit()

    return jsonify({"message": "Notice deleted"})


# ---------- MAIN ----------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
