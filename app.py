from flask import Flask, request, send_file
from werkzeug.utils import secure_filename
from flask_cors import CORS  # ✅ NEW
import os
import numpy as np
import cv2
from io import BytesIO
from Blur import blur

app = Flask(__name__)
CORS(app)  # ✅ Allow all origins (good for dev; restrict later in prod)

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return 'No file part in request', 400

    file = request.files['image']
    width = int(round(float(request.form["width"])))
    height = int(round(float((request.form["height"]))))
    blur_value = int(round(float(request.form["blur"])))

    if file.filename == '':
        return 'No selected file', 400

    file_byte = file.read()
    np_arr  = np.frombuffer(file_byte, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    resized = cv2.resize(image, (width, height))

    resized = blur(resized, k=blur_value)
    

    success, buffer = cv2.imencode(".jpg", resized)

    if not success :
        return "Image encoding failed", 500

    output = BytesIO(buffer.tobytes())
    output.seek(0)

    return send_file(output, mimetype = "image/jpeg", as_attachment= True, download_name = "resized.jpg")


if __name__ == '__main__':
    port = 5000
    app.run(host='0.0.0.0', port=port,debug=True)
