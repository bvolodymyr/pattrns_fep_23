
from cryptography.fernet import Fernet

class CreditCard:
    def __init__(self, client: str, account_number: str, credit_limit: float, grace_period: int, cvv: str, encryption_key: bytes):
        self.client = client
        self.account_number = account_number
        self.credit_limit = credit_limit
        self.grace_period = grace_period
        self.encryption_key = encryption_key
        self._cvv = self.encrypt(cvv, encryption_key)

    @property
    def cvv(self):
        return self.decrypt(self._cvv, self.encryption_key)

    @cvv.setter
    def cvv(self, value):
        self._cvv = self.encrypt(value, self.encryption_key)

    def give_details(self) -> dict:
        return {
            "client": self.client,
            "account_number": self.account_number,
            "credit_limit": self.credit_limit,
            "grace_period": self.grace_period,
            "cvv": self.cvv,
        }

    def encrypt(self, value: str, encryption_key: bytes) -> bytes:
        cipher = Fernet(encryption_key)
        encrypted_value = cipher.encrypt(value.encode())
        return encrypted_value

    def decrypt(self, encrypted_value: bytes, encryption_key: bytes) -> str:
        cipher = Fernet(encryption_key)
        decrypted_value = cipher.decrypt(encrypted_value)
        return decrypted_value.decode()

class GoldenCreditCardDecorator(CreditCard):
    def give_details(self) -> dict:
        details = super().give_details()
        details['card_type'] = 'Golden'
        return details

class CorporateCreditCardDecorator(CreditCard):
    def give_details(self) -> dict:
        details = super().give_details()
        details['card_type'] = 'Corporate'
        return details
