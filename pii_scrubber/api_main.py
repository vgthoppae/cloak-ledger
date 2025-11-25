from flask import Flask, jsonify, request
import os
from mcp.server.fastmcp import FastMCP

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = './uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

# Initialize MCP server
mcp = FastMCP("PII Scrubber MCP Server")

@app.route('/')
def hello_world():
    return jsonify({"message": "Hello World"})

@app.route('/api/greet/<name>')
def greet(name):
    return jsonify({"message": f"Hello {name}!"})

@app.route('/pii/scrub', methods=['POST'])
def do_pii_scrub():
    # Check if file is in request
    if 'file' not in request.files:
        return jsonify({"error": "No file part in request"}), 400

    file = request.files['file']

    # Check if file is selected
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    if file:
        # Save the file
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        return jsonify({
            "message": "File uploaded successfully",
            "filename": filename,
            "size": os.path.getsize(filepath)
        }), 200

# MCP Tools (using same logic functions)
@mcp.tool()
def say_hello() -> dict:
    """Returns a hello world greeting"""
    return {"message": "Hello World"}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)