#figure out how to not overwrite the entire output.csv file for every loo
#figure out how to avoid the Rapportive timeout

import csv
import time
import random
import requests

class EmailFinder(object):
	"""Finds emails based on an inputted csv
	"""

	def __init__(self, input_csv, output_csv):
		self.input_csv = input_csv
		self.output_csv = output_csv
		self.inputs = []
		self.emails = []
		self.results = []

	def find_emails(self):
		self.csv_reader()
		self.i = 0
		while self.i < len(self.inputs):
			self.set_name(self.i)
			self.email_permutator()
			self.tryer(self.i)
			self.csv_writer()
			self.i += 1

	def csv_reader(self):
		with open('input.csv', 'rU') as initial_file:
			wr = csv.reader(initial_file, delimiter=',')
			for row in wr:
				self.inputs.append(row)

	def set_name(self, i):
		self.first_name = self.inputs[i][0]
		self.first_initial = self.first_name[0]
		self.last_name = self.inputs[i][1]
		self.last_initial = self.last_name[0]
		self.domain = self.inputs[i][2]
		self.ending = '@%s' %(self.domain)

	def email_permutator(self):
		'''This takes the data from the set_name method and creates common email formats.
		'''
		self.trials = [self.first_name,
					'%s.%s'%(self.first_initial, self.last_name),
					'%s%s'%(self.first_initial, self.last_name),
					'%s.%s'%(self.first_name, self.last_name),
					'%s%s'%(self.first_name, self.last_name)]
		for x in self.trials:
			self.emails.append('%s%s'%(x, self.ending))

	def find_token(self, email):
		response = requests.get('https://rapportive.com/login_status?user_email=%s' %(email))
		json_response = response.json()
		self.token = json_response['session_token']

	def rapportive(self, email):
		req = requests.get('https://profiles.rapportive.com/contacts/email/%s' %(email), headers={'X-Session-Token' : self.token})
		self.resp = req.json()

	def tryer(self, i):
		for count, email in enumerate(self.emails):
			self.find_token(email)
			self.rapportive(email)
			if self.resp["contact"]["first_name"] == self.first_name and self.resp["contact"]["last_name"] == self.last_name:
				correct_email = self.resp["contact"]["email"]
				print correct_email
				self.inputs[i].append(correct_email)
				break
			else:
				count += 1
				if count == len(self.trials):
					self.inputs[i].append("Email not found")
				time.sleep(random.randrange(5,10))
		self.emails[:] = []

	def csv_writer(self):
		with open('output.csv', 'w') as results_file:
			wr = csv.writer(results_file)
			for x in self.inputs:
				wr.writerow(x)

email_finder = EmailFinder('input.csv', 'output.csv')
email_finder.find_emails()