
import requests

import cfg
import utils

route = utils.getRoute()

""" temporary test command """
async def test(cmd):
    response = 'test'
    return await utils.send_message(cmd.message.channel, response)

""" count questions from topic name """
async def count_questions(cmd):

    response = ''

    if cmd.tokens_count < 2:
        response = "Usage: {}".format(cfg.usages[cfg.cmd_count_questions])
    
    else:
        # go thru list of topic
        found = False
        for t in cfg.topics:
            # topic hit
            if t.lower().startswith(cmd.tokens[1].lower()):
                found = True
                r = requests.get("{}test/topic/{}".format(route, t))
                if r.status_code != 200:
                    response = "Error: Status Code {}".format(r.status_code)
                else:
                    result = r.json()
                    # utils.logMsg(str(r.elapsed))
                    response = "{} questions found for topic '{}'".format(len(result), t)
                break
        
        if not found:
            response = "Topic not found. Here's a list: " + ", ".join(cfg.topics)
                

    return await utils.send_message(cmd.message.channel, response)