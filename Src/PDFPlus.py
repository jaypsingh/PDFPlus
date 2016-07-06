'''
# PDFPlus.py
# Author : Jay P Singh
'''
import os, PyPDF2, sys, logging, traceback

class PDFPlus(object):
    '''
    Author:
    Jay P Singh

    Status:
    Under Development

    Dependency:
    For doing any PDF operation please keep the PDF you want to process in C:\Temp\PDFPlus path.

    PDFPlus class contains the implementation for the below methods:
    -------------------------------------------------
    -------------------------------------------------

    1. ReadPDF() :
    -------------
    This method reads the PDF File and writes the PDF File contents to a text file.

    Read PDF Valid Commands:
    ------------------------
    >>pdfPlus.py <pagenum>:
    This command will read the text (only) from PDF file present in the C:\Temp\PDFPlus Directory.
    If More than one file is present both the files will be read. The text will be read and
    written to a .txt file in c:\Temp\PDFPlus directly containing the PDF contents.
    -------------------------------------------------

    >>pdfPlus.py R <fileName> or <pagenum>:
    This command will read the text (only) from PDF file present in the C:\Temp\PDFPlus Directory.
    If More than one file is present both the files will be read. The text will be read and
    written to a .txt file in c:\Temp\PDFPlus directly containing the PDF contents.
    -------------------------------------------------

    >>pdfPlus.py R <filename> <pagenum>:
    This command will read the text (only) from PDF file <filename>
    present in the C:\Temp\PDFPlus Directory. <filename> can also be coplete pdf path.
    If this argument is missing the file present in default path will be read.
    <pagenum> is the page number that user wants to read. If this argument is missing complete document
    will be read.
    page num can be :
        a number like 20, 31 etc
        a range like 5-7, 10-15 etc
        seprate page numbers like 5,8,21,25
        <TODO> mix of range and seprate pages like 5,8,10-15
    -------------------------------------------------
    -------------------------------------------------


    2. MergePDF() :
    --------------
    This method merges two or more PDF File which is kept in C:\Temp\PDFPlus directory.
    This method currently works only on the files kept in C:\Temp|PDFPlus directory.
    It can merge all the files together in C:\Temp\PDFPlus directory and creates the
    result file with name MergedByPDFPlus.pdf.

    Merge PDF Valid Commands:
    ------------------------
    >>pdfPlus.py M
    This command will merge all teh PDF Files kept in C:\Temp\PDFPlus directory.

    -------------------------------------------------
    -------------------------------------------------


    3. SplitPDF() :
    ---------------
    This method splits a PDF File which is kept in C:\Temp\PDFPlus directory or,
    from the path given as argument bu user.
    It will split all the pages and creates multiple pdf file with page numbers of the
    pdf file as prefix, eg 1_MyFile.PDF, 2_MyFile.PDF etc.

    Split PDF Valid Commands:
    -------------------------

    >>pdfPlus.py S
    This command will split all the pages from PDF File kept in C:\Temp\PDFPlus directory
    and create new files with page number as prefix.
    -------------------------------------------------

    >>pdfPlus.py S <FullPath\FileName>
    This command will split all the pages from PDF File <FileName> kept in <FullPath> directory
    and create new files with page number as prefix.
    -------------------------------------------------

    -------------------------------------------------
    -------------------------------------------------

    4. ExtractPDF() :
    -----------------
    This method extracts a page number PDF File which is kept in C:\Temp\PDFPlus directory or,
    from the path given as argument bu user.
    It will extract the given page number and creates separate pdf file with the
    page numbers of the pdf file as prefix, eg 1_MyFile.PDF, 2_MyFile.PDF etc.
    Extract PDF Valid Commands:

    >>pdfPlus.py E <PageNumber>
    This command will extract page <PageNumber> from a PDF File kept in C:\Temp\PDFPlus directory
    and create new files with page number as prefix.
    Page number can also be in range format like 5-8, 2-15 etc or
    or multiple comma separated page numbers will also work like 5,6,13,18
    -------------------------------------------------

    >>pdfPlus.py E <FullPath\FileName> <PageNum>
    This command will extract page <PageNum> from PDF File <FileName> kept in <FullPath> directory
    and create new files with page number as prefix.
    Please note that if full path of the file is not given in argument the program will assume the
    file <FileName> is kept in the default path.
    Page number can also be in range format like 5-8, 2-15 etc or
    or multiple comma separated page numbers will also work like 5,6,13,18
    -------------------------------------------------

    CAUTION:
    1. If no (pdf) file is present in present in C:\Temp\PDFPlus Directory an error will be generated
    and program will terminate.
    For Read method If the page range given are mixed, an error will be be generated and program
    will terminate.
    The method that supports full path as argument works good with a complete valid PDF path,
    but its advisory to use the application by keeping you PDF files in the default path
    C:\Temp\PDFPlus
    2. For Extract method if no file name argument is passed and multiple PDF files are present OR
    If a file name argument is passed and PDF file is not present than program will terminate.
    -------------------------------------------------
    -------------------------------------------------
    '''

    def __init__(self, logEnabled = True, workingDir = 'C:\\Temp\\PDFPlus\\'):
        '''
        This is the constructor for the PDFPlus method.
        @param logEnabled: This is a boolean variable. If True the logging will be enabled
        and the logs will be printed on console. Default value is True.
        @param workingDir: This is string. This path determines where our PDF files are located.
        Default working path is C:\Temp\PDFPlus\
        '''
        self.author = 'Jay P Singh'
        self.PDFPlusPath = workingDir
        self.__validFileOperation = ['R', 'M', 'S', 'E']
        # Default file operation is read mode. Is no arguments are passed we read the file.
        self.fileOperation = 'R'
        self.fileName = None
        self.mergeFileOutput = 'MergedByPDFPlus.pdf'
        self.pageRange = []
        self.isLogEnabled = logEnabled
        # self.errorCode = {2: 'One or more file is not PDF.', 3: 'No valid file to read.'}
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s = %(levelname)s - %(message)s')
        if self.isLogEnabled:
            pass
        else:
            logging.disable(logging.WARNING)

    def __changeCurrDir(self):
        '''This is a private method to change the current working directory to PDFPlusPath.'''
        os.chdir(self.PDFPlusPath)

    def __getFileOperation(self, operationStr):
        '''
        This is a private method to make sure the file operation user wants to perform is valid.
        If the operation is not valid, we change default operation to Read mode.
        @param operationStr: This is a string. It determines if the file Operation is
        Read(R), Merge(M), Extract(E) or Split(S).
        @return: This method returns the file operation to calling method in upper case (R, M, E or S).
        If the operationStr was not valid, default value 'R' is returned.
        '''
        logging.debug('in method: __getFileOperation')
        if operationStr.upper() in self.__validFileOperation:
            return operationStr.upper()
        else:
            logging.warning("Wrong File Operation Argument Argument (%s). Setting it to default Read mode (%s)."%(operationStr.upper(), self.fileOperation))
            return self.fileOperation.upper()

    def __getFileNameWithPath(self, nameStr):
        '''
        This is a private method to get the complete file name with complete path as input by user.
        @param nameStr: This is a string. This is the file name with complete path, eg c:\users\jay\mypdffile.pdf.
        @return: This method returns the file name along with path as whole without any processing.
        '''
        return nameStr


    def __getFileNamesFromDir(self):
        '''
        This is a private method. This method returns the list of files present in C:\Temp\PDFPlus directory in a list.
        If there is no files in the c:\temp\pdfplus this method will return an empty list.
        @Param : None
        @return: Returns a list of files present in the C:\Temp\PDFPlus directory to the calling method.
        '''
        for tempPath, tempDir, pdfFileNames in os.walk(self.PDFPlusPath):
            return pdfFileNames

    def __validatePDF(self):
        '''
        This is a private method. It validates if the PDF file is valid for processing.
        It returns a boolean value. True if there is a valid file to process else False.
        @return: True if file is valid or False if not.
        '''
        isValid = True
        if not self.fileName:
            return False
        for myFile in self.fileName:
            pdfPath = self.__getPDFPath(myFile)
            pdfFile = self.__getBaseFileName(myFile)
            if os.path.exists(pdfPath+'\\'+pdfFile):
                pass
            else:
                isValid = False
                break
        return isValid

    def __getBaseFileName(self, pdfFileName):
        '''
        This is a private method. It returns the base filename of the PDF file.
        @param pdfFileName : This argument is a string. Contains either the file name or
        the complete path along with the file name. eg test.pdf or c:\temp\test.pdf.
        @returns: PDF File Name
        '''
        if '\\' in pdfFileName:
            return os.path.basename(pdfFileName)
        else:
            return pdfFileName

    def __getPDFPath(self, pdfFileName):
        '''
        This is a private method. It returns the path of the PDF file.
        @param pdfFileName: This argument is a string. Contains either the file name or
        the complete path along with the file name. eg test.pdf or c:\temp\test.pdf.
        @returns: PDF File Path
        '''
        logging.debug('PDFFileName is : {}'.format(pdfFileName))
        if '\\' in pdfFileName:
            return os.path.dirname(pdfFileName)
        else:
            return 'C:\Temp\PDFPlus'

    def __writePDFDataToTextFile(self, filehandle, pageNum, pageData):
        '''
        This method writes the data read from PDF File, to a text file. This is a private method.
        @param filehandle: This is the file handle to the test file.
        @param pageNum: This is the PDF page number which have to written to the file.
        @param pageData: This is the data read from PDF pageNum which have to be written to the file
        @return: None.
        '''
        logging.debug('Writing page To TextFile: {}'.format(pageNum))
        filehandle.write('Page {} : \n'.format(pageNum))
        filehandle.write('{}'.format(pageData.encode('utf-8')))
        filehandle.write('-------------------------------------------------------------------------------------\n')

    def __isFilePDF(self, testFile):
        '''
        This is a private method. This method returns the file name if the file is a pdf file.
        If the file is not PDF File the method returns None.
        @return: Returns the file name if the file is a pdf file, if the file is not a pdf file the method returns None.
        '''
        pdfExt = '.PDF'
        myFileExt = testFile[-4:]
        if myFileExt.upper() == pdfExt:
            return testFile
        else:
            return None

    def __getPDFFileNameFromDir(self):
        '''
        This is a private method. This method returns a list of all PDF files present in C:\Temp\PDFPlus
        If there is no PDF File present in C:\Temp\PDFPlus this method returns blank list.
        @return: Returns a list of all PDF files present in C:\Temp\PDFPlus or Blanks List if no pdf file is present.
        '''
        pdfFileName = self.__getFileNamesFromDir()
        return filter(self.__isFilePDF, pdfFileName)

    def __getPageNum(self, pageNumStr):
        '''
        This is a private method to get the page number(s) that have to be processed by method.
        This method raises exception if the pageNumStr is not a valid input.
        @param pageNumStr: a string variable with page number data like '1','2-6' etc
        @return: Returns the pageRange list updated with the page numbers that have to be processed.
        '''
        if pageNumStr.isdigit():
            self.pageRange.append(int(pageNumStr))
        else:
            if '-' in pageNumStr:
                pageRangeToFrom = pageNumStr.split('-')
                for num in range(int(pageRangeToFrom[0]), int(pageRangeToFrom[1])+1):
                    self.pageRange.append(num)
            elif ',' in pageNumStr:
                pageRangeToFrom = pageNumStr.split(',')
                print pageRangeToFrom
                for num in pageRangeToFrom:
                    self.pageRange.append(int(num))
            else:
                logging.debug('Invalid Input %s, Raising exception'%pageNumStr)
                raise IOError, 'Invalid Input {}. Please see help file for valid input list'.format(pageNumStr)
        logging.debug(self.pageRange)
        return self.pageRange

    def __validateAndUpdatePageRange(self, pdfFileTotalPages):
        '''
        This is a private method. This method validates the page range that have to be processes.
        If the page range is out of rnage or invalid it updates the page range accordingly.
        @param pdfFileTotalPages: Total number of pages in the pdf File.
        return: returns the valid page range for processing.
        '''
        while((self.pageRange) and (max(self.pageRange)>pdfFileTotalPages)):
            if self.pageRange:
                logging.debug('Cannot read out of range page : {}'.format(max(self.pageRange)))
            self.pageRange.remove(max(self.pageRange))

    # __getReadParams method implementation
    def __getReadParams(self, readInput):
        if len(readInput) > 4:
            # >> pdfPlus.py R <PagenNum>, <PagenNum>, <PagenNum>, <PagenNum>, <PagenNum>, <PagenNum>
            self.fileOperation = self.__getFileOperation(readInput[1])
            tempList = readInput[2:]
            self.pageRange = self.__getPageNum(" ".join(tempList))
        elif len(readInput) == 4:
            # >> pdfPlus.py R <fileName> <PagenRange>
            self.fileOperation = self.__getFileOperation(readInput[1])
            self.fileName = [self.__getFileNameWithPath(readInput[2])]
            self.pageRange = self.__getPageNum(readInput[3])
        elif len(readInput) == 3:
            # >> pdfPlus.py R <fileName> or # >> pdfPlus.py R <PagenRange>
            self.fileOperation = self.__getFileOperation(readInput[1])
            if readInput[2].upper().endswith('.PDF'):
                self.fileName = [self.__getFileNameWithPath(readInput[2])]
            else:
                self.fileName = self.__getPDFFileNameFromDir()
                self.pageRange = self.__getPageNum(readInput[2])
        elif len(readInput) == 2:
            # >> pdfPlus.py R
            self.fileOperation = self.__getFileOperation(readInput[1])
            self.fileName = self.__getPDFFileNameFromDir()
        elif len(readInput) == 1:
            self.fileName = self.__getPDFFileNameFromDir()
        else:
            raise ValueError('Invalid Input to process Read Operation. See Help')

    # __getMergeParams method implementation
    def __getMergeParams(self, mergeInput):
        if len(mergeInput) == 3:
            # >> pdfPlus.py M <MergeOutputFileName.pdf>
            self.mergeFileOutput = self.__getBaseFileName(mergeInput[2])
            if self.__isFilePDF(self.mergeFileOutput) is None:
                raise ValueError("Merge file output extensions must be .pdf")
            self.fileOperation = self.__getFileOperation(mergeInput[1])
            self.fileName = self.__getPDFFileNameFromDir()
        elif len(mergeInput) == 2:
            # >> pdfPlus.py M <MergeOutputFileName.pdf>
            self.fileOperation = self.__getFileOperation(mergeInput[1])
            self.fileName = self.__getPDFFileNameFromDir()
        else:
            raise ValueError('Invalid Input to process Merge Operation. See Help')

    # __getSplitParams method implementation
    def __getSplitParams(self, splitInput):
        if len(splitInput) == 3:
            # >> pdfPlus.py S <FullPath\FileTOSplit.pdf>
            self.fileOperation = self.__getFileOperation(splitInput[1])
            self.fileName = [self.__getFileNameWithPath(splitInput[2])]
        elif len(splitInput) == 2:
            # >> pdfPlus.py S
            self.fileOperation = self.__getFileOperation(splitInput[1])
            self.fileName = self.__getPDFFileNameFromDir()
        else:
            raise ValueError('Invalid Input to process Merge Operation. See Help')

    # __getSplitParams method implementation
    def __getExtractParams(self, extractInput):
        if len(extractInput) > 4:
            # >> pdfPlus.py E <FileToExtract.pdf> <PageNum>
            self.fileOperation = self.__getFileOperation(extractInput[1])
            self.fileName = [self.__getFileNameWithPath(extractInput[2])]
            tempList = extractInput[2:]
            self.pageRange = self.__getPageNum(" ".join(tempList))

        if len(extractInput) == 4:
            # >> pdfPlus.py E <FileToExtract.pdf> <PageNum>
            self.fileOperation = self.__getFileOperation(extractInput[1])
            self.fileName = [self.__getFileNameWithPath(extractInput[2])]
            self.pageRange = self.__getPageNum(extractInput[3])
        elif len(extractInput) == 3:
            # >> pdfPlus.py E <PageNum>
            self.fileOperation = self.__getFileOperation(extractInput[1])
            self.fileName = self.__getPDFFileNameFromDir()
            self.pageRange = self.__getPageNum(extractInput[2])
        else:
            raise ValueError('Invalid Input to process Extract Operation. See Help')

    def ParseInputs(self, args):
        '''
        def ParseInputs(self, args)
        This method parses the input sent by command line, and updates the member variable of the PDFPlus class.
        @param args: The arguments passed by command line
        @return: None
        '''
        if len(args) > 1:
            self.fileOperation = args[1]

        if (self.fileOperation.upper() == 'R'):
            self.__getReadParams(args)
        elif (self.fileOperation.upper() == 'M'):
            self.__getMergeParams(args)
        elif (self.fileOperation.upper() == 'S'):
            self.__getSplitParams(args)
        elif (self.fileOperation.upper() == 'E'):
            self.__getExtractParams(args)
        else:
            raise ValueError('Valid Operations are (R)ead,, (M)erge, (S)plit and (E)xtract')


    def ReadPDF(self):
        '''
        def ReadPDF(self):
        This method is the primary interface to read the PDFfile.
        return: None.
        '''
        pdfReadIndex = 1 # To increment the index, since it always starts from 0
        logging.debug("in ReadPDF Method")
        logging.debug("FileName is: {}".format(self.fileName))
        logging.debug("Initial PDF file name is : {}".format(self.fileName))
        # Validate that the files in the directory are pdf files
        isValidPFD = self.__validatePDF()
        logging.debug("isValidPFD : {}".format(isValidPFD))
        if isValidPFD:
            for pfdFile in self.fileName:
                workingPath = self.__getPDFPath(pfdFile)
                workingFile = self.__getBaseFileName(pfdFile)
                logging.debug("PDF File Name : {}".format(pfdFile))
                logging.debug("PDF File Operation : {}".format(self.fileOperation))
                logging.debug("Working Path : {}".format(workingPath))
                logging.debug("Working File : {}".format(workingFile))
                pfdFileObj = open(workingPath+'\\'+workingFile, 'rb')
                txtFilehandle = open(workingPath+'\\'+workingFile.replace('pdf', 'txt'), 'w')
                pdfReaderObj = PyPDF2.PdfFileReader(pfdFileObj)
                logging.debug("Number of pages in pdf file is %s"%pdfReaderObj.numPages)
                self.__validateAndUpdatePageRange(pdfReaderObj.numPages)
                if not self.pageRange:
                    for i in range(pdfReaderObj.numPages):
                        self.pageRange.append(i)
                logging.debug("self.pageRange: %s"%self.pageRange)

                # add logic to print correct page numbers since when we print all page we run from index 0...n.
                if self.pageRange[0] == 0:
                    incrementPage = 1
                else:
                    incrementPage = 0

                for pageIndex in self.pageRange:
                    logging.debug('pageIndex : {}'.format(pageIndex))
                    logging.debug('calculation : {}'.format(pageIndex-pdfReadIndex+incrementPage))
                    pageObj = pdfReaderObj.getPage(pageIndex-pdfReadIndex+incrementPage)
                    pageText = pageObj.extractText()
                    # Write PDF Data to a text file
                    self.__writePDFDataToTextFile(txtFilehandle, pageIndex+incrementPage, pageText)
                txtFilehandle.close()
                pfdFileObj.close()
                # setting the variable blank after use, so that it can be re-used if there are multiple PDF Files
                self.pageRange = []
        else:
            raise IOError('Either no PDF File or Invalid PDF File. Please verify the path and the file.')

    def MergePDF(self):
        '''
        This method merges two or more PDF File which is kept in C:\Temp\PDFPlus directory.
        #TODO: Update this method to work with below command
        >>PDFPlus.py M <NewFileName> where newFile name is an argument passed by user.
        This should be the file name of the new file generated after merging.
        @return: None.
        '''
        # TODO: See comments inline
        logging.debug("in MergePDF Method")
        logging.debug("FileName is: {}".format(self.fileName))
        if self.mergeFileOutput in self.fileName:
            self.fileName.remove(self.mergeFileOutput)
        # Validate that the files in the directory are pdf files
        isValidPFD = self.__validatePDF()
        logging.debug("isValidPFD : {}".format(isValidPFD))
        if isValidPFD:
            # Create PDF Writer Object
            pdfWriterObj = PyPDF2.PdfFileWriter()
            for pfdFile in self.fileName:
                workingPath = self.__getPDFPath(pfdFile)
                workingFile = self.__getBaseFileName(pfdFile)
                logging.debug("PDF File Name : {}".format(pfdFile))
                fileObj = open(workingPath+'\\'+workingFile, 'rb')
                pdfReaderObj = PyPDF2.PdfFileReader(fileObj)
                logging.debug("Number of pages in pdf file is %s"%pdfReaderObj.numPages)
                for pageIndex in range(pdfReaderObj.numPages):
                    pageObj = pdfReaderObj.getPage(pageIndex)
                    pdfWriterObj.addPage(pageObj)
            mergedPDFFile = open(workingPath+'\\'+self.mergeFileOutput, 'wb')
            pdfWriterObj.write(mergedPDFFile)
            mergedPDFFile.close()
            fileObj.close()
        else:
            raise IOError('Either no PDF File or Invalid PDF File. Please verify the path and the file.')

    def SplitPDF(self):
        '''
        This method splits all the pages of a PDF file and creates separate PDF documents.
        @return: To be implemented
        '''
        logging.debug("in SplitPDF Method")
        logging.debug("FileName is: {}".format(self.fileName))
        # Validate that the files in the directory are pdf files
        isValidPFD = self.__validatePDF()
        logging.debug("isValidPFD : {}".format(isValidPFD))
        if isValidPFD:
            # Create PDF Writer Object
            for pfdFile in self.fileName:
                workingPath = self.__getPDFPath(pfdFile)
                workingFile = self.__getBaseFileName(pfdFile)
                logging.debug("PDF File Name : {}".format(pfdFile))
                fileObj = open(workingPath + '\\' + workingFile, 'rb')
                pdfReaderObj = PyPDF2.PdfFileReader(fileObj)
                logging.debug("Number of pages in pdf file is %s" % pdfReaderObj.numPages)
                for pageIndex in range(pdfReaderObj.numPages):
                    pdfWriterObj = PyPDF2.PdfFileWriter()
                    pageObj = pdfReaderObj.getPage(pageIndex)
                    pdfWriterObj.addPage(pageObj)
                    outputPDFFile = open(workingPath + '\\'+str(pageIndex+1)+"_"+workingFile, 'wb')
                    pdfWriterObj.write(outputPDFFile)
                    outputPDFFile.close()
            fileObj.close()
        else:
            raise IOError('Either no PDF File or Invalid PDF File. Please verify the path and the file.')


    def ExtractPDF(self):
        '''
        PDF Extraction Implementation
        @return: To be implemented
        '''
        logging.debug("in ExtractPDF Method")
        logging.debug("FileName is: {}".format(self.fileName))
        # Validate that the files in the directory are pdf files
        isValidPFD = self.__validatePDF()
        logging.debug("isValidPFD : {}".format(isValidPFD))
        if isValidPFD:
            # Create PDF Writer Object
            for pfdFile in self.fileName:
                workingPath = self.__getPDFPath(pfdFile)
                workingFile = self.__getBaseFileName(pfdFile)
                logging.debug("PDF File Name : {}".format(pfdFile))
                fileObj = open(workingPath + '\\' + workingFile, 'rb')
                pdfReaderObj = PyPDF2.PdfFileReader(fileObj)
                logging.debug("Page Range is %s" %self.pageRange)
                logging.debug("Number of pages in pdf file is %s" % pdfReaderObj.numPages)
                self.__validateAndUpdatePageRange(pdfReaderObj.numPages)
                for pageIndex in self.pageRange:
                    logging.debug("Page Index is  {}".format(pageIndex))
                    pdfWriterObj = PyPDF2.PdfFileWriter()
                    pageObj = pdfReaderObj.getPage(pageIndex-1)
                    pdfWriterObj.addPage(pageObj)
                    outputPDFFile = open(workingPath + '\\'+str(pageIndex)+"_"+workingFile, 'wb')
                    pdfWriterObj.write(outputPDFFile)
                    outputPDFFile.close()
            fileObj.close()
        else:
            raise IOError('Either no PDF File or Invalid PDF File. Please verify the path and the file.')


    def PDFOperation(self):
        '''
        This method determines what PDF Operation is to be performed.
        @return: None. raises exception is the fileOperation is not a valid value.
        '''
        logging.debug("In PDFOperation method.")
        if self.fileOperation == 'R':
            self.ReadPDF()
        elif self.fileOperation == 'M':
            self.MergePDF()
        elif self.fileOperation == 'S':
            self.SplitPDF()
        elif self.fileOperation == 'E':
            self.ExtractPDF()
        else:
            raise ValueError('Invalid Input. Please see help')


# ******************************* Program Execution Starts here *****************************************************
# Create Class Object
pdfObj = PDFPlus()

# Create the temp/pdfplus directory if not present already.
if not os.path.exists(pdfObj.PDFPlusPath):
    os.makedirs(pdfObj.PDFPlusPath)

if len(sys.argv) > 1:
    if sys.argv[1].upper() == 'HELP':
        print pdfObj.__doc__
        print pdfObj.ParseInputs.__doc__
        print pdfObj.ReadPDF.__doc__
    else:
        try:
            pdfObj.ParseInputs(sys.argv)
            pdfObj.PDFOperation()
        except (ValueError, IOError):
            errorHande = open(pdfObj.PDFPlusPath+'PDFPlusLog.txt', 'w')
            logging.critical('PDF Operation could not be completed due to critical error in the input. \
            Please see the logs for details.')
            errorHande.write(traceback.format_exc())
            errorHande.close()
            logging.info('The traceback info was written to errorInfo.txt.')
else:
    try:
        pdfObj.ParseInputs(sys.argv)
        pdfObj.PDFOperation()
    except (ValueError, IOError):
        errorHandle = open(pdfObj.PDFPlusPath + 'PDFPlusLog.txt', 'w')
        logging.critical('PDF Operation could not be completed due to critical error in the input.\
        Please see the logs for details.')
        errorHandle.write(traceback.format_exc())
        errorHandle.close()
        logging.info('The traceback info was written to errorInfo.txt.')
