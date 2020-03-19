import requests
import urllib.request
import os.path
import shutil
import csv

def main():
    with open("data.csv") as i: #Open the data.csv file
        instances = i.readlines()  #Write them into memory
    instances = [x.strip() for x in instances] #Strip any weird issues from writing
 
    instances.sort() #Sort them alphabetically
    setup(instances) #Run setup to create all the necessary files and subfolders
    count = len(instances) #Get the count just for fun
    i = 0 
    try:
        for name in instances:
            try:
                i += 1
                print("-----!"+name+"!-----")
                print(str(i) +" of " + str(count) + " remaining!")
                fetch(name) #Run the fetching code
            except Exception as e:
                print(e) #Print the error. We catch errors here for pleroma instances, weirdly encoded urls, etc
                pass #Don't stop the beat
    except Exception as e:
        print("Instance Error")
        print(e)
        pass
    clone(instances) #Clone all of them into one big folder for ease of access


def fetch(name):
    r = requests.get('https://%s/api/v1/custom_emojis'% name, allow_redirects=True) #Throw the instance name into the standard url for fetching data
    path = "emoji/%s/" % name #Because of the clone function we know all of these folders will exist
    try:
        for emoji in r.json(): #Emoji = the json code from the request
            try:
                if os.path.isfile(path+emoji['shortcode']+".png"): #Check to see if it exists. 
                    pass
                else:
                    if "ms_" not in emoji['shortcode']: #Cut out Mutant Standard Emojis (Or at least most of them). #Mutant standard is huge and common
                        #print(emoji['shortcode'] + " found!")
                        emojiimage = requests.get(emoji['static_url'],allow_redirects=True) #Get the image from the json
                        open(path + emoji['shortcode']+".png",'wb').write(emojiimage.content) #Now save it as an image in the filesystem
            except Exception as e:
                print("Did not get: " + emoji['url']) #If somethings fucky throw a nice error then keep going.
                print(e)
                pass
    except Exception as e:
        print(e)

def setup(instances): 
    if (os.path.isdir("emoji/")): #Check to see if emoji/ exists 
        pass   
    else:
        os.mkdir("emoji/") #make it if it doesnt

    for name in instances:
        if (os.path.isdir("emoji/%s/"%name)):
            pass
        else: os.mkdir("emoji/%s/"%name)
 
    if (os.path.isdir("emoji/all")):
        pass
    else:
        os.mkdir("emoji/all")

def clone(instances):
    for name in instances:
        print("Copying emoji for: %s"% name)
        path = "emoji/%s/" % name
        files = os.listdir(path)
        for name in files: #This gets alll files
            try: 
                shutil.copyfile(path+name,"emoji/all/"+name) #Then copies them into the all folder
            except Exception as e:
                print(e)
                pass
 

if __name__ == '__main__':
    main()
