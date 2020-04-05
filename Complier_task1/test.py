def isSame(nstate1, nstates):
    tmp1 = nstate1.copy()
    tmp2 = nstates.copy()
    for item in nstate1:
        if item in nstates:
            tmp1.remove(item)
            tmp2.remove(item)
    print(tmp1)
    print(tmp2)
    if len(tmp1) == 0:
        print('yes')
    if tmp1 is None and tmp2 is None:
        return True
    else:
        return False

if __name__ == '__main__':
    n1 = []
    if n1 is not None:
        print('yes')