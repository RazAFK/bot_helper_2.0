def funk(n):
    for i in range(n):
        yield i

print(list(funk(4)))