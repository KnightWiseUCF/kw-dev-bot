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

