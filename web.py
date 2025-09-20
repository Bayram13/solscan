from flask import Flask
import threading
import bot  # sənin bot kodun (bot.py içindədir)

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running on Render!"

def run_bot():
    bot.main()  # bot.py içində main funksiyan varsa onu çağır

if __name__ == "__main__":
    # Botu ayrı thread-də işə salırıq
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
