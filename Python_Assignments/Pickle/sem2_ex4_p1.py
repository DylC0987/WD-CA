# Question 1.  
#This contains code that writes a dictionary to a pickle file. 
#A function called createDummyPickle writes a dictionary to a pickle.
#The contents of that file can be viewed by calling a second function that you have been provided with called viewPickle. 
# You are required to complete a third method called update. 
# This takes the name of the pickle file, a student name and their score. 
# This function should open the pickle and add/update the student score before resaving the pickle.   
 
import pickle

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

def update(filename, name, newvalue):
    '''
        name: updateWithAverage
        inputs: filename - string with filename
                name - string with name to update
                newvalue - number with value to update
        returns: none
        exceptions: none
    '''
    # load pickle data to dictionary
    # Add or update the key in the loaded dictionary
   
    fin = open(filename, "rb") #open file for binary write 

    mydict = pickle.load(fin)

    fin.close()

    # update mydict
    mydict[name] = newvalue

    # Save the dictionary to the pickle file
    fout = open(filename, "wb")
    pickle.dump(mydict, fout)
    fout.close() #close file

if __name__ == "__main__":

    filename = "mydata.dat"
    mydict = {"Cathal":100, "Polly":90, "Laura":80}
    createDummyPickle(filename, mydict)
    update(filename, "Cathal", 60)
    viewPickle(filename)