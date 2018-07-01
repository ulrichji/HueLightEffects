import util
from PIL import ImageGrab
import numpy as np
from threading import Thread
import time

program_running = True
sleep_time = 0.5

#requires phue, PIL, numpy

def screenColorMean(img):
	r_array = img[:,:,0]
	g_array = img[:,:,1]
	b_array = img[:,:,2]
	
	r = np.mean(r_array)
	g = np.mean(g_array)
	b = np.mean(b_array)
	
	return (r,g,b)

def getScreenColor():
	pil_image = ImageGrab.grab()
	img = np.array(pil_image)
	
	return screenColorMean(img)

def lightLoop():
	global program_running, sleep_time
	
	b = util.connectBridge()
	if(b is None):
		return None
	
	while(program_running):
		screen_color = getScreenColor()
		util.setLightsRGB(b, screen_color)
		time.sleep(sleep_time)

def main():
	global program_running
	
	thread = Thread(target=lightLoop, args = ())
	thread.start()
	
	input("Type any key to stop:\n")
	program_running = False
	thread.join()

if __name__ == "__main__":
	main()
