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
		raw_text = re.sub(r"(.Am\. State Paper.*)",r"",raw_text) #eliminating citations
		raw_text = re.sub(r"(.*\[Statutes.*)",r"",raw_text) #eliminating citations
		raw_text = re.sub(r"(.*NYPL.*)",r"",raw_text) #eliminating citations
		raw_text = re.sub(r"(.*\[Treaties.*)",r"",raw_text) #eliminating citations
		raw_text = re.sub(r"(.*\[LC.*)",r"",raw_text) #eliminating citations
		raw_text = re.sub(r"(.*\[GAO.*)",r"",raw_text) #eliminating citations
		raw_text = re.sub(r"(N D A.*)",r"",raw_text) #eliminating citations
		raw_text = re.sub(r"\s",r" ", raw_text) #eliminating tabs etc.	
        	return raw_text

	def author(self):
		author = re.search(r"(.*To)(.*)(from\s)(.*)",self.doc)
		if author:
			author = author.group(4)
			author = re.sub(r"(\w+\s*\w+),.*",r"\1",author) #getting rid of following titles
			author = re.sub(r"Captain",r"",author) #getting rid of Captain
			author = re.sub(r"\.",r"_",author) #getting rid of periods in names 
			author = re.sub(r" ",r"",author) #Removing spaces to make it fit in the filename better
			return author
		else:
			return "Unknown"

	def recipient(self):
		recipient = re.search(r"(To )(.*)(from.*)",self.doc)
		if recipient:
			recipient = recipient.group(2)
			recipient = re.sub(r"(\w+\s*\w+),.*",r"\1",recipient) #attempting to clear out titles and such
			return recipient
		else:
			return "Unknown"
  
	def metadata(self):
		pass

	def get_date(self):
		date = re.search(r"(\d+)\s(\w\w\w+)\W*\s(\d{4})",self.doc)
		if date:
			 return date.group(1) + "-" + date.group(2) + "-" + date.group(3)
		else:
			return "Unknown"

	def does_this_look_suspicious(self):
		pass

if __name__=="__main__":
	generator = snippetyielder("v1.txt")
	for snippet in generator:
		snippet = generator.next()
		doc = Document(snippet)
		#print doc.author()
		f = open("input.txt", "a")
		f.write(doc.get_date() + "_" + doc.author() + "\t" + doc.raw_text() + "\n")
		f.close()

	
	
