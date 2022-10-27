module = "game"

def updateVal(val, vel):
    #move the ball
    val += vel 
    return val 

def bounce(vel, pos, radius, maxVal):
    if pos > maxVal - radius or pos < radius:
        vel *= -1;
    return vel
