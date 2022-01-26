from flask import Flask, render_template, Response
import cv2
import numpy as np

app = Flask(__name__)

# Capture the first camera on the system
camera = cv2.VideoCapture(0)

# This function gets called by the /video_feed route below
def gen_frames():  # generate frame by frame from camera

    # We want to loop this forever
    while True:

        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame

        # If something goes wrong with the camera, exit the function
        if not success:
            break

        # We convert the image into HSV format. HSV is used for image
        # tracking later
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # To detect a color we need to set an upper and lower bound on the
        # color. The array of numbers is HSV format which is not a standard
        # in any way.
        # You can use the color-picker.py script to help figure
        # these numbers out, it's much easier than trying to figure this
        # out by hand

        # Example Red
        lower_color = np.array([150,100,100], dtype=np.uint8)
        upper_color = np.array([220,255,255], dtype=np.uint8)


        # Example Blue
        #lower_color = np.array([100,100,100], dtype=np.uint8)
        #upper_color = np.array([110,130,150], dtype=np.uint8)

        # We now take the lower and upper bound colors and look for
        # anything that falls inside of this range.
        mask = cv2.inRange(hsv, lower_color, upper_color)

        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(frame,frame, mask= mask)

        # Convert the image to grayscale
        imgray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)

        # This turns the image into a black and white. Lighter pixels are
        # turned white, darker pixels turn black
        ret,thresh = cv2.threshold(imgray,127,255,0)

        # This step looks for shapes in the black and white image
        contours, hierarchy = cv2.findContours(imgray,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        # This variable is going to hold the largest rectangle we find. We
        # can do multiple object tracking, but it's easier for us to track
        # just the largest rectangle
        rectangle = {
            "area": 0,
            "x": 0,
            "y": 0,
            "w": 0,
            "h": 0
        }

        # We will loop over all the rectangles found
        for cnt in contours:

            # Get the rectangle dimensions
            x,y,w,h = cv2.boundingRect(cnt)

            # If this rectangle is larger than the currently largest
            # recrangle, store it
            if w * h > rectangle["area"]:
                rectangle["area"] = w * h
                rectangle["x"] = x
                rectangle["y"] = y
                rectangle["w"] = w
                rectangle["h"] = h

        # Only frame the biggest rectangle
        x = rectangle["x"]
        y = rectangle["y"]
        w = rectangle["w"]
        h = rectangle["h"]

        # We draw the rectangle onto the screen here
        cv2.rectangle(frame,(x,y),(x+w,y+h),[255,0,0],2)

        # This step encodes the data into a jpeg image
        ret, buffer = cv2.imencode('.jpg', frame)

        # We have to return bytes to the user
        frame = buffer.tobytes()

        # Return the image to the browser
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
