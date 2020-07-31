import praw
import requests
import os.path

'''
===================================== ABOUT ===================================

Running the python script downloads videos into a folder with path:
./downloads/*subreddit name*/*id.extension*

A tracker file is also created and appends the links to the reddit posts with
its correlating file name

==================================== TO DO ====================================

- Be able to download videos hosted on reddit
- GUI

'''

#================================= Functions ==================================

def download(subreddit_name, lim):	# args: subreddit name, number of posts to download
	print("Started download")

	subreddit = reddit.subreddit(subreddit_name)
	subreddit_section = subreddit.hot(limit=lim)

	if not os.path.isdir("downloads/" + subreddit_name):
		os.makedirs("downloads/" + subreddit_name)

	if not os.path.exists("downloads/" + subreddit_name + "/tracker.txt"):
		open("downloads/" + subreddit_name + "/tracker.txt", "x")

	for submission in subreddit_section:
		if submission.stickied:		# make sure submission is not pinned
			continue

		if submission.is_self:		# make sure submission is not text
			continue

		# get media url (not reddit url)

		url = submission.url

		if "imgur.com" in url:		# specific e.g.: https://i.imgur.com/89EA5fE.gifv
			if url[-5:] == ".gifv":			
				url = url[:url.rfind(".")] + ".mp4"
			file_name = "(imgur) " + str(url)[url.rfind("/") + 1:]
		elif "giphy.com" in url:	# specific e.g.: https://media.giphy.com/media/W35nvFeYMwbR6xvx0r/giphy.gif
			file_name = "(giphy) " + url[url.rfind("/", 0, url.rfind("/")) + 1:url.rfind("/")] + url[url.rfind("."):]
		else:
			file_name = str(url)[url.rfind("/") + 1:]

		path = "downloads/" + subreddit_name + "/" + file_name

		# if the submission does not already exist, download it

		if not os.path.isfile(path):
			try:
				r = requests.get(url, allow_redirects=True)
				open(path, "wb").write(r.content)
				open("downloads/" + subreddit_name + "/tracker.txt", "a").\
					write(file_name + " : " + submission.permalink + "\n")
			except:
				print("An error occurred with: " + submission.permalink)

	print("Finished downloading")

#================================ Main Program ================================

reddit = praw.Reddit(client_id = "",
					 client_secret = "",
					 username = "",
					 password = "",
					 user_agent = "Bulk Media Downloader")

download("memes", 20)