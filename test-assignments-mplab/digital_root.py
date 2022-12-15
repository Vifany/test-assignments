'''
Fix code:
def digital_root(n):
    return if n < 10 n else digital_root(summ(map(int,str(n))))
'''
def digital_root(n):
    return n if n <10 else digital_root(sum(map(int, str(n))))