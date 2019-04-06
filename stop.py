class Stop(object):
	def __init__(self, id, x, y):
		self.id = id
		self.x = x
		self.y = y
		self.passengers = []

	def add_passenger(self, passenger_id):
		self.passengers.append(passenger_id)