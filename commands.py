import utils
import requests

import cfg

route = ""

""" temporary test command """
async def test(cmd):
    response = 'test'
    return await utils.send_message(cmd.message.channel, response)

""" get questions from topic name """
async def get_questions_from_topic(cmd):
    usage = ""
    
    response = ''

    if cmd.tokens_count < 2:
        response = usage

    return await utils.send_message(cmd.message.channel, response)