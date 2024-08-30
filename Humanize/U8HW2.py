class Fraction:
    def __init__(self, numerator, denominator):
        self.numerator = numerator
        self.denominator = denominator

    def __str__(self):
        return f"{self.numerator}/{self.denominator}"

    def __eq__(self, other):
        return self.numerator * other.denominator == self.denominator * other.numerator

    def times(self, other):
        return Fraction(self.numerator * other.numerator, self.denominator * other.denominator)

    def divide(self, other):
        return Fraction(self.numerator * other.denominator, self.denominator * other.numerator)

    def add(self, other):
        new_numerator = self.numerator * other.denominator + other.numerator * self.denominator
        new_denominator = self.denominator * other.denominator
        return Fraction(new_numerator, new_denominator)

    def subtract(self, other):
        new_numerator = self.numerator * other.denominator - other.numerator * self.denominator
        new_denominator = self.denominator * other.denominator
        return Fraction(new_numerator, new_denominator)

# Test cases
f1 = Fraction(1, 5)
f2 = Fraction(2, 3)
f3 = Fraction(4, 7)
f4 = Fraction(3, 8)

# Addition
try:
    assert(f1.add(f2) == Fraction(13, 15))
    print("Addition test case 1 passed")
    assert(f2.add(f3) == Fraction(38, 21))
    print("Addition test case 2 passed")
    assert(f3.add(f4) == Fraction(65, 56))
    print("Addition test case 3 passed")
except AssertionError:
    print("Assertion Error in addition")

# Subtraction
try:
    assert(f1.subtract(f2) == Fraction(-7, 15))
    print("Subtraction test case 1 passed")
    assert(f2.subtract(f3) == Fraction(2, 21))
    print("Subtraction test case 2 passed")
    assert(f3.subtract(f4) == Fraction(13, 56))
    print("Subtraction test case 3 passed")
except AssertionError:
    print("Assertion Error in subtraction")
