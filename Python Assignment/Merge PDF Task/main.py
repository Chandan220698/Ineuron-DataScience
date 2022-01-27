from distutils.log import ERROR, INFO
from tkinter import *
import os
from tkinter import messagebox
import PyPDF2
import logging

logging.basicConfig(filename='main_log.log',
                    filemode='a',
                    level= INFO,
                    format='%(asctime)s %(levelname)s-%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                    )

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

root = Tk()                     # root(base) window
root.title("PDF Merger")        # root window Title
root.geometry("1280x800")       # window resolution

## myClick Button - Search the current directory
def myClick():
    logger.info('User clicked on search')
    searchString = search01.get()
    logger.info('Search path: ' + str(searchString))

    resultArea.configure(state='normal')
    resultArea.delete('1.0', END)
    try:
        os.chdir(searchString)      # Changing cwd to searched directory
    except Exception as e:
        logger.error(str(e) + ' - Invalid Directory Path !')
        messagebox.showerror("Directory Error!", "No such Directory Exists")
    else:
        files = os.listdir()
        #resultArea.configure(state='normal')
        pdfCount = 0
        for file in files:
            resultArea.insert(END, file + '\n')
            file_details = os.path.splitext(file)   ## Spliting the file into filename and extension
            if file_details[1] == '.pdf':
                pdfCount += 1

        resultArea.insert(END, '\n\n' + 'Total PDFs Found: ' + str(pdfCount) + '\n')
        resultArea.configure(state='disable')
        logger.info('Total PDF(s): '+str(pdfCount))
        logger.info('Directory information is displayed onto Text Area')


## mergePDF Button - Function to merge all the PDF files
def mergePDF():
    logger.info('User clicked on Merge PDF')
    searchString = search01.get()
    logger.info('Beginning the merging process: ' + str(searchString))

    try:
        os.chdir(searchString)
    except Exception as e:
        logger.error(str(e) + ' - Invalid Directory Path !')
    else:
        files = os.listdir()               ## Contains all the file name 
        mergeFile = PyPDF2.PdfFileMerger()
        flag = False
        for file in files:
            file_details = os.path.splitext(file)                           # Spliting the file into filename and extension
            # if file is .pdf merging them
            if file_details[1] == '.pdf':
                flag = True
                mergeFile.append(PyPDF2.PdfFileReader(file, 'rb'))          # Append the pdf into a mergeFile object     
        if flag == True:
            mergeFile.write("Merged-PDF.pdf")
            messagebox.showinfo("Merge Completed!", "PDF name: Merged-PDF") # Pop up on success merge   
            logger.info('Merge Completed')
            logger.info('Merged PDF File Name: Merged-PDF') 
        else:
            messagebox.showerror("Merge Error!", "NO! PDF File(s) to Merge")
            logger.error('Merge Error!, No PDF to Merge')

try:
    ## Creating row 0
    label00 = Label(root, text="Search Directory: ", padx=3)
    label00.grid(row=0, column=0, padx=15)

    search01 = Entry(root, width=170, borderwidth=2)
    search01.grid(row=0, column=1, pady=25)

    myButton02 = Button(root, text='Search', padx=10, pady=7, command=myClick)
    myButton02.grid(row=0, column=2)

    ## Creating row1,2 - label, result TextArea
    label10 = Label(root, text="Directory Conatins: ")
    label10.grid(row=1, column=1, padx=15)

    resultArea = Text(root, width=130, height=30)
    resultArea.grid(row=2, column=1)
    resultArea.configure(state='disable')

    ## Creating row 3 - Merge PDF functionality
    myButton3 = Button(root, text='Merge PDFs', command=mergePDF)
    myButton3.grid(row=3, column=1, pady=10)

    logger.info('Main window created successfully!')

except Exception as e:
    logger.error(str(e) +  ' - Error while creating main window')

root.mainloop()