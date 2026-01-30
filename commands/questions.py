import os
import time

from html2image import Html2Image
from discord import File

import cfg
import utils

route = utils.getRoute()
admin = utils.getAdminKey()

def html_from_str(html_str):
    hti = Html2Image(size=(1000,1000))
    time_now = time.time()
    hti.screenshot(html_str=html_str, css_str=cfg.css_str, save_as=cfg.temp_img)
    last_rendered = os.path.getmtime(cfg.temp_img)
    if (time_now > last_rendered):
        return None
    with open(cfg.temp_img, 'rb') as f:
        image = File(f)
    return image

async def preview_question(cmd):
    response = ''
    image = None

    if cmd.tokens_count < 2:
        response = "Usage: `{}`".format(cfg.cmd_usages[cfg.cmd_preview_question])
    
    else:
        html = cmd.message.content[len(cfg.cmd_preview_question)+2:]
        image = html_from_str(html)
        if image is None:
            response = "Failed to render HTML. Remember to enclose with quotes."
    
    await utils.send_message(cmd.message.channel, response, embed=image)

async def create_question(cmd):
    return