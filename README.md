# PDFPlus
Structure contains:
-------------------
1. Src: It contains the source file PDFPlus.py
2. Release_Package: It contains the PDFPlus release package.
(including PDFPlus.exe and all the dependent files).
3. README.md : It contains the help file to use the tool.

Note: If you are using the release package please use PDFPlus.exe instead of PDFPlus.py with refrence to below commands.
Rest all syntax and command remains same.
Application was devloped and tested on windows.  

Dependency:
-----------
For doing any PDF operation please keep the PDF you want to process in C:\Temp\PDFPlus path.
For help on PDFPlus type the command:
>>PDFPlus.py help


PDFPlus contains the implementation for the below functionalities:
***********************************************************************

1. ReadPDF() - R :
-------------
This method reads the PDF File and writes the PDF File contents text file.

Read PDF Valid Commands:
------------------------

>>PDFPlus.py <pagenum>:
This command will read the text (only) from PDF file present in C:\Temp\PDFPlus directory. 
If More than one file is present both the files will be read. The text will be read and 
written to a .txt file in c:\Temp\PDFPlus directly containing the PDF contents.
-------------------------------------------------

>>PDFPlus.py R <fileName> or <pagenum>:
This command will read the text (only) from PDF file present in C:\Temp\PDFPlus Directory. 
If More than one file is present both the files will be read. The text will be read and 
written to a .txt file in c:\Temp\PDFPlus directly containing the PDF contents.
-------------------------------------------------

>>PDFPlus.py R <filename> <pagenum>:
This command will read the text (only) from PDF file <filename> present in the 
C:\Temp\PDFPlus Directory. <filename> can also be complete pdf path.
If this argument is missing the file present in default path will be read. 
<pagenum> is the page number that user wants to read. If this argument is missing 
complete document will be read. 
page num can be :
a number like 20, 31 etc
a range like 5-7, 10-15 etc
seprate page numbers like 5,8,21,25
<TODO> mix of range and separate pages like 5,8,10-15

*************************************************
*************************************************


2. MergePDF() - M :
--------------
This method merges two or more PDF File which is kept in C:\Temp\PDFPlus directory.
This method currently works only on the files kept in C:\Temp|PDFPlus directory.
It can merge all the files together in C:\Temp\PDFPlus directory and creates the result 
file with name MergedByPDFPlus.pdf.

Merge PDF Valid Commands:
------------------------
>>PDFPlus.py M
This command will merge all the PDF Files kept in C:\Temp\PDFPlus directory.

*************************************************
*************************************************


3. SplitPDF() - S:
---------------
This method splits a PDF File which is kept in C:\Temp\PDFPlus directory or, from the 
path given as argument by user.
It will split all the pages and creates multiple pdf file with page numbers of the pdf 
file as prefix, eg 1_MyFile.PDF, 2_MyFile.PDF etc.

Split PDF Valid Commands:
-------------------------

>>PDFPlus.py S
This command will split all the pages from PDF File kept in C:\Temp\PDFPlus directory 
and create new files with page number as prefix.
-------------------------------------------------

>>PDFPlus.py S <FullPath\FileName>
This command will split all the pages from PDF File <FileName> kept in <FullPath> directory 
and create new files with page number as prefix.
-------------------------------------------------

*************************************************
*************************************************

4. ExtractPDF() - E:
-----------------
This method extracts a page number PDF File which is kept in C:\Temp\PDFPlus directory or, 
from the path given as argument by user.
It will extract the given page number and creates separate pdf file with the page numbers of 
the pdf file as prefix, eg 1_MyFile.PDF, 2_MyFile.PDF etc.

Extract PDF Valid Commands:
---------------------------

>>PDFPlus.py E <PageNumber>
This command will extract page <PageNumber> from a PDF File kept in C:\Temp\PDFPlus directory 
and create new files with page number as prefix.
Page number can also be in range format like 5-8, 2-15 etc or or multiple comma separated page 
numbers will also work like 5,6,13,18
-------------------------------------------------

>>PDFPlus.py E <FullPath\FileName> <PageNum>
This command will extract page <PageNum> from PDF File <FileName> kept in <FullPath> directory 
and create new files with page number as prefix. 
Please note that if full path of the file is not given in argument the program will assume the file 
<FileName> is kept in the default path.
Page number can also be in range format like 5-8, 2-15 etc or multiple comma separated page numbers 
will also work like 5,6,13,18
-------------------------------------------------

CAUTION:
1. If no (pdf) file is present in present in C:\Temp\PDFPlus Directory an error will be generated and 
program will terminate.
2. For Read method If the page range given are mixed, an error will be generated and program will terminate.
3. For Extract method if no file name argument is passed and multiple PDF files are present OR If a file name 
argument is passed and PDF file is not present than program will terminate.
The method that supports full path as argument works good with a complete valid PDF path, but its advisory to 
use the application by keeping your PDF files in the default path C:\Temp\PDFPlus

*************************************************