import requests
import asyncio

import cfg
import utils

route = utils.getRoute()
admin = utils.getAdminKey()

deletion_target = None

""" helper for displaying user info from a json """
def user_info_str(info):
    return "Username: {}, ID: {}\nEmail: {}\nName: {} {}\nPassword (encrypted): `{}`".format(
        info['USERNAME'],
        info['ID'],
        info['EMAIL'],
        info['FIRSTNAME'],
        info['LASTNAME'],
        info['PASSWORD']
    )

""" get a user from an input id and return info about it. """
async def get_user(cmd):
    response = ''
    image = None
    usage_text = "Usage: `{}`".format(cfg.cmd_usages[cfg.cmd_get_user])

    if cmd.tokens_count < 3:
        response = usage_text

    else:
        body = {}
        if cmd.tokens[1].endswith('id'):
            body['id'] = cmd.tokens[2]
        elif cmd.tokens[1].endswith('name'):
            body['username'] = cmd.tokens[2]
        headers = utils.get_headers(admin)
        r = requests.get("{}admin/getuser".format(route), headers=headers, params=body)
        if r.status_code > 201:
            response = "Error: Status Code {} ({})".format(r.status_code, r.reason)
        
        else:
            info = r.json()
            response += user_info_str(info)

    await utils.send_message(cmd.message.channel, response, embed=image)

""" delete a user account """
async def delete_user(cmd):
    response = ''
    headers = utils.get_headers(admin)
    global deletion_target

    if cmd.tokens_count < 2:
        response = "Usage: `{}`".format(cfg.cmd_usages[cfg.cmd_delete_user])
    
    else:
        # if a confirmation is input, try and delete the user
        if cmd.tokens[1].endswith("confirm") and deletion_target is not None:
            target = deletion_target

            r = requests.delete("{}admin/users/{}".format(route, target), headers=headers)

            # utils.logMsg(r.elapsed)

            if r.status_code != 200:
                response = "Error: Status Code {} ({})".format(r.status_code, r.reason)
            
            else:
                response = "User deleted."
        
        elif cmd.tokens[1].endswith("clear") and deletion_target is not None:
            response = "Cleared."
            deletion_target = None
        
        # track down the user and give info
        else:
            target = cmd.tokens[1]

            r = requests.get("{}admin/getuser".format(route), headers=headers, json={'id': target})
            if r.status_code > 201:
                response = "Error: Status Code {} ({})".format(r.status_code, r.reason)
            else:
                # we found a user, show info and prompt for confirmation
                response += user_info_str(r.json())
            
                response += "\n\nPlease use `!deleteuser confirm` to finalize the deletion."

                deletion_target = target

                await utils.send_message(cmd.message.channel, response)

                await asyncio.sleep(cfg.expire_time)

                # only reset if its the same target
                if deletion_target == target:
                    deletion_target = None

    return await utils.send_message(cmd.message.channel, response)


""" create a user account """
async def create_user(cmd):
    tokens = cmd.tokens
    count = cmd.tokens_count
    
    if count < 3:
        response = "Usage: `{}`".format(cfg.cmd_usages[cfg.cmd_create_user])
    
    else:
        user = {
            "username": tokens[1],
            "email": tokens[2],
            "password": "password",
            "firstName": "First",
            "lastName": "Last",
            }

        if count >= 4:
            user["password"] = tokens[3]
        if count >= 5:
            user["firstName"] = tokens[4]
        if count >= 6:
            user["lastName"] = tokens[5]
        
        headers = {
            'Authorization': 'Bearer {}'.format(admin),
            'Content-Type': 'application/json'
        }

        r = requests.post("{}admin/createuser".format(route), headers=headers, json=user)

        if r.status_code > 201:
            response = "Error: Status Code {} ({})".format(r.status_code, r.reason)
            if r.status_code == 400:
                response += "\nUsername or email might already exist."
        
        else:
            response = "User created! ID: {}".format(r.json()["userId"])

    return await utils.send_message(cmd.message.channel, response)
