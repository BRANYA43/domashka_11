"""
Описати клас Банківсткий рахунокб атрибути якого:
- ім'я олікового запису - str
- унікальний id - uuid
- баланс - float or Decimal
Методи
    депозит коштів
    виведення коштів
    отримання балансу
"""

from decimal import Decimal
from uuid import uuid1
from datetime import datetime
from random import randint


class Transaction:
    def __init__(self, amount: Decimal, _type: str):
        self.amount = amount
        self.type = _type
        self.date = datetime.now().strftime('%d.%m.%Y')

    def print_info(self, index):
        print(f'    {index}. Гроші: {self.amount}, Операція: {self.type}, Дата: {self.date}')


class BankAccount:
    def __init__(self, name: str):
        self._name = name
        self._id = uuid1()
        self._balance = Decimal(0.00)
        self._transactions = []

    def calculate_balance(self, transaction):
        operations = {
            'Deposit': self._balance + transaction.amount,
            'Withdrawal': self._balance - transaction.amount
        }
        self._balance = operations[transaction.type]

    def deposit(self, amount: int | float):
        self._transactions.append(Transaction(Decimal(amount), 'Deposit'))
        self.calculate_balance(self._transactions[-1])

    def withdrawal(self, amount: int | float):
        self._transactions.append(Transaction(Decimal(amount), 'Withdrawal'))
        self.calculate_balance(self._transactions[-1])

    @property
    def balance(self):
        return self._balance

    def print_info(self):
        print(f'Ім\'я: {self._name}\n'
               f'ІД: {self._id}\n'
               f'Баланс: {self._balance}\n'
               f'Список транзакцій:')

        for index, transaction in enumerate(self._transactions):
            transaction.print_info(index)
        print('*' * 20)


def main():
    bogdan = BankAccount('Bogdan')
    bogdan.print_info()
    for i in range(randint(10, 50)):
        t_triger = randint(0, 1)
        if t_triger == 0:
            bogdan.deposit(randint(10, 1000))
        else:
            bogdan.withdrawal(randint(10, 1000))
    bogdan.print_info()
    for i in range(randint(10, 50)):
        t_triger = randint(0, 1)
        if t_triger == 0:
            bogdan.deposit(randint(10, 1000))
        else:
            bogdan.withdrawal(randint(10, 1000))
    bogdan.print_info()


if __name__ == '__main__':
    main()
