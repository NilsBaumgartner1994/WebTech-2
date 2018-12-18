def appendDict(request, dict):
    dict = add_nightmode(request, dict)
    return dict

def add_nightmode(request, dict):
    if "nightmode" in request.cookies:
        dict["nightmode"] = request.cookies["nightmode"]
    return dict