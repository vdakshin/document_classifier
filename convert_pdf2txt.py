# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 10:55:13 2015

@author: kirut_000
"""

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage, PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from cStringIO import StringIO
import sys
import os
import glob

src = 'C:\Users\kirut_000\Documents\periday\document_classification\Docs'
#src = 'Docs'
dest = 'C:\Users\kirut_000\Documents\periday\document_classification\Docs-txt'

def convert_pdf_to_txt(path, dest_folder, outtype='txt'):
    outfile = path[:-3] + outtype
    file_name = os.path.basename(outfile)
    rsrcmgr = PDFResourceManager()
    codec = 'utf-8'
    laparams = LAParams()
    destfile = os.path.join(dest_folder,file_name)
#    print destfile
    if outfile:
#        outfp = file(outfile, 'w')
        outfp = file(destfile, 'w')
    else:
        outfp = sys.stdout
    device = TextConverter(rsrcmgr, outfp, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()
    parser = PDFParser(fp)
    document = PDFDocument(parser, password)
    if document.is_extractable:
        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
            interpreter.process_page(page)
    fp.close()
    device.close()
    outfp.close()
    return
    
if __name__ == '__main__':
#    if len(sys.argv) > 1:
#        file_location = sys.argv[1].strip()
#        print file_location
    for path, dirlist, filelist in os.walk(src):
        for folder in dirlist:
#            print folder
            src_location = os.path.join(src,folder)
            os.chdir(src_location)
            for filename in glob.iglob('*.pdf'):
                file_location = os.path.join(src,folder,filename)
                dest_folder = os.path.join(dest,folder)
                if not os.path.exists(dest_folder):
                    os.makedirs(dest_folder)
                convert_pdf_to_txt(file_location,dest_folder,'txt')
#    else:
#        print 'Usage: python convert_pdf2txt.py <path>/file.pdf'