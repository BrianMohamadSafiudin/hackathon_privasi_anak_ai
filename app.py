from flask import Flask, request, jsonify
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

app = Flask(__name__)
endpoint = "https://<AZURE_TEXT_ANALYTICS_ENDPOINT>.cognitiveservices.azure.com/"
key = "<AZURE_TEXT_ANALYTICS_KEY>"
credential = AzureKeyCredential(key)
text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=credential)

def detect_unsafe_content(text):
    try:
        response = text_analytics_client.analyze_sentiment(documents=[text])[0]
        if response.sentiment == "negative":
            return True
        else:
            return False
    except Exception as err:
        print("Error:", err)
        return False

@app.route('/')
def home():
    return send_from_directory('/home/brianmohamads/mysite', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '')
    unsafe = detect_unsafe_content(user_input)
    if unsafe:
        reply = "Hati-hati! Pesan ini mengandung konten yang mungkin tidak aman. Yuk kita bicara hal lain yang menyenangkan!"
    else:
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
    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(debug=True)
