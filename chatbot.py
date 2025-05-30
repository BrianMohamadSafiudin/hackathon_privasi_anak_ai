from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Inisialisasi Flask dan spaCy
app = Flask(__name__)
CORS(app)  # Mengaktifkan CORS untuk semua route

nlp = spacy.load("en_core_web_sm")  # Model bahasa Inggris untuk spaCy
analyzer = SentimentIntensityAnalyzer()  # Untuk analisis sentimen

# Fungsi untuk analisis entitas dan sentimen
def analyze_text(text):
    doc = nlp(text)
    entities = [ent.text for ent in doc.ents]  # Mengambil entitas (misal: nama, lokasi)
    sentiment_score = analyzer.polarity_scores(text)  # Skor sentimen

    # Menghasilkan respons berdasarkan analisis
    response = {
        "entities": entities,
        "sentiment": sentiment_score
    }

    # Peringatan konten berbahaya berdasarkan skor sentimen
    if sentiment_score['compound'] <= -0.5:
        response['warning'] = "Konten ini mengandung sentimen negatif atau berbahaya!"
    
    return response

# Route untuk chat
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '')
    analysis = analyze_text(user_input)
    
    if "privasi" in user_input.lower():
        reply = "Privasi berarti menjaga data pribadi kamu agar tidak disalahgunakan oleh pihak lain. Jangan berbagi informasi pribadi dengan orang yang tidak dikenal!"
    else:
        reply = "Halo! Aku di sini untuk membantu kamu belajar tentang privasi di dunia digital."

    return jsonify({"reply": reply, "analysis": analysis})

if __name__ == '__main__':
    app.run(debug=True)
