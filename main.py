import discord
import sys
import asyncio
import time
import shlex

from dotenv import load_dotenv, dotenv_values

import utils
import cfg
import commands.general
import commands.users
import commands.questions

from models import Cmd

# map command names to their methods
cmd_map = {
    cfg.cmd_test: commands.general.test,
    cfg.cmd_help: commands.general.help,
    cfg.cmd_count_questions: commands.general.count_questions,
    cfg.cmd_delete_user: commands.users.delete_user,
    cfg.cmd_create_user: commands.users.create_user,
    cfg.cmd_preview_question: commands.questions.preview_question,
    cfg.cmd_create_question: commands.questions.create_question,
    cfg.cmd_get_question: commands.questions.get_question,
}

utils.logMsg('Starting up...')
init_complete = False

class MyClient(discord.Client):
    
    async def on_ready(self):
        
        # if already initialized, return
        global init_complete
        if init_complete:
            return
        init_complete = True

        # log client
        utils.logMsg('Logged in as {} ({}).'.format(client.user.name, client.user.id))

        time_now = int(time.time())

        # Every three hours we log a message saying the periodic task hook is still active. On startup, we want this to happen within about 60 seconds, and then on the normal 3 hour interval.
        time_last_logged = time_now - cfg.update_hookstillactive + 60

        utils.logMsg('Beginning periodic hook loop.')
        while not utils.TERMINATE:
            time_now = int(time.time())

            # Periodic message to log that this stuff is still running.
            if (time_now - time_last_logged) >= cfg.update_hookstillactive:
                time_last_logged = time_now

                utils.logMsg("Periodic hook still active.")
            
            # we can perform periodic actions here if need be
            
            await asyncio.sleep(15)


    async def on_message(self, message):
        
        """ do not interact with our own messages """
        if message.author.id == client.user.id or message.author.bot == True:
            return
        
        """ read messages with command prefix """
        if message.content.startswith(cfg.cmd_prefix):
            # tokenize the message. the command should be the first word.
            try:
                tokens = shlex.split(message.content)  # it's split with shlex now because shlex regards text within quotes as a single token
            except:
                tokens = message.content.split(' ')  # if splitting via shlex doesnt work (odd number of quotes), use the old splitting method so it doesnt give an exception

            tokens_count = len(tokens)
            command = tokens[0].lower().replace("!", "") if tokens_count >= 1 else ""

            # remove mentions to us
            mentions = list(filter(lambda user: user.id != client.user.id, message.mentions))

            attachments = message.attachments

            # Create command object
            cmd_obj = Cmd(
                tokens=tokens,
                message=message,
                client=client,
                mentions=mentions,
                attachments=attachments
            )

            # Check the main command map for the requested command.
            global cmd_map
            cmd_fn = cmd_map.get(command)

            if cmd_fn is not None:
                # Execute found command
                return await cmd_fn(cmd_obj)


# find our REST API token
token = utils.getToken()

if token == None or len(token) == 0:
    utils.logMsg('INSERT ERROR HERE')
    sys.exit(0)

# connect to discord and run indefinitely
try:
    intents = discord.Intents.default()
    intents.message_content = True
    client = MyClient(intents=intents)
    client.run(token)
finally:
    utils.TERMINATE = True
    utils.logMsg("Main thread terminated!")