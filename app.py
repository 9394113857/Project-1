import os
import logging
from datetime import date
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Flask setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Setup logger
logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
os.makedirs(logs_dir, exist_ok=True)
log_file = os.path.join(logs_dir, f'{date.today()}.log')

log_handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024, backupCount=5)
log_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s [%(module)s:%(lineno)d] %(message)s'))

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

# Clean up older logs except today's
for filename in os.listdir(logs_dir):
    if filename.endswith('.log'):
        filepath = os.path.join(logs_dir, filename)
        if filepath != log_file:
            os.remove(filepath)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(100))
    passid = db.Column(db.String(100))
    username = db.Column(db.String(100))
    address = db.Column(db.String(200))
    country = db.Column(db.String(100))
    zip = db.Column(db.String(20))
    email = db.Column(db.String(100))
    sex = db.Column(db.String(10))
    language = db.Column(db.String(100))
    desc = db.Column(db.Text)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            new_user = User(
                userid=request.form.get("userid"),
                passid=request.form.get("passid"),
                username=request.form.get("username"),
                address=request.form.get("address"),
                country=request.form.get("country"),
                zip=request.form.get("zip"),
                email=request.form.get("email"),
                sex=request.form.get("sex"),
                language=request.form.get("language"),
                desc=request.form.get("desc")
            )
            db.session.add(new_user)
            db.session.commit()
            logger.info(f"New user submitted: {new_user.username} ({new_user.email})")
            return redirect(url_for('thank_you', from_page='submit'))

        except Exception as e:
            db.session.rollback()
            logger.error(f"Error saving user data: {e}", exc_info=True)
            return f"Error saving data: {e}"
    
    has_data = User.query.count() > 0
    logger.info("Index page accessed. Existing data present: %s", has_data)
    return render_template("index.html", has_data=has_data)

@app.route("/thankyou")
def thank_you():
    from_page = request.args.get("from_page", "view")
    users = User.query.all()
    users_with_index = [(idx + 1, user) for idx, user in enumerate(users)]
    logger.info("Thank You page accessed. Source: %s | Total records: %d", from_page, len(users))
    return render_template("thank_you.html", data=users_with_index, from_page=from_page)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        logger.info("Database tables created.")
    logger.info("Starting Flask application...")
    app.run(debug=True)
