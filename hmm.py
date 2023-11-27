input_file = open("hmm.in", "r")
sequences = []
values = []
measurements = []
measurement_probs = {}
state_probs = {}
cases = []

def getPS(s):
    #print(f"P({s})")
    if s in state_probs.keys():
        #print(f"return P({s})")
        return state_probs[s]
    else:
        state_probs[s] = 0
        for i in list(state_probs):
            if i.startswith(s[0]):
                if not i[-1].isdigit():
                    state_probs[s] = state_probs[s] + state_probs[i]*getPS(i[1]+str(int(s[1:])-1))
                    if(s[0] == values[0]):
                        state_probs[values[1]+s[1:]] = 1 - state_probs[s]
                        #print(f"{values[1]+s[1:]}: {state_probs[values[1]+s[1:]]}")
                    else:
                        state_probs[values[0]+s[1:]] = 1 - state_probs[s]
                        #print(f"{values[0]+s[1:]}: {state_probs[values[0]+s[1:]]}")
                    #print(f"{s}: {state_probs[s]}")

        return state_probs[s]

def getPM(m):
    PM = 0
    for i in list(measurement_probs):
            if i.startswith(m[0]):
                PM = PM + measurement_probs[i]*state_probs[i[1]+m[1:]]
                #print(f"+ {measurement_probs[i]}*{state_probs[i[1]+m[1]]}")
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
    print(f"Cases: {cases}")

    input_file.close()
    output = open("hmm.out", "w")

    #determine probabilities for each possible state
    #TODO: replace sequences[0] with loop
    for sequence in sequences:
        state_probs = {}
        for i in range(len(values)):
            for j in range(len(values)):
                a = 0
                b = 0
                for k in range(len(sequence)-1):
                    if(sequence[k] == values[j]):
                        b += 1
                        if(sequence[k+1] == values[i]):
                            a+=1
                #print(f"{values[i]+values[j]}: {a}/{b} = {a/b}")
                state_probs[values[i]+values[j]] = a/b
        #determine probability for each possible starting state
        for i in range(len(values)):
            state_probs[values[i]+"0"] = 1 if sequence[0] == values[i] else 0
        print(f"State Probabilities: {state_probs}")
        
        output.write(sequence + "\n")
        case_probs = {}
        for i in range(len(cases)):
            case_probs[i] = (measurement_probs[cases[i][1][0]+cases[i][0][0]]*getPS(cases[i][0])) / getPM(cases[i][1])
            #print(f"({measurement_probs[cases[i][1][0]+cases[i][0][0]]} * {str(getPS(cases[i][0]))[:6]}) / {str(getPM(cases[i][1]))[:6]} = {str(case_probs[i])[:6]}")
            output.write(f"{cases[i][0]} given {cases[i][1]} = {str(case_probs[i])[:6]}\n")
        
    output.close()