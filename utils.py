def safety_color(status):
    if status == "SAFE":
        return "GREEN"
    elif status == "UNSAFE":
        return "RED"
    else:
        return "AMBER"