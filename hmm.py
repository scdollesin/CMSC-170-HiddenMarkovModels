input_file = open("hmm.in", "r")

if (input_file.readable()):
    
    #no. of string sequences to be considered
    numString = int(input_file.readline().strip())
    #get the string sequences
    sequences = []
    for i in range(numString):
        sequences.append(input_file.readline().strip())
    print(sequences)

    #determine the values
    values = input_file.readline().strip().split(" ")
    print(values)

    #determine the measurements
    measurements = input_file.readline().strip().split(" ")
    print(measurements)

    #create a dictionary for storing the respective probability of each measurement
    #example: {'SE': 0.1, 'SF': 0.9, 'TE': 0.6, 'TF': 0.4}
    measurement_probs = {}
    for i in range(len(values)):
        probs = input_file.readline().strip().split(" ")
        for j in range(len(measurements)):
            measurement_probs[values[i]+measurements[j]] = float(probs[j])
    print(measurement_probs)

    #determine number of cases to solve
    numCases = int(input_file.readline().strip())
    #extract the cases
    cases = []
    for i in range(numCases):
        cases.append(input_file.readline().strip().replace(" given ", ""))
    print(cases)
