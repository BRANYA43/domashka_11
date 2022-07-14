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
    """Клас транзакцій"""
    COMMISION = '0.01'

    def __init__(self, amount: Decimal, _type: str, status='Settled'):
        """Ініціалізює кількість коштів, тип, статут, комісію за операцію та дату."""
        self.amount = round(amount, 2)
        self.type = _type
        self.status = status
        self.commission_calculated = round(amount * Decimal(self.COMMISION), 2)
        self.dt = datetime.now()

    def print_info(self, index):
        """Видає інформацію у консоль об транзакції. Номер, дату, статус, тип, кошти, комісію."""
        print(f'    {index}. {self.dt.strftime("%d.%m.%Y %H:%M:%S")}\n'
              f'        Status: {self.status}, Type: {self.type}\n'
              f'        Sum: {self.amount}, Commission: {self.commission_calculated}')
        if self.status == 'Failed':
            print('        !!!Insufficient funds for transaction!!!')


class BankAccount:
    """Клас банківського рахунку"""

    def __init__(self, name: str):
        """Ініціалізює ім'я, ід, рахунок та список транзакцій."""
        self._name = name
        self._id = uuid1()
        self._balance = Decimal(0)
        self._transactions = []

    def calculate_balance(self, transaction):
        """Розраховує кошти залежно від типу транзакції та враховує комісію.
        При поповненні рахунку комісія знімаеться з коштів що додаються до разунку.
        При виведенні коштів комісія знімаеться с рахунку користувача."""
        operations = {
            'Deposit': self._balance + transaction.amount - transaction.commission_calculated,
            'Withdrawal': self._balance - transaction.amount + transaction.commission_calculated
        }
        self._balance = operations[transaction.type]

    def deposit(self, amount: str):
        """Поповнює кошти на рахунок ствоюючи об'єкт транзакцій та зберігає у список транзакці зі статусом Settled."""
        self._transactions.append(Transaction(Decimal(amount), 'Deposit'))
        self.calculate_balance(self._transactions[-1])

    def withdrawal(self, amount: str):
        """Виводить кошти з рахунку ствоюючи об'єкт транзакцій та зберігає у список транзакцій зі статусом Settled.
        Також перевіряє чи можливо зняти грощі, якщо ні то додає цю транзакію у список зі статусом Failed."""
        if self._balance - Decimal(amount) * Decimal(Transaction.COMMISION + '1') < 0:
            self._transactions.append(Transaction(Decimal(amount), 'Withdrawal', 'Failed'))
        else:
            self._transactions.append(Transaction(Decimal(amount), 'Withdrawal'))
            self.calculate_balance(self._transactions[-1])

    @property
    def balance(self):
        """Повертає рахунок користувача"""
        return self._balance

    def print_info(self):
        """Видає інформацію об користувачі. Його ім'я, ід, рахунок та список останіх 10-ти транзакцій."""
        print(f'Name: {self._name}\n'
              f'ID: {self._id}\n'
              f'Balance: {self._balance}\n'
              f'List transaction:')

        for index, transaction in enumerate(self._transactions[:-10:-1]):
            transaction.print_info(len(self._transactions) - index)
        print('*' * 20)


def main():
    bogdan = BankAccount('Bogdan')
    bogdan.print_info()
    bogdan.deposit('890.134215')
    bogdan.withdrawal('277.456579')
    bogdan.withdrawal('10000')
    bogdan.print_info()


if __name__ == '__main__':
    main()
