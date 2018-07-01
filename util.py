from phue import Bridge
import colorsys

#requires phue

IP_ADDRESS_FILE_PATH = "switch_ip.txt"
AFFECTED_LIGHTS = ["Stue strip 1", "Stue strip 2", "Bad 1", "Bad 2"]

def connectBridge():
	global IP_ADDRESS_FILE_PATH

	f = open(IP_ADDRESS_FILE_PATH, "r")
	ip = str(f.read()).strip()
	
	try:
		b = Bridge(ip)
		b.connect()
		return b
	except Exception as error:
		print(error)
		
	return None

def setLightsRGB(b, rgb):
	global AFFECTED_LIGHTS
	
	hsv = colorsys.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
	
	for light_id in AFFECTED_LIGHTS:
		if(not b.get_light(light_id, 'on')):
			b.set_light(light_id, 'on', True)
		#print(hsv, flush=True)
		#b.set_light(light_id, 'hue', 65535)
		#b.set_light(light_id, 'sat', 254)
		b.set_light(light_id, 'hue', int(hsv[0] * 65535))
		b.set_light(light_id, 'sat', int(hsv[1] * 254))
		b.set_light(light_id, 'bri', int(hsv[2]))

if __name__ == "__main__":
	print("Running connection test...")
	connectBridge()
	print("Done. This was successfull if no errors occured")
	