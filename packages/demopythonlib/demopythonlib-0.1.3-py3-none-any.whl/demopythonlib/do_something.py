

class Calculator:
    def __init__(self):
        """Just a simple example, no thread-safe
        """
        self.result = 0

    def add(self, number):
        self.result += number
        return self

    def sub(self, number):
        self.result -= number
        return self

    def mul(self, number):
        self.result *= number

    def div(self, number):
        self.result /= number
        return self

    def get_result(self):
        return self.result