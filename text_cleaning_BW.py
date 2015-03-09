import re
import json
import warnings

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
	docbreak = re.sub(r"(CL,.*)",r"\1DOCBREAK",docbreak)

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

	def get_date(self):
		head = self.doc[:150]
		# import dateutil.parser.parse
		#Rewrite to catch only first five or six lines
		# These are some regexes to match parts of dates.
		month = r"\[*[A-Z][a-z]+"
		december = r"[Dd][ec]+[\.\']*"
		#This is something to try to catch misreadings of 12th, which seem really bad           
		messedUpDaySuffix = r" ?(?:.?.t*\?h)?"
		day = r"\d{1,2}" + messedUpDaySuffix
		dayOrNone = r"\d{0,2}" + messedUpDaySuffix
		year = r"1\d{3}"
		#Then create a number of regex from these elements. First run the ones that actually look for a day;
		#then run the wider net-casting ones that allow the day field to be empty and just give you "October 1789"
		possibleFormats = [
			r"(%s)\s.*(%s)\W*\s*(%s)" % (day, month, year),
			r"(%s)\s.*(%s)\W*\s(%s)" % (day, december, year),
			r"(%s)\s+\W*(%s).{0,5}\s*(%s)" % (month, day, year),
			r"(%s)\s+\W*(%s).{0,5}\s+(%s)" % (december, day, year),
			r"[\[1I](%s) (%s) (%s)[\[I1]" %(dayOrNone,month,year) ,
			r"(%s)\s(%s)\W*\s*(%s)" % (dayOrNone, month, year),
			r"(%s)\s+\W*(%s)(?<!Dale\s).{0,5}\s+(%s)" % (month, dayOrNone, year), #added the Dale reverse lookup
			]
		for reformat in possibleFormats:
			date = re.search(reformat,head)
			if date:
				rough = date.group(1) + ' ' + date.group(2) + ' ' + date.group(3)
				return rough
				



			#Uncomment this line to see what sort of expressions you're missing on.
			#warnings.warn("\n"+"\n"+"*"*100 + head[:200])
		return "Unknown"


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
	def does_this_look_suspicious(self):
		pass

if __name__=="__main__":
	generator = snippetyielder("v1.txt")
	for snippet in generator:
		snippet = generator.next()
		doc = Document(snippet)
		print doc.get_date()
		# f = open("date_test.txt", "a")
		# f.write(str(doc.get_date()) + '\t' + str(doc.raw_text()) + '\n')
		#  # + "_" + doc.author() + "\t" + doc.raw_text() + "\n") #change to integer ascending
		# f.close()

		# data = [ {'searchstring' : "To " + doc.recipient() + " from " + doc.author() + ", " + doc.get_date(), 
		# 'author': doc.author(), 'recipient': doc.recipient(), 'date': doc.get_date(), 'filename': doc.get_date() + "_" + doc.author()
		# }] #possibly add full text
		# data_string = json.dumps(data)
		# j = open("jsoncatalog.txt", "a")
		# j.write(data_string)
		# j.close()

	
	
