def mutiplier(op1):
    return lambda op2: op1 * op2


three_mul = mutiplier(3)

print(three_mul(2))
print(mutiplier(5)(3))

