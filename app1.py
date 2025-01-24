import os
import subprocess
from flask import Flask, render_template_string

# Limit thread usage for OpenBLAS
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

# Create Flask app
app = Flask(__name__)

# HTML Template to display a simple page
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>HR Candidate Ranking App</title>
</head>
<body>
    <h1>HR Candidate Ranking App</h1>
    <p>The Streamlit app is running in the background.</p>
    <p>If it doesn’t open automatically, <a href="http://127.0.0.1:8501" target="_blank">click here</a>.</p>
</body>
</html>
"""

@app.route("/")
def index():
    """
    Main route to start the Streamlit app and show a basic web page.
    """
    # Command to run the Streamlit app
    streamlit_command = f"streamlit run {os.path.abspath('streamlit_app.py')} --server.port 8501 --server.headless true"
    # Start the Streamlit app as a subprocess
    subprocess.Popen(streamlit_command, shell=True)
    # Return a simple HTML page with a link to the Streamlit app
    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
