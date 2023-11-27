# EXERCISE #9 HIDDEN MARKOV MODELS
# AUTHOR: Samantha Shane C. Dollesin
# STUDENT NO.: 2020-01893
# SECTION: WX-1L

input_file = open("hmm.in", "r")
sequences = []
values = []
measurements = []
measurement_probs = {}
transition_probs = {}
cases = []

#This is a recursive function that calculates for P(s) using total probability
def getPS(s):
    #print(f"P({s})")
    if s in transition_probs.keys():     #if the value for P(s) has already been computed, return the value
        #print(f"return P({s})")
        return transition_probs[s]
    else:                           #otherwise, solve for the value using recursion
        transition_probs[s] = 0
        for i in list(transition_probs):
            if i.startswith(s[0]):
                if not i[-1].isdigit():
                    transition_probs[s] = transition_probs[s] + transition_probs[i]*getPS(i[1]+str(int(s[1:])-1))
                    if(s[0] == values[0]):
                        transition_probs[values[1]+s[1:]] = 1 - transition_probs[s]
                        #print(f"{values[1]+s[1:]}: {transition_probs[values[1]+s[1:]]}")
                    else:
                        transition_probs[values[0]+s[1:]] = 1 - transition_probs[s]
                        #print(f"{values[0]+s[1:]}: {transition_probs[values[0]+s[1:]]}")
                    #print(f"{s}: {transition_probs[s]}")

        return transition_probs[s]

def getPM(m):
    PM = 0
    for i in list(measurement_probs):
            if i.startswith(m[0]):
                PM = PM + measurement_probs[i]*transition_probs[i[1]+m[1:]]
                #print(f"+ {measurement_probs[i]}*{transition_probs[i[1]+m[1]]}")
    return PM
        
if (input_file.readable()):
    
    #get the string sequences
    numString = int(input_file.readline().strip()) 
    for i in range(numString):
        sequences.append(input_file.readline().strip())

    #determine the values
    values = input_file.readline().strip().split(" ")
    #determine the measurements
    measurements = input_file.readline().strip().split(" ")

    #create a dictionary for storing the respective probability of each measurement
    #example: {'ES': 0.1, 'FS': 0.9, 'ET': 0.6, 'FT': 0.4}
    for i in range(len(values)):
        probs = input_file.readline().strip().split(" ")
        for j in range(len(measurements)):
            measurement_probs[measurements[j]+values[i]] = float(probs[j])
    print(f"Measurement Probabilities: {measurement_probs}")

    #extract the cases
    numCases = int(input_file.readline().strip()) 
    for i in range(numCases):
        cases.append(input_file.readline().strip().split(" given "))
    print(f"Cases: {cases}\n")

    input_file.close()
    output = open("hmm.out", "w")

    #determine probabilities for each possible transition
    for sequence in sequences:
        print(f"Sequence: {sequence}")
        transition_probs = {}
        for i in range(len(values)):
            for j in range(len(values)):
                b = 0   #contains the total number of S or T with a next state
                a = 0   #contains the number of S or T followed by a given value out of b occurances
                for k in range(len(sequence)-1):
                    if(sequence[k] == values[j]):   
                        b += 1
                        if(sequence[k+1] == values[i]):
                            a+=1
                #print(f"{values[i]+values[j]}: {a}/{b} = {a/b}")
                transition_probs[values[i]+values[j]] = a/b
        #determine probability for possible starting states
        for i in range(len(values)):
            transition_probs[values[i]+"0"] = 1 if sequence[0] == values[i] else 0
        #print(f"Transition Probabilities: {transition_probs}")
        
        #compute for each case and write results to output file
        output.write(sequence + "\n")
        case_probs = {}   #stores the value computed for each case
        for i in range(len(cases)):
            case_probs[i] = (measurement_probs[cases[i][1][0]+cases[i][0][0]]*getPS(cases[i][0])) / getPM(cases[i][1])
            #print(f"({measurement_probs[cases[i][1][0]+cases[i][0][0]]} * {str(getPS(cases[i][0]))[:6]}) / {str(getPM(cases[i][1]))[:6]} = {str(case_probs[i])[:6]}")
            output.write(f"{cases[i][0]} given {cases[i][1]} = {str(case_probs[i])[:6]}\n")
        print(f"Transition Probabilities: {transition_probs}\n")

    output.close()