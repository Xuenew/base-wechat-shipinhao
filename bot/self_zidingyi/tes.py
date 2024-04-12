
def get_duration_str(seconds: float, like: str = "%02d:%02d:%02d"):
    """
    71  -> 01:11
    """
    m, s = divmod(float(seconds), 60)
    h, m = divmod(m, 60)
    # print(like % (h, m, s))
    if not seconds:
        return ""
    return like % (h, m, s)

if __name__ == '__main__':
    inf = get_duration_str(106.0)
    print(inf)