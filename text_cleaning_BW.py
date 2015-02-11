import re


#f = open("v1.txt", 'r')



def snippetyielder(file):
	with open(file, 'r') as text:
		for line in text:
			if re.match(r"(.*SDA.*)",line):
				line = re.sub(r"(.*SDA.*)",r"\1---",line)
				print line
				
	#print sub


snippetyielder('test.txt')
# class document:
# 	def _init_(self, string):
# 		self.string = string

# 	def raw_text:

# 	def metadata:

# 	def get_date:

# 	def does_this_look_suspicious:
		



