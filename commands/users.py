import requests

import cfg
import utils

route = utils.getRoute()
secret = utils.getJwtSecret()

""" delete a user account (TODO delete using the username) """
async def delete_user(cmd):
    response = ''

    if cmd.tokens_count < 2:
        response = "Usage: `{}`".format(cfg.cmd_usages[cfg.cmd_delete_user])
    
    else:
        target = cmd.tokens[1]

        headers = {
            'Authorization': 'Bearer {}'.format(secret),
        }

        r = requests.delete("{}users/{}".format(route, target), headers=headers)

        utils.logMsg(r.elapsed)

        if r.status_code != 200:
            response = "Error: Status Code {} ({})".format(r.status_code, r.reason)
        
        else:
            response = "User deleted."

    return await utils.send_message(cmd.message.channel, response)