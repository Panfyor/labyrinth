

class Cell:
	"""
	This class - CELL, which has
	position: (x,y)
	content : str # empty, wormhole, etc.
	"""
	def __init__(self, content='empty', position=None):
		"""

		Parameters
		----------
		content
		position
		"""
		self.content = content
		self.position = position