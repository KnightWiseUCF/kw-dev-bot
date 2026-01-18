import requests

import cfg
import utils

route = utils.getRoute()

""" temporary test command """
async def test(cmd):
    response = 'test'
    return await utils.send_message(cmd.message.channel, response)


""" print out a list of commands """
async def help(cmd):
    response = 'Command List:```'
    for c in cfg.cmd_descriptions.keys():
        response += "\n{}{}: {}\n\tUsage: {}".format(cfg.cmd_prefix, c, cfg.cmd_descriptions[c], cfg.cmd_usages[c])
    response += "```"
    return await utils.send_message(cmd.message.channel, response)


""" count questions from topic name """
async def count_questions(cmd):

    response = ''

    if cmd.tokens_count < 2:
        response = "Usage: `{}`".format(cfg.cmd_usages[cfg.cmd_count_questions])
    
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