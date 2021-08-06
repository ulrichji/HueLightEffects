from urllib.request import urlopen
import xml.etree.ElementTree as ET
import calendar
import time
import re
import util

WEATHER_URL = "http://www.yr.no/sted/Norge/Telemark/Sauherad/Gvarv/varsel.xml"

def getForecastElement(element):
	forecast_element = {}
	forecast_time = 0
	
	time_str = element.attrib['from']
	time_format = "%Y-%m-%dT%H:%M:%S"
	forecast_time = int(time.mktime(time.strptime(time_str, time_format)))
	
	for child in element:
		if(child.tag == 'pressure'):
			forecast_element['pressure'] = child.attrib
		elif(child.tag == 'temperature'):
			forecast_element['temperature'] = child.attrib
		elif(child.tag == 'windSpeed'):
			forecast_element['windSpeed'] = child.attrib
		elif(child.tag == 'windDirection'):
			forecast_element['windDirection'] = child.attrib
		elif(child.tag == 'precipitation'):
			forecast_element['precipitation'] = child.attrib
		elif(child.tag == 'symbol'):
			forecast_element['symbol'] = child.attrib
	
	return (forecast_time, forecast_element)

def getForecastList(element):
	forecast_list = []
	for child in element:
		if(child.tag == 'tabular'):
			for forecast in child:
				if(forecast.tag == 'time'):
					forecast_element = getForecastElement(forecast)
					if(not forecast_element is None):
						forecast_list.append(forecast_element)
	
	return forecast_list

def getForecastFromTime(forecast_list, time):
	closest_time = float('inf')
	closest_forecast = None
	
	for forecast in forecast_list:
		forecast_time = forecast[0]
		forecast_time_diff = abs(forecast_time - time)
		if(forecast_time_diff < closest_time):
			closest_time = forecast_time_diff
			closest_forecast = forecast
	
	return closest_forecast

def getObservations(element):
	pass

def getColorFromForecastSymbol(forecast):
	forecast_data = forecast[1]
	forecast_symbol = forecast_data['symbol']
	#Symbols can be found at https://om.yr.no/symbol/
	symbol_text = forecast_symbol['var']
	number = re.findall(r'\d+', symbol_text)
	if(len(number) <= 0):
		print("Unable to parse number", symbol_text)
		return None
	number = int(number[0])
	color_rgb = (255, 0, 200)
	
	#Clear sky
	if(number == 1):
		color_rgb = (254, 128, 0)
	#Fair
	elif(number == 2):
		color_rgb = (128, 64, 8)
	#Partly cloudy
	elif(number == 3):
		color_rgb = (64 , 32, 16)
	#Cloudy
	elif(number == 4):
		color_rgb = (32, 32, 32)
	#Showers
	elif(number == 40):
		color_rgb = (170, 170, 255)
	#Rain showers
	elif(number == 5):
		color_rgb = (100, 100, 255)
	#Heavy rain showers
	elif(number == 41):
		color_rgb = (0,0,0)
	#Light rain showers and thunder
	elif(number == 24):
		color_rgb = (0,0,0)
	#Rain showers and thunder
	elif(number == 6):
		color_rgb = (0,0,0)
	#Heavy rain showers and thunder
	elif(number == 25):
		color_rgb = (0,0,0)
	#Light sleet showers
	elif(number == 42):
		color_rgb = (0,0,0)
	#Sleet showers
	elif(number == 7):
		color_rgb = (0,0,0)
	#Heavy sleet showers
	elif(number == 43):
		color_rgb = (0,0,0)
	#Light sleet showers and thunder
	elif(number == 26):
		color_rgb = (0,0,0)
	#Sleet showers and thunder
	elif(number == 20):
		color_rgb = (0,0,0)
	#Heavy sleet showers and thunder
	elif(number == 27):
		color_rgb = (0,0,0)
	#Light snow showers
	elif(number == 44):
		color_rgb = (0,0,0)
	#Snow showers
	elif(number == 8):
		color_rgb = (0,0,0)
	#Heavy snow showers
	elif(number == 45):
		color_rgb = (0,0,0)
	#Light snow showers with thunder
	elif(number == 28):
		color_rgb = (0,0,0)
	#Snow showers and thunder
	elif(number == 21):
		color_rgb = (0,0,0)
	#Heavy snow showers and thunder
	elif(number == 29):
		color_rgb = (0,0,0)
	#Light rain
	elif(number == 46):
		color_rgb = (0,0,0)
	#Rain
	elif(number == 9):
		color_rgb = (0,0,0)
	#Heavy rain
	elif(number == 10):
		color_rgb = (0,0,0)
	#Light rain and thunder
	elif(number == 30):
		color_rgb = (0,0,0)
	#Rain and thunder
	elif(number == 22):
		color_rgb = (0,0,0)
	#Heavy rain and thunder
	elif(number == 11):
		color_rgb = (0,0,0)
	#Light sleet
	elif(number == 47):
		color_rgb = (0,0,0)
	#Sleet
	elif(number == 12):
		color_rgb = (0,0,0)
	#Heavy sleet
	elif(number == 48):
		color_rgb = (0,0,0)
	#Light sleet and thunder
	elif(number == 31):
		color_rgb = (0,0,0)
	#Sleet and thunder
	elif(number == 23):
		color_rgb = (0,0,0)
	#Heavy sleet and thunder
	elif(number == 32):
		color_rgb = (0,0,0)
	#Light snow
	elif(number == 49):
		color_rgb = (0,0,0)
	#Snow
	elif(number == 13):
		color_rgb = (0,0,0)
	#Heavy snow
	elif(number == 50):
		color_rgb = (0,0,0)
	#Light snow and thunder
	elif(number == 33):
		color_rgb = (0,0,0)
	#Snow and thunder
	elif(number == 14):
		color_rgb = (0,0,0)
	#Heavy snow and thunder
	elif(number == 34):
		color_rgb = (0,0,0)
	#Fog
	elif(number == 15):
		color_rgb = (0,0,0)
	
	return color_rgb
	
def main():
	global WEATHER_URL
	sleep_time = 60
	
	xml = urlopen(WEATHER_URL).read().decode('utf-8')
	
	root = ET.fromstring(xml)
	for child in root:
		if(child.tag == 'forecast'):
			forecasts = getForecastList(child)
			current_time = int(calendar.timegm(time.gmtime()))
			time_difference = 60 * 60
			forecast_to_use = getForecastFromTime(forecasts, current_time + time_difference)
			weather_color = getColorFromForecastSymbol(forecast_to_use)
			
			b = util.connectBridge()
			if(b is None or weather_color is None):
				time.sleep(sleep_time)
				continue
			
			util.setLightsRGB(b, weather_color)
			time.sleep(sleep_time)
		if(child.tag == 'observations'):
			observations = getObservations(child)
		

if __name__ == "__main__":
	main()
