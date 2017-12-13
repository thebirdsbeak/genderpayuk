import csv
import requests 
import arrow
import os

def download_data():
	'''Downloads and decodes the dataset 
	and passes to org_list function'''
	dataset = [] 
	timenow = arrow.now('GMT').format('DDMMYY')
	filename = "{}paydata.csv".format(timenow)
	if filename in os.listdir('.'):
		with open(filename, 'r') as olddata:
			readdata = olddata.read()
			csv_read = csv.reader(readdata.splitlines(), delimiter=",")
	else:
		print(filename)			
		with open(filename, 'w+') as data_file:
			data = 'https://gender-pay-gap.service.gov.uk/Viewing/download-data?year=2017'
			with requests.Session() as sesh:
				download = sesh.get(data)
				decoded_content = download.content.decode('utf-8')
				data_file.write(decoded_content)
				csv_read = csv.reader(decoded_content.splitlines(), delimiter=",")
	
	my_list = list(csv_read)
	for i in (my_list[1::]):
		dataset.append(i)
	org_list(dataset)

def org_list(searchlist):
	'''Takes downloaded data and spits out results'''
	for index, i in enumerate(searchlist):
		print("{} - {}".format(index, i[0]))
	choice = int(input("\n>>> "))
	comp = searchlist[choice]
	selected_company = searchlist[choice]
	diffpaymean = comp[4] #women paid x% less mean
	diffpaymed = comp[5] #women paid x% less median
	diffbonusmean = comp[6] #women paid less bonus mean
	diffbonusmed = comp[7] #women paid less bonus median
	malebonusmed = comp[8] #% men getting bonuses
	femalebonusmed = comp[9] #%women getting bonuses

	print('''
	{}\n
	Paygap (mean)        {}
	Paygap (median)      {}
	Bonus gap (mean)     {}
	Bonus gap (median)   {}
	Men with bonuses     {}
	Women with bonuses   {}
	'''.format(comp[0], diffpaymean, diffpaymed, diffbonusmean, diffbonusmed, malebonusmed, femalebonusmed))

	graph_request = input("See another? (y/n): ")
	if type(graph_request) == str and graph_request.upper() == "Y":
		org_list(searchlist)
	else:
		quit()

#Kicks off the program
download_data()
