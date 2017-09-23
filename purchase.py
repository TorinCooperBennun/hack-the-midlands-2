'''
A function used to work out the time since the price 
    dropped below a threshold
@param dropLimit{float} the limit of a coin drop
    as a percentage before breaking
@param data{[(int, float)} a list of time stamped price data
    for an individual coin
@returns (time, change)
    where time is a unix time stamp of the amount of time past 
        @example 1800 is 30min
    where change is the amount risen in total since the drop as a float
        @example 0.012 is 1.2% rise
'''
def timeSinceDropped(dropLimit, data):
    finishTime = None
    for d in reversed(data):
        #inits the time and value we're checking against
        if finishTime is None:
            finishTime = d[0]
            finishValue = d[1]
            lastValue = finishValue
            lastTime = finishTime
            lowestPoint = lastValue
            continue
        
        #the value dropped too much to continue searching
        if d[1]-d[1]*dropLimit > lowestPoint:
            change = risePercentage(lastTime, finishTime)
            timeDiff = finishTime-lastTime
            return (timeDiff, change)

        if d[1] < lowestPoint:
            lowestPoint = d[1]

        #no major change, update last values and continue
        lastTime = d[0]
        lastValue = d[1]
    
    print("Been rising since the dawn of time!")
    change = risePercentage(lastValue, finishValue)
    timeDiff = finishTime-lastTime
    return (timeDiff, change)

'''
A function to estimate how certain a continuation above our limit
    based on the last x amount of data
@param dropLimit{float} the limit of a coin drop
    before recommend selling
@param data{float} a list of price data for an individual coin
@returns (certainty, change)
    Where certainty is the percentage of time it would have dropped
        the dropLimit
        @example 0.5 means it drops below every two rises
    where change is the amount risen from start to highest point
        @example 0.012 is 1.2% rise
'''
def riseCertainty(dropLimit, data):
    if len(data) == 1:
        return (None, 0)
    rises = 0
    highestValue = None
    for d in data:
        if highestValue is None:
            highestValue = d
            continue
        if highestValue-highestValue*dropLimit < d:
            rises += 1
        else:
            print("Dropped")
        if d > highestValue:
            highestValue = d
    certainty = rises/(len(data)-1)
    total_rise = risePercentage(d, highestValue)
    return (certainty, total_rise)

'''
Used to calculate the rise of a value in percentages
@param start{float} the starting value
@param end{float} the ending value
@returns percentage change
    @example 0.01 = 1% rise
    @example -0.5 = 50% drop
'''
def risePercentage(start, end): 
    change = (end - start)/start
    return change
    