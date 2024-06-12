# creating a custom exception
class BioFlowInsightError(Exception):
    """
    This is the custom BioFlow-Insight error class, from this class, errors can be made.

    Attributes:
        error: A string indicating the error message to the user
        num: An integers indicating the type of error (see below)
        origin: A "Nextflow Building Bloc" derived type object, from this the file address can be given to the user
        
    """
    def __init__(self, error, num, origin = None):
        self.origin = origin
        #TODO -> add message at the end
        if(origin!=None):
            super().__init__(f"[{num}] Error in the file '{self.origin.get_file_address()}': "+error)
        else:
            super().__init__(f"[{num}] {error}")

#To handle the different type of errors; I'm gonna add numbers to the errors 
#Pair numbers if it's the users fault
#Odd if it's the bioflow-insight's fault
#This is really just to be able to do stats

#In the case something can disputed between the two, i categorise it in the users fault
#Since in futur updates i could handle when the tool makes a mistake, but i won't have
#to update the errors -> for example the numnber of parameters for a call
#In the current version, i can't handle implicit parameter (eg. multiple values in the channel)
#In any case, there is always a different way of writing it.

########################
#         PAIR
########################
#* [2] -> not the same number of parameters given for a process or a subworkflow
#* [4] -> a channel is trying to be created with a name already given to something else  
#* [6] -> multiple channels were given by an emit eventhough only expecting one
#* [8] -> tried to acces an emit even though the thing has not been called  
#* [10] -> tried to include a file which doesn't exist
#* [12] -> an include was present in a main or subworkflow
#* [14] -> in a pipe operator, the first thing called is unknown
#* [16] -> syntaxe error in the code
#* [18] -> something is expected to be defined in a file but is not 
#* [20] -> The sibworkflow either emits nothing or to many values for a use in an operation 
#* [22] -> a subworkflow or process defined was defined badly


########################
#         ODD
########################
#* [1] -> presence of an import java or groovy (NOT USED RIGHT NOW) 
#* [3] -> unkonwn thing in a pipe operator  
#* [5] -> A ternary conditional operator was used with an tuple   
#* [7] -> Tuple with emit (ch1, ch2) = emit.out 
#* [9] -> Tuple with call (ch1, ch2) = wf()
#* [11] -> Failed to extract the operation or call at the line x. Try rewriting it in a simplified version.
            
        





            