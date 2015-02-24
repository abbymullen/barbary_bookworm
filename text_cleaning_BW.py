import re

def snippetyielder(filename):
	text = open(filename, "r")
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
	docbreak = re.sub(r"(N D A.*)",r"\1DOCBREAK",docbreak)

	docbreaks = docbreak.split("DOCBREAK")

#yielding one document at a time
	for doc in docbreaks:
		yield doc




#defining a class to pull out stuff from the snippets
class Document():
	def __init__(self, doc):
		self.doc = doc

	def raw_text(self, doc):
		doc = str(doc)
		raw_text = re.sub(r"\f.*[0-9]+",r"",doc) #using formfeed to get rid of some page numbers/running heads
		raw_text = re.sub(r"NAVAL OP.*",r"",raw_text) #eliminating more headers
		raw_text = re.sub(r"W.*B.*",r"",raw_text) #eliminating more headers
		raw_text = re.sub(r"(.*SDA.*)",r"",raw_text) #eliminating citations
		raw_text = re.sub(r"(.*NDA.*)",r"",raw_text) #eliminating citations
		raw_text = re.sub(r"(.*NR\&L.*)",r"",raw_text) #eliminating citations


		print raw_text

	def author(self,doc):
		author = re.search(r"(.*To)(.*)(from\s)(.*)",doc)
		if author:
			print author.group(4)
		else:
			print "Unknown"

	def recipient(self, doc):
		recipient = re.search(r"(To )(.*)(from.*)",doc)
		if recipient:
			print recipient.group(2)
		else:
			print "Unknown"
  
	def metadata(self):
		pass

	def get_date(self, doc):
		date = re.search(r"(\d\d*)\s(\w\w\w+)\W*\s(\d{4})",doc)
		if date:
			print date.group(1), date.group(2), date.group(3)
		else:
			print "Unknown"

	def does_this_look_suspicious(self):
		pass

if __name__=="__main__":
	generator = snippetyielder("test.txt")
	for snippet in generator:
		snippet = generator.next()
		doc = Document(snippet)
		print doc.get_date(snippet)
		#print doc.raw_text(snippet)
	
	