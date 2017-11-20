import xlswriter
import codecs
import Tkinter, tkFileDialog
import re
import mySpacy as ms

def open_file(path):
    ''' Open file and process as a list if path exists. Return None otherwise '''
    try:
        f = codecs.open(path, 'r', 'latin-1')
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
        curPool.append(line)
    newPool.append(curPool)
    return newPool

def main():
    Tkinter.Tk().withdraw()
    path = tkFileDialog.askopenfilename()
    rawTextPool = open_file(path)
    if f == None:
        return
    else:
        textPool = process_input(rawTextPool)
        print("File successfully opened.")
    print("Creating a new excel file")
    myExcel = xlsxwriter.Workbook(path + '.xlsx')
    worksheet = myExcel.add_worksheet()
    wrap = myExcel.add_format({'text_wrap': True})

    row = 0
    for pool in textPool:
        print("Writing Scenatrio " + row + "......")
        worksheet.write(row, 0, row)
        for line in pool:
            textToWrite = ""
            svalue = ""
            if re.search("Yes >", line):
                value = line.split("Yes >", 1)
                print(value)
                svalue = ms.toStatement(value, "yes")
                print(svalue)
            elif re.search("No >", line):
                value = line.split("No >", 1)
                svalue = ms.toStatement(value, "no")
                print(svalue)
            textToWrite += svalue + '\n'
        worksheet.write(row, 1, textToWrite, wrap)
        row += 1
    myExcel.close()
    print("Finish writing excel file")
    temp = raw_input("Prees any key to exit")
    return

    if __name__ == '__main__': main()
