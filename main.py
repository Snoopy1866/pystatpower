class TestFloat(float):
    def __new__(cls, value):
        return super().__new__(cls, value)


a = TestFloat(1.0)
b = TestFloat(2.0)
print(a)
print(b)

c = TestFloat(a)

print(c)

float.__new__()
