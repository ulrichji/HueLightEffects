from phue import Bridge
import colorsys
import json

#requires phue

CONFIG_FILE_PATH="config/config.json"

def getConfig(path):
	try:
		f = open(path, "rb")
		data = f.read()
		json_data = json.loads(data.decode())
		f.close()
		
		return json_data
		
	except Expection as e:
		print("Failed to read configuration file at "+str(path)+": "+str(e))
	
	return None

def connectBridge():
	global CONFIG_FILE_PATH

	config = getConfig(CONFIG_FILE_PATH)
	ip = config['switch_ip'] if 'switch_ip' in config else None
	if(ip is None):
		raise Exception('Didn\'t find switch_ip in config/config.json. Make sure format is correct')
	
	try:
		b = Bridge(ip)
		b.connect()
		return b
	except Exception as error:
		print(error)
		
	return None

def setLightsRGB(b, rgb):
	global CONFIG_FILE_PATH
	
	config = getConfig(CONFIG_FILE_PATH)
	affected_lights = config['affected_lights'] if 'affected_lights' in config else None
	if(affected_lights is None):
		raise Exception('Didn\'t find affected_lights in config/config.json. Make sure format is correct')
	
	hsv = colorsys.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
	
	for light_id in affected_lights:
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
	