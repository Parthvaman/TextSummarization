import PyPDF2 as pdf
import docx2txt as wd

def readfile(filename):
    file=filename.split('.')

    if file[1]=='txt':
        text=open(filename,'r')
        return (text.read())
    
    elif file[1]=='docx' or file[1]=='doc':
        
        text = wd.process(filename)
        return (text)

    elif file[1]=='pdf':

        pdreader = pdf.PdfReader(filename)

        print(len(pdreader.pages))
        text=''

        for i in range(0,len(pdreader.pages)):
            text+=pdreader.pages[i].extract_text()
        
        return text