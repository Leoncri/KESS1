# color list for editor
def GetColorByType(type):
    if type == "MVDC":
        return "orange"
    if type == "LVDC":
        return "blue"
    if type == "LVAC":
        return "green"
    return "gray"