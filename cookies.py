def appendDict(request, dict):
    """ adds the noghtmode to our dict"""
    dict = add_nightmode(request, dict)
    return dict

def add_nightmode(request, dict):
    """ adds the nightmode if in cookies"""
    if "nightmode" in request.cookies:
        dict["nightmode"] = request.cookies["nightmode"]
    return dict