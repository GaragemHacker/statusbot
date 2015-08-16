#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import json 
import time
import requests
from urlparse import urljoin

token = 'TELEGRAM_BOT_TOKEN'
base_url = 'https://api.telegram.org/bot'+token+'/'
headers = {'content-type': 'application/x-www-form-urlencoded'}

last_message_id = None
last_stick_id = None

def status_garagem():
	
	response = requests.get('http://garagemhacker.org/status.txt')
	if response.status_code != 200:
		sys.exit(2)

	return response.text

	

def get_updates():
	response = requests.get(urljoin(base_url, 'getUpdates'))
	if response.status_code != 200:
		sys.exit(1)
	response = response.json()
	result = response['result'][-1]
	message = result['message']
	if message.has_key('text'):
		if message['text'].startswith('/status'):
			status = status_garagem()
			#import ipdb; ipdb.set_trace()
			send_message(message['chat']['id'], status, message['message_id'])
			if status.rstrip() == 'aberto':
				send_sticker(message['chat']['id'], 'BQADAQADQQADyIsGAAEBJ1h7N54y1wI', message['message_id'])
			else:
				send_sticker(message['chat']['id'], 'BQADAQADIAADyIsGAAGeqFpovvSWiwI', message['message_id'])


def send_sticker(chat_id, sticker, message_id):
	data_sticker = {
		'chat_id': chat_id,
		'sticker': sticker
	}

	global last_stick_id
	if last_stick_id == message_id:
		return

	response = requests.post(urljoin(base_url, 'sendSticker'), data=data_sticker, headers=headers)
	if response.status_code != 200:
		sys.exit(1)
		
	last_stick_id = message_id


def send_message(chat_id, text, message_id):
	data = {
		'chat_id': chat_id, 
		'text': text
	}

	global last_message_id
	if last_message_id == message_id:
		return
	
	response = requests.post(urljoin(base_url, 'sendMessage'), data=data, headers=headers)
	if response.status_code != 200:
		sys.exit(1)

	
	last_message_id = message_id



def main():
	while True:
		get_updates()
		time.sleep(1)


if __name__ == '__main__':
	main()
