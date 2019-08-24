import animations.common as common


class Anim:
	"""Animation template.
	Must have a parent class Anim, that has an __init__ and an iter() function"""

	def __init__(self, length, func, config):
		self.length = length
		self.setpixel = func
		self.conf = config

	def iter(self):
		for i in range(self.length):
			self.setpixel(i, common.rgb(255, 0, 255))
