# 💳 Telegram Stars Payment Bot

Simple Telegram bot to accept payments using **Telegram Stars**.

---

## 🚀 Features

* Admin command `/makelink`
* Enter Stars amount
* Sends payment invoice
* Detects successful payment
* Sends confirmation message

---

## 📦 Setup

### 1. Install dependencies

```
pip install -r requirements.txt
```

### 2. Set environment variables

```
BOT_TOKEN=your_bot_token
ADMIN_ID=your_telegram_id
```

### 3. Run bot

```
python bot.py
```

---

## 🌐 Deploy on Heroku

1. Create app on Heroku
2. Add Config Vars:

   * BOT_TOKEN
   * ADMIN_ID
3. Deploy repo
4. Enable **worker dyno**

---

## 💡 Notes

* Uses Telegram Stars (`XTR`)
* No provider token needed
* Payments handled inside Telegram

---

## 📌 Contact

Telegram: @alex_clb
