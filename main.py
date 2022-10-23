import re
import io
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.converter import HTMLConverter
from pdfminer.pdfpage import PDFPage


file = "Lernwortschatz-Kapitel2.pdf"
words = []
with open(file, 'rb') as fh:
    for page in PDFPage.get_pages(fh):
        resource_manager = PDFResourceManager()
        fake_file_handle = io.StringIO()
        converter = HTMLConverter(resource_manager, fake_file_handle)
        page_interpreter = PDFPageInterpreter(resource_manager, converter)
        page_interpreter.process_page(page)
        text = fake_file_handle.getvalue()
        strokes = list(text.split('<span style="font-family: PoloCEF-Medium; font-size:25px">'))
        for num, s in enumerate(strokes):
            if re.match(r'<span style="font-family: PoloCEF-Light; font-size:25px">', s.split('</span>')[1]) != None:
                k = s.split('</span>')[0]
                v = s.split('</span>')[1:]
                value = []
                strich = 0
                for num, string in enumerate(v):
                    string = string.replace('<span style="font-family: PoloCEF-Light; font-size:25px">', '')
                    string = string.split(',')[0]
                    if re.match(r'<span style="font-family: PoloDivisTremaLeicht', string) != None:
                        strich = 3
                    string = string.split('<span')[0].replace(' (Pl.)', '').replace(' (Sg.)', '').replace('\n', '')
                    string = string.replace('das', '').replace('die', '').replace('der', '').strip().split('|')[0]
                    if strich <= 0 and len(string) != 0:
                        value.append(string)
                    strich -= 1
                print(k, value)
