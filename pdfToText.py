from pypdf import PdfReader

output = './output.txt'
reader = PdfReader("./Physio by Dr.Fawzy [Sensory].pdf")
page = reader.pages[3]
text = page.extract_text()
number_of_pages = len(reader.pages)
lineCounter = 1
with open(output, 'w') as f_out:
    f_out.write("[DOC_START]\n")
    for i in range(number_of_pages):
        f_out.write("[Page %d]\n" % (i + 1))
        pageText = reader.pages[i].extract_text(extraction_mode="layout", layout_mode_space_vertically=False)
        for line in pageText.split('\n'):
            f_out.write("[Line %s]: %s\n" % (lineCounter, line))
            lineCounter = lineCounter + 1
    f_out.write("[DOC_END]")
    

    
print(number_of_pages)