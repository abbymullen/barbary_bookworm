import re
import json
import warnings
import uuid
import dateutil.parser
from datetime import *
DEFAULT = datetime(1798,1,1)



def snippetyielder(filename):
	"""
	This function takes a text file with many small documents in it, and returns those documents broken out into 
	individual units. I used the citation at the end of each document as the breaking point. I had to use a custom
	break because the OCR of the text file incorporates almost every non-printing character in its read."""
	text = open(filename, "r")
	a = text.readlines()
	p = "".join(a) 	  #detecting the breaks between documents and identifying them to break the docs with


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
	docbreak = re.sub(r"(.*\[*F\.\s*D\..*)",r"\1DOCBREAK\n",docbreak)
	docbreak = re.sub(r"(\[*.*GLB.*)",r"\1DOCBREAK\n",docbreak)
	docbreak = re.sub(r"(DOCBREAK)+",r"DOCBREAK\n",docbreak) 	
	docbreaks = docbreak.split("DOCBREAK") 	  #yielding one document at a time
	for doc in docbreaks:
		if re.search(r".+",doc): 	
			yield doc 	

class Regexdate():
 	def __init__(self,string):
		self.string = string 
 	"""  Initialized with a portion of a string suspected to contain a date. 	 	 	 
 	""" 	 	 	  
 		 	   
	def return_date(self): 
		""" 
		After performing all necessary transformations, returns a string of the date in ISO XXXX format.
		""" 	 	 	 	 	 	  
	 	best_guess = find_daty_string(self.string) 	 	 	 
		best_guess = reorder(best_guess) 	 	 	 
	 	return to_iso(best_guess) 	  

	def find_year(self): 	
		"""
		Pulls out a year without recourse to datetime and corrects small OCR problems
		""" 	 	 
	 	year = re.search(r"[I1]\d{3}",self.string)
	 	if year: 	 	 	  
	 		if re.search(r"(\d{4})",year.group()):
	 			return year.group()
	 		if re.search(r"I\d{3}",year.group()):
	 			year = re.sub(r"I(\d{3})",r"1\1",year.group())
	 			return year

	 	return "Unknown" 	 	 	  

	# def find_daty_string(self,string): 
	#  	possibleFormats = [
	#  	r"[1I\[]*(\d{1,2}).*\s*([A-Za-z]+.*)\s*(1\d{3})[\]1I]",
	#  	]
	#  	for formats in possibleFormats:
	#  		rough = re.search(formats,self.string)
	#  		return rough

	 		 

	# def fix_months(self,string): 	 	 	 	 
	# 	monthLookups = {r"January":r"\[*Jan[a-z]+", 	 	 	 	 	 	 	 	 
	# 	r"February":r"\[*Fe[a-z]+", 	 	 	 	 	 	 	 	 
	# 	r"March":r"\[*M[na]r[a-z]+", 	 	 	 	 	 	 	 	 
	# 	r"April":r"\[*Ap[a-z]+", 	 	 	 	 	 	 	 	 
	# 	r"May":r"\[*May", 	 	 	 	 	 	 	 	 
	# 	r"June":r"\[*J[nu][nem]+", 	 	 	 	 	 	 	 	 
	# 	r"July":r"\[*J[udl]*y", 	 	 	 	 	 	 	 	 
	# 	r"August":r"\[*Au[a-z]*", 	 	 	 	 	 	 	 	 
	# 	r"September":r"\[*Sep[a-z]*", 	 	 	 	 	 	 	 	 
	# 	r"October":r"\[*O[a-z]+", 	 	 	 	 	 	 	 	 
	# 	r"November":r"\[*[NB][a-z]*", 	 	 	 	 	 	 	 	 
	# 	r"December":r"\[*[Dd]e[ec][\.a-z]*'*"}	 	 

	# 	rough = find_daty_string(self.string)


	# def reorder(rough): 	 	 	 
	# 	""" 	 	 	 
	# 	Takes as input a string that has been reformatted to include reformatted months. 	 	 	 
	# 	Returns a string representing a date in "Year Month day" format 
	# 	where Year and day are numeric and the month is text but free of spaces. 	 	 	 
	# 	""" 	 	 	 	  
	# 	# return rough 	 	 	 
	# 	clean = re.sub(r"[1I](\d{2}) ",r"\1",rough) 	 	 	 
	# 	clean = re.sub(r"I(\d{3})",r"1\1",clean) 	 	 	 
	# 	clean = re.sub(r"[\[\.\"]",r"",clean) 	 	 	 
	# 	clean = re.sub(r"[A-Za-z\d]*(\d{4}).",r" \1",clean) 	 	 	  
	# 	clean = re.sub(r"\s+",r" ",clean) 	 	 	 
	# 	clean = re.sub(r"Dep[tf]",r"",clean) 	 	 	 
	# 	clean = re.sub(r"[\'@\*\?\)\%\+]",r"",clean) 	 	 	 
	# 	clean = re.sub(r"(\d{1,2})[A-Za-z]*",r"\1",clean) 	 	 	 
	# 	clean = re.sub(r"^\s",r"",clean) 	 	 	 
	# 	clean = re.sub(r"([A-Za-z])\s([A-Za-z\d]+)(\d{4})",r"\1 \2 \3",clean) 	 	 	 
	# 	clean = re.sub(r",",r" ",clean) 	 	 	   

	# 	# if re.search(r"[A-Za-z]*\s*(.{0,2})\s([A-Za-z]+)\s(\d{4})",clean): 	 	 	 
	# 	# 	reorder = re.sub(r"[A-Za-z]*\s*(.{0,2})\s+([A-Za-z]+)\s+(\d{4})",r"\3 \2 \1",clean) 	 	 	 
	# 	# 	reorder = re.sub(r"(\d{4}) ([A-Za-z]+) ([A-Za-z\W]+)",r"\1 \2",reorder) 	 	 	 
	# 	# 	reorder = re.sub(r"\,",r"",reorder) 	 	 	 
	# 	# 	return reorder 	 	 	 
	# 	# if re.search(r"[A-Za-z]*\s*([A-Za-z]+)\s(.{0,2})\s(\d{4})",clean): 	 	 	 
	# 	# 	reorder = re.sub(r"([A-Za-z]+)\s+(.{0,2})\s+(\d{4})",r"\3 \1 \2",clean) 	 	 	 
	# 	# 	reorder = re.sub(r"(\d{4}) ([A-Za-z]+) ([A-Za-z\W]+)",r"\1 \2",reorder) 	 	 	 
	# 	# 	reorder = re.sub(r"\,",r"",reorder) 	 	 	 
	# 	# 	return reorder 	 	 	 
	# 	if re.search(r"(\d{0,2}) ([A-Za-z]+)\s+(\d{4})",clean): 	 	 	 	 	 
	# 		reorder = re.sub(r"(\d{0,2}) ([A-Za-z]+)\s+(\d{4})",r"\3 \2 \1",clean) 	 	 	 	 	 
	# 		return reorder 	 	 	 
	# 	if re.search(r"([A-Za-z]+)\s+.*(\d{4})",clean): 	 	 	 	 	 
	# 		reorder = re.sub(r"([A-Za-z]+)\s+.*(\d{4})",r"\2 \1",clean) 	 	 	 	 	 
	# 		return reorder

	# def dateparser(rough):
	# 	rough = reorder(rough)
	# 	clean = dateutil.parser.parse(rough, default = DEFAULT)
	# 	return clean
	# 	# return rough

	# for reformat in possibleFormats:
	# 	date = re.search("|".join(possibleFormats),head)
	# 	if date: 	
	# 		rough = date.group() 	
	# 		return rough 	 	#Uncomment this line to see what sort of expressions you're missing on.
	# 	#warnings.warn("\n"+"\n"+"*"*100 + head[:200]) 	   
	# def reformatAsISO(self): 	 	 	 
	# 	pass 	 	 	 	 

#defining a class to pull out stuff from the snippets
class Document():
	def __init__(self, doc):
		self.doc = doc

	def test(self):
		return self.doc + 'BREAK\n'

	def raw_text(self): 
		"""
		This takes a string (a document) and returns a string clean of all headers and citations
		"""
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
		raw_text = re.sub(r"(CL,.*)",r"",raw_text)		#eliminating citations
		raw_text = re.sub(r"(.*\[*F\.\s*D\..*)",r"",raw_text) #eliminating citations
		raw_text = re.sub(r"(\[*.*GLB.*)",r"",raw_text) #eliminating citations
		raw_text = re.sub(r"NAVAL OP.*",r"",raw_text) #eliminating more headers
		raw_text = re.sub(r"FROM 1785 TO 1801",r"",raw_text) #eliminating more headers
		raw_text = re.sub(r"W.*B.*",r"",raw_text) #eliminating more headers
		raw_text = re.sub(r"\s",r" ", raw_text) #eliminating tabs etc. 	 	  
		return raw_text
	

	def get_date(self):
		"""
		Right now this takes a string and returns a year; hopefully someday it will return a more specific date.
		"""
		head = self.raw_text()[:200] 	 	 
		parser = Regexdate(head) 	 		
		try:
			year = parser.find_year()		
			return year 	
		except:
			return "Unknown"

	def author(self):
		"""
		Takes a string--the first bit of the document--and returns the author
		Accomplishes this through extracting data from formulaic headings on documents
		Tries to account for non-letter documents such as daily journal entries
		"""
		author = re.search(r"(.*[tT]\s*o)(.*)(from\s)(.+)",self.raw_text()[:150])
		attr_journal = re.search(r".*[Jj]o[nu]rn[sa]l of (Mids.*),.*",self.raw_text()[:150])
		journal = re.search(r".*[Jj]o[nu]rn[sa]l of ([US86\.,5 ]+) ([\w ]{0,15})[,.]",self.raw_text()[:250])
		if journal:
			journal = journal.group(1) + journal.group(2)
			return journal
		if attr_journal:
			attr_journal = attr_journal.group(1)
			return "Journal of " + attr_journal
		if author: 	
			author = author.group(4) 	
			author = re.sub(r"(\w+\.*\s*\w*\.*\s*\w+),.*",r"\1",author) #getting rid of following titles 	
			author = re.sub(r"Captain",r"",author) #getting rid of Captain 	
			author = re.sub(r"\.",r"",author) #getting rid of periods in names 
			author = re.sub(r"([sS]ecre[a-z]+ of the \w+).*","Secretary of the Navy",author)		
			return author
		
		return "Unknown"

	def recipient(self):
		"""
		Takes a string, the first bit of a document, and returns the recipient of the document if there is one
		Tries to account for non-letter documents by recording an alternate "recipient"
		"""
		recipient = re.search(r"([Tt]\s*o )(.*)(from.*)",self.raw_text()[:250])
		journal = re.search(r".*[Jj]ournal of ([US86\. ]+) ([\w ]{0,15})[,.]",self.raw_text()[:250])
		if journal:
			return "Journal Entry"
		if recipient: 	
			recipient = recipient.group(2) 	
			recipient = re.sub(r"(\w+\s*\w+),.*",r"\1",recipient) #attempting to clear out titles and such
			recipient = re.sub(r"([sS]ecre[a-z]+ of the \w+).*","Secretary of the Navy",recipient) 	
			return recipient
		return "Unknown" 		
	
	def id(self): 	
		"""
		randomly generated ID
		""" 	 	 	 
		self.id = uuid.uuid4().hex
		return self.id


	def metadata(self): 	 	 	 	 
		metadata = { 	 	 	 	 	 	 
			"filename":self.id(), 	 	 	 	 	 	 
			"author":self.author(), 	 	 	 	 	 	 
			"recipient":self.recipient() 	 	 	 	 
			}
		return json.dumps(metadata) 	 	 	 	 		

	def does_this_look_suspicious(self):
		pass


if __name__=="__main__":
	f = open("input.txt", "a")
	j = open("jsoncatalog.txt", "a")
	for snippet in snippetyielder("all_vol.txt"):
		doc = Document(snippet)
		# print doc.id() + '\t' + doc.raw_text()
		f.write("ID_" + doc.id() + '\t'	+ doc.raw_text() + '\n')
		data = {'searchstring': "To " + doc.recipient() + " from " + doc.author() + ", " 
			+ doc.get_date()
			, 'author': doc.author()
			, 'recipient': doc.recipient()
			, 'date': doc.get_date()
			, 'filename': "ID_" + doc.id
			, 'full_text': doc.raw_text()
		} 
		data_string = json.dumps(data)
		j.write(data_string + '\n')
		
	j.close()
	f.close()
