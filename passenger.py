class Passenger(object):
	def __init__(self, id, x, y):
		self.id = id
		self.x = x
		self.y = y
		self.closest_stop = None
		self.in_range_stops = []

	def add_closest_stop(self, stop_id):
		self.stop = stop_id

	def add_in_range_stop(self, stop_id):
		self.in_range_stops.append(stop_id)