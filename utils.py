import discord
import datetime

TERMINATE = False

""" read a file named fname and return its contents as a string """
def getValueFromFileContents(fname):
	token = ""

	try:
		f_token = open(fname, "r")
		f_token_lines = f_token.readlines()

		for line in f_token_lines:
			line = line.rstrip()
			if len(line) > 0:
				token = line
	except IOError:
		token = ""
		print("Could not read {} file.".format(fname))
	finally:
		f_token.close()

	return token

""" get the Discord API token from the config file on disk """
def getToken():
	return getValueFromFileContents("token")

""" internal console log messages """
def logMsg(string):
    print("[{}] {}".format(datetime.datetime.now(), string))

    return string

""" send a message on discord """
async def send_message(channel, text = None, embed = None):
    try:
        if text is not None:
                                          
            return await channel.send(content=text)
        if embed is not None:
            return await channel.send(embed=embed)
    except discord.errors.Forbidden:
        logMsg('Could not message user: {}\n{}'.format(channel, text))
        raise
    except:
        logMsg('Failed to send message to channel: {}\n{}'.format(channel, text))

""" Find a chat channel by name in a server. might not need this """
def get_channel(server = None, channel_name = ""):
	channel = None

	for chan in server.channels:
		if chan.name == channel_name:
			channel = chan
	
	if channel == None:
		logMsg('Error: In get_channel(), could not find channel using channel_name "{}"'.format(channel_name))

	return channel