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
    name = "Arvind Sahni" 
    
    try:
        username = getpass.getuser()
    except Exception:
        username = "Unknown"
    
    # Get server time in IST
    try:
        ist = pytz.timezone('Asia/Kolkata')
        server_time = datetime.datetime.now(ist).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    except Exception:
        server_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    
    # Get top output 
    try:
        result = subprocess.run(
            ['top', '-bn1'],
            capture_output=True,
            text=True,
            timeout=5  
        )
        if result.returncode == 0:
            top_output = result.stdout
        else:
            top_output = f"Command failed with error: {result.stderr}"
    except subprocess.TimeoutExpired:
        top_output = "Error: Command timed out after 5 seconds"
    except subprocess.SubprocessError as e:
        top_output = f"Subprocess error: {str(e)}"
    except Exception as e:
        top_output = f"Error getting top output: {str(e)}"
    
    return render_template('htop.html', 
                          name=name, 
                          username=username, 
                          server_time=server_time, 
                          top_output=top_output)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)