""" class to send general data about an interaction to a command """
class Cmd:
	cmd = ""
	tokens = []
	tokens_count = 0
	message = None
	client = None
	mentions = []
	mentions_count = 0
	attachments = []
	attachments_count = 0

	def __init__(
		self,
		tokens = [],
		message = None,
		client = None,
		mentions = [],
		attachments = [],
	):
		self.tokens = tokens
		self.message = message
		self.client = client
		self.mentions = mentions
		self.mentions_count = len(mentions)
		self.attachments = attachments
		self.attachments_count = len(attachments)


		if len(tokens) >= 1:
			self.tokens_count = len(tokens)
			self.cmd = tokens[0]