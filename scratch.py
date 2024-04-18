x = 4
y = 5

class Multiply():
    def multi(self, x, y):
        return x * y

    def combine(self, x, y):
        # Corrected to use self.multi(x, y)
        return "The product of " + str(x) + " and " + str(y) + " is: " + str(self.multi(x, y))

    def run(self, x, y):
        count = 0
        while count < 10:
            print(self.multi(x, y))
            print(self.combine(x, y))
            print()
            count += 1

        for i in range(10):
            print(self.multi(x, y))
            print(self.combine(x, y))
            print()

m = Multiply()
m.run(x, y)