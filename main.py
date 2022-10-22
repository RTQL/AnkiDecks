import re
import io

from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.converter import HTMLConverter
from pdfminer.pdfpage import PDFPage


file = "Lernwortschatz-Kapitel2.pdf"
with open(file, 'rb') as fh:
    for page in PDFPage.get_pages(fh):
        resource_manager = PDFResourceManager()
        fake_file_handle = io.StringIO()
        converter = HTMLConverter(resource_manager, fake_file_handle)
        page_interpreter = PDFPageInterpreter(resource_manager, converter)
        page_interpreter.process_page(page)
        text = fake_file_handle.getvalue()
        data = list(text.split("/"))
        strich = 0
        for num, d in enumerate(data):
            string = d.split('<span style="position')[0].split(' (')[0].split(',')[0]
            string = string.replace('span><span style="font-family: PoloCEF-Light; font-size:25px">', "")
            string = string.replace('span>', "").replace('<', "")
            try:
                if re.findall(r'>-<', d)[0] == '>-<':
                    strich = 1
                    string = ""
            except:
                if strich == 1:
                    string = ""
                strich = 0
                print(f"{num} {string}")
                pass

