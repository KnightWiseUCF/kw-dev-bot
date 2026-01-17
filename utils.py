import discord
import datetime
import os

from dotenv import load_dotenv, dotenv_values 

TERMINATE = False

""" return varname from .env file """
def getEnvVar(varname):
	
	token = ""

	try:
		load_dotenv()
		token = os.getenv(varname)
	except IOError:
		token = ""
		print("Could not read {} from .env file.".format(varname))

	return token

""" get the Discord API token from .env """
def getToken():
	return getEnvVar("BOT_TOKEN")

""" get jwt secret from .env """
def getJwtSecret():
	return getEnvVar("JWT_SECRET")

""" get api route url from .env """
def getRoute():
	return getEnvVar("API_ROUTE")

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