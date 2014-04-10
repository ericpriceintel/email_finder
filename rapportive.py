#change token based on email address - right now it says "unicode" not callable

import csv
import urllib2
import json
import time

inputs = []
emails = []
results = []
	

def email_permutator():
	"This takes the above information and creates common email formats:"
	global trials
	trials = [first_name, '.'.join([first_initial,last_name]),''.join([first_initial, last_name]), '.'.join([first_name, last_name]), ''.join([first_name,last_name])]
	for x in trials:
		emails.append(''.join([x, ending]))

def token(email):
	response = urllib2.Request('https://rapportive.com/login_status?user_email=' + email)
	token_json = json.load(urllib2.urlopen(response))
	global token
	token = token_json["session_token"]
	print token

def rapportive(email):
	req = urllib2.Request('https://profiles.rapportive.com/contacts/email/' + email, None, {'X-Session-Token' : token})
	global resp
	resp = json.load(urllib2.urlopen(req))

def csv_writer(results):
	resultsFile = open('input.csv', 'w')
	wr = csv.writer(resultsFile)
	for row in inputs:
		wr.writerow(row)

def csv_reader():
	initialFile = open('input.csv', 'rU')
	wr = csv.reader(initialFile, delimiter=",")
	for row in wr:
		inputs.append(row)
	initialFile.close()

def tryer(i):
	count = 0
	for email in emails:
		print email
		token(email)
		rapportive(email)
		if resp["contact"]["first_name"] == first_name and resp["contact"]["last_name"] == last_name:
			correct_email = resp["contact"]["email"]
			inputs[i].append(correct_email)
			break
		else:
			count += 1
			if count == len(trials):
				inputs[i].append("Email not found")
			time.sleep(15)
	emails[:] = []

def set_name(i):
	global first_name, first_initial, last_name, last_initial, ending
	first_name = inputs[i][0]
	first_initial = first_name[0]
	last_name = inputs[i][1]
	last_initial = last_name[0]
	domain = inputs[i][2]
	ending = ''.join(['@',domain])

def iterator():
	csv_reader()
	csv_writer(results)
	i = 0
	while i < len(inputs):
		set_name(i)
		email_permutator()
		tryer(i)
		i += 1

iterator()
