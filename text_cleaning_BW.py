import re


#f = open("v1.txt", 'r')



def snippetyielder(file):
	with open(file, 'r') as text:
		for line in text:
			if re.match(r"(.*SDA.*)",line):
			 	re.sub(r"(.*SDA.*)",r"\1\f",line).split("\f")
			print line
			# elif re.match(r"(.*NDA.*)",line):
			# 	print line	
			# elif re.match(r"(.*NR\&L.*)",line):
			# 	print line
			# elif re.match(r"(.Am\. State Paper.*)",line):
			# 	print line
			# elif re.match(r"(.*\[Statutes.*)",line):
			# 	print line
			# elif re.match(r"(.*NYPL.*)",line):
			# 	print line
			# elif re.match(r"(.*\[Treaties.*)",line):
			# 	print line	
			# elif re.match(r"(.*\[LC.*)",line):
			# 	print line
			# elif re.match(r"(.*\[GAO.*)",line):
			# 	print line
	#print line


snippetyielder('test.txt')
# class document:
# 	def _init_(self, string):
# 		self.string = string

# 	def raw_text:

# 	def metadata:

# 	def get_date:

# 	def does_this_look_suspicious:
		



