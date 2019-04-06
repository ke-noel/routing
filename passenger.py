class Passenger(object):
	def __init__(self, id, x, y):
		self.id = id
		self.x = x
		self.y = y
		self.closest_stop = None
		self.in_range_stops = None

	def add_closest_stop(self, stop_id):
		self.stop = stop_id

	def add_in_range_stops(self, stop_ids):
		self.in_range_stops = stop_ids