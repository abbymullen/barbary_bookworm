all: v1.pdf v1.txt v2.pdf v2.txt v3.pdf v3.txt v4.pdf v4.txt v5.pdf v5.txt v6.pdf v6.txt all_vol.txt input.txt jsoncatalog.txt

v1.pdf:
	curl -o v1.pdf 'http://www.ibiblio.org/anrs/docs/E/E3/nd_barbarywars_v01.pdf'

v1.txt:v1.pdf
	pdftotext -f 19 -l 686 v1.pdf

v2.pdf: 
	curl -o v2.pdf 'http://www.ibiblio.org/anrs/docs/E/E3/nd_barbarywars_v02.pdf'

v2.txt:v2.pdf
	pdftotext -f 15 -l 570 v2.pdf

v3.pdf:
	curl -o v3.pdf 'http://www.ibiblio.org/anrs/docs/E/E3/nd_barbarywars_v03.pdf'

v3.txt:v3.pdf
	pdftotext -f 15 -l 584 v3.pdf

v4.pdf:
	curl -o v4.pdf 'http://www.ibiblio.org/anrs/docs/E/E3/nd_barbarywars_v04.pdf'

v4.txt:v4.pdf
	pdftotext -f 17 -l 572 v4.pdf

v5.pdf:
	curl -o v5.pdf 'http://www.ibiblio.org/anrs/docs/E/E3/nd_barbarywars_v05.pdf'

v5.txt:v5.pdf
	pdftotext -f 17 -l 595 v5.pdf

v6.pdf:
	curl -o v6.pdf 'http://www.ibiblio.org/anrs/docs/E/E3/nd_barbarywars_v06.pdf'

v6.txt:v6.pdf
	pdftotext -f 15 -l 612 v6.pdf

all_vol.txt:v1.txt v2.txt v3.txt v4.txt v5.txt v6.txt
	cat $(wildcard v*.txt) >> all_vol.txt

input.txt jsoncatalog.txt: all_vol.txt
	python text_cleaning_BW.py
