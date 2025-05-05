import os
import logging
from datetime import date
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Flask setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking
db = SQLAlchemy(app)  # Initialize the SQLAlchemy object for database interaction

# Setup logger
logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')  # Directory for logs
os.makedirs(logs_dir, exist_ok=True)  # Create logs directory if not exists
log_file = os.path.join(logs_dir, f'{date.today()}.log')  # Log file with today's date

# Rotating file handler for logging
log_handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024, backupCount=5)  # Rotate logs after 1MB, keep 5 backups
log_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s [%(module)s:%(lineno)d] %(message)s'))  # Log format

logger = logging.getLogger(__name__)  # Get the logger
logger.setLevel(logging.INFO)  # Set logging level to INFO
logger.addHandler(log_handler)  # Add the rotating log handler to the logger

# Clean up older logs except today's
for filename in os.listdir(logs_dir):
    if filename.endswith('.log'):
        filepath = os.path.join(logs_dir, filename)
        if filepath != log_file:  # Skip today's log file
            os.remove(filepath)  # Remove old log files

# User model for the database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Auto-incrementing primary key
    userid = db.Column(db.String(100))  # User ID
    passid = db.Column(db.String(100))  # Password
    username = db.Column(db.String(100))  # User's full name
    address = db.Column(db.String(200))  # Address
    country = db.Column(db.String(100))  # Country
    zip = db.Column(db.String(20))  # Zip code
    email = db.Column(db.String(100))  # Email address
    sex = db.Column(db.String(10))  # Gender (Male/Female)
    language = db.Column(db.String(100))  # Preferred language
    desc = db.Column(db.Text)  # Description

# Route for the index page
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            # Get data from the form and create a new User object
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
            db.session.add(new_user)  # Add new user to the session
            db.session.commit()  # Commit the session to save the data in the database
            logger.info(f"New user submitted: {new_user.username} ({new_user.email})")  # Log the action
            return redirect(url_for('thank_you', from_page='submit'))  # Redirect to the thank-you page

        except Exception as e:
            db.session.rollback()  # Rollback in case of an error
            logger.error(f"Error saving user data: {e}", exc_info=True)  # Log the error
            return f"Error saving data: {e}"  # Return error message
    
    # Check if there is any existing user data in the database
    has_data = User.query.count() > 0
    logger.info("Index page accessed. Existing data present: %s", has_data)  # Log page access and data status
    return render_template("index.html", has_data=has_data)  # Render the index page

# Route for the thank-you page
@app.route("/thankyou")
def thank_you():
    from_page = request.args.get("from_page", "view")  # Get the source page for redirection
    users = User.query.all()  # Get all user records from the database
    users_with_index = [(idx + 1, user) for idx, user in enumerate(users)]  # Add an index to each user
    logger.info("Thank You page accessed. Source: %s | Total records: %d", from_page, len(users))  # Log the page access
    return render_template("thank_you.html", data=users_with_index, from_page=from_page)  # Render the thank-you page

# Run the application
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create the database tables if they don't exist
        logger.info("Database tables created.")  # Log the creation of tables
    logger.info("Starting Flask application...")  # Log the start of the application
    app.run(debug=True)  # Start the Flask application in debug mode
