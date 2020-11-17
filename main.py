import tweepy

# Authenticate to Twitter
auth = tweepy.OAuthHandler("y9BC5MgmPBk9TDvCFzIcR4gMV", 
    "lBdsgS6jaFBbEiCPawPSgwQskfbD33mVrDMUcVhHcxErrNMDU1")
auth.set_access_token("4729544248-NrUJga5dzRVyu12l5Vj2VGbsbnBNzNQJ402k4cA", 
    "IbUgDt9mCkc7hCYsCP7KyiNdmKqcCpwd0mGcHs7aO6TT8")

api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")




f = open("import.txt", "w", encoding="utf-8")


for tweet in api.search(q="wolf AND (#ssbu OR ssbu)", lang="en", rpp=100, count=100, tweet_mode='extended'):
    print(f"{tweet.user.name}:{tweet.full_text}")
    f.write(str({tweet.full_text}) + "\n")

f.close