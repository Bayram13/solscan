import os
import requests
import time
from telegram import Bot

# Config
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
SOLSCAN_API_KEY = os.getenv("SOLSCAN_API_KEY")
RPC_URL = os.getenv("RPC_URL", "https://api.mainnet-beta.solana.com")

bot = Bot(token=TELEGRAM_TOKEN)

seen_tokens = {}

def fetch_new_tokens():
    url = "https://public-api.solscan.io/token/list?sortBy=createdAt&direction=desc&limit=10"
    headers = {"token": SOLSCAN_API_KEY}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            return r.json().get("data", [])
    except Exception as e:
        print("Fetch error:", e)
    return []

def check_filters(token):
    top10_share = token.get("top10Share", 100)
    dex_paid = token.get("dexPaid", False)
    dev_tokens = token.get("devTokens", 999)
    socials = token.get("socials", {})

    if top10_share >= 20:
        return False
    if not dex_paid:
        return False
    if dev_tokens >= 10:
        return False
    if not (socials.get("tg") or socials.get("x") or socials.get("web")):
        return False
    return True

def format_message(token):
    msg = f"""{token.get('name')} ({token.get('url')}) | #{token.get('symbol')} | ${token.get('symbol')}
CA: {token.get('ca')}
├ 📊 MC: ${token.get('mc')}
├ 💬 Replies: {token.get('replies')}
├ 👤 DEV:
│        Tokens: {token.get('devTokens')} | KoTH: {token.get('koth')} | Complete: {token.get('complete')}
├ 🌐 Socials: TG ({token.get('socials', {}).get('tg')}) | X ({token.get('socials', {}).get('x')}) | WEB ({token.get('socials', {}).get('web')})
├ 🔊 Volume: ${token.get('volume')}
├ 📈 ATH: ${token.get('ath')}
├ 🧶 Bonding Curve: {token.get('bondingCurve')}%
├ 🔫 Snipers: {token.get('snipers')}
├ 👥 Holders: {token.get('holders')}
├ 👤 Dev hold: {token.get('devHold')}%
└ 🏆 Top 10 Holders: Σ {token.get('top10Share')}% \n{token.get('top10Distribution')}
DEX PAID"""
    return msg

def format_multiplier_message(token, mult, mc):
    ca = token.get("ca")
    symbol = token.get("symbol")
    link = f"https://solscan.io/token/{ca}"
    return f"🚀 {symbol} just hit {mult}x!\nMC: ${mc}\n🔗 {link}"

def process_tokens():
    tokens = fetch_new_tokens()
    for t in tokens:
        ca = t.get("ca")
        if not ca:
            continue

        if not check_filters(t):
            continue

        mc = t.get("mc", 0)

        if ca not in seen_tokens:
            seen_tokens[ca] = {"ath": mc, "next_mult": 2}
            bot.send_message(chat_id=CHAT_ID, text=format_message(t))
        else:
            if mc > seen_tokens[ca]["ath"]:
                seen_tokens[ca]["ath"] = mc

            ath = seen_tokens[ca]["ath"]
            next_mult = seen_tokens[ca]["next_mult"]
            if mc >= (ath * next_mult):
                bot.send_message(chat_id=CHAT_ID, text=format_multiplier_message(t, next_mult, mc))
                seen_tokens[ca]["next_mult"] += 1

# ---------------------------
# Əsas dəyişiklik burada:
# ---------------------------
def main():
    print("Bot started...")
    while True:
        process_tokens()
        time.sleep(30)

if __name__ == "__main__":
    main()
