"""WhatsApp Business API client."""

import os
from typing import Dict, Optional

import requests


class WhatsAppClient:
    """Client for WhatsApp Business API integration.

    Handles message sending and webhook parsing for WhatsApp Business API.

    Attributes:
        phone_number_id: WhatsApp Business phone number ID.
        access_token: WhatsApp Business API access token.
        verify_token: Token for webhook verification.
        api_url: WhatsApp Business API endpoint URL.
    """

    def __init__(self) -> None:
        """Initialize WhatsApp client with environment variables."""
        self.phone_number_id: str = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")
        self.access_token: str = os.getenv("WHATSAPP_ACCESS_TOKEN", "")
        self.verify_token: str = os.getenv("WHATSAPP_VERIFY_TOKEN", "")
        self.api_url: str = (
            f"https://graph.facebook.com/v18.0/{self.phone_number_id}/messages"
        )

    def send_message(self, phone: str, message: str) -> bool:
        """Send text message via WhatsApp Business API.

        Args:
            phone: Recipient phone number in international format.
            message: Text message to send.

        Returns:
            True if message sent successfully, False otherwise.
        """
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

    def parse_webhook(self, data: dict) -> Optional[Dict[str, str]]:
        """Parse incoming webhook data from WhatsApp.

        Args:
            data: Webhook payload from WhatsApp Business API.

        Returns:
            Dictionary with phone, message, and message_id if valid, None otherwise.
        """
        try:
            entry = data.get("entry", [{}])[0]
            changes = entry.get("changes", [{}])[0]
            value = changes.get("value", {})
            messages = value.get("messages", [])
            if not messages:
                return None
            msg = messages[0]
            return {
                "phone": msg.get("from", ""),
                "message": msg.get("text", {}).get("body", ""),
                "message_id": msg.get("id", ""),
            }
        except Exception as e:
            print(f"Error parsing webhook: {e}")
            return None
