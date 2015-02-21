import re


f = open("v1.txt", 'r')
text = open('test.txt')
a = text.readlines()
p = "".join(a)

#detecting the breaks between documents and identifying them to break the docs with
docbreak = re.sub(r"(.*SDA.*)",r"\1DOCBREAK",p)
docbreak = re.sub(r"(.*NDA.*)",r"\1DOCBREAK",docbreak)
docbreak = re.sub(r"(.*NR\&L.*)",r"\1DOCBREAK",docbreak)
docbreak = re.sub(r"(.Am\. State Paper.*)",r"\1DOCBREAK",docbreak)
docbreak = re.sub(r"(.*\[Statutes.*)",r"\1DOCBREAK",docbreak)
docbreak = re.sub(r"(.*NYPL.*)",r"\1DOCBREAK",docbreak)
docbreak = re.sub(r"(.*\[Treaties.*)",r"\1DOCBREAK",docbreak)
docbreak = re.sub(r"(.*\[LC.*)",r"\1DOCBREAK",docbreak)
docbreak = re.sub(r"(.*\[GAO.*)",r"\1DOCBREAK",docbreak)

docbreaks = docbreak.split("DOCBREAK")

#yielding one document at a time
def snippetyielder(docbreaks):
	for doc in docbreaks:
		yield doc


generator = snippetyielder(docbreaks)

snippet = generator.next()

#defining a class to pull out stuff from the snippets
class Document():
	def __init__(self, doc):
		self.doc = doc

	def raw_text(self, doc):
		raw_text = re.sub(r"\f.*[0-9]+",r"",doc) #using formfeed to get rid of some page numbers/running heads
		raw_text = re.sub(r"NAVAL OP.*",r"",raw_text) #eliminating more headers
 		raw_text = re.sub(r"W.*B.*",r"",raw_text) #eliminating more headers
 		raw_text = re.sub(r"(.*SDA.*)",r"",raw_text) #eliminating citations
 		print raw_text

 	def author(self,doc):
 		author = re.search(r"[Ff]rom (\w \w)",doc)
 		print author


# 	def title(self, doc):
 #		title = 

# def metadata:

# def get_date:

# def does_this_look_suspicious:

text = Document(test)
for test in generator:
	print text.author(test)