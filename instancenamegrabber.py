from mastodon import Mastodon, StreamListener
import re
import csv

mastodon = Mastodon(
    access_token = "", #Put mastodon creds here
    api_base_url = "https://mastodon.social", 
)
#I use mastodon.social as it is the largest instance that preforms moderation extensively. 
#This gives me access to the largest node in the federated network.
#While I am scraping data from the fediverse it's only instance names.

class myListener(StreamListener): 
	def on_update(self,status):
		username = status["account"]["acct"] #Grab the username. That's the best way to get the username

		if "@" not in username:
			username = username + "@mastodon.social" 

		instancename = re.sub(r'.*@', '', username) #Regex to strip the username and grab the instance

		foundname = False #Set this to be false while we iterate

		with open("data.csv") as csvfile: #Open the csv
			csvreader = csv.reader(csvfile, delimiter=',')

			for row in csvreader:
				if instancename in row:
					foundname = True #If the instance is in the data.csv file then we can ignore it.

			if foundname == True:
				print("Instance already in database...")
			else:
				print("Instance not in database! Adding...")
				print(instancename)
				with open("data.csv",'a') as csvfile:
					csvwriter = csv.writer(csvfile, delimiter=',')
					csvwriter.writerow([instancename]) #Write to data.csv

listener = myListener() #Make a streamer
mastodon.stream_public(listener)  #Start the show
