import re
import json
import warnings
import dateutil.parser
from datetime import *
DEFAULT = datetime(1798,1,1)

def snippetyielder(filename):
	text = open(filename, "r")
	a = text.readlines()
	p = "".join(a)

    #detecting the breaks between documents and identifying them to break the docs with
	docbreak = re.sub(r"(.*SDA.*)",r"\1DOCBREAK\n",p)
	docbreak = re.sub(r"(.*NDA.*)",r"\1DOCBREAK\n",docbreak)
	docbreak = re.sub(r"(.*NR\&L.*)",r"\1DOCBREAK\n",docbreak)
	docbreak = re.sub(r"(.Am\. State Paper.*)",r"\1DOCBREAK\n",docbreak)
	docbreak = re.sub(r"(.*\[Statutes.*)",r"\1DOCBREAK\n",docbreak)
	docbreak = re.sub(r"(.*NYPL.*)",r"\1DOCBREAK\n",docbreak)
	docbreak = re.sub(r"(.*\[Treaties.*)",r"\1DOCBREAK\n",docbreak)
	docbreak = re.sub(r"(.*\[LC.*)",r"\1DOCBREAK\n",docbreak)
	docbreak = re.sub(r"(.*\[GAO.*)",r"\1DOCBREAK\n",docbreak)
	docbreak = re.sub(r"(N D A.*)",r"\1DOCBREAK\n",docbreak)
	docbreak = re.sub(r"(CL,.*)",r"\1DOCBREAK\n",docbreak)
	docbreak = re.sub(r"(NA. SDA. CL.*)",r"\1DOCBREAK\n",docbreak)
	docbreak = re.sub(r"(\[*HA.*)",r"\1DOCBREAK\n",docbreak)
	docbreak = re.sub(r"(\[*WDA.*)",r"\1DOCBREAK\n",docbreak)
	docbreak = re.sub(r"(\[*MCA.*)",r"\1DOCBREAK\n",docbreak)
	docbreak = re.sub(r"(DOCBREAK)+",r"DOCBREAK\n",docbreak)
	
	docbreaks = docbreak.split("DOCBREAK")

    #yielding one document at a time
	for doc in docbreaks:
		if re.search(r".+",doc):
			yield doc

#defining a class to pull out stuff from the snippets
class Document():
	def __init__(self, doc):
		self.doc = doc

	def test(self):
		return self.doc + 'BREAK\n'

	def raw_text(self):
		
		raw_text = re.sub(r"\f.*[0-9]+",r"",self.doc) #using formfeed to get rid of some page numbers/running heads
		raw_text = re.sub(r"(.*SDA.*)",r"",raw_text) #eliminating citations
		raw_text = re.sub(r"(.*NDA.*)",r"",raw_text) #eliminating citations
		raw_text = re.sub(r"(.*NR\&L.*)",r"",raw_text) #eliminating citations
		raw_text = re.sub(r"(.Am\. State Paper.*)",r"",raw_text) #eliminating citations
		raw_text = re.sub(r"(.*\[Statutes.*)",r"",raw_text) #eliminating citations
		raw_text = re.sub(r"(.*NYPL.*)",r"",raw_text) #eliminating citations
		raw_text = re.sub(r"(.*\[*Treaties.*)",r"",raw_text) #eliminating citations
		raw_text = re.sub(r"(.*\[*LC.*)",r"",raw_text) #eliminating citations
		raw_text = re.sub(r"(.*\[*GAO.*)",r"",raw_text) #eliminating citations
		raw_text = re.sub(r"(.*\[*N D A.*)",r"",raw_text) #eliminating citations
		raw_text = re.sub(r".*\[*(NA.*)",r"",raw_text) #eliminating citations
		
		raw_text = re.sub(r"NAVAL OP.*",r"",raw_text) #eliminating more headers
		raw_text = re.sub(r"W.*B.*",r"",raw_text) #eliminating more headers
		raw_text = re.sub(r"\s",r" ", raw_text) #eliminating tabs etc.	
		return raw_text


	def get_date(self):
		head = self.doc[:175]
		# import dateutil.parser.parse
		# These are some regexes to match parts of dates.
		month = r"\[*[A-Z][a-z]+"
		december = r"[Dd][ec]+"
		#This is something to try to catch misreadings of 12th, which seem really bad           
		messedUpDaySuffix = r" ?(?:.?.t\?h)?"
		day = r"\d{1,2}\**" + messedUpDaySuffix
		dayOrNone = r"\d{0,2}" + messedUpDaySuffix
		year = r"[I1]\d{3}"
		#Then create a number of regex from these elements. First run the ones that actually look for a day;
		#then run the wider net-casting ones that allow the day field to be empty and just give you "October 1789"
		
		def reorder(rough):
			# return rough
			clean = re.sub(r"[1I](\d{2}) ",r"\1",rough)
			clean = re.sub(r"I(\d{3})",r"1\1",clean)
			clean = re.sub(r"[\[\.\"]",r"",clean)
			clean = re.sub(r"[A-Za-z\d]*(\d{4}).",r" \1",clean)
			
			clean = re.sub(r"\s+",r" ",clean)
			clean = re.sub(r"Dep[tf]",r"",clean)
			clean = re.sub(r"[\'@\*\?\)\%\+]",r"",clean)
			clean = re.sub(r"(\d{1,2})[A-Za-z]*",r"\1",clean)
			clean = re.sub(r"^\s",r"",clean)
			clean = re.sub(r"([A-Za-z])\s([A-Za-z\d]+)(\d{4})",r"\1 \2 \3",clean)
			clean = re.sub(r",",r" ",clean)
			

			# if re.search(r"[A-Za-z]*\s*(.{0,2})\s([A-Za-z]+)\s(\d{4})",clean):
			# 	reorder = re.sub(r"[A-Za-z]*\s*(.{0,2})\s+([A-Za-z]+)\s+(\d{4})",r"\3 \2 \1",clean)
			# 	reorder = re.sub(r"(\d{4}) ([A-Za-z]+) ([A-Za-z\W]+)",r"\1 \2",reorder)
			# 	reorder = re.sub(r"\,",r"",reorder)
			# 	return reorder
			# if re.search(r"[A-Za-z]*\s*([A-Za-z]+)\s(.{0,2})\s(\d{4})",clean):
			# 	reorder = re.sub(r"([A-Za-z]+)\s+(.{0,2})\s+(\d{4})",r"\3 \1 \2",clean)
			# 	reorder = re.sub(r"(\d{4}) ([A-Za-z]+) ([A-Za-z\W]+)",r"\1 \2",reorder)
			# 	reorder = re.sub(r"\,",r"",reorder)
			# 	return reorder
			if re.search(r"(\d{0,2}) ([A-Za-z]+)\s+(\d{4})",clean):
				reorder = re.sub(r"(\d{0,2}) ([A-Za-z]+)\s+(\d{4})",r"\3 \2 \1",clean)
				return reorder
			if re.search(r"([A-Za-z]+)\s+.*(\d{4})",clean):
				reorder = re.sub(r"([A-Za-z]+)\s+.*(\d{4})",r"\2 \1",clean)
				return reorder
		
			
			return clean

		def dateparser(rough):
			rough = reorder(rough)
			clean = dateutil.parser.parse(rough, default = DEFAULT)
			return clean
			# return rough

		possibleFormats = [
			# r"(%s)\s(%s)[\"\.]\s(%s)" % (month, day, year),
			# r"(%s).\s(%s)\s(%s)" % (dayOrNone, month, year),
			# r"(%s)[\'\"]*\s*(%s)\s(%s)[\'\.]*" % (day, december, year),
			# r"(%s)\s+(%s)['\"]*.{0,5}\s*(%s)[\'\.]*" % (month, day, year),
			# r"(%s)\s+(%s)[\'\"]*.{0,5}\s+(%s)[\'\.]*" % (december, day, year),
			# r"[\[1I]*(%s)\s*(%s) (%s)[\]I1]*" % (day, month, year),
			# r"(%s)\s(%s)*[\'\"]*\W*\s*(%s)[\'\.]*" % (dayOrNone, month, year),
			# r"(%s)\s+\W*(%s)(?<!Dale)\s.{0,5}\s+(%s)[\'\.]*" % (month, dayOrNone, year),
			# r".*(%s)" % (year),
			r"\s*[\[I1]*(\d{0,2})[\'\"]*\s*([A-Za-z]+),*\s*([1I]\d{3})[\]1I\.]*",
			]
		for reformat in possibleFormats:
			date = re.search("|".join(possibleFormats),head)
			if date:
				rough = date.group()
				if rough:
					if re.search(r"\[*Jan[a-z]+",rough):
						rough = re.sub(r"\[*Jan[a-z]+",r" January",rough)
						rough = reorder(rough)
						# if dateparser(rough):
						# 	clean =dateparser(rough)
						# 	return str(clean)
						return rough
					if re.search(r"\[*Fe[a-z]+",rough):
						rough = re.sub(r"\[*Fe[a-z]+",r" February",rough)
						rough = reorder(rough)
						return rough
						clean = dateparser(rough)
						return clean
					if re.search(r"\[*M[na]r[a-z]+",rough):
						rough = re.sub(r"\[*M[na]r[a-z]+",r" March",rough)
						rough = reorder(rough)
						return rough
						clean = dateparser(rough)
						return clean
					if re.search(r"\[A*p[a-z]+",rough): 
						rough = re.sub(r"\[*Ap[a-z]+",r" April",rough)
						rough = reorder(rough)
						return rough
						clean = dateparser(rough)
						return clean
					if re.search(r"\[*May",rough):
						rough = re.sub(r"\[*May",r" May",rough)
						rough = reorder(rough)
						return rough
						clean = dateparser(rough)
						return clean
					if re.search(r"\[*J[nu][nem]+",rough):
						rough = re.sub(r"\[*J[nu][nem]+",r" June",rough)
						rough = reorder(rough)
						return rough
						clean = dateparser(rough)
						return clean
					if re.search(r"\[*J[udl]*y",rough):
						rough = re.sub(r"\[*J[udl]*y",r" July",rough)
						rough = reorder(rough)
						return rough
						clean = dateparser(rough)
						return clean
					if re.search(r"\[*Au[a-z]*",rough):
						rough = re.sub(r"\[*Au[a-z]*",r" August",rough)		
						rough = reorder(rough)
						return rough
						clean = dateparser(rough)
						return clean
					if re.search(r"\[*Sep[a-z]*",rough):
						rough = re.sub(r"\[*Sep[a-z]*",r" September",rough)
						rough = reorder(rough)
						return rough
						clean = dateparser(rough)
						return clean
					if re.search(r"\[*O[a-z]+",rough):
						rough = re.sub(r"\[*O[a-z]+",r" October",rough)
						rough = reorder(rough)
						return rough
						clean = dateparser(rough)
						return clean
					if re.search(r"\[*[NB][a-z]*",rough):
						rough = re.sub(r"\[*[NB][a-z]*",r" November",rough)
						rough = reorder(rough)
						return rough
						clean = dateparser(rough)
						return clean
					if re.search(r"\[*[Dd]e[ec][\.a-z]*'*",rough):
						rough = re.sub(r"\[*[Dd]e[ec][\.a-z]*'*",r" December",rough)
						rough = reorder(rough)
						return rough
						clean = dateparser(rough)
						return clean


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
  
	
	def id(self):
		pass
		
	def metadata(self):
		pass
	def does_this_look_suspicious(self):
		pass




if __name__=="__main__":
	for snippet in snippetyielder("v1.txt"):
		doc = Document(snippet)
		# print doc.get_date()
		f = open("snippet_test.txt", "a")
		f.write(doc.get_date() + '\t' + doc.raw_text()[:175] + '\n') #change to integer ascending
		f.close()

		# data = [ {'searchstring' : "To " + doc.recipient() + " from " + doc.author() + ", " + doc.get_date(), 
		# 'author': doc.author(), 'recipient': doc.recipient(), 'date': doc.get_date(), 'filename': doc.get_date() + "_" + doc.author()
		# }] #possibly add full text
		# data_string = json.dumps(data)
		# j = open("jsoncatalog.txt", "a")
		# j.write(data_string)
		# j.close()