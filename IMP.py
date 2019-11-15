import sys
from math import *
import getopt
import random
import ISE


# network is a dict from node to list of tuple
# the structure of tuple is (node, weight)
# in default, take epsilon as 0.5 and lemma as 1
def imm(network, k, epsilon, lemma):
	lemma = lemma * (1 + log(2, len(network)))
	r = sampling(network, k, epsilon, lemma)
	s = node_selection(r, k, network)
	return s


def node_selection(r, k, network):
	s = []
	for i in range(k):
		maximum = 0
		vertex = 0
		for v in network.keys():
			diff = f(r, s + [v]) - f(r, s)
			if diff > maximum:
				vertex = v
				maximum = diff
		s.append(vertex)
	return s


def sampling(network, k, epsilon, lemma):
	r = []
	lb = 1
	n = len(network)
	_epsilon = epsilon * sqrt(2)
	for i in range(1, int(log2(n))):
		x = n / pow(2, i)
		theta = (2 + 2 / 3 * _epsilon) * (
				log10(factorial(n) / (factorial(k) * factorial(n - k))) + lemma * log10(n) + log10(log2(n))) * n / pow(
			_epsilon, 2) / x
		while len(r) <= theta:
			v = pick(network)
			r.append(generate(network, v))
		s = node_selection(r, k, network)
		if n * f(r, s) >= (1 + _epsilon) * x:
			lb = n * f(r, s) / (1 + _epsilon)
			break
	alpha = sqrt(lemma * log10(n) + log10(2))
	beta = sqrt((1 - 1 / e) * (log10(factorial(n) / (factorial(k) * factorial(n - k))) + lemma * log10(n) + log10(2)))
	theta = (2 * n * pow((1 - 1 / e) * alpha + beta, 2) * pow(epsilon, -2)) / lb
	while len(r) <= theta:
		v = pick(network)
		r.append(generate(network, v))
	return r


def pick(network):
	return random.choice(list(network.keys()))


def generate(network, v):
	ls = []
	for i in network[v]:
		ls.append(i[0])
	return ls


# this return the fraction of RR sets in r that are
# covered by a node set s
# two sets cover each other if r & s != empty
def f(r, s):
	count = 0
	for rr in r:
		cache = [i for i in rr if i in s]
		if cache:
			count = count + 1
	return count / len(r)


def main(argv):
	network_file = ''
	network_file_name = ''
	seed_count = 0
	model = ''
	time = ''
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
	network = {}
	if model == 'IC':
		network = create_dict('IC', network_file)
	elif model == 'LT':
		network = create_dict('LT', network_file)
	seeds = imm(network, seed_count, 0.5, 1)
	calculate_ise(network_file_name, seeds, model, time)


def create_dict(model, network_file):
	dict = {}
	lines = network_file.readlines()[1:]
	for line in lines:
		triple = line.rstrip().split(' ')
		triple[0] = int(triple[0])
		triple[1] = int(triple[1])
		triple[2] = float(triple[2])
		if model == 'IC':
			if triple[0] not in dict:
				dict[triple[0]] = [(triple[1], triple[2]), ]
			else:
				dict[triple[0]].append((triple[1], triple[2]))
		if model == 'LT':
			if triple[1] not in dict:
				dict[triple[1]] = [(triple[0], triple[2]), ]
			else:
				dict[triple[1]].append((triple[0], triple[2]))
	return dict


def calculate_ise(network_file_name, seeds, model, time):
	cache_file = 'seeds.txt'
	f = open(cache_file, 'w')
	for seed in seeds:
		print(seed, file=f)
	f.close()
	network_file = open(network_file_name, 'r')
	seeds_file = open(cache_file, 'r')
	if model == 'IC':
		print(ISE.ise_ic(network_file, seeds_file))
	elif model == 'LT':
		print(ISE.ise_lt(network_file, seeds_file))


if __name__ == "__main__":
	main(sys.argv[1:])
