from flask import Flask, request, jsonify
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

app = Flask(__name__)

# Konfigurasi Azure Text Analytics
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

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '')
    unsafe = detect_unsafe_content(user_input)
    if unsafe:
        reply = "Hati-hati! Pesan ini mengandung konten yang mungkin tidak aman. Yuk kita bicara hal lain yang menyenangkan!"
    else:
        if "privasi" in user_input.lower():
            reply = "Privasi berarti menjaga data dan informasi pribadimu agar tidak disalahgunakan orang lain."
        else:
            reply = "Halo! Aku di sini untuk membantumu belajar tentang keamanan di dunia digital. Apa yang ingin kamu tahu?"
    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(debug=True)
