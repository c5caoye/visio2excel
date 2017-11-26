import xlsxwriter
import tkinter as Tkinter
import re
import mySpacy as ms
from tkinter import filedialog as tkFileDialog

def open_file(path):
    ''' Open file and process as a list if path exists. Return None otherwise '''
    try:
        # f = codecs.open(path, 'r', 'latin-1')
        f = open(path, 'r')
        textPool = []
        for line in f:
            if line[0].isdigit():
                textPool.append(line)
        return textPool
    except IOError:
        print ("Error: Cannot open file, plase try again")
        return None

def process_input(textPool):
    ''' Process the format of textPool '''
    newPool = []
    curPool = []
    for line in textPool:
        if line[0] == "1" and not line[1].isdigit():
            newPool.append(curPool)
            curPool = []
        curPool.append(line)
    newPool.append(curPool)
    return newPool

def main():
    print("Hello...")
    Tkinter.Tk().withdraw()
    path = tkFileDialog.askopenfilename()

    rawTextPool = open_file(path)
    if rawTextPool == None:
        return
    else:
        textPool = process_input(rawTextPool)
        print("File successfully opened.")

    print("Creating a new excel file")
    myExcel = xlsxwriter.Workbook(path + '.xlsx')
    worksheet = myExcel.add_worksheet()
    worksheet.set_column(1, 1, 100)
    wrap = myExcel.add_format({'text_wrap': True})

    row = 0
    for pool in textPool:
        print("Writing Scenatrio " + str(row) + "......")
        worksheet.write(row, 0, row)
        textToWrite = ""

        for i in range(len(pool)):
            pool[i] = re.sub('\d*\.', '', pool[i])
            pool[i] = re.sub('Yes > ', '', pool[i])
            pool[i] = re.sub('No > ', '', pool[i])
            if i+1 < len(pool):
                if re.search('Yes >', pool[i+1]):
                    pstate = ms.toStatement(pool[i], 'yes')
                    textToWrite += pstate + '\n'
                elif re.search('No >', pool[i+1]):
                    nstate = ms.toStatement(pool[i], 'no')
                    textToWrite += nstate + '\n'
                else:
                    textToWrite += pool[i] + '\n'
            else: textToWrite += pool[i] + '\n'
        worksheet.write(row, 1, textToWrite, wrap)
        row += 1


    myExcel.close()
    print("Finish writing excel file")
    temp = input("Prees any key to exit")
    return

if __name__ == '__main__': main()
