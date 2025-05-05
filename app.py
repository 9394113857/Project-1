from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

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
            return redirect(url_for('thank_you'))
        except Exception as e:
            db.session.rollback()
            return f"Error saving data: {e}"
    
    # Check if any data exists in DB
    has_data = User.query.count() > 0
    return render_template("index.html", has_data=has_data)

@app.route("/thankyou")
def thank_you():
    users = User.query.all()
    users_with_index = [(idx + 1, user) for idx, user in enumerate(users)]
    return render_template("thank_you.html", data=users_with_index)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
