import webbrowser
from urllib.parse import quote
from src.logger import log_info

class WhatsAppClient:
    def __init__(self):
        self.base_url = "https://web.whatsapp.com/send"
    
    def send_message(self, phone, message):
        """
        Opens WhatsApp Web with pre-filled message.
        Phone format should be international (e.g., 50688888888).
        """
        if not phone: return False
        
        # Clean phone
        clean_phone = ''.join(filter(str.isdigit, str(phone)))
        
        encoded_msg = quote(message)
        url = f"{self.base_url}?phone={clean_phone}&text={encoded_msg}"
        
        try:
            log_info(f"Opening WhatsApp for {clean_phone}")
            webbrowser.open(url)
            return True
        except Exception as e:
            log_info(f"Failed to open WhatsApp: {e}")
            return False

    def send_invoice_link(self, phone, invoice_id, public_link="http://mitienda.com/factura/"):
        msg = f"Hola, gracias por su compra. Su factura #{invoice_id} está disponible aquí: {public_link}{invoice_id}"
        return self.send_message(phone, msg)
