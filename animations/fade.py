import animations.common as common
import colour


class Anim:
	"""Fades through several colors. Can fade the entire zone at once, or scroll the colors across the zone."""

	def __init__(self, length, func, config):
		self.length = length
		self.setpixel = func
		self.conf = config
		self.wheel = self._gen_fade()
		# entire zone is one color vs the colors are set down the line
		self.as_whole = (self.conf.get("combine_zone") == True)
		self.iters = 0

	""" generates a color wheel to use for fading """
	def _gen_fade(self):
		cols = self.conf.get("colors")
		steps = self.conf.get("steps")
		if steps is None:
			steps = self.length

		colors = []

		for color in cols:
			colors.append(colour.Color(color))
		# to make it loop properly
		colors.append(colors[0])

		wheel = []
		prev = colors[0]
		for color in colors[1:]:
			wheel += list(prev.range_to(color, steps))[:-1] # ignore the last one of each range to prevent overlap
			prev = color

		# convert color objects to ints
		wheel = [common.from_colour(color) for color in wheel]

		return wheel

	def iter(self):
		if self.as_whole:
			ind = self.iters
		for i in range(self.length):
			if not self.as_whole:
				ind = (i + self.iters) % len(self.wheel)
			# noinspection PyUnboundLocalVariable
			self.setpixel(i, self.wheel[ind])
		self.iters = (self.iters + 1) % len(self.wheel)

