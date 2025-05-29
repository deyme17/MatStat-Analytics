def get_default_bin_count(data):
    if data.empty:
        return 1
    n = len(data)
    if n <= 100:
        bins = int(n ** 0.5)
    else:
        bins = int(n ** (1 / 3))
    return max(bins, 1)