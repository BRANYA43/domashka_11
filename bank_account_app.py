"""
Описати клас "Банківський рахунок", атрибути якого:

   - ім'я облікового запису - str
   - унікальний id (uuid)
   - баланс float (чи Decimal)
   - транзакції (список)
   Методи

     депозит коштів
     виведення коштів
     отримати баланс


   При зміні балансу записувати в транзакції (сума, тип операції, поточна_дата)

   * Дод. додати та враховувати банківські комісії (1%)
"""
from decimal import Decimal
from uuid import uuid1
from datetime import datetime


class Transaction:
    def __init__(self, amount: Decimal, _type: str, status='Settled'):
        self.amount = amount
        self.type = _type
        self.status = status
        self.commission = round(amount * Decimal(0.01), 2)
        self.dt = datetime.now()

    def print_info(self, index):
        print(f'    {index}. {self.dt.strftime("%d.%m.%Y %H:%M:%S")}\n'
              f'        Status: {self.status}, Type: {self.type}\n'
              f'        Sum: {self.amount}, Commission: {self.commission}')
        if self.status == 'Failed':
            print('        !!!Insufficient funds for transaction!!!')



class BankAccount:
    def __init__(self, name: str):
        self._name = name
        self._id = uuid1()
        self._balance = Decimal(0)
        self._transactions = []

    def calculate_balance(self, transaction):
        operations = {
            'Deposit': self._balance + transaction.amount - transaction.commission,
            'Withdrawal': self._balance - transaction.amount + transaction.commission
        }
        self._balance = operations[transaction.type]

    def deposit(self, amount: int | float):
        self._transactions.append(Transaction(Decimal(str(round(amount, 2))), 'Deposit'))
        self.calculate_balance(self._transactions[-1])

    def withdrawal(self, amount: int | float):
        if self._balance - Decimal(amount) < 0:
            self._transactions.append(
                Transaction(Decimal(str(round(amount, 2))), 'Withdrawal', 'Failed'))
        else:
            self._transactions.append(Transaction(Decimal(str(round(amount, 2))), 'Withdrawal'))
            self.calculate_balance(self._transactions[-1])

    @property
    def balance(self):
        return self._balance

    def print_info(self):
        print(f'Ім\'я: {self._name}\n'
               f'ІД: {self._id}\n'
               f'Баланс: {self._balance}\n'
               f'Список транзакцій:')

        for index, transaction in enumerate(self._transactions[:-10:-1]):
            transaction.print_info(len(self._transactions) - index)
        print('*' * 20)


def main():
    bogdan = BankAccount('Bogdan')
    bogdan.print_info()
    bogdan.deposit(890.134215)
    bogdan.withdrawal(277)
    bogdan.withdrawal(10000)
    bogdan.print_info()


if __name__ == '__main__':
    main()
