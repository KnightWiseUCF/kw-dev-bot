import utils

""" temporary test command, move later TODO """
async def test(cmd):
    response = 'test'
    return await utils.send_message(cmd.message.channel, response)
