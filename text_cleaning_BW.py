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
# 			# elif re.match(r"(.*NDA.*)",line):
# 			# 	print line	
# 			# elif re.match(r"(.*NR\&L.*)",line):
# 			# 	print line
# 			# elif re.match(r"(.Am\. State Paper.*)",line):
# 			# 	print line
# 			# elif re.match(r"(.*\[Statutes.*)",line):
# 			# 	print line
# 			# elif re.match(r"(.*NYPL.*)",line):
# 			# 	print line
# 			# elif re.match(r"(.*\[Treaties.*)",line):
# 			# 	print line	
# 			# elif re.match(r"(.*\[LC.*)",line):
# 			# 	print line
# 			# elif re.match(r"(.*\[GAO.*)",line):
# 			# 	print line
# 	#print line
# 				#print line

t = snippetyielder(docbreaks)

txt = open('snippets.txt', 'w')
txt.write(t)

#testdoc = open('testdoc.txt', 'r')

# class Document(object):
# 	def __init__(self, doc):
# 		self.doc = doc

# 	def raw_text(self, doc):

# 		doc = doc.readlines()
# 		j = "".join(doc)
# 		raw_text = re.sub(r"\f.*[0-9]+",r"",j) #using formfeed to get rid of some page numbers/running heads
# 		raw_text = re.sub(r"NAVAL OP.*",r"",j) #eliminating more headers
#  		raw_text = re.sub(r"W.*B.*",r"",j) #eliminating more headers
#  		print raw_text


# def metadata:

# def get_date:

# def does_this_look_suspicious:

trial_doc = Document(t)

print trial_doc.raw_text(trial_doc)