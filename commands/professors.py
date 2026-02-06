import requests

import cfg
import utils

route = utils.getRoute()
admin = utils.getAdminKey()

async def get_unverified_professors(cmd):
    response = 'Unverified professor accounts:\n'
    headers = utils.get_headers(admin)
    r = requests.get("{}admin/unverifiedprofs".format(route), headers=headers)

    info = r.json()

    for p in info.keys():
        current_prof = info[p]
        response += "- ID: {}, Username: {}, Email: {}, Name: {} {}\n".format(
            current_prof['ID'],
            current_prof['USERNAME'],
            current_prof['EMAIL'],
            current_prof['FIRSTNAME'],
            current_prof['LASTNAME']
            )

    await utils.send_message(cmd.message.channel, response)

""" verify a professor with an id """
async def verify_professor(cmd):
    response = ''

    if cmd.tokens_count < 2:
        response = "Usage: `{}`".format(cfg.cmd_usages[cfg.cmd_verify_prof])

    else:
        headers = utils.get_headers(admin)
        r = requests.post("{}admin/verifyprof/{}".format(route, cmd.tokens[1]), headers=headers)
        if r.status_code > 201:
            response = "Error: Status Code {} ({})".format(r.status_code, r.reason)
        
        else:
            response = "Verified!"

    await utils.send_message(cmd.message.channel, response)