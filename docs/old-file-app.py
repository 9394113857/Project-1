import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import date
import socket
import webbrowser
import time

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
for filename in os.listdir(logs_dir):  # Iterate through all files in the logs directory
    if filename.endswith('.log'):  # Check if it's a log file
        filepath = os.path.join(logs_dir, filename)
        if filepath != log_file:  # Skip today's log file
            os.remove(filepath)  # Remove old log files

# Flask app setup
app = Flask(__name__)

# Create database and table
conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    userid TEXT,
    passid TEXT,
    username TEXT,
    address TEXT,
    country TEXT,
    zip TEXT,
    email TEXT,
    sex TEXT,
    language TEXT,
    desc TEXT
)''')  # Create users table if it doesn't exist
conn.commit()
conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':  # When the form is submitted
        try:
            # Collect data from the form
            data = (
                request.form['userid'],
                request.form['passid'],
                request.form['username'],
                request.form['address'],
                request.form['country'],
                request.form['zip'],
                request.form['email'],
                request.form['sex'],
                ', '.join(request.form.getlist('language')),  # Join selected languages into a string
                request.form['desc']
            )
            conn = sqlite3.connect('users.db')  # Connect to the database
            c = conn.cursor()
            c.execute('''INSERT INTO users (userid, passid, username, address, country, zip, email, sex, language, desc)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', data)  # Insert data into the database
            conn.commit()
            conn.close()

            logger.info(f"New user submitted: {request.form['username']} ({request.form['email']})")  # Log new user submission
            return redirect(url_for('thank_you', from_page='submit'))  # Redirect to thank you page
        except Exception as e:
            logger.error(f"Error submitting user: {e}")  # Log error if something goes wrong
            return "An error occurred. Please try again later."  # Return error message to user
    return render_template('index.html')  # Render index.html when it's a GET request

@app.route('/thank_you')
def thank_you():
    from_page = request.args.get('from_page', '')  # Get the 'from_page' parameter to determine where we came from
    try:
        conn = sqlite3.connect('users.db')  # Connect to the database
        c = conn.cursor()
        c.execute('SELECT * FROM users')  # Fetch all user data from the database
        data = c.fetchall()
        conn.close()
        logger.info("User list retrieved for thank you page")  # Log user list retrieval
        return render_template('thank_you.html', data=data, from_page=from_page)  # Render thank_you.html with data
    except Exception as e:
        logger.error(f"Error retrieving users for thank you page: {e}")  # Log error if something goes wrong
        return "An error occurred. Please try again later."  # Return error message to user

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = sqlite3.connect('users.db')  # Connect to the database
    c = conn.cursor()
    if request.method == 'POST':  # If the form is submitted
        try:
            # Collect data from the form for editing
            data = (
                request.form['userid'],
                request.form['passid'],
                request.form['username'],
                request.form['address'],
                request.form['country'],
                request.form['zip'],
                request.form['email'],
                request.form['sex'],
                ', '.join(request.form.getlist('language')),  # Join selected languages into a string
                request.form['desc'],
                id  # Include the user ID to update the correct record
            )
            c.execute('''UPDATE users SET userid=?, passid=?, username=?, address=?, country=?, zip=?, email=?, sex=?, language=?, desc=? WHERE id=?''', data)  # Update user in the database
            conn.commit()
            conn.close()
            logger.info(f"User {id} updated: {request.form['username']}")  # Log the user update
            return redirect(url_for('thank_you', from_page='view'))  # Redirect to the thank you page
        except Exception as e:
            logger.error(f"Error updating user {id}: {e}")  # Log error if something goes wrong
            return "An error occurred. Please try again later."  # Return error message to user
    c.execute('SELECT * FROM users WHERE id=?', (id,))  # Fetch user data by ID for editing
    user = c.fetchone()
    conn.close()
    return render_template('edit.html', user=user)  # Render edit.html with the user's data

@app.route('/delete/<int:id>')
def delete(id):
    try:
        conn = sqlite3.connect('users.db')  # Connect to the database
        c = conn.cursor()
        c.execute('DELETE FROM users WHERE id=?', (id,))  # Delete the user with the given ID
        conn.commit()
        conn.close()
        logger.info(f"User {id} deleted")  # Log user deletion
        return redirect(url_for('thank_you', from_page='view'))  # Redirect to the thank you page
    except Exception as e:
        logger.error(f"Error deleting user {id}: {e}")  # Log error if something goes wrong
        return "An error occurred. Please try again later."  # Return error message to user

def is_port_open(port):
    """ Check if the given port is available (not in use). """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(('0.0.0.0', port))
        s.close()
        return True
    except socket.error:
        return False

if __name__ == '__main__':
    # Default port to check is 5000
    default_port = 5000
    port = input(f"Enter port (default is {default_port}): ") or default_port
    
    try:
        port = int(port)
        # First, check if the default port is available, even if the user has specified another port.
        if not is_port_open(default_port):
            print(f"Port {default_port} is already in use.")
            logger.error(f"Port {default_port} is already in use.")  # Log the error for default port
            # If the default port is in use, check user-provided port or offer the user a chance to choose a new one
            if is_port_open(port):
                app.run(host='0.0.0.0', port=port, debug=True)  # Run the app with the user-specified port
                logger.info(f"App running on port {port}")  # Log that the app is running
                time.sleep(2)  # Give Flask some time to start the server
                webbrowser.open(f'http://localhost:{port}')  # Open the browser automatically
            else:
                print(f"Port {port} is also unavailable. Please choose another port.")
                logger.error(f"Port {port} is unavailable.")  # Log the error for the provided port
        else:
            app.run(host='0.0.0.0', port=default_port, debug=True)  # Run the app with the default port
            logger.info(f"App running on port {default_port}")  # Log that the app is running
            time.sleep(2)  # Give Flask some time to start the server
            webbrowser.open(f'http://localhost:{default_port}')  # Open the browser automatically
            
    except ValueError:
        print("Invalid port number. Please provide a valid number.")
        logger.error("Invalid port number entered.")  # Log the error
    except Exception as e:
        print(f"Error: {e}")
        logger.error(f"Unexpected error: {e}")  # Log any other unexpected errors
