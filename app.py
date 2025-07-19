from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
import openai
import os
from zipfile import ZipFile

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate_website():
    prompt = request.json.get("prompt")
    if not prompt:
        return jsonify({"error": "Prompt is required."}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional web developer who builds SEO-optimized websites using HTML, CSS, and best practices."},
                {"role": "user", "content": f"Create a responsive, SEO-optimized, modern website based on this prompt: {prompt}. Include meta tags, schema markup, and mobile-first layout."}
            ],
            temperature=0.7,
            max_tokens=3000
        )

        html_code = response.choices[0].message.content

        with open("website/index.html", "w", encoding="utf-8") as f:
            f.write(html_code)

        zip_path = "website.zip"
        with ZipFile(zip_path, 'w') as zipf:
            zipf.write("website/index.html", arcname="index.html")

        return send_file(zip_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    if not os.path.exists("website"):
        os.makedirs("website")
    app.run(host="0.0.0.0", port=10000)
