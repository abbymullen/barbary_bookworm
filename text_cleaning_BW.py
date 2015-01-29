import re


f = open("v1.txt", 'r')


#running headers regexes: this regex works in Pythex
regex = re.compile('.WARS .*')

# This might be the problem
for line in f:
	header = regex.findall(line)
	for word in header:
		print word
