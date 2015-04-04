from util import log2


def calc_gain(lNums, p_iSum=None):
    if p_iSum is None: p_iSum = sum(lNums)
    fSum = float(p_iSum)
    fResult = 0
    for num in lNums:
        value = (num / fSum)
        fResult += -value * log2(value)
    return fResult