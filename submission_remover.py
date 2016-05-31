import praw
import time


def is_mod_of_sub(subreddit, user):
	mods = subreddit.get_moderators()
	for mod in mods:
		if str(mod) == str(user):
			return True
	return False


def gen_log(data):
	f = open(LOGFILE, 'a')
	datetime =  str(time.strftime("%Y/%m/%d")) + " " + str(time.strftime("%H:%M:%S"))
	f.write(datetime + ": " + data + "\n")
	f.close()
	print datetime + ": " + data


### MAIN #######################################################

USERNAME=''
PASSWORD=''
LOGFILE='/home/pandemic/Documents/scripts/remove_posts/remove_posts.log'
rules = ['one',
	'two',
	'three',
	'four']
r = praw.Reddit("Submission remover by /u/Pandemic21")
r.login(USERNAME,PASSWORD,disable_warning="True")

while 1:
	messages = r.get_unread()
	for message in messages:
		gen_log("New removal request. Author: " + str(message.author) + ", Subject: " + message.subject + ", Body: " + message.body)
		perform_removal = True
		failure_reply = ""
		message.mark_as_read()

		try:
			submission = r.get_submission(url=message.body)
			#make sure the subject is a valid rule
			if not int(message.subject)-1 < len(rules):
				gen_log("Removal aborted, not a valid rule. Rule: " + message.subject)
				failure_reply = failure_reply + "Not a valid rule number, please try again. Make sure the subject is **only** a single number, and nothing else.\n\n"
				perform_removal = False
			#make sure the person sending PM is a mod of the sub
			if not is_mod_of_sub(submission.subreddit, str(message.author)):
				gen_log("Removal aborted, user sending PM not a mod. PM author: " + str(message.author) + ", Subreddit: " + str(submission.subreddit))
				failure_reply = failure_reply + "The submission is in a subreddit of which you are not a mod.\n\n"
				perform_removal = False
			#make sure the bot is mod of the sub
			if not is_mod_of_sub(submission.subreddit, USERNAME):
				gen_log("Removal aborted, bot is not a mod. Subreddit: " + str(submission.subreddit))
				failure_reply = failure_reply + "The submission is in a subreddit of which this bot is not a mod.\n\n"
				perform_removal = False
			if perform_removal:
				gen_log("Comment removal success.")
				submission.add_comment(rules[int(rule)-1])
				submission.remove()
				message.reply("Submission has been removed.")
			if not perform_removal:
				message.reply(failure_reply)
		except Exception as e:
			gen_log("Removal failure, exception: " + str(e))
			message.reply("Something went wrong, please try again. Make sure to include **only** the URL in the body, and **only** the rule number in the subject.")

	time.sleep(60)





