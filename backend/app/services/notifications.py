import requests
import os

class TelegramSOC:
    def __init__(self, bot_token=None, chat_id=None):
        """
        To activate:
        1. Create a bot via @BotFather on Telegram.
        2. Get your Chat ID via @userinfobot.
        """
        self.bot_token = bot_token or os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = chat_id or os.getenv("TELEGRAM_CHAT_ID")
        self.is_active = self.bot_token is not None and self.chat_id is not None

    def send_alert(self, alert_data):
        """Sends a high-priority SOC alert to your Telegram."""
        if not self.is_active: return

        emoji = "🚨" if alert_data.get('risk_score', 0) > 8 else "⚠️"
        message = (
            f"{emoji} *IDS SOC ALERT: CRITICAL THREAT DETECTED*\n\n"
            f"*Timestamp:* `{alert_data['timestamp']}`\n"
            f"*Source IP:* `{alert_data['src_ip']}`\n"
            f"*Vector:* `{alert_data['attack_type']}`\n"
            f"*Risk Score:* `{alert_data['risk_score']}/10`\n"
            f"*Location:* `{alert_data.get('geo', {}).get('country', 'Unknown')}`\n\n"
            f"🛡️ _Action: Remote block suggested._"
        )
        
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            payload = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "Markdown"
            }
            requests.post(url, json=payload, timeout=5)
        except Exception as e:
            print(f"[!] Telegram Alert Failed: {e}")

    def update_credentials(self, token, chat_id):
        self.bot_token = token
        self.chat_id = chat_id
        self.is_active = True
        print("[*] Telegram SOC Bot Activated.")
