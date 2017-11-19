import xlsxwriter
import codecs
import Tkinter
import tkFileDialog

def check_file(fileName):
    try:
      f = codecs.open(fileName, 'r', 'latin-1')
      return 1
    except IOError:
      print "Error: File does not appear to exist."
      return 0

def read_file(fileName):
    f = codecs.open(fileName, 'r', 'latin-1')
    resultList = []
    for line in f:
        if line[0].isdigit():
            resultList.append(line)
    return resultList

def writeExcel(fileName, inputList):
    row = 0
    col = 0 
    content = fileName

    excel = xlsxwriter.Workbook(fileName + '.xlsx')
    worksheet = excel.add_worksheet()
    wrap = excel.add_format({'text_wrap': True})

    for i in range(len(inputList)):
        if inputList[i][0] == "1" and not inputList[i][1].isdigit():
            worksheet.write(row, col, row)
            worksheet.set_column(col + 1, col + 1, 100)
            worksheet.write(row, col + 1, content, wrap)
            row += 1
            content = inputList[i] + '\n'
        elif i == len(inputList) - 1:
            worksheet.write(row, col, row)
            worksheet.set_column(col + 1, col + 1, 100)
            worksheet.write(row, col + 1, content, wrap)
        else:
            content += inputList[i] + '\n'
    excel.close()
    return

def main():
    print("****Make sure that the file you want to convert is at the same location with this script****")

    Tkinter.Tk().withdraw() # Close the root window
    myFile = tkFileDialog.askopenfilename()
    # myFile_raw = raw_input("What's the file name that you want to convert? (Do not include '.txt'):\n")
    # myFile = myFile_raw + ".txt"
    print("The file you choose convert is: ", myFile)
    if not check_file(myFile):
        print("Can't find the file, please try again")
        return 
    print("Reading file contents......")
    l = read_file(myFile)

    # x = tkSimpleDialog.askstring("Enter Name")

    print("Writing excel file......")
    writeExcel(myFile, l)
    print("Done!")
    temp = raw_input("Prees any key to exit")
    print("Done!")


if __name__  == '__main__':
    main()
