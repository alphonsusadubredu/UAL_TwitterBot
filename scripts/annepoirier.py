#! /usr/bin/env python
# encoding=utf8


'''
This file contains the program for the main operation routine of the TwitterBot.
This is the property of Urban Attitudes Lab, Tufts University.
Written by Alphonsus Adu-Bredu
'''


import tweepy as tp
from time import sleep
import random
import requests
from os import listdir
from os.path import isfile, join

count = 0


class Bot:
        #Constructor for the Bot class
        def __init__(self):
                #Reads the twitter credentials of the Bot's Twitter account
                #from the file named 'credentials'
                #These credentials are kept in a separate file because
                #much like a password, they are confidential.
                credentials = []
                infile = open("credentials","rb")
                for line in infile:
                        credentials.append(line)
                infile.close()
                
                #DONT_TWEET flag. This flag is set to True if the tweet
                #has gone through the screening process for offensive words
                # and is deemed fit for retweeting. Else it is set to false.
                self.DONT_TWEET = False

                #This array contains all the keywords to be searched for 
                #in incoming tweets
                self.KEYWORD = ['smart city', 'smart cities', 'smart community', 'creative city', 'posthuman', 'urban smartness', 'smart city policy', 
                'smart home', 'computational thinking', 'smart learning cities', 'innovation capacity', 'future cities', 'real-time data', 'city dashboards',
                 'citizen sensing', 'programmed city', 'experiemental urbanism', 'eco-city', 'citizen sensor', 'digital city', 'intelligent city', 'live city',
                 'open city', 'smart meters', 'smart grid', 'urban innovation', 'e-government', 'big data', 'informational capitilism', 'copmutational urbanism',
                 'urban experiments', 'smart transport', 'smart natural resources', 'smart energy', 'smart mobility', 'smart culture and tourism', 
                 'smart participation', 'fantasy cities', 'smart city systems']
                

                #This array contains responses to accepted tweets that contain 
                # keyword(s) in both the KEYWORD array and the GREET_QUERY
                #array.
                self.GREETING = ['Check this out',
                'Hmm.. What do you think?',
                'Not bad',
                'Something different',
                'You might find this interesting',
                'Did they get it right?',
                'Descriptive',
                'I have mixed feelings about this, you?',
                'What do you reckon?',
                'How would you summarize it?',
                'Makes you think…',
                'Not what I expected',
                'I wonder…',
                'Lots to reflect on',
                'Lots to analyze',
                'Worth examining further',
                '#imaginethat',
                'Really need to stop and consider',
                'Will take it under consideration',
                'Will need time to think it over',
                'How does it make you feel?',
                'Love to hear your thoughts on this',
                'Timely? Too early? Too late?',
                'Pros? Cons?',
                'Unsure how to react',
                'Can see both sides of it..',
                'Important to weigh out both sides',
                'Diffcult to put into words',
                "What's your reaction?",
                'Easy to appreciate, hard to evaluate',
                'All kinds of mixed feelings',
                'I know what I think, but is it what they had in mind?',
                'What does it make you think of?',
                'Spark any memories?',
                'Ahh makes me think',
                'Up to date or out of date?',
                'Where to from here?',
                'I wonder what is next…',
                'Do you have it figured out?',
                'Your guess is as good as mine',
                'Everything comes with assumptions',
                'Is seeing believing?',
                'What did you expect?',
                'What do you believe in?',
                'Think think think',
                'What would you do?',
                "My oh my it's all so complicated",
                'If only we could see into the future',
                'How would you describe it in one word?']
                

                #This array contains keywords to look for in accepted tweets
                #that contain a keyword in the KEYWORD array
                self.GREET_QUERY = ['research','project', 'gorgeous', 'lovely','interesting', 'amazing', 
                'honor', 'honored', 'glad', 'happy', 'impressive', 'impressed', 'good work', 'encouraged', 
                'fascinating', 'fascinated', 'love','joy', 'great', 'delighted','delight']
                
                #This array contains responses to accepted tweets that contain
                #keyword(s) in the KEYWORD array but not in the GREET_QUERY
                #array
                self.GREET_NON_REPLY = ['Interesting', 'Nice', "That's cool", 'Really interesting' , 
                'hmmm...']
                

                #This array contains prefixes that would be concatenated with 
                #the descriptions received from Microsoft's Computer Vision API
                self.IMAGE_DESCRIPTION_PREFIX = ["Interesting, ","You've got to see this: ", "Love this stuff! ", 
                "Not what I expected: ", "Fun: ", "Lovely! ", "Have you seen this? ", "You've got to see this! ", 
                'Wow! ', 'OK… ', 'Oh… ', 'Not what I expected.  ', 'Can you believe it? ', 'Not really what it seems. ', 
                 'Appearances can be deceiving. ', "You can't look away. ", 'Try to look away. ', 'Makes you wonder… ', 
                 'Why not? ', 'Can you see that? ', 'Look at this! ']
                

                #This array contains keywords to look for in accepted tweets
                #that contain a keyword in the KEYWORD array
                self.SAD_QUERY = ['poor', 'unfortunate','irresponsible','bad','sad', 'evil', 'destroy']    
                

                #This array contains responses to accepted tweets that contain 
                # keyword(s) in both the KEYWORD array and the SAD_QUERY
                #array.
                self.SAD_REPLY = ["That's sad", "That's unfortunate", "Sad", "Too bad"]
                

                #This array contains a list of profane words the incoming
                #tweets are screened against. Any tweet with any of these
                #words is rejected.
                self.AVOID_WORDS = ['conservative', 'liberal', 'republican', 'democrat', 'progressive', 'alt-right', 
                'right-wing', 'left-wing', 'far right', 'leftist', 'trump', 'trumpian', 'politics', 'political', 
                'jesus', 'slavery', 'marxist', 'lenin', 'slave', 'christ', 'religious', 'religion', 'devil', 'satan', 
                'pagan', 'anal', 'anus','arse','ass','ballsack','balls','bastard','bitch','biatch','bloody','blowjob',
                "blow job","bollock","bollok","boner",'boob',"bugger","bum","butt",'buttplug','clitoris','cock','coon',
                'crap','cunt','damn','dick','dildo','dyke','fag','feck','fellate','fellatio','felching','fuck','f u c k',
                'fudgepacker','fudge packer','flange','Goddamn','God damn','hell','homo','jerk','jizz','knobend',
                'knob end','labia','lmao','lmfao','muff','nigger','nigga','omg','penis','piss','poop','prick','pube',
                'pussy','queer','scrotum','sex','shit','s hit','sh1t','slut','smegma','spunk','tit','tosser','turd','twat',
                'vagina','wank','whore','wtf']
                
                ###TO CHANGE####
                #These are the credentials for the Microsoft Vision API.
                #Just like the Twitter credentials, they are to be kept private.
                self.follow_count = 0;
                self.CONSUMER_KEY = "fPDn0LlpvAqhnhUSG6thhaHku"
                self.CONSUMER_KEY_SECRET = 
"ZSOhxxiuoygPgiEGxu72BRydA8X4iJ8Gurib0ziMd9vyKkqefL"
                self.ACCESS_TOKEN = "1054015992572112896-ys3I9NO5SctrAhkqFxKlCVgkJNGafu"
                self.ACCESS_TOKEN_SECRET = "S73ldHtNaRbFu3lae4FQB4IwTC1CZjLQtmlRQHa9eaLuj"
                self.api = self.authenticate()
                self.subscription_key = "a93af90b5b03496ebb9d3032e567dde3"
                self.vision_base_url = "https://eastus.api.cognitive.microsoft.com/vision/v1.0/"

                #These are the names of the image directories from which an 
                #image is selected at random and submitted to Microsoft
                #Computer Vision API for analyses.
                self.images_path = "/home/ubuntu/UAL_TwitterBot/images/"
                self.image_directory_names=["Design/","environment/", "FinancialPlanning/",
                "food/", "metropolitan/", "policydebate/", "sustainability/", "urban/", "urban_planning/"]
        

        #This function authenticates and log's in to the Twitterbot's 
        #Twitter account        
        def authenticate(self):
                auth = tp.OAuthHandler(self.CONSUMER_KEY, self.CONSUMER_KEY_SECRET)
                auth.set_access_token(self.ACCESS_TOKEN, self.ACCESS_TOKEN_SECRET)
                api = tp.API(auth)
                
                try:
                        api.verify_credentials()
                
                except:
                        print "Unable to authenticate"
                        
                else:
                        print "Authenticated"
                        return api
          
        #This function selects an image at random from the image 
        #directories and submits it to Microsoft Computer Vision API for 
        #analysis
        #It returns the chosen image and the description of the image provided
        #by the Microsoft Computer Vision API              
        def analyze_image(self):
                assert(self.subscription_key)
                analyze_url = self.vision_base_url+"analyze"
                directory = self.image_directory_names[random.randint(0,len(self.image_directory_names)-1)]
                path = self.images_path + directory
                image_array = [f for f in listdir(path) if isfile(join(path, f))]
                chosen_image = image_array[random.randint(0,len(image_array)-1)]
                chosen_image = path + chosen_image
                
                image_data = open(chosen_image, "rb").read()
                headers    = {'Ocp-Apim-Subscription-Key': self.subscription_key,
                              'Content-Type': 'application/octet-stream'}
                params     = {'visualFeatures': 'Categories,Description,Color'}
                response = requests.post(
                    analyze_url, headers=headers, params=params, data=image_data)
                response.raise_for_status()
                
                analysis = response.json()
                image_caption = analysis["description"]["captions"][0]["text"].capitalize()
                
                return chosen_image, image_caption
                
                
                
                        
                        
        #This is the main function of the program.
        #It follows a specific routine to handle the Twitter activity of 
        #the bot.
        #It's not currently the most aesthetically-pleasing function.
        #Efforts would be made to modularize it by splitting it into multiple
        #sub-functions :)
        '''
        ***********The routine*************
        * First, the bot initializes some useful boolean flags.
        * Next, it chooses a keyword at random from the KEYWORD array.
        * It calls the analyze_image function and gets back an image
          and its description
        * It posts the image and its description on Twitter.
        * It then waits for 4 hours.
        * After, it searches through the most recent tweets posted on Twitter
          for the top 15 tweets that contain the keyword that was chosen.
        * For each of the 15 tweets
                * It favorites the tweet
                * It follows the tweeter
                * If the tweet has never been retweeted, it screens the 
                  tweet for AVOID_WORDS
                * If the tweet is pure, it searches for keywords in the 
                  GREET_QUERY array and SAD_QUERY array and retweets accordingly
                  with those responses as comments to the retweet
                * If the tweet doesn't contain any of these words, it chooses
                  a phrase at random from the GREET_QUERY and retweets 
                  with that phrase as a comment to the retweet.
                *It  sleeps for 2 hours before checking out the next of the 15 
                  tweets.
        * After going through the 15 tweets, it sleeps for 10 hours and recalls
          the entire function.

        * It repeats this routine infinitely (Til the server is shutdown)
        '''
        def retweet_keyword(self):
                followed = False
                picture_posted = False
                global count
                key_index = random.randint(0,len(self.KEYWORD)-1)
                
                image, description = self.analyze_image()
                message = self.IMAGE_DESCRIPTION_PREFIX[random.randint(0, len(self.IMAGE_DESCRIPTION)-1)]+ str(description) + "."
                
                self.api.update_with_media(image, status=message)
                sleep(14400)
                for tweet in tp.Cursor(self.api.search, q=self.KEYWORD[key_index], tweet_mode = 'extended').items(15):
                        try:                                                                        
                                if not tweet.favorited:
                                        tweet.favorite()
                                
                                if self.follow_count >=3:
                                        if not followed:
                                                if not tweet.user.following:
                                                        tweet.user.follow()
                                                        self.follow_count = 0;
                                                        followed = True
                                
                                tweet_content = tweet.full_text
                                tweet_content = tweet_content.lower()
                                
                                greet_index = random.randint(0,len(self.GREETING)-1)
                                
                                if not tweet.retweeted:                                        
                                        found = False
                                        
                                        for word in self.AVOID_WORDS:
                                                if tweet_content.find(word) != -1:
                                                        self.DONT_TWEET = True
                                        
                                        if not self.DONT_TWEET:
                                                for word in self.GREET_QUERY:
                                                        if tweet_content.find(word) != -1:
                                                                count = count + 1
                                                                reply = self.GREETING[greet_index] + ' https://twitter.com/'+tweet.user.screen_name+'/status/'+tweet.id_str
                                                                self.api.update_status(status = reply)
                                                                found = True
                                                                break
                                                
                                                if not found:
                                                        if count < 3:
                                                                sad_index = random.randint(0,len(self.SAD_REPLY)-1)
                                                                for sad_word in self.SAD_QUERY:
                                                                        if tweet_content.find(sad_word) != -1:
                                                                                reply = self.SAD_REPLY[sad_index] + ' https://twitter.com/'+tweet.user.screen_name+'/status/'+tweet.id_str
                                                                                self.api.update_status(status = reply)
                                                                                break
                                                if not found:                                                                                               
                                                        if count < 2:
                                                                if greet_index%6 == 0:
                                                                        non_greet_index = random.randint(0,len(self.GREET_NON_REPLY)-1)
                                                                        rep = self.GREET_NON_REPLY[non_greet_index]+' https://twitter.com/'+tweet.user.screen_name+'/status/'+tweet.id_str
                                                                        self.api.update_status(status = rep)
                                                                        count = count + 1
                                                                else:
                                                                        tweet.retweet()
                                                                
                                                        else:
                                                                tweet.retweet()
                                        
                                        self.DONT_TWEET = False
                                sleep(14400)
                                
                        except tp.TweepError as e:
                                print(e.reason)
                        
                self.follow_count+=1;
                        
mybot = Bot()
while True:
        mybot.retweet_keyword()
        count = 0
        sleep(36000)















'''
credentials = []
inFile = open("credentials","r")
for line in inFile:
        credentials.append(line)

        
for x in credentials:
        print x
'''
