import os
import threading
from flask import Flask
import bot  # yuxarıdakı bot.py faylı

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Bot is running on Render!"

if __name__ == "__main__":
    # Botu ayrı thread-də işə salırıq
    threading.Thread(target=bot.main).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
