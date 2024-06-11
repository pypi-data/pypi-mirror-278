# @michaelrex2012
# 6/7/2024
# Adds ConvertTime() function

def convertTime(time, inputType, outputType):
    if inputType == "minutes" and outputType == "hours":
        print(time / 60)
        print("In Hours")
    if inputType == "hours" and outputType == "minutes":
        print(time * 60)
        print("In Minutes")
    if inputType == "hours" and outputType == "hours":
        print(time)
        print("In Hours")
    if inputType == "minutes" and outputType == "minutes":
        print(time)
        print("In Minutes")
    if inputType != "minutes" and inputType != "hours":
        print("inputType must be 'minutes' or 'hours'")
    if outputType != "minutes" and outputType != "hours":
        print("outputType must be 'minutes' or 'hours'")
