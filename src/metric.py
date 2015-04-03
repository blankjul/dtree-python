from util import log2


def info_gain(lNums):
    fSum = float(sum(lNums))
    fResult = 0
    for num in lNums:
        value = (num / fSum)
        fResult += -value * log2(value)
    return fResult