import util
import time
import urllib.request
import json
from difflib import SequenceMatcher
from threading import Thread

program_running = True

def getScoreFromPosition(page_json, score_scale):
	#First, look at result
	if('position' in page_json and 'result' in page_json['position']):
		result_str = page_json['position']['result']
		if(result_str == "1-0"):
			return 1.0
		elif(result_str == "0-1"):
			return -1.0
		elif(result_str == "1/2"):
			return 0.0

	#Second, look at mate moves
	#I have no idea how to find this...
	if('score' in page_json):
		score_data = page_json['score']
		if(len(score_data) >= 2):
			score_type = score_data[0]
			if(score_type == 'm'):
				score_value = int(score_data[1])
				toplay = "W"
				if('position' in page_json and 'toplay' in page_json['position']['toplay']):
					toplay = page_json['position']['toplay']
				else:
					print("[WARNING] no to-play found in json. Assuming white to move")
				
				if(score_value == 0):
					if(toplay == "W"):
						return 1.0
					elif(toplay == "B"):
						return -1.0
					else:
						print("[WARNING] Unknown to-play value: "+str(toplay))
				elif(score_value < 0):
					return -1.0
				else:
					return 1.0
			
	
	#Third, look at evaluated score
	if('score' in page_json):
		score_data = page_json['score']
		if(not score_data is None and len(score_data) == 2):
			score_type = page_json['score'][0]
			score_value = float(page_json['score'][1])
			return score_value / score_scale
		else:
			print("[WARNING] Skipping score because format is unknown")
	
	return None

def getPosition(config):
	score_url = config['score_url']
	player_list = config['playerlist']
	score_scale = float(config['score_scale'])
	
	try:
		page = urllib.request.urlopen(score_url)
		page_content = page.read()
		page_json = json.loads(page_content.decode())
	
		white_player = ""
		black_player = ""
	
		if('position' in page_json and 'player_w' in page_json['position']):
			white_player = page_json['position']['player_w']
		else:
			print("[WARNING] didn't find name of white player")
		if('position' in page_json and 'player_b' in page_json['position']):
			black_player = page_json['position']['player_b']
		else:
			print("[WARNING] didn't find name of black player")
		
		if(white_player == "" and black_player == ""):
			print("No players found, will assume you are following white player")

		best_match_value = 0.0
		negate_score = False
		for player in player_list:
			white_player_similarity = SequenceMatcher(None, player, white_player).ratio()
			black_player_similarity = SequenceMatcher(None, player, black_player).ratio()
			temp_negate_score = black_player_similarity > white_player_similarity
			max_similarity = max(white_player_similarity, black_player_similarity)
			if(max_similarity > best_match_value):
				best_match_value = max_similarity
				negate_score = temp_negate_score

		score = getScoreFromPosition(page_json, score_scale)
		if(score is None):
			print("[WARNING] found no score from downloaded position")
			return None

		if(negate_score):
			return -score
		else:
			return score
	
	except Exception as e:
		print("Error reading score from document: " + str(e))
	
	return None

def getScoreColor(score):
	if(score > 1.0):
		score = 1.0
	elif(score < -1.0):
		score = -1.0
	
	green_ratio = (score + 1.0) / 2.0
	red_ratio = (1.0 - green_ratio)
	blue_ratio = (1.0 - abs(green_ratio - red_ratio)) * 0.5
	
	return (int(red_ratio * 255), int(green_ratio * 255), int(blue_ratio * 255))

def lightLoop():
	global program_running
	
	b = util.connectBridge()
	if(b is None):
		print("Unable to connect to HUE bridge")
		return None
	config = util.getConfig("config/sesse_config.json")
	if(config is None):
		print("Unable to load config")
		return config
	
	loop_time = float(config['update_interval'])
	
	previous_score = 0
	
	while(program_running):
		start_time = time.time()
		
		score = getPosition(config)
		if(not score is None and score != previous_score):
			color = getScoreColor(score)
			util.setLightsRGB(b, color)
		
		previous_score = score
		
		end_time = time.time()
		remaining_time = loop_time - (end_time - start_time)
		if(remaining_time > 0):
			time.sleep(remaining_time)

def main():
	global program_running
	
	thread = Thread(target=lightLoop, args = ())
	thread.start()
	
	input("Type any key to stop:\n")
	program_running = False
	thread.join()

if __name__ == "__main__":
	main()
