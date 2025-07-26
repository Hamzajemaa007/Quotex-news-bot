import requests
import time
import datetime
import telebot

# إعدادات البوت
BOT_TOKEN = "8386439594:AAHELXmMC0YleBh-BUaQHB8nz2XS_86-eb0"
CHANNEL_ID = "@Quotex_news"

bot = telebot.TeleBot(BOT_TOKEN)

# جدول الأخبار المهمة (أمثلة فقط)
SCHEDULE = [
    {"time": "13:30", "currency": "USD", "event": "CPI", "date": "2025-07-30"},
    {"time": "15:00", "currency": "USD", "event": "FOMC", "date": "2025-07-30"},
]

def get_today_events():
    today = datetime.date.today().isoformat()
    return [e for e in SCHEDULE if e["date"] == today]

def send_alert(message):
    try:
        bot.send_message(CHANNEL_ID, message)
    except Exception as e:
        print("Error sending message:", e)

def main_loop():
    already_alerted = set()
    while True:
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M")
        today_events = get_today_events()
        
        for event in today_events:
            key_before = f"{event['event']}-before"
            key_after = f"{event['event']}-after"

            # تنبيه قبل دقيقة
            if current_time == event["time"]:
                if key_before not in already_alerted:
                    send_alert(f"🔔 بعد دقيقة: خبر {event['event']} على {event['currency']}\n📈 تابع أول شمعة لتقرر Buy أو Sell")
                    already_alerted.add(key_before)

            # تنبيه بعد دقيقة (افتراضي)
            alert_time = (now - datetime.timedelta(minutes=1)).strftime("%H:%M")
            if alert_time == event["time"] and key_after not in already_alerted:
                send_alert(f"📊 أول شمعة بعد خبر {event['event']} ظهرت، قرر الآن حسب الاتجاه Buy/Sell")
                already_alerted.add(key_after)

        time.sleep(30)

if __name__ == "__main__":
    print("🔄 Bot started...")
    main_loop()
