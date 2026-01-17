import utils

""" temporary test command, move later TODO """
async def test(cmd):
    response = 'test'.format(cmd.message.author.id)
    return await utils.send_message(cmd.message.channel, response)
