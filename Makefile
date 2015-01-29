all: v1.pdf v1.txt

v1.pdf:
	curl -o v1.pdf 'http://www.ibiblio.org/anrs/docs/E/E3/nd_barbarywars_v01.pdf'

v1.txt:v1.pdf
	pdftotext -f 19 v1.pdf

