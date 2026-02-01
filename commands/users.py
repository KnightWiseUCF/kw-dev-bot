import requests

import cfg
import utils

route = utils.getRoute()
admin = utils.getAdminKey()

""" get a user from an input id and return info about it. """
async def get_user(cmd):
    response = ''
    image = None
    usage_text = "Usage: `{}`".format(cfg.cmd_usages[cfg.cmd_get_user])

    if cmd.tokens_count < 3:
        response = usage_text

    else:
        body = {'id': None, 'username': None}
        if cmd.tokens[1].endswith('id'):
            body['id'] = cmd.tokens[2]
        elif cmd.tokens[1].endswith('name'):
            body['username'] = cmd.tokens[2]
        headers = utils.get_headers(admin)
        r = requests.get("{}admin/getuser".format(route), headers=headers, json=body)
        if r.status_code > 201:
            response = "Error: Status Code {} ({})".format(r.status_code, r.reason)
        
        else:
            info = r.json()
            response += "Username: {} - ID: {}\nEmail: {}\nName: {} {}\nPassword (encrypted): `{}`".format(
                info['ID'],
                info['USERNAME'],
                info['EMAIL'],
                info['FIRSTNAME'],
                info['LASTNAME'],
                info['PASSWORD']
                )

    await utils.send_message(cmd.message.channel, response, embed=image)

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
