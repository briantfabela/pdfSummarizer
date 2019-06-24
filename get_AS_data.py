# SUMMARIZE ADDRESS ASSIGNMENT / VERIFICATION PDF FORMS

import PyPDF2, sys

#pdf_name = 'addass.pdf'

def main(pdf_name):

    pdf_file = open(pdf_name, 'rb') # pdf object
    pdf_reader = PyPDF2.PdfFileReader(pdf_file) # pdf reader object
    pdf_page = pdf_reader.getPage(0) # read the 1st page of the pdf
    pdf_text = pdf_page.extractText() # read all the raw text on the pdf

    print_info(get_info(pdf_text))

def get_info(txt):
    '''get relevant info from raw text'''

    # clean large chunks of text containing no useful data
    pdf_txt = txt.split('Emergency Service')[0].split('Current Street Address of')[1]
    pdf_txt = ' '.join(pdf_txt.split())

    # get the full address and the ESN from pdf txt
    full_address_ESN = pdf_txt.split('ASSIGNED AS:')[-1].split('New Street')[0].strip()

    # get the parcel id
    pidnum = get_digits(pdf_txt[pdf_txt.find('Year Book'): pdf_txt.find('Parcel')+11])

    # get all street-type elements alone
    full_address = full_address_ESN[:-11]
    esn = full_address_ESN[-4:]
    zipcode = full_address_ESN[-10:-5]
    st_num = full_address.split()[0]
    st_name = ' '.join(full_address.split()[1:-1])
    st_type = full_address.split()[-1]

    return AddressPoint(pidnum, full_address, st_num, st_name, st_type, zipcode, esn)

def print_info(p):
    '''print relevant info in readable format from AddressPoint Class Object'''

    print(f'''\
    ADDRESS_NUMBER: {p.st_num}
    STREET_NAME: {p.st_name}
    STREET_TYPE: {p.st_type}
    ZIP_CODE: {p.zipcode}
    FULL_ADDRESS: {p.f_address}
    PARCEL_KEY: {p.pidnum}
    ESN: {p.esn}
    ''')
    
def get_digits(text):
    '''get the digits in string and string and remove whitespace'''

    return ''.join([char for char in text if char.isdigit()]).strip()

class AddressPoint:
    '''Contains all information extracted from the PDF for easy reference'''
    def __init__(self, pid, full_ad, st_num, st_name, st_type, zipcode, esn):
        self.pidnum = pid
        self.f_address = full_ad
        self.st_num = st_num
        self.st_name = st_name
        self.st_type = st_type
        self.zipcode = zipcode
        self.esn = esn

# call python file from command like this (from same directory)
# python get_AS_data.py filename.pdf

if __name__ == "__main__":
    filename = str(sys.argv[1])
    main(filename)


# TODO: Consider integrating ArcPy and generating the point with this data
# TODO: GUI with file navigator/selector and multiple PDF processing
