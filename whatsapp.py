"""WhatsApp Business API integration."""

import os
import requests
from typing import Optional


class WhatsAppClient:
    """WhatsApp Business API client."""

    def __init__(self):
        """Initialize WhatsApp client with credentials from environment."""
        self.phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
        self.access_token = os.getenv("WHATSAPP_ACCESS_TOKEN")
        self.verify_token = os.getenv("WHATSAPP_VERIFY_TOKEN")
        self.api_url = f"https://graph.instagram.com/v18.0/{self.phone_number_id}/messages"

    def send_message(self, phone: str, message: str) -> bool:
        """Send text message via WhatsApp."""
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "messaging_product": "whatsapp",
            "to": phone,
            "type": "text",
            "text": {"body": message},
        }
        
        try:
            response = requests.post(self.api_url, json=payload, headers=headers)
            return response.status_code == 200
        except Exception as e:
            print(f"Error sending WhatsApp message: {e}")
            return False

    def parse_webhook(self, data: dict) -> Optional[dict]:
        """Parse incoming webhook message from WhatsApp."""
        try:
            entry = data.get("entry", [{}])[0]
            changes = entry.get("changes", [{}])[0]
            value = changes.get("value", {})
            messages = value.get("messages", [])
            
            if not messages:
                return None
            
            msg = messages[0]
            return {
                "phone": msg.get("from"),
                "message": msg.get("text", {}).get("body", ""),
                "message_id": msg.get("id"),
            }
        except Exception as e:
            print(f"Error parsing webhook: {e}")
            return None
