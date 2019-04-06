from passenger import Passenger
from stop import Stop
import csv
import math

# Populate passengers list from csv
def read_passengers(in_file):
	passengers = []
	with open(in_file, 'r') as file:
		reader = csv.reader(file)
		for row in reader:
			try:
				passengers.append(Passenger(int(row[0]), int(row[1]), int(row[2])))
			except:
				pass
	return passengers

# Populate stops list from csv
def read_stops(in_file):
	stops = []
	with open(in_file, 'r') as file:
		reader = csv.reader(file)
		for row in reader:
			try:
				stops.append(Stop(int(row[0]), int(row[1]), int(row[2])))
			except:
				pass
	return stops

def get_distance(a, b):  # where a and b have attributes x and y
	return math.sqrt((a.x-b.x)**2+(a.y-b.y)**2)

# Return the distance to nearest stop and add closest stop attribute to passenger
# TODO: brute force right now, but could group passengers into quadrants to improve function
def get_closest_stop_distance(passenger, stops):
	closest_stop = None
	for stop in stops:
		tmp_distance = get_distance(passenger, stop)
		if not closest_stop or tmp_distance < closest_stop_distance:
			closest_stop = stop
			closest_stop_distance = tmp_distance
	passenger.closest_stop = closest_stop
	return closest_stop_distance

# Print as passenger_id, stop_id, distance
def print_closest_stop(passenger, stops):
	distance = get_closest_stop_distance(passenger, stops)
	print('%d, %d, %d' %(passenger.id, passenger.closest_stop.id, distance))

def add_passenger_to_stop(passenger, stops):
	if passenger.closest_stop is None:
		get_closest_stop_distance(passenger, stops)
	passenger.closest_stop.add_passenger(passenger.id)

def print_stop_passengers(stop):
	print('%d, %d' %(stop.id, len(stop.passengers)))

def get_stop_order(stops):
	# Try with each of the stops as the first stop
	best_order = []
	best_order_cost = None
	for stop in stops:
		# Fill to_visit list
		to_visit = []
		for s in stops:
			to_visit.append(s)

		curr_order = [stop]

		order_cost = 0  # total distance travelled with this route
		to_visit.remove(stop)
		curr_stop = stop

		# Iterate through stops until all stops have been visited
		while to_visit:
			best_cost = None
			next_stop = None

			# Iterate through remaining stops to find closest
			for neighbour in to_visit:
				curr_cost = get_distance(curr_stop, neighbour)
				if (not best_cost) or (curr_cost < best_cost):
					best_cost = curr_cost
					next_stop = neighbour

			curr_order.append(next_stop)
			to_visit.remove(next_stop)
			order_cost += best_cost
			curr_stop = next_stop

		if (best_order_cost is None) or (order_cost < best_order_cost):
			best_order = curr_order
			best_order_cost = order_cost

	return best_order


def get_route_distance(stops):
	distance = 0
	for i in range(0, len(stops) - 1):
		distance += get_distance(stops[i], stops[i+1])

	return distance

if __name__ == '__main__':
	passengers = read_passengers("passengers.csv")
	stops = read_stops("stops.csv")
	stops_to_visit = []

	print('Question 1')
	for passenger in passengers:
		# Assign each passenger a closest stop and get the distance
		print_closest_stop(passenger, stops)

		# Add to passenger list in stop object
		add_passenger_to_stop(passenger, stops)


	print('\nQuestion 2')
	for stop in stops:
		print_stop_passengers(stop)

		# Don't visit a stop if there are no passengers
		if len(stop.passengers) != 0:
			stops_to_visit.append(stop)

	
	print('\nQuestion 3')
	stop_order = get_stop_order(stops_to_visit)
	# Change list of objects to list of ids 
	stop_id_order = []
	for stop in stop_order:
		stop_id_order.append(stop.id)
	print(stop_id_order)

	print('\nQuestion 4')
	print('%d' % get_route_distance(stop_order))
