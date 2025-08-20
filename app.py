from flask import Flask, render_template, request, jsonify
from google.cloud import vision
import os

app = Flask(__name__)

# Google Vision kimlik dosyası: ORTAM DEĞİŞKENİNDEN okunur.
# Örn (terminal): export GOOGLE_APPLICATION_CREDENTIALS="your-key.json"
credential_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if not credential_path or not os.path.exists(credential_path):
    raise RuntimeError(
        "Google Vision API key bulunamadı. "
        "Lütfen terminalde: export GOOGLE_APPLICATION_CREDENTIALS=\"your-key.json\" ayarla."
    )

# Vision istemcisi
client = vision.ImageAnnotatorClient()

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_image():
    if "image" not in request.files:
        return jsonify({"error": "Dosya gönderilemedi"}), 400

    image_file = request.files["image"]
    content = image_file.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    if response.error.message:
        # API'den hata dönerse kontrol
        return jsonify({"error": f"Vision API hata: {response.error.message}"}), 500

    texts = response.text_annotations
    detected_text = texts[0].description if texts else "Metin algılanamadı."

    return jsonify({"text": detected_text})

if __name__ == "__main__":
    # Geliştirme aşamasında debug=True; prod'da kapat.
    app.run(host="0.0.0.0", port=5000, debug=True)
