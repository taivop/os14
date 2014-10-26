s = "0,10;4,5;12,4"

# INPUT
# pattern string, consisting of >1 semicolon-separated pairs
# each pair consists of process arrive time and process length
def testPatternToArrays(s):
    pairs = s.strip().split(";")

    arrived = []
    duration = []

    for pair_str in pairs:
        pair = pair_str.strip().split(",")
        arrived.append(int(pair[0]))
        duration.append(int(pair[1]))

    # input checks
    assert len(arrived) == len(duration)
    assert len(arrived) != 0

    return arrived, duration