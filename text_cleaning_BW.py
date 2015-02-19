import re


f = open("v1.txt", 'r')
text = open('test.txt')
a = text.readlines()
p = "".join(a)
docbreak = re.sub(r"(.*SDA.*)",r"\1DOCBREAK",p)
docbreaks = docbreak.split("DOCBREAK")

def snippetyielder(docbreaks):
	for doc in docbreaks:
		yield doc
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

generator = snippetyielder(docbreaks)
test = generator.next()

#testdoc = open('testdoc.txt', 'r')

class Document():
	def __init__(self, doc):
		self.doc = doc

	def raw_text(self, doc):
		raw_text = re.sub(r"\f.*[0-9]+",r"",doc) #using formfeed to get rid of some page numbers/running heads
		raw_text = re.sub(r"NAVAL OP.*",r"",doc) #eliminating more headers
 		raw_text = re.sub(r"W.*B.*",r"",doc) #eliminating more headers
 		raw_text = re.sub(r"(.*SDA.*)",r"",doc) #eliminating citations
 		print raw_text


# def metadata:

# def get_date:

# def does_this_look_suspicious:

text = Document(test)
print text.raw_text(test)