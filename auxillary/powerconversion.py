def PowerToRegisterValue(maxPower, inputPower):
    # limit inpout power to +- maxPower
    if inputPower > maxPower:
        inputPower = maxPower
    elif inputPower < -maxPower:
        inputPower = -maxPower
    
    # find ratio and multiply by 10.000
    r = int(inputPower / maxPower * 10000)
    
    # return register value
    register = 32768 + r
    
    return register;

def ParsePowerValue(value):
    # split into exponent and significant
    s = value >> 6
    e = value & 0x003F
    
    return s * 10 ** e