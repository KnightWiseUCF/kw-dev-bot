import os
import time
import requests
import asyncio

from html2image import Html2Image
from discord import File
from ast import literal_eval

import cfg
import utils

route = utils.getRoute()
admin = utils.getAdminKey()

question_add_temp_queue = []

""" helper for html previews """
def html_from_str(html_str):
    hti = Html2Image(size=(1000,1000), temp_path="C:/Users/Minerva/Desktop/Storage/Coding/!!SENIOR DESIGN/kw-dev-bot")
    time_now = time.time()
    hti.screenshot(html_str=html_str, css_str=cfg.css_str, save_as=cfg.temp_img)
    last_rendered = os.path.getmtime(cfg.temp_img)
    if (time_now > last_rendered):
        return None
    with open(cfg.temp_img, 'rb') as f:
        image = File(f)
    return image

""" takes input html and renders it to an image """
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

""" get a question from an input id and return info about it. """
async def get_question(cmd):
    response = ''
    image = None

    if cmd.tokens_count < 2:
        response = "Usage: `{}`".format(cfg.cmd_usages[cfg.cmd_get_question])

    else:
        headers = utils.get_headers(admin)
        r = requests.get("{}admin/problems/{}".format(route, cmd.tokens[1]), headers=headers)
        if r.status_code > 201:
            response = "Error: Status Code {} ({})".format(r.status_code, r.reason)
        
        else:
            info = r.json()
            answers = info["answers"]

            response += "Type: {} - Points: {} - Author: {} - OwnerID: {}\nSection {} - Category: {} - Subcategory: {}\n".format(
                info['TYPE'],
                info['POINTS_POSSIBLE'],
                info['AUTHOR_EXAM_ID'],
                info['OWNER_ID'],
                info['SECTION'],
                info['CATEGORY'],
                info['SUBCATEGORY'],
                )
            try:
                image = html_from_str(info['QUESTION_TEXT'])
            except:
                response += "Question Text:\n{}".format(info['QUESTION_TEXT'])

            for a in answers:
                response += "Answer (Correctness {} Priority {}): `{}`\n".format(a['IS_CORRECT_ANSWER'], a['PRIORITY'], a['TEXT'])

    await utils.send_message(cmd.message.channel, response, embed=image)

""" read a user's file upload and add it to the database as a set of questions """
async def create_question(cmd):
    response = ''
    image = None

    usage_text = "Usage: `{}`\nText file format:\n```{}```".format(cfg.cmd_usages[cfg.cmd_create_question], cfg.question_input_template)

    # default unless changed with arguments
    num_questions = 1
    i_separator = "\r\n$\r\n"
    q_separator = "\r\n***\r\n"

    tokens = cmd.tokens
    t_count = cmd.tokens_count

    # read args for question processing, all optional
    for t in range(t_count):
        # we dont really need the batch command
        if tokens[t] == "-batch" and t < t_count:
            if tokens[t+1].isdigit():
                num_questions = int(tokens[t+1])

        # custom separators
        elif tokens[t].endswith("info-separator") and t < t_count:
            i_separator = "\r\n{}\r\n".format(tokens[t+1])
        elif tokens[t].endswith("question-separator") and t < t_count:
            q_separator = "\r\n{}\r\n".format(tokens[t+1])
        
        # triggers usage text
        elif tokens[t].endswith("help"):
            cmd.attachments_count = 0

    # if theres no attachments, it will either be question confirmation, or return usage text
    if (cmd.attachments_count == 0):
        if (cmd.tokens_count == 2):
            if cmd.tokens[1].endswith("confirm"):
                # if the queue isnt empty, time to post whats in there
                q_count = len(question_add_temp_queue)
                ids = []
                if q_count > 0:
                    for q in question_add_temp_queue:
                        headers = utils.get_headers(admin)
                        
                        r = requests.post("{}admin/createquestion".format(route), headers=headers, json=q)

                        if r.status_code > 201:
                            response = "Error: Status Code {} ({})".format(r.status_code, r.reason)
                            return await utils.send_message(cmd.message.channel, response)
                        
                        ids.append(r.json()["questionId"])
                    
                    response = "Added {} questions to the database.\nIDs: {}".format(q_count, ids)

                else:
                    response = "There's nothing to confirm."
            elif cmd.tokens[1].endswith("clear"):
                question_add_temp_queue.clear()
                response = "Queue cleared."
            else:
                response = usage_text
        else:
            response = usage_text

    # read from attachment
    else:
        file = await cmd.attachments[0].read()

        questions = file.decode("utf-8").split(q_separator)
        q_count = 0
        for q in questions:
            raw_info = q.split(i_separator)

            try:
                current_question = {}
                current_question["type"] = raw_info[0]
                current_question["author_exam_id"] = raw_info[1]
                current_question["section"] = raw_info[2]
                current_question["category"] = raw_info[3]
                current_question["subcategory"] = raw_info[4]
                current_question["points_possible"] = float(raw_info[5])
                current_question["question_text"] = raw_info[6]
                current_question["owner_id"] = int(raw_info[7])

                # interpret lists
                current_question["answer_text"] = literal_eval(raw_info[8])
                current_question["answer_correctness"] = literal_eval(raw_info[9])
                current_question["answer_priority"] = literal_eval(raw_info[10])

                question_add_temp_queue.append(current_question)
            # if theres a valueerror, the input is probably improper
            except ValueError as err:
                response = "Error reading input: {}\nMake sure your formatting is as follows:\n```{}```".format(err, cfg.question_input_template)
                return await utils.send_message(cmd.message.channel, response)
            except KeyError as err:
                response = "Error reading input: {}\nMake sure your formatting is as follows:\n```{}```".format(err, cfg.question_input_template)
                return await utils.send_message(cmd.message.channel, response)

            if q_count == 0:
                image = html_from_str(current_question["question_text"])
            
            q_count += 1
            
        response = "Read {} questions from file upload. Please double-check your input and type `!addquestion confirm` to confirm (expires in 5 minutes).".format(q_count)
        await utils.send_message(cmd.message.channel, response, embed=image)

        await asyncio.sleep(cfg.expire_time)

        if len(question_add_temp_queue) != 0:
            question_add_temp_queue.clear()
            response = ""
            image = None
        
        else:
            return
    
    await utils.send_message(cmd.message.channel, response, embed=image)
