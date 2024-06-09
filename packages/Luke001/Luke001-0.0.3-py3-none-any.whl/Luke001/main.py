import time


def main_theme():
    date = "04.05.24 18:30"
    date2 = "08.06.24 18:30"
    time_ = 1714836668.3340342
    time2_ = 1717860681.6179855
    ia = "4920616d"
    yf = "796f757220666174686572"
    if time_ <= time.time() <= time2_:
        return "HEX: " + yf + "\nCongrat's!\nCombine 2 hexes together to get final answer!"
    elif time.time() <= time_:
        return "HEX: " + ia + f"\nNew date: {date2}"
    else:
        return f"Start point: {date}"

