'''
Fix code:
count_bits = lambda: bin(n).count('1')
'''


count_bits = lambda n: len(bin(n)[2:])

print((count_bits(9), bin(9)))