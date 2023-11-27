input_file = open("hmm.in", "r")
sequences = []
values = []
measurements = []
measurement_probs = {}
state_probs = {}
cases = []
case_probs = {}

def getPS(s):
    print(f"s: {s}")
    if s in state_probs.keys():
        #print(f"return {s}")
        return state_probs[s]
    else:
        state_probs[s] = 0
        #print(state_probs.keys())
        for i in list(state_probs):
            if i.startswith(s[0]):
                if not i[-1].isdigit():
                    state_probs[s] = state_probs[s] + state_probs[i]*getPS(i[1]+str(int(s[1])-1))
                    if(s[0] == values[0]):
                        state_probs[values[1]+s[1]] = 1 - state_probs[s]
                        #print(f"{values[1]+s[1]}: {state_probs[values[1]+s[1]]}")
                    else:
                        state_probs[values[0]+s[1]] = 1 - state_probs[s]
                        #print(f"{values[0]+s[1]}: {state_probs[values[0]+s[1]]}")
                    #print(f"{s}: {state_probs[s]}")

        return state_probs[s]
                

def getPM(m):
    PM = 0
    for i in list(measurement_probs):
            if i.startswith(m[0]):
                PM = PM + measurement_probs[i]*state_probs[i[1]+m[1]]
                #print(f"+ {measurement_probs[i]}*{state_probs[i[1]+m[1]]}")
    return PM
        
if (input_file.readable()):
    
    #no. of string sequences to be considered
    numString = int(input_file.readline().strip())
    #get the string sequences
    for i in range(numString):
        sequences.append(input_file.readline().strip())
    print(f"sequences: {sequences}")

    #determine the values
    values = input_file.readline().strip().split(" ")
    print(f"values: {values}")

    #determine the measurements
    measurements = input_file.readline().strip().split(" ")
    print(f"measurements: {measurements}")

    #create a dictionary for storing the respective probability of each measurement
    #example: {'ES': 0.1, 'FS': 0.9, 'ET': 0.6, 'FT': 0.4}
    for i in range(len(values)):
        probs = input_file.readline().strip().split(" ")
        for j in range(len(measurements)):
            measurement_probs[measurements[j]+values[i]] = float(probs[j])
    print(f"measurement_probs: {measurement_probs}")

    #determine number of cases to solve
    numCases = int(input_file.readline().strip())
    #extract the cases
    for i in range(numCases):
        case = input_file.readline().strip().replace(" given ", "")
        cases.append(case)
        case_probs[case] = 0
    print(f"cases: {cases}")

    #determine probabilities for each possible state
    #TODO: replace sequences[0] with loop
    for i in range(len(values)):
        for j in range(len(values)):
            a = 0
            b = 0
            for k in range(len(sequences[0])-1):
                if(sequences[0][k] == values[j]):
                    b += 1
                    if(sequences[0][k+1] == values[i]):
                        a+=1
            #print(f"{values[i]+values[j]}: {a}/{b} = {a/b}")
            state_probs[values[i]+values[j]] = a/b
    #determine probability for each possible starting state
    for i in range(len(values)):
        state_probs[values[i]+"0"] = 1 if sequences[0][0] == values[i] else 0
    print(f"state_probs: {state_probs}")
    
    case_probs[cases[0]] = (measurement_probs[cases[0][2]+cases[0][0]]*getPS(cases[0][:2])) / getPM(cases[0][2:])
    print(f"({(measurement_probs[cases[0][2]+cases[0][0]])} * {getPS(cases[0][:2])}) / {getPM(cases[0][2:])}")
    print(f"= {case_probs[cases[0]]}")

