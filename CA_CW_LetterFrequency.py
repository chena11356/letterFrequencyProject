import random as r

FIRST_ID=ord('a')#enumerates a
LAST_ID=ord('z')#enumerates z
TOTAL_LETTERS=LAST_ID-FIRST_ID+1 #number of letters in alphabet (26)

def fileCheck(fn,op,string): #error handling to check to see if file can be opened
    try:
        f=open(fn,op)
    except IOError:
        print string+"\nError occurred when opening '%s.'"%(fn)
        return -1 #if file cannot be opened, return -1 to indicate no
    return f

def rightJustify(num,string): #spaces out a number to the right by num spaces
    return (num-len(string))*" "+string

def leftJustify(num,string):
    return string+(num-len(string))*" " #spaces out a number to the left by num spaces

def iMax(lst): #determines maximum value of list
    currMax=lst[0]
    for i in lst:
        if i>currMax: #if value of list is greater than temporary max, then it becomes max
            currMax=i
    return currMax

def getCount(fileName,exNum): #gets line count of file
    f=fileCheck("input\\words.txt","r","File not found. Please verify its existence and try again.")
    if f==-1:
        return -1
    numLines=0 #initialize line number as 0
    while True: #loop and increment numLines until the file is over
        isWord=f.readline()
        if isWord == "":
            break
        numLines+=1
    f.close() #close file, return the number of lines
    if numLines < exNum: #error handling if too few lines in input
        print "Too few lines in input, please add more words and try again."
        return -1
    return numLines

def randNum(num,fileName,maxNum): #generates random number list and retrieves words
    numList=[r.randint(1,maxNum) for i in range(num)] #list of numbers
    sortedList=delDuplicates(sort(numList)) #list gets sorted
    f=fileCheck(fileName,"r","File not found, please try again.")
    if f==-1:
        return -1
    crspWord=[] #corresponding words list
    wordNum=0
    ind=0
    while True:
        wordNum+=1
        word=f.readline()
        if word=="":
            print "A word is out of bound. If the file has been modified, restore it to its initial state or choose a new file to use and restart the program."
            f.close()
            return -1 #if word doesn't work, return -1 to indicate no
        if ind==len(sortedList): #if index reaches length of sorted list, then we're done
            break
        if wordNum==sortedList[ind]: #otherwise, increment index and add on word
            ind+=1
            crspWord.append(word.strip()) #add on the word, stripped of extra characters
    f.close()
    return [numList,sortedList,crspWord] #return list of lists

def findJustLen(lst,string): #find the length that output should be justified by
    justLen=len(str(iMax(lst))) #initialize as the length of the longest string
    if justLen<len(string): #if too small, then increase justLen
        justLen=len(string)
    justLen+=1 #add one for an extra space
    return justLen

def generateWords(numList,sortNum,crspWord,fileName):
    f=fileCheck(fileName,"w","File cannot be opened, please try again.") #check to make sure file can be opened
    if f==-1:
        return -1 #if file cannot be opened, return -1 to indicate no
    t=range(1,101) #100 numbers
    colJ1=findJustLen(t,"Number") #find the length to justify each column by
    colJ2=findJustLen(numList,"Random Number")
    colJ3=findJustLen(crspWord,"Word")
    text="" #stuff to add on to each column
    text+=leftJustify(colJ1,"Number")+" "+leftJustify(colJ2,"Random Number")+" "+leftJustify(colJ3,"Word")+"\n"
    i=0 #initialize i as 0
    words=""
    while i<100: #until i reaches 100 words, add on to words
        text+=rightJustify(colJ1-1,str(i+1))+"  "+ rightJustify(colJ2-1,str(numList[i]))+"  "+ leftJustify(colJ3,crspWord[sortNum.index(numList[i])])+"\n"
        words+=crspWord[sortNum.index(numList[i])] #add on corresponding word
        i+=1
    f.write(text)
    f.close()
    return words

def letterCount(lst): #count how many times each letter appears
    extList=[] #initialize empty list
    for i in lst: #add on to empty list by i
        extList.extend(i)
    countList=[0 for s in range(TOTAL_LETTERS)] #list of counts for each letter
    for i in extList: #retrieve each letter of the alphabet
        countList[ord(i)-FIRST_ID]+=1
    return countList #return the list of letter frequencies

def generateLCount(lst): #generate letter count file
    text="" #initialize text and i
    i=0
    justLen=len(str(iMax(lst)))+1 #identify length to justify by
    while i < TOTAL_LETTERS: #build the text and justify it
       text+=leftJustify(4,str(chr(FIRST_ID+i)))
       text+=rightJustify(justLen,str(lst[i]))
       text+='\n'
       i+=1
    f=fileCheck("letter_count.txt",'w',"File cannot be opened, please try again.")
    if f==-1:
        return -1 #if file cannot be opened, return -1 to indicate no
    f.write(text) #write the text into the file
    f.close() #close the file
    return

def generateHistogram(lst): #lst is the list of occurrences of each letter, which the first object being the occurrences of a
    letterlst=[] #initialize empty list
    for char in range(FIRST_ID,LAST_ID+1): #append corresponding letters
        letterlst.append(chr(char))
    res="" #initialize thing to write into file
    i=0 #initialize index
    for char in letterlst: #add on certain amounts of corresponding letter
        temp=char*lst[i] #multiply each character by the corresponding amounts
        res+=temp+"\n" #add on a new line between each new letter
        i+=1 #increment i for the list of numbers
    f=fileCheck("letter_histogram.txt","w","File cannot be opened, please try again")
    if f==-1:
        return -1 #if file cannot be opened, return -1 to indicate no
    f.write(res) #write into file
    f.close() #close file

def issorted(lst): #determines if list is completely sorted
    temp=lst[0]
    res=True
    for char in lst:
        if char<temp: #if the next character is less than the one before it,
            res=False   #then the list is not sorted
        else:
            temp=char #otherwise, move on and temp becomes char
    return res

def swap(lst,i1,i2): #swaps two items of a list
    temp=lst[i1] #index 1
    lst[i1]=lst[i2] #swap
    lst[i2]=temp #swap
    return lst

def sort(lst):
    nlst=lst[:]
    while issorted(nlst)==False: #run through list until it's completely sorted
        temp=nlst[0]
        i=0 #index needed for char swapping
        for char in nlst: #swap if next char is less than previous char
            if char<temp:
                nlst=swap(nlst,i,i-1)
                break #start swapping again from the beginning
            temp=char #current char becomes next char
            i+=1
    return nlst

def delDuplicates(lst): #delete duplicates in a list
    nlst=[] #initialize empty list
    for ele in lst: #for each element of the list, if there are duplicates, break
        i=0
        for char in nlst:
            if char==ele:
                i=1
                break
        if i==0:
            nlst.append(ele)
    return nlst #return list of eles without duplicates

def main(): #main function that calls each function
    lineCount=getCount("input\\words.txt",100) #call each function
    if lineCount==-1: #if anything is -1, basically stop the program
        return
    t=randNum(100,"input\\words.txt",lineCount)
    if t==-1:
        return
    words=generateWords(t[0],t[1],t[2],"random_words.txt")
    if words==-1:
        return
    count=letterCount([words])
    lcount=generateLCount(count)
    if lcount==-1:
        return
    hgram=generateHistogram (count)
    if hgram==-1:
        return
    if lineCount!=getCount("input\\words.txt",100): #if the counts don't correspond, something went wrong
        print "The file has been modified during the course of the program. Output files have been generated based on its initial state."

main()
