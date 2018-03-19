*************************
*	Web Crawler	*
*  CSE 5337 Project #1  *
*     Henry Warren      *
*    hwarren@smu.edu    *
*************************


OVERVIEW
- Program written entirely in Python 3.6
- Non-standard libraries used:
--> BeautifulSoup4


INSTALLATION
1. Unzip project archive.
2. Assuming you have Python 3 installed on you machine,
open a terminal window and run the following command:

$ pip install BeautifulSoup4

If you do not have Python 3 installed on your machine, you can 
follow the instructions for your respective operating system provided here:
http://docs.python-guide.org/en/latest/starting/install3/win/
http://docs.python-guide.org/en/latest/starting/install3/linux/
http://docs.python-guide.org/en/latest/starting/install3/osx/


EXECUTION
1. Open a terminal window and navigate to the project directory 
containing all the source files.
2. Run the following command:

$ python3 master.py 100 stopwords.txt

(note that 100 is an example value for input argument N, the parameter that 
limits the number of pages our crawler will visit before exiting. the second
argument is the path to a text file containing a \n-delimited list of stop words)


OUTPUT
1. Observe the program output in the console. This information pertains to 
the questions posed in the project requirements.
2. Observe the term-frequency matrix in the csv file named "term-frequency.csv".
This file can be found in the directory "out" located in the "src" folder.

matrix output location: /src/out/term-frequency.csv
