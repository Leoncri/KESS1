def GetTypeList():
    return ["MVDC", "LVDC", "LVAC", "none"]

def GetTypeID(type):
    if type == "MVDC":
        return 1
    if type == "LVDC":
        return 2
    if type == "LVAC":
        return 3
    return 0

def GetTypeFromID(id):
    if id == 1:
        return "MVDC"
    if id == 2:
        return "LVDC"
    if id == 3:
        return "LVAC"
    return "none"