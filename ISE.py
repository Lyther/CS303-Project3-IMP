import sys
import getopt
import random

N = 1000

def imp():
	pass

def ise_lt(network_file, seeds_file):
	sum = 0.0
	network_dict = create_dict(network_file)
	seeds_list = create_list(seeds_file)
	for i in range(N):
		sum += lt_sample(network_dict, seeds_list)
	return sum / N

def ise_ic(network_file, seeds_file):
	sum = 0.0
	network_dict = create_dict(network_file)
	seeds_list = create_list(seeds_file)
	for i in range(N):
		sum += ic_sample(network_dict, seeds_list)
	return sum / N

# The dictionary key is node 1, with value is a list of neighbours.
# node 1 -> [(neighbour node, weight), ...]
# Important: the dictionary should be directed!
def create_dict(network_file):
	network = network_file.read().splitlines()[1:]
	network_file.close()
	network_dict = {}
	for i in network:
		triple = i.split(' ')
		triple = [int(triple[0]), int(triple[1]), float(triple[2])]
		if triple[0] not in network_dict:
			network_dict[triple[0]] = []
		# if triple[1] not in network_dict:
		# 	network_dict[triple[1]] = []
		network_dict[triple[0]].append((triple[1], triple[2]))
		# network_dict[triple[1]].append((triple[0], triple[2]))
	return network_dict

def create_list(seeds_file):
	seeds = seeds_file.read().splitlines()
	seeds_file.close()
	seeds = [int(i) for i in seeds]
	return seeds

def lt_sample(network_dict, seeds_list):
	active_nodes = seeds_list.copy()
	activity_set = seeds_list.copy()
	thresh_dict = {}
	for i in network_dict:
		thresh_dict[i] = random.random()
		for j in network_dict[i]:
			if j[0] not in thresh_dict:
				thresh_dict[j[0]] = random.random()
	for i in thresh_dict:
		if thresh_dict[i] == 0:
			active_nodes.append(i)
			activity_set.append(i)
	count = len(activity_set)
	while activity_set:
		new_activity_set = []
		for i in activity_set:
			if i not in network_dict:
				continue
			for node, weight in network_dict[i]:
				if node in active_nodes:
					continue
				thresh_dict[node] -= weight
				if thresh_dict[node] <= 0:
					active_nodes.append(node)
					new_activity_set.append(node)
		count += len(new_activity_set)
		activity_set = new_activity_set.copy()
	return count

def ic_sample(network_dict, seeds_list):
	active_nodes = seeds_list.copy()
	activity_set = seeds_list.copy()
	count = len(activity_set)
	while activity_set:
		new_activity_set = []
		for i in activity_set:
			if i not in network_dict:
				continue
			for node, weight in network_dict[i]:
				if node in active_nodes:
					continue
				if random.random() < weight:
					active_nodes.append(node)
					new_activity_set.append(node)
		count += len(new_activity_set)
		activity_set = new_activity_set.copy()
	return count

def main(argv):
	network_file = ''
	seeds_file = ''
	model = ''
	time = ''
	try:
		opts, args = getopt.getopt(argv, "i:s:m:t:")
	except getopt.GetoptError:
		print('ISE.py –i <network> -s <seeds> -m <model> -t <time>')
		sys.exit(-1)
	for opt, arg in opts:
		if opt == '-i':
			network_file = open(arg, 'r')
		elif opt == '-s':
			seeds_file = open(arg, 'r')
		elif opt == '-m':
			model = arg
		elif opt == '-t':
			time = int(arg)
	if model == 'IC':
		print(ise_ic(network_file, seeds_file))
	elif model == 'LT':
		print(ise_lt(network_file, seeds_file))

if __name__ == "__main__":
	main(sys.argv[1:])