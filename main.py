#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Given csv files of stop and passenger coordinates, find the closest stop(s)
for each passenger and generate optimized routes to most efficiently pick up
all of the passengers.
'''
from passenger import Passenger
from stop import Stop
import csv
import math

# Populate passengers list from csv
def read_passengers(in_file):
	passengers = {}
	with open(in_file, 'r') as file:
		reader = csv.reader(file)
		for row in reader:
			try:
				tmp = Passenger(int(row[0]), int(row[1]), int(row[2]))
				passengers[tmp.id] = tmp
			except:
				pass
	return passengers


# Populate stops list from csv
def read_stops(in_file):
	stops = {}
	with open(in_file, 'r') as file:
		reader = csv.reader(file)
		for row in reader:
			try:
				tmp = Stop(int(row[0]), int(row[1]), int(row[2]))
				stops[tmp.id] = tmp
			except:
				pass
	return stops


# Get distance between two objects with x and y attributes
def get_distance(a, b):
	return math.sqrt((a.x-b.x)**2+(a.y-b.y)**2)


# Add closest stop attribute to passenger and return distance
# TODO: group passengers into quadrants to improve speed
def get_closest_stop(passenger, stops):
	closest_stop = None
	for stop in stops:
		stop_distance = get_distance(passenger, stops[stop])
		if (not closest_stop) or (stop_distance < closest_stop_distance):
			closest_stop = stop
			closest_stop_distance = stop_distance
	passenger.closest_stop = closest_stop
	return closest_stop_distance


# Add in range stop attribute to passengers
def get_in_range_stops(passenger, stops, range):
	for stop in stops:
		if get_distance(passenger, stops[stop]) < range:
			passenger.add_in_range_stop(stop)
	# If no stops are in range, select closest stop
	if not passenger.in_range_stops:
		if not passenger.closest_stop:
			get_closest_stop(passenger, stops)
		passenger.add_in_range_stop(passenger.closest_stop)


# Print as passenger_id, stop_id, distance
def print_closest_stop(passenger, stops):
	distance = get_closest_stop(passenger, stops)
	print('%d, %d, %d' %(passenger.id, passenger.closest_stop, distance))


def add_passenger_to_stop(passenger, stops):
	if passenger.closest_stop is None:
		get_closest_stop(passenger, stops)
	stops[passenger.closest_stop].add_passenger(passenger.id)


# Print as stop_id, number_of_passengers
def print_stop_passengers(stop):
	print('%d, %d' %(stop.id, len(stop.passengers)))


def deepcopy(l):
	tmp = []
	for e in l:
		tmp.append(e)
	return tmp


# Get id of nearest stop
def get_next_stop(stop, to_visit, stops_dict):
	best_cost = None
	next_stop = None
	for neighbour in to_visit:
		cost = get_distance(stops_dict[stop], stops_dict[neighbour])
		if not best_cost or cost < best_cost:
			best_cost = cost
			next_stop = neighbour
	return next_stop


# Return an optimized order for visitin stops
def get_route(stops, stops_dict):
	best_order = []
	best_order_cost = None

	# Try each stop as the first stop in the route and compare cost
	for stop in stops:
		order_cost = 0  # total distance travelled with this route
		to_visit = deepcopy(stops)
		to_visit.remove(stop)
		curr_order = [stop]		
		curr_stop = stop

		# Iterate through stops until all stops have been visited
		while to_visit:
			next_stop = get_next_stop(curr_stop, to_visit, stops_dict)
			order_cost = get_distance(stops_dict[curr_stop], stops_dict[next_stop])

			curr_order.append(next_stop)
			to_visit.remove(next_stop)
			curr_stop = next_stop

		if (not best_order_cost) or (order_cost < best_order_cost):
			best_order = curr_order
			best_order_cost = order_cost

	return best_order


# Return reduced number of stops to visit by having passengers walk to further stops
def get_in_range_stops_to_visit(passengers, stops, range):
	freq = {}  # track number of passengers in range of stop
	for stop in stops:
		freq[stop] = 0

	stops_on_route = []
	passengers_not_on_route = deepcopy(passengers)

	# Add stops for passengers who can only reach one
	for passenger in passengers:
		get_in_range_stops(passengers[passenger], stops, range)

		in_range_stops = passengers[passenger].in_range_stops
		if len(in_range_stops) is 1 and in_range_stops[0] not in stops_on_route:
			stops_on_route.append(in_range_stops[0])
			passengers_not_on_route.remove(passenger)

	# Remove passengers who can reach one of the neccesary stops
	for passenger in passengers:
		if passenger in passengers_not_on_route:
			for stop in passengers[passenger].in_range_stops:
				if stop in stops_on_route:
					passengers_not_on_route.remove(passenger)

	# Fill frequency dictionary
	for passenger in passengers_not_on_route:
		for stop in passengers[passenger].in_range_stops:
			freq[stop] += 1

	# Use frequency dictionary to assign stops to rest of passengers
	for passenger in passengers:
		if passenger in passengers_not_on_route:
			on_route = False
			# Check if they can access one of the new stops
			for stop in passengers[passenger].in_range_stops:
				if stop in stops_on_route:
					passengers_not_on_route.remove(passenger)
					on_route = True
					break

			# Find the highest frequency stop, removing influence as it goes
			highest_freq = 0
			for stop in passengers[passenger].in_range_stops:
				best_stop = None
				if freq[stop] > highest_freq:
					highest_freq = freq[stop]
					best_stop = stop
				freq[stop] -= 1  # remove influence on frequency
		
			# Add the highest frequency stop
			if not on_route:
				stops_on_route.append(best_stop)
				passengers_not_on_route.remove(passenger)
	return stops_on_route


def get_route_distance(stops, stops_dict):
	distance = 0
	for i in range(0, len(stops) - 1):
		distance += get_distance(stops_dict[stops[i]], stops_dict[stops[i+1]])
	return distance


if __name__ == '__main__':
	passengers = read_passengers("passengers.csv")
	stops = read_stops("stops.csv")

	print('Question 1')
	for passenger in passengers:
		# Assign each passenger a closest stop and get the distance
		print_closest_stop(passengers[passenger], stops)
		# Add to passenger list in stop object
		add_passenger_to_stop(passengers[passenger], stops)

	print('\nQuestion 2')
	stops_on_route = []
	for stop in stops:
		print_stop_passengers(stops[stop])

		# Don't visit a stop if there are no passengers
		if len(stops[stop].passengers) != 0:
			stops_on_route.append(stop)

	print('\nQuestion 3')
	stop_order = get_route(stops_on_route, stops)
	print(stop_order)

	print('\nQuestion 4')
	print('%d' %(get_route_distance(stop_order, stops)))

	print('\nBonus')
	reduced_stops_on_route = get_in_range_stops_to_visit(passengers, stops, 250)
	print(len(reduced_stops_on_route))