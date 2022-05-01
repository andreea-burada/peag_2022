
# 5. GCD(greatest common divisor) recursive algorithm for two unsigned integers
# a = 10
# b = 25


def recursive_gcd(x, y):
    if x == 0 or y == 0:
        return 0
    if x == y:
        return x
    if x > y:
        return recursive_gcd(x - y, y)
    else:
        return recursive_gcd(x, y - x)


def test():
    a = int(input("a = "))
    b = int(input("b = "))
    result = recursive_gcd(a, b)
    print("GCD of ", a, " and ", b, " is: ", result)

# comment lines 19-20 and uncomment 3-4 for a quicker test
