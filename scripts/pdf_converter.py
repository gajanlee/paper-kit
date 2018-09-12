#!/usr/bin/python3
import argparse
import logging
import os

from pdfminer.pdfparser import PDFParser,PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal,LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed

# preprocess textbox
def replace_invisible(content):
    content = content.strip()
    
    for c in ["\n"]:
        content = content.replace(c, "")
    return content if content not in [" ", ""] else None

# extract by pdfminer
def get_pdf_content(pdf_path):
    print(pdf_path)
    with open(pdf_path, "rb") as file:
        parser = PDFParser(file)
        doc = PDFDocument()
        parser.set_document(doc)
        doc.set_parser(parser)

        doc.initialize()
        
        # When the file can't convert to txt, it will throw an error
        if not doc.is_extractable:
            raise PDFTextExtractionNotAllowed

        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)

        interpreter = PDFPageInterpreter(rsrcmgr, device)

        content_recoder = []
        # process by page
        for page in doc.get_pages():
            interpreter.process_page(page)
            layout = device.get_result()

            for x in layout:
                if (isinstance(x, LTTextBoxHorizontal)):
                    content_recoder.append(replace_invisible(x.get_text()))
            
            # Page procession done, we need detect page number and remove it
            try:
                if content_recoder[-1].isdigit():
                    content_recoder = content_recoder[:-1] + [" "]
            except:
                pass
        if content_recoder:
            content_recoder = list(filter(lambda c: c and c != content_recoder[0], content_recoder))
        else:
            pass
            #raise Exception("No Extracted Content.")
        
        return "\n".join(content_recoder)

def save_txt(stream, origin, output):
    """
    Save string to a text file.

    Args:
        stream: the content of extracted pdf
        origin: the file name or full path of origin file
        output: the base path of output file, the name will nominated by origin file name
    """
    if not os.path.exists(output):
        os.makedirs(output)

    logger = logging.getLogger("save_log")
    output_file = os.path.join(output, "{filename}.txt".format(filename=os.path.basename(origin)))
    with open(output_file, "w") as fp:
        fp.write(stream)
    logger.info("Extract from {} to {}".format(origin, output_file))

# extract pdf content in a directory, it will return nothing but store all into files
def extract_directory(dir_path, suffix=[".pdf"], output="."):
    if not os.path.exists(dir_path):
        raise Exception("Directory Error")
    
    for path in os.listdir(dir_path):
        # the real path to get document's location, it can be an absolute path to judge its type
        r_path = os.path.join(dir_path, path)
        if os.path.isdir(r_path):
            extract_directory(r_path)
        elif os.path.isfile(r_path) and os.path.splitext(path)[-1] in suffix:
            save_txt(get_pdf_content(r_path), origin=path, output=output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--paths", nargs="+", required=True, help="dest dirs' path which contains required documents")
    parser.add_argument("--save_path", type=str, default=".", help="base path to save extracted text files")
    args = parser.parse_args()
    print("the input paths is ", args.paths)
    print("the input save_path is ", args.save_path)

    for path in args.paths:
        extract_directory(path, output=args.save_path)