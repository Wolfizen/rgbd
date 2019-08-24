import animations.common as common

import fractions


class Anim:
	"""Draw rainbow that fades across all pixels at once."""

	def __init__(self, length, func, config):
		self.iters = 0
		self.length = length
		self.setpixel = func
		self.conf = config
		self.whole = self.conf.get("strip_as_whole", True)
		self.steps = self.conf.get("steps", self.length)
		self.colors = self._gen_wheel(self.steps)
		self.max_iters = self.length * self.steps // fractions.gcd(self.length, self.steps)

	@staticmethod
	def _gen_wheel(num):
		colors = []
		for i in range(num):
			colors.append(common.col_wheel(i, num))
		return colors

	def iter(self):
		if self.whole:
			for pos in range(self.length):
				self.setpixel(pos, self.colors[self.iters])
			self.iters = (self.iters + 1) % self.steps
		else:
			for pos in range(self.length):
				self.setpixel(pos, self.colors[(pos + self.iters) % self.steps])
			self.iters = (self.iters + 1) % self.max_iters
