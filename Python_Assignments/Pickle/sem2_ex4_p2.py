import pickle

# This contains code that writes a dictionary to a pickle file. 
# A function called createDummyPickle writes a dictionary to a pickle. 
# The contents of that file can be viewed by calling a second function called viewPickle. 
# You are required to complete a third method called addClassAverage. 
# This takes the name of the pickle file. 
# You should complete the function by having it open the pickle file, read the dictionary,
# calculate an average value for the student scores, add this to the dictionary with key ‘classaverage’ 
# and write the modified dictionary back to the same pickle file.   

def createDummyPickle(filename, dict):
    '''
        name: createDummyPickle
        inputs: filename - string with filename
                dict - dictionary to write to file
        returns: none
        exceptions: none
    '''

    fout = open(filename, "wb") #open file for binary write 

    pickle.dump(dict, fout) #dump dict to pickle
    
    fout.close() #close file

def viewPickle(filename):
    '''
        name: viewPickle 
        inputs: filename - string with filename
        returns: none
        exceptions: none
    '''
    fin = open(filename, "rb")
    mydict = pickle.load(fin)
    fin.close()

    print(mydict)

def addClassAverage(filename):
    '''
        name: updateWithAverage
        inputs: filename - string with filename
        returns: none
        exceptions: none
    '''

    # open file in read, assign to mydict, then close file
    fin = open(filename, "rb")
    mydict = pickle.load(fin)
    fin.close()

    #Get average of dictionary values, and update dictionary
    average = sum(mydict.values()) / (len(mydict))
    mydict["classaverage"] = average

     # Save the dictionary to the pickle file
    fout = open(filename, "wb")
    pickle.dump(mydict, fout)
    fout.close() #close file


    

if __name__ == "__main__":

    filename = "mydata.dat"
    mydict = {"Cathal":100, "Polly":90, "Laura":80}
    createDummyPickle(filename, mydict)
    addClassAverage(filename)
    viewPickle(filename)