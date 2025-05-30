from flask import Flask, request, jsonify
from flask_cors import CORS 
import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = Flask(__name__)
CORS(app)
nlp = spacy.load("en_core_web_sm")
analyzer = SentimentIntensityAnalyzer()

def analyze_text(text):
    doc = nlp(text)
    entities = [ent.text for ent in doc.ents] 
    sentiment_score = analyzer.polarity_scores(text)
    response = {
        "entities": entities,
        "sentiment": sentiment_score
    }
    if sentiment_score['compound'] <= -0.5:
        response['warning'] = "Konten ini mengandung sentimen negatif atau berbahaya!"    
    return response

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '').lower()
    analysis = analyze_text(user_input)
    if "privasi" in user_input:
        reply = ("Privasi berarti menjaga data pribadi kamu agar tidak disalahgunakan oleh pihak lain. "
                 "Ajarkan anak untuk tidak membagikan informasi pribadi seperti alamat, nomor telepon, atau sekolah secara online.")
    elif "keamanan digital" in user_input or "keamanan anak" in user_input:
        reply = ("Untuk memperkuat keamanan digital anak, gunakan kontrol orang tua (parental control), "
                 "batasi akses aplikasi, dan selalu dampingi mereka saat berselancar di internet.")
    elif "literasi" in user_input or "belajar privasi" in user_input:
        reply = ("Literasi privasi membantu anak memahami risiko berbagi informasi secara online. "
                 "Ajak mereka belajar mengenali tautan atau konten yang mencurigakan dan pentingnya menjaga data pribadi.")
    elif "password" in user_input:
        reply = ("Gunakan password yang kuat dan unik untuk setiap akun, serta ajarkan anak untuk tidak memberitahukan password mereka kepada siapapun, termasuk teman.")
    elif "sosial media" in user_input or "media sosial" in user_input:
        reply = ("Sosial media bisa berisiko jika privasi tidak dijaga. Atur pengaturan privasi akun agar hanya teman dekat yang bisa melihat informasi, "
                 "dan jangan mudah menerima permintaan pertemanan dari orang asing.")
    elif "kontrol orang tua" in user_input or "parental control" in user_input:
        reply = ("Kontrol orang tua membantu memantau dan membatasi konten yang dapat diakses anak, "
                 "sehingga mereka lebih aman saat menggunakan perangkat digital.")
    elif "aplikasi" in user_input:
        reply = ("Sebelum mengizinkan anak menggunakan aplikasi, pastikan aplikasi tersebut aman dan sesuai usia, "
                 "dan periksa izin akses yang diminta aplikasi tersebut.")
    elif "cyberbullying" in user_input:
        reply = ("Cyberbullying adalah perilaku negatif di dunia maya. Ajarkan anak untuk melaporkan jika mengalami atau melihat bullying, "
                 "dan berikan dukungan agar mereka merasa aman.")
    elif "data pribadi" in user_input:
        reply = ("Data pribadi adalah informasi yang harus dilindungi. Jangan sembarangan membagikan data pribadi seperti alamat, nomor telepon, "
                 "atau foto tanpa izin orang tua.")
    else:
        reply = ("Terima kasih sudah bertanya! Jika kamu ingin tahu lebih banyak tentang bagaimana menjaga keamanan digital anak "
                 "atau literasi privasi, silakan tanyakan hal lain ya.")
    return jsonify({"reply": reply, "analysis": analysis})

if __name__ == '__main__':
    app.run(debug=True)
