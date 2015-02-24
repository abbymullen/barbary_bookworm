import re
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
			return recipient.group(2)
		else:
			return "Unknown"
  
	def metadata(self):
		pass

	def get_date(self):


                # These are some regexes to match parts of dates.
                month = r"[A-Z][a-z]+"
                #This is something to try to catch misreadings of 12th, which seem really bad
                
                messedUpDaySuffix = r" ?(?:.?.t\?h)?"
                day = r"\d{1,2}" + messedUpDaySuffix
                dayOrNone = r"\d{0,2}" + messedUpDaySuffix
                year = r"\d{4}"

                #Then create a number of regex from these elements. First run the ones that actually look for a day;
                #then run the wider net-casting ones that allow the day field to be empty and just give you "October 1789"
                possibleFormats = [
                        r"(%s)\s(%s)\W*\s(%s)" % (day, month, year),
                        r"(%s)\s+\W*(%s).{0,5}\s+(%s)" % (month, day, year),
                        r"[\[1I](%s) (%s) (%s)[\[I1]" %(dayOrNone,month,year) ,
                        r"(%s)\s(%s)\W*\s(%s)" % (dayOrNone, month, year),
                        r"(%s)\s+\W*(%s).{0,5}\s+(%s)" % (month, dayOrNone, year),
                ]

                
                #loop through the formats:
                
                for reformat in possibleFormats:
                        date = re.search(reformat,self.doc)
                        if date:
                                return date.group(1), date.group(2), date.group(3)


                #Uncomment this line to see what sort of expressions you're missing on.
                #warnings.warn("\n"+"\n"+"*"*100 + self.doc[:200])
                return None


	def does_this_look_suspicious(self):
		pass

if __name__=="__main__":
	generator = snippetyielder("test.txt")
	for snippet in generator:
		snippet = generator.next()
		doc = Document(snippet)
		print doc.get_date()
		#print doc.raw_text(snippet)
	
	
