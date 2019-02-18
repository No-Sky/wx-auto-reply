#-*-coding:utf8-*-
import requests
import json

def getShici():
	res = requests.get("https://api.gushi.ci/all.json")
	res.encoding = 'UTF-8'
	shici = json.loads(res.text)
	return shici['content']
