from flask import Flask, jsonify, request, Response
import os
from pii_scrubber import cloak_logger, pii_driver

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = './uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

clog = cloak_logger.CloakLogger()
clog.configure()

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
    file_bytes = file.read()

    pd = pii_driver.PiiDriver(img_bytes= file_bytes)
    pd.do_ocr()
    pd.plan_redact()
    pd.apply_redact()

    with open("safe.png", "rb") as f:
        safe_image_bytes = f.read()

    # convert to png
    # images_list = pd.convert_to_image()
    print("after ocr")

    return Response(
        safe_image_bytes,
        mimetype="image/png",
        headers={
            "Content-Disposition": "inline; filename=redacted_image.png"
        },
    )
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)