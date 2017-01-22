'''
This program splits the xml version of a textbook into .html files based on the <page> tag
Each text file is saved as 1.html,2.html ... corresponding to the page number.
Each file contains the text on that page from the textbook

Important*** : Make sure you create a separate folder for this program. It creates the total page number of text files.
'''
import xml.etree.cElementTree as ET

tree = ET.ElementTree(file='Textbook.xml')
root = tree.getroot()

i = len(root)
print(i)

startPage = int(input())
endPage = int(input())

j=startPage

for page in root:
	if(page.tag=='page'):
		if (startPage <= int(page.get('number')) <= endPage):
			fo = open((page.get('number') + '.html'), 'w')
      #path should refer a folder too! Use relative addressing mode.
			print ("Converting page", page.get('number'))
			fo.write('<html>\n<body>\n')
			for attr in page:
				if((attr.tag=='text') and attr.text!=None):	
					mainText = attr.text.replace('<','&lt;')
					mainText = mainText.replace('>','&gt;')
          #finish this list if there are more.
					fo.write(mainText)
					fo.write('\n')
			if (j != endPage):
				fo.write('<a href="'+str(j+1)+'.html">'+str(j+1)+'.html</a>\n')
			fo.write('</html>\n</body>')
			j=j+1
