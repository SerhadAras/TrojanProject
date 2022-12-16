import mss
import mss.tools
import os
import base64


def run(**args):
    print("[*] In Screener Module")
    with mss.mss() as sct:
        # The monitor or screen part to capture
        monitor = sct.monitors[1]  # or a region

        # Grab the data
        sct_img = sct.grab(monitor)
        # Generate the PNG
        png = mss.tools.to_png(sct_img.rgb, sct_img.size)
        #
        # # Save png to file
        with open('screenshot.png', 'wb') as f:
            f.write(png)
        # # Save png to file
        with open("screenshot.png", "rb") as image:
            encoded_string = image.read()
        # delete screenshot.PNG
        os.remove('screenshot.png')
        return(encoded_string)

