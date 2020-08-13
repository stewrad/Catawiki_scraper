#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import pandas as pd
from os import path
import re
import time

url = 'https://www.catawiki.com/a/'
a = int(input('\nEnter auction ID: '))
search_cat = input("Enter a category to search for: ")

# iterator = url.split('/')[-1:]
b = 0
file_name = 'catawiki_IDs.csv'

if path.exists(file_name) is True:
	df2 = pd.read_csv(file_name, delimiter=',')
	list1 = [list(row) for row in df2.values]
else:
	list1 = []

list2 = []

def loop_down(url, a, b, list1, list2, file_name, search_cat):
	time1 = time.time()
	for i in range(100):

		fullurl	= url + str(a)
		r = requests.get(fullurl)
		stat = r.status_code
		soup = BeautifulSoup(r.content, 'html.parser')

		try:
			category = soup.select('h1.c-page__heading')[0].text.strip()
			#setup regex search to ignore case from user input as error protection
			regex_cat = re.compile(rf'{search_cat}', re.IGNORECASE)
			res = regex_cat.search(category)
			if res:
				if any(a in sublist for sublist in list1):
					print(f'| Status_code: {stat} | ID: {a} | **ID already captured**')
				else:
					print(f'| Status_code: {stat} | ID: {a} |')
					datetime = soup.select('div.be-auction__header-bottom')
					check = re.search(r'(\d{4}).(\d{1,2}).(\d{1,2})', str(datetime))
					date = check.group()
					list2.append([date, category, stat, fullurl, a])
			else:
				print(f'| Status_code: {stat} | ID: {a} | <-- Not a "{search_cat}"')
		except IndexError:	
			b+=1
			# print(f'IndexError on ID: {a}')
			print(f'| Status_code: {stat} | ID: {a} | IndexError')
		except ConnectionError:
			print('Connectioned failed: killed by end-client')

		if b == 75:
			break

		a-=2
		i+=1
	time2 = time.time()

	print(f'Downward count took {time2-time1:.2f} s')
	return list2

def loop_up(url, a, b, list1, list2, file_name, search_cat):
	time1 = time.time()
	a+=2
	for i in range(100):
		fullurl	= url + str(a)
		r = requests.get(fullurl)
		stat = r.status_code
		soup = BeautifulSoup(r.content, 'html.parser')

		try:
			category = soup.select('h1.c-page__heading')[0].text.strip()
			#setup regex search to ignore case from user input as error protection
			regex_cat = re.compile(rf'{search_cat}', re.IGNORECASE)
			res = regex_cat.search(category)
			if res:
				if any(a in sublist for sublist in list1):
					print(f'| Status_code: {stat} | ID: {a} | **ID already captured**')
				else:
					print(f'| Status_code: {stat} | ID: {a} |')
					datetime = soup.select('div.be-auction__header-bottom')
					check = re.search(r'(\d{4}).(\d{1,2}).(\d{1,2})', str(datetime))
					date = check.group()
					list2.append([date, category, stat, fullurl, a])
			else:
				print(f'| Status_code: {stat} | ID: {a} | <-- Not a "{search_cat}"')
		except IndexError:	
			b+=1
			# print(f'IndexError on ID: {a}')
			print(f'| Status_code: {stat} | ID: {a} | IndexError')
		except ConnectionError:
			print('Connectioned failed: killed by end-client')

		if b == 25:
			break

		a+=2
		i+=1
	time2 = time.time()

	print(f'Upward count took {time2-time1:.2f} s')

	return list2

time1 = time.time()
loop_up(url, a, b, list1, list2, file_name, search_cat)
loop_down(url, a, b, list1, list2, file_name, search_cat)

print('\nFinished writing to file!')
time2 = time.time()

print(f'\nTotal time taken: {time2-time1:.2f} s')

if path.exists(file_name) is False:
	df = pd.DataFrame(list2, columns=('Date', 'Category', 'Status_code', 'Full_URL', 'Path'))
	df.to_csv(file_name, index=False)
else:
	try:
		df = pd.DataFrame(list2)
		df.to_csv(file_name, mode='a', header=False, index=False)
	except PermissionError:
		print(f'{file_name} is open. File must be closed before running script.')


