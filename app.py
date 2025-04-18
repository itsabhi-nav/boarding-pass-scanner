import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/extract-boarding-pass', methods=['POST'])
def extract_boarding_pass():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image_bytes = request.files['image'].read()

    prompt = """
Extract these fields from the boarding pass image and return exactly this JSON object,
with no markdown or extra text:

{
  "airline_name": "",
  "passenger_name": "",
  "flight_no": "",
  "pnr": "",
  "seat": "",
  "boarding_time": "",
  "gate": "",
  "departure_airport": "",
  "arrival_airport": ""
}
    """.strip()

    try:
        response = model.generate_content([
            prompt,
            {"mime_type": "image/jpeg", "data": image_bytes}
        ])
        return jsonify({"data": response.text.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
