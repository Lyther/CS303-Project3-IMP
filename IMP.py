import sys
import getopt
import random
import ISE
import time as t

EPOCH = 100
N = 16
MUT_RATE = 0.02


# network is a dict from node to list of tuple
# the structure of tuple is (node, weight)
def imp(network, seed_count, model, network_file_name, time):
	start = t.time()
	generation = [random.sample(list(network.keys()), seed_count) for i in range(N)]
	for i in range(EPOCH):
		# print('running epoch', i, 'for current time', t.time() - start)
		if t.time() - start > time - 5:
			break
		genetic(generation, network, seed_count, model, network_file_name)
	return generation[0]


def genetic(generation, network, seed_count, model, network_file_name):
	seed_list = list(network.keys())
	# generate generation gene pool
	gene_pool = []
	for i in generation[:N // 2]:
		for j in i:
			if j not in gene_pool:
				gene_pool.append(j)
	# if gene pool is too small, append to enlarge
	while len(gene_pool) < seed_count:
		gene_pool.append(random.choice(seed_list))
	# hybrid N // 4 from previous generation
	for i in range(N // 4):
		generation[N // 2 + i] = random.sample(gene_pool, seed_count)
	# randomly pick new unit from seed list
	for i in range(N - N // 4 - N // 2):
		generation[N // 4 + N // 2 + i] = random.sample(seed_list, seed_count)
	# mutate to enlarge the gene pool
	for i in range(N):
		for j in range(len(generation[i])):
			if random.uniform(0, 1) < MUT_RATE:
				generation[i][j] = random.choice(seed_list)
	# measure the fitness
	fitness = [0 for i in range(N)]
	for i in range(N):
		if model == 'IC':
			fitness[i] = calculate_ise(network_file_name, generation[i], 'IC')
		elif model == 'LT':
			fitness[i] = calculate_ise(network_file_name, generation[i], 'LT')
	# pass the fittest N // 2 units to next generation
	for i in range(N // 2):
		maximum = 0
		index = 0
		for j in range(len(fitness)):
			if fitness[j] > maximum:
				maximum = fitness[j]
				index = j
		generation[i] = generation[index].copy()
		fitness[index] = 0


def main(argv):
	network_file = ''
	network_file_name = ''
	seed_count = 0
	model = ''
	time = 0
	try:
		opts, args = getopt.getopt(argv, "i:k:m:t:")
	except getopt.GetoptError:
		print('IMP.py –i <network> -k <seedCount> -m <model> -t <time>')
		sys.exit(-1)
	for opt, arg in opts:
		if opt == '-i':
			network_file = open(arg, 'r')
			network_file_name = arg
		elif opt == '-k':
			seed_count = int(arg)
		elif opt == '-m':
			model = arg
		elif opt == '-t':
			time = int(arg)
	network = create_dict(network_file)
	seeds = imp(network, seed_count, model, network_file_name, time)
	for i in seeds:
		print(i)
	# print('Result:', calculate_ise(network_file_name, seeds, model))


def create_dict(network_file):
	dictionary = {}
	lines = network_file.readlines()[1:]
	for line in lines:
		triple = line.rstrip().split(' ')
		triple[0] = int(triple[0])
		triple[1] = int(triple[1])
		triple[2] = float(triple[2])
		if triple[0] not in dictionary:
			dictionary[triple[0]] = [(triple[1], triple[2]), ]
		else:
			dictionary[triple[0]].append((triple[1], triple[2]))
	return dictionary


def calculate_ise(network_file_name, seeds, model):
	cache_file = '/tmp/seeds.txt'
	f = open(cache_file, 'w')
	for seed in seeds:
		print(seed, file=f)
	f.close()
	network_file = open(network_file_name, 'r')
	seeds_file = open(cache_file, 'r')
	if model == 'IC':
		return ISE.ise_ic(network_file, seeds_file)
	elif model == 'LT':
		return ISE.ise_lt(network_file, seeds_file)


if __name__ == "__main__":
	main(sys.argv[1:])
