"""
import time 
t = time.strftime('%H:%M:%S')
hour = int(time.strftime('%H')) 
print(hour)
for a in  range(hour>=59):
  
  print (hour)
  a=a+1

if(hour>=0 and hour<12):
  print("Good Morning Sir!")
elif(hour>=12 and hour<17):
  print("Good Afternoon Sir!")
elif(hour>=17 ):
  print("Good Night Sir!")
  
 



a=[1,2,3,4,5,6,7,8,99,44,43,523,63,51]
print(a[0])
b=int(input())
if ( b in a):
    print("hello")
print(a[2:7]






a=[11,222,333,2,1,0]
a.append(2)
a.insert(1,22)
a.sort()
a.remove(11)
print(a.count(1))
b=[1,2,3,4,56,7,78]
a.reverse
c=a=b=a=1
a=c=2
c=b=3
b=a
print(c,b) 




en_a=int(input("enter the value of en\n"))
en_b=int(input("enter the value of en\n"))
for a in range(en_a,en_b):
    print(a)

if(en_a<en_b):
    print("h\n",en_a)
a=5
while a==5: 
  letter = (input("enter your string"))
  country = "India"
  name = "Harry"

  print(letter.format( name,country))
#print(f"Hey my name is {name} and I am from {country}")
print(f"We use f-strings like this: Hey my name is {{name}} and I am from {{country}}")
price = 49.09999
txt = f"For only {price:f} dollars!"
print(txt)
print(txt.format())
print(type(f"{2 * 30}"))

for a in range(1,9):
    a=a+a+1
    print(a)
set={"amit",1,3,4,4.555,"helo"}
setb={"amit",1,3,4,4.555,"helo"}
setc={1,4,6}
set.discard(1)
setb.discard(1)
set.difference_update(setc)
set.clear()
print(set.intersection(setb))
seta=set.union(setb)
print(seta)
if(set==setb):
    print("they are equal")
else:
    print("they are not equal")    
info = {'name':'Karan', 'age':19, 'eligible':True}
# print(info) 
# print(info.keys())
# print(info.values())

# for key in info.keys():
#   print(f"The value corresponding to the key {key} is {info[key]}")

print(info.items())
for key, value in info.items():
  print(f"The value corresponding to the key {key} is {value}") 
def sum(a, b, c ):
    return a + b + c

def printBoard(xState, zState):
    zero = 'X' if xState[0] else ('O' if zState[0] else 0)
    one = 'X' if xState[1] else ('O' if zState[1] else 1)
    two = 'X' if xState[2] else ('O' if zState[2] else 2)
    three = 'X' if xState[3] else ('O' if zState[3] else 3)
    four = 'X' if xState[4] else ('O' if zState[4] else 4)
    five = 'X' if xState[5] else ('O' if zState[5] else 5)
    six = 'X' if xState[6] else ('O' if zState[6] else 6)
    seven = 'X' if xState[7] else ('O' if zState[7] else 7)
    eight = 'X' if xState[8] else ('O' if zState[8] else 8)
    print(f"{zero} | {one} | {two} ")
    print(f"--|---|---")
    print(f"{three} | {four} | {five} ")
    print(f"--|---|---")
    print(f"{six} | {seven} | {eight} ") 

def checkWin(xState, zState):
    wins = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
    for win in wins:
        if(sum(xState[win[0]], xState[win[1]], xState[win[2]]) == 3):
            print("X Won the match")
            return 1
        if(sum(zState[win[0]], zState[win[1]], zState[win[2]]) == 3):
            print("O Won the match")
            return 0
    return -1
    
if __name__ == "__main__":
    xState = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    zState = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    turn = 1 # 1 for X and 0 for O
    print("Welcome to Tic Tac Toe")
    while(True):
        printBoard(xState, zState)
        if(turn == 1):
            print("X's Chance")
            value = int(input("Please enter a value: "))
            xState[value] = 1
        else:
            print("O's Chance")
            value = int(input("Please enter a value: "))
            zState[value] = 1
        cwin = checkWin(xState, zState)
        if(cwin != -1):
            print("Match over")
            break
        
        turn = 1 - turn
# a = input("Enter the number: ")
# print(f"Multiplication table of {a} is: ")
# try:
#   for i in range(1, 11):
#     print(f"{int(a)} X {i} = {int(a)*i}")
# except:
#   print("Invalid  Input!")

# print("Some imp lines of code")
# print("End of program")

try:
    num = int(input("Enter an integer: "))
    w = [6, 3]
    print(a[num])
except:
    print("Number entered is not an integer.")
    
print("hello")
questions = [

import os

if(not os.path.exists("data")):
    os.mkdir("c++")

for i in range(0, 2):
    os.mkdir(f"c++/Day{i+1}")
import os
folders = os.listdir("c++")
os.rename("a++","")
try:
  for folder in folders:
    print(folder)
    print(os.listdir(f"c++/{folder}"))
except:
  print(folder)  
f=open('ak.py','r')
text=f.read()
print(text)
f.close()
f = open('myfile.txt', 'a')
f.write('Hello, world!')
f.close()


with open('myfile.txt', 'a') as f:
  f.write("Hey I am inside with")
a=4
while a>=2:
    b=int(input("enter the number\n"))
    c=int(input("enter the number 2\n"))
    d=b%c
    print(d)
  


#metooo

# l = [1, 2, 4, 6, 4, 3]
# # newl = []
# # for item in l:
# #   newl.append(cube(item))

# newl = list(map(lambda x: x*x*x, l))
# print(newl)

# # FILTER
# def filter_function(a):
#   return a>2
  
# newnewl = list(filter(filter_function, l))
# print(newnewl)

from functools import reduce

# List of numbers
numbers = [1, 2, 3, 4, 5] 

# Calculate the sum of the numbers using the reduce function
def mysum(x, y):
  return x + y
  
sum = reduce(mysum, numbers)

# Print the sum
print(sum)
import os

if(not os.path.exists("data")):
    os.mkdir("b++")

for i in range(0, 2):
    os.mkdir(f"b++/Day{i+1}")

folders = os.listdir("c++")
os.rename("b++","00")
try:
  for folder in folders:
    print(folder)
    print(os.listdir(f"00/{folder}"))
except:
  print(folder) ?
import os
os.rmdir("00")  """
#import os
#appli = r"C:\Users\91935\Desktop\my doc"
#os.startfile(appli)"""
"""
class Person:
  name = "Harry"
  occupation = "Software Developer"
  networth = 10
  def info(self):
    print(f"{self.name} is a {self.occupation}")


a = Person()
b = Person()
c = Person()

a.name = "Shubham"
a.occupation = "Accountant"

b.name = "amit"
b.occupation = ""

# print(a.name, a.occupation)
a.info()
b.info()
c.info()
class Person:

  def __init__(self, name, occ):
    print("Hey I am a person")
    self.name = name
    self.occ = occ

  def info(self):
    print(f"{self.name} is a {self.occ}")


a = Person("Harry", "Developer")
b = Person("Divya", "HR") 
a.info()
b.info()
# print(a.name)
# a.name = "Divya"
# a.occ = "HR"
# a.info()
marks = [12, 56, 32, 98, 12,  45, 1, 4]

# index = 0
# for mark in marks:
#   print(mark)
#   if(index == 3):
#     print("Harry, awesome!")
#   index +=1

for index, mark in enumerate(marks, start=1):
  print(mark)
  if(index == 3):
    print("Harry, awesome!")

def greet(fx):
  def mfx(*args, **kwargs):
    print("Good Morning")
    fx(*args, **kwargs)
    print("Thanks for using this function")
  return mfx
devi62725
@greet
def hello():
  print("Hello world")

@greet
def add(a, b):
  print(a+b)
 
# greet(hello)()
hello()
# greet(add)(1, 2)
add(1, 2)
#zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz
import logging

def log_function_call(func):
    def decorated(*args, **kwargs):
        logging.info(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        logging.info(f"{func.__name__} returned {result}")
        return result
    return decorated

@log_function_call
def my_function(a, b):
    return a + b    
    """
"""
n = 10
num1 = 0
num2 = 1
next_number = num2  
count = 1
 
while count <= n:
    print(next_number, end=" ")
    count += 1
    num1, num2 = num2, next_number
    next_number = num1 + num2
print()

n=1
i=1
j=1
for i in range(3,5):
    
    
    for j in range (1,i):
        print(j,end="")
    print("")    
m=10    

nterms=8
n1, n2 = 0, 1
count = 0

while count < nterms:
       print(n2)
       nth = n1 + n2
       # update values
       n1 = n2
       n2 = nth
       count += 1   
 
class Library:
  def __init__(self):
    self.noBooks = 0
    self.books = []
    
  def addBook(self, book):
    self.books.append(book)
    self.noBooks = len(self.books)

  def showInfo(self):
    print(f"The library has {self.noBooks} books. The books are")
    for book in self.books:
      print(book)

a=0
l1 = Library()
while a<=4:
  name =input("inter the book name")
  l1.addBook(name)
  a+=1
l1.showInfo()

import os

if(not os.path.exists("data")):
    os.mkdir("b++")

for i in range(0, 2):
    os.mkdir(f"b++/Day{i+1}")
import os
folders = os.listdir("c++")
os.rename("a++","")
try:
  for folder in folders:
    print(folder)
    print(os.listdir(f"b++/{folder}"))
except:
  print(folder)  
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def save_code_to_pdf(file_path, output_pdf):
    # Read the Python code
    with open(file_path, 'r') as file:
        code = file.readlines()

    # Create the PDF file
    c = canvas.Canvas(output_pdf, pagesize=letter)
    c.setFont("Courier", 10)  # Use monospaced font for exact indentation

    # Adjust margins and line height
    x_margin = 50
    y_margin = 750
    line_height = 12

    # Add line numbers and code to the PDF
    line_number = 1
    for line in code:
        # Strip any trailing whitespace characters like newlines or carriage returns
        line = line.rstrip()

        # Print line number and the corresponding code with exact indentation
        c.drawString(x_margin, y_margin, f"{line_number:4}: {line}")
        line_number += 1
        y_margin -= line_height

        # Check if we need a new page
        if y_margin < 50:
            c.showPage()
            y_margin = 750

    # Save the PDF
    c.save()

# Example usage
save_code_to_pdf('test.py', 'output_code.pdf')
"""
import os
import subprocess
import re

def sanitize_filename(filename):
    """Remove invalid characters from filename"""
    return re.sub(r'[\\/*?:"<>|]', "", filename)

def download_playlist_as_mp3(playlist_url, output_path="downloads"):
    """
    Downloads all videos from a YouTube playlist and converts them to MP3 using yt-dlp.
    
    Args:
        playlist_url (str): URL of the YouTube playlist
        output_path (str): Directory to save the MP3 files
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)
    
    print(f"Starting download of playlist...")
    
    try:
        # Use yt-dlp to download and convert to mp3
        subprocess.run([
            'yt-dlp',
            '-x',  # Extract audio
            '--audio-format', 'mp3',  # Convert to mp3
            '--audio-quality', '0',  # Best quality
            '--embed-thumbnail',  # Embed thumbnail in audio file
            '--add-metadata',  # Add metadata
            '--output', f'{output_path}/%(title)s.%(ext)s',
            playlist_url
        ], check=True)
        
        print("\nAll downloads completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"\nError occurred during download: {e}")

if __name__ == "__main__":
    # Get playlist URL from user
    playlist_url = input("Enter YouTube playlist URL: ").strip()
    
    # Optional: Get custom output path
    output_path = input("Enter output directory (leave blank for 'downloads'): ").strip()
    output_path = output_path if output_path else "downloads"
    
    # Download and convert
    download_playlist_as_mp3(playlist_url, output_path)