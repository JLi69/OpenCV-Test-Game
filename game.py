module = "game"

def initBricks(rows, camWidth):
    bricks = []
    brickWidth = 80
    brickHeight = 40
    for i in range(rows):
        for j in range(int(camWidth / brickWidth)):
            bricks.append({ "x" : j * brickWidth,
                            "y" : brickHeight * i,
                            "w" : brickWidth,
                            "h" : brickHeight,
                            "broken" : False })
    return bricks

def updateVal(val, vel):
    #move the ball
    val += vel 
    return val 

def bounce(vel, pos, radius, maxVal):
    if pos > maxVal - radius or pos < radius:
        vel *= -1;
    return vel

def bound(val, minVal, maxVal):
    if(val < minVal):
        return minVal
    if(val > maxVal):
        return maxVal
    return val

def colliding(ballX, ballY, ballRadius, rectX, rectY, rectWidth, rectHeight):
    return ballX + ballRadius > rectX and ballX - ballRadius < rectX + rectWidth and ballY - ballRadius < rectY + rectHeight and ballY + ballRadius > rectY

def checkBrickCollision(ballX, ballY, ballRadius, bricks):
    for brick in bricks:
        if colliding(ballX, ballY, ballRadius, brick["x"], brick["y"], brick["w"], brick["h"]) and not brick["broken"]:
            brick["broken"] = True
            return [ bricks, True ] 
    return [ bricks, False ]
