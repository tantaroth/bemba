#!/usr/bin/env python
import re, os

def execute():
	objPath = os.environ['SCRIPT_FILENAME'].split('/')

	code = Bemba( objPath[len(objPath)-1].replace('.py', '.html') )
	exec code.toHTML(code.pretty())

class Bemba:
	"""ESTA CLASE EJECUTA EL CODIGO PYTHON DEL HTML"""
	def __init__(self, fileName):
		self.content = False
		self.fileName = fileName
	def pretty(self):
		content = open(self.fileName,'r')
		return content.read()
	def toHTML(self, content):
		result = ''
		self.content = content
		statusTagsPy = False
		iLine = False
		iTabs = 0

		for line in content.split('\n'):
			if line != '':
				if line.find('{{{') > -1 or line.find('}}}') > -1:
					if re.match("<.+>", self.cleanerTab(line)):
						result += '# Es HTML con CODIGO:\nprint """'+(((line.replace('{{{', '""";')).replace('}}}', ';print """')).replace('print """;', '')).replace(';print ', '+')+'"""\n'
					else:
						if line.find('{{{') > -1:
							if line.find('}}}') > -1:
								statusTagsPy = False
								iLine = False
								iTabs = 0

								nowLine = line.replace('{{{', '""";')
								newLine = nowLine.replace('}}}', '; print """')
								result += '# Es CIERRE con CODIGO:\nprint """'+newLine+'"""\n'
							else:
								statusTagsPy = True
								iLine = 0

								result += '# ES APERTURA (SE DEBE OMITIR): {{{\n'
						elif line.find('}}}') > -1:
							statusTagsPy = False
							iLine = False
							iTabs = 0

							result += '# Es CIERRE (SE DEBE OMITIR): }}}\n'
						else:
							if statusTagsPy == True:
								iLine = iLine+1

								if iLine == 1:
									iTabs = len(line.split('\t'))-1

									result += '# 1. Es Parte del CODIGO:\n'+(line.replace('\t', '', iTabs))+'\n'
								else:
									result += '# +1. Es Parte del CODIGO:\n'+(line.replace('\t', '', iTabs))+'\n'
							else:
								result += '# Es TEXTO >>\n'+line+'\n'
				else:
					if re.match("<.+>", self.cleanerTab(line)):
						result += '# Es HTML:\nprint """'+line+'"""\n'
					else:
						if statusTagsPy == True:
							iLine = iLine+1

							if iLine == 1:
								iTabs = len(line.split('\t'))-1

								result += '# 1. Es Parte del CODIGO:\n'+(line.replace('\t', '', iTabs))+'\n'
							else:
								result += '# +1. Es Parte del CODIGO:\n'+(line.replace('\t', '', iTabs))+'\n'
						else:
							result += '# Es TEXTO:\nprint """'+line+'"""\n'
		
		return result
	def cleanerTab(self, str):
		return str.replace('\t', '')
	def execute():
		print "page"
		#objPath = os.environ['SCRIPT_FILENAME'].split('/')

		#code = Code( objPath[len(objPath)-1].replace('.py', '.html') )
		#print code.toHTML(code.pretty())

