from flask import Flask, render_template
import subprocess
import datetime
import pytz
import os
import getpass

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Flask app. Visit /htop for system information."

@app.route('/htop')
def htop():
    # Get full name (replace with your actual full name)
    name = "Arvind Sahni"  # IMPORTANT: Replace with your actual full name
    
    # Get system username
    username = getpass.getuser()
    
    # Get server time in IST
    ist = pytz.timezone('Asia/Kolkata')
    server_time = datetime.datetime.now(ist).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    
    # Get top output
    try:
        top_output = subprocess.check_output(
            ['top', '-bn1'], 
            text=True
        )
    except Exception as e:
        top_output = f"Error getting top output: {str(e)}"
    
    return render_template('htop.html', 
                          name=name, 
                          username=username, 
                          server_time=server_time, 
                          top_output=top_output)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)