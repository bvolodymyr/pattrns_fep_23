
class BankInfo:
    def __init__(self, bank_name: str, holder_name: str, accounts_number: list, credit_history: dict):
        self.bank_name = bank_name
        self.holder_name = holder_name
        self.accounts_number = accounts_number
        self.credit_history = credit_history

    def add_account(self, credit_card):
        account_details = credit_card.give_details()
        self.accounts_number.append(account_details['account_number'])
        self.credit_history[account_details['account_number']] = {
            'credit_limit': account_details['credit_limit'],
            'grace_period': account_details['grace_period']
        }
