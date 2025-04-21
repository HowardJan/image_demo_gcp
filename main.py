import os
from dotenv import load_dotenv
load_dotenv()

import openai
from flask import Flask, request, render_template
from google.cloud import storage
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

BUCKET_NAME = os.environ.get('GCS_BUCKET')
openai.api_key = os.environ.get("OPENAI_API_KEY")

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def upload_to_gcs(local_file_path, dest_blob_name):
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(dest_blob_name)
    blob.upload_from_filename(local_file_path)
    blob.make_public()
    return blob.public_url

def analyze_image_with_openai(image_url):
    prompt = f"請分析這張圖片的內容：{image_url}"
    response = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",
        messages=[
            {"role": "user", "content": [{"type": "text", "text": prompt},
                                         {"type": "image_url", "image_url": {"url": image_url}}]}
        ],
        max_tokens=1000
    )
    return response.choices[0].message.content

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if 'file' not in request.files:
            return "No file part"
        file = request.files['file']
        if file.filename == '':
            return "No selected file"
        filename = secure_filename(file.filename)
        local_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(local_path)

        gcs_url = upload_to_gcs(local_path, filename)
        result = analyze_image_with_openai(gcs_url)
        return render_template("upload.html", result=result, image_url=gcs_url)

    return render_template("upload.html")