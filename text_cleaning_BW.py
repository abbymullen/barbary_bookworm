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

	def raw_text(self):
		doc = str(self.doc)
		raw_text = re.sub(r"\f.*[0-9]+",r"",doc) #using formfeed to get rid of some page numbers/running heads
		raw_text = re.sub(r"NAVAL OP.*",r"",raw_text) #eliminating more headers
		raw_text = re.sub(r"W.*B.*",r"",raw_text) #eliminating more headers
		raw_text = re.sub(r"(.*SDA.*)",r"",raw_text) #eliminating citations
		raw_text = re.sub(r"(.*NDA.*)",r"",raw_text) #eliminating citations
		raw_text = re.sub(r"(.*NR\&L.*)",r"",raw_text) #eliminating citations


                return raw_text

	def author(self):
		author = re.search(r"(.*To)(.*)(from\s)(.*)",self.doc)
		if author:
			return author.group(4)
		else:
			return "Unknown"

	def recipient(self):
		recipient = re.search(r"(To )(.*)(from.*)",self.doc)
		if recipient:
			recipient = recipient.group(2)
			recipient = re.sub(r"(\w+\s*\w+),.*",r"\1",recipient)
			return recipient
		else:
			return "Unknown"
  
	def metadata(self):
		pass

	def get_date(self):
		date = re.search(r"(\d+)\s(\w\w\w+)\W*\s(\d{4})",self.doc)
		if date:
			 return date.group(1) + " " + date.group(2) + " " + date.group(3)
		else:
			return "Unknown"

	def does_this_look_suspicious(self):
		pass

if __name__=="__main__":
	generator = snippetyielder("v1.txt")
	#for snippet in generator:
	snippet = generator.next()
	doc = Document(snippet)
	f = file.open("test_snippet_input.txt", "w")
	f.write(doc.get_date() + "_" doc.author() + "\t" + doc.raw_text())
	f.close()
		#print doc.recipient()
		#print doc.raw_text(snippet)
	
	
