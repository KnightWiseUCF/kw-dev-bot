import requests

import cfg
import utils

route = utils.getRoute()
admin = utils.getAdminKey()


""" delete a user account (TODO find id via username) """
async def delete_user(cmd):
    response = ''

    if cmd.tokens_count < 2:
        response = "Usage: `{}`".format(cfg.cmd_usages[cfg.cmd_delete_user])
    
    else:
        target = cmd.tokens[1]

        headers = {
            'Authorization': 'Bearer {}'.format(admin)
        }

        r = requests.delete("{}admin/users/{}".format(route, target), headers=headers)

        # utils.logMsg(r.elapsed)

        if r.status_code != 200:
            response = "Error: Status Code {} ({})".format(r.status_code, r.reason)
        
        else:
            response = "User deleted."

    return await utils.send_message(cmd.message.channel, response)


""" create a user account """
async def create_user(cmd):
    tokens = cmd.tokens
    count = cmd.tokens_count
    
    if count < 2:
        response = "Usage: `{}`".format(cfg.cmd_usages[cfg.cmd_create_user])
    
    else:
        user = {
            "username": tokens[1],
            "email": "dummy@knightwise.dev",
            "password": "password",
            "firstName": "First",
            "lastName": "Last",
            }

        if count >= 3:
            user["password"] = tokens[2]
        if count >= 4:
            user["email"] = tokens[3]
        if count >= 5:
            user["firstName"] = tokens[4]
        if count >= 6:
            user["lastName"] = tokens[5]
        
        headers = {
            'Authorization': 'Bearer {}'.format(admin),
            'Content-Type': 'application/json'
        }

        r = requests.post("{}admin/createuser".format(route), headers=headers, json=user)

        if r.status_code >= 201:
            response = "Error: Status Code {} ({})".format(r.status_code, r.reason)
        
        else:
            response = "User created! ID: {}".format(r.text)

    return await utils.send_message(cmd.message.channel, response)
