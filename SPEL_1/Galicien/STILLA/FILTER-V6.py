import re
import statistics


# Reads log and extracts all  sitcheck-lines
def find_lines_with_phrase(file_path, phrase):
    info = "XXXXXXXXXXXXXX"
    linelist = [] # list with all sitcheck lines
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if phrase in line:
                    # print(line.strip())
                    linelist.append(line.strip())
                if "C:\KEX" in line: # Used to label the output file
                    line = line.strip()
                    info = line.split("\\")
                    # print(info)
                        
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    
    return info, linelist

# Reads log and extracts all relevant lines with config information
def find_lines_with_config(file_path, config_phrases):
    matching_config_items = [] # Lines with config info for all sitchecks in the log
    try:
        with open(file_path, 'r') as file:
            for line in file:
                for phrase in config_phrases:
                    if phrase in line:
                        matching_config_items.append(line)
                        break  # Exit the inner loop if any phrase is found

            # Print the matching items in the order they appear in the input list
            '''
            for matching_item in matching_config_items:
                print(matching_item)
            '''
            
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
 
    Country_All = [string.split()[3] for string in matching_config_items]
    Country = list(set(Country_All)) # List of the power being checked in every sitcheck in the log.
    
    return Country

# Reads sitcheck-line-list and extracts the relevant lines (Power and actions)
def items_containing_sitcheck_phrases(my_list, phrases):
    matching_items = [] # list of powers and their actions
    for item in my_list:
        for phrase in phrases:
            if phrase in item:
                matching_items.append(item)
                break  # Exit the inner loop if any phrase is found

    # Print the matching items in the order they appear in the input list
    '''
    for matching_item in matching_items:
        print(matching_item)
    '''
         
    return matching_items


# Takes sitcheck-lines and cleans them to only output power, action and probability weight, and number of sitcheck iterations
def cleaner(sitcheck_lines):
    shortlist = [] # action and probability weight
    number_of_games = 0 # number of sitcheck iterations
    countries = [] # What powers the sitcheck checks (often only one)
    
    for line in sitcheck_lines:
        words = line.split()  # Split the line into words
        if len(words) == 6:
            if not words[5] in shortlist:
                shortlist.append(' '.join(words[5:]))  # Join words starting from the sixth word
                shortlist.append('-----'*10)
                countries.append(words[5])
                
            number_of_games = number_of_games + 1
        if len(words) > 6:
            shortlist.append(' '.join(words[5:]))     
        else:
            shortlist.append('-----')  
        
    return shortlist, number_of_games, countries

# Creates dictionary of actions and the sum of their probability weights
def action_dictionary(shortlist):
    action_dict = {} # Dictionary of actions and the sum of their probability weights
    
    
    for line in shortlist:
        parts = line.split()  # Split the line into parts
    
        if len(parts) >= 2: # if the line contains action and probability weight.
            string = ' '.join(parts[1:])  # Makes the actin a string
            number = float(parts[0])  # Convert the probability weight to a float 
            if string in action_dict:
                action_dict[string][0] += number  # If the action exists, add the corresponding probability weight
            else:
                action_dict[string] = [number]  # Otherwise, create a new list for the new action and add the corresponding probability weight
    
    return action_dict


#Calculates the normalised mean value of the probability weights for each action.
def normalised_mean_calculation(action_dict, number_of_games):
    probsumsum = 0
    
    for key, value in action_dict.items(): 
        
        if len(action_dict[key]) == 1: # Makes each probabilty sum a float
            probsumstring = float(action_dict[key][0])
        else:
            raise ValueError("ERROR 1!")
        
        probsumsum += probsumstring # adds the probsum of each action to a total of all probsums
        
        
    for key, value in action_dict.items(): # Devides all actions probsums with the total probsum (probsumsum) to create a normalised mean value
        if isinstance(key, str):  # Ensuring the key (action) is a string
            action_dict[key] = [num / probsumsum for num in value]
        else:
            raise ValueError("Error 2!")


    action_dict_normal_mean = list(action_dict.items()) # makes a list of the new action_dictionary
    return action_dict_normal_mean

#Calculates the  mean value of the probability weights for each action.
def mean_calculation(action_dict, number_of_games):
    
    
    for key, value in action_dict.items(): # Devides all actions probsums with the number of games to create a mean value
        if isinstance(key, str):  # Ensuring the key (action) is a string
            action_dict[key] = [num / number_of_games for num in value] # Devides all probsums 
        else:
            raise ValueError("Error 3!")


    action_dict_mean = list(action_dict.items()) # makes a list of the new action_dictionary
    return action_dict_mean


# Creates a dictionary with actions and the standard deviation for corresponding probability weights, also number of action occurences. 
def standard_deviation(cleaner_list, number_of_games):
    prob_list_dict = {}
    std_dev_dict = {}

    # Creates a dict with actions and corresponding prob-weights in a list
    for line in cleaner_list:
        parts = line.split()  # Split the line into parts
        
        if len(parts) >= 2: # if the line contains action and probability weight.
            string = ' '.join(parts[1:]) # Makes the action a string
            number = float(parts[0])  # Convert the probability weight to a float
            if string in prob_list_dict:
                prob_list_dict[string].append(number)  # If the action exists, append the probability weight to corresponding list 
            else:
                prob_list_dict[string] = [number]  # Otherwise, create a new list for the new action and add the corresponding probability weight

    print("All values dict:")
    for key, value in prob_list_dict.items():
        print(key + ":", value)
    
    
    # Calculate standard deviation for each list in the dictionary
    for key, value in prob_list_dict.items(): # For each action in dictionary:
        if len(value) < number_of_games: # If fewer prob-weights than number of games:
            missing_values = number_of_games - len(value)
            for i in range(missing_values):
                prob_list_dict[key].append(0)
                
        std_dev = statistics.stdev(value) # Calculate standard deviation of all prob-weights in list
        
        number_of_weights = len(value)
        std_dev_dict[key] = " Standard deviation: " + str(std_dev) + "     Number of occurences: " + str(number_of_weights) # Creates a new dictionary with action and corresponding stddev and number of weights (number of action)

    print("All values dict after adding 0:")
    for key, value in prob_list_dict.items():
        print(key + ":", value)
        
    print("Standard deviation dict:")
    for key, value in std_dev_dict.items():
        print(key + ":", value)
    
    standarddeviation = list(std_dev_dict.items()) # Turns the dict to a list

    return standarddeviation


# Creates a dictionary with actions and the standard deviation ! ONLY COUNTING OCCURING ACTIONS ! for corresponding probability weights, also number of action occurences. 
def standard_deviation_2(cleaner_list):
    prob_list_dict = {}
    std_dev_dict = {}

    # Creates a dict with actions and corresponding prob-weights in a list
    for line in cleaner_list:
        parts = line.split()  # Split the line into parts
        
        if len(parts) >= 2: # if the line contains action and probability weight.
            string = ' '.join(parts[1:]) # Makes the action a string
            number = float(parts[0])  # Convert the probability weight to a float
            if string in prob_list_dict:
                prob_list_dict[string].append(number)  # If the action exists, append the probability weight to corresponding list 
            else:
                prob_list_dict[string] = [number]  # Otherwise, create a new list for the new action and add the corresponding probability weight

    print("All values dict (standard_deviation_2):")
    for key, value in prob_list_dict.items():
        print(key + ":", value)
    
    
    # Calculate standard deviation for each list in the dictionary
    for key, value in prob_list_dict.items(): # For each action in dictionary:
        if len(value) > 1: # If more than one prob-weight
            std_dev = statistics.stdev(value) # Calculate standard deviation of all prob-weights in list
        else: # If only one prob-weight the standard deeviation is zero
            std_dev = 0 
            
        number_of_weights = len(value)
        std_dev_dict[key] = " Standard deviation (standard_deviation_2): " + str(std_dev) + "     Number of occurences: " + str(number_of_weights) # Creates a new dictionary with action and corresponding stddev and number of weights (number of action)

    print("Standard deviation (standard_deviation_2) dict:")
    for key, value in std_dev_dict.items():
        print(key + ":", value)
    
    standarddeviation = list(std_dev_dict.items()) # Turns the dict to a list

    return standarddeviation




# Uses extracted and compiled info to write the output file
def create_text_document(strings_1, strings_2, analysed, summary, summary_normal, number_games, filename, standarddeviation, standarddeviation_2):
    with open(filename, 'w') as file:
        file.write("="*60 + '\n'*2 + "CONFIG" + '\n'*2 + "="*60 + '\n')
        
        for string in strings_1:
            file.write(string + '\n') # Config info
            
        file.write("="*60 + '\n'*2 + "SITCHECK" + '\n'*2 + "="*60 + '\n')
        
        for string in strings_2:
            file.write(string + '\n') # Entire sitcheck line containg power and action

        file.write("="*60 + '\n'*2 + "ORDER   " + str(number_games) + " SPEL" + '\n'*2 + "="*60 + '\n') 
        
        for string in analysed:
            file.write(string + '\n') # Cleaned sitcheck lines (only power, actions and probability weights)

        file.write("="*60 + '\n'*2 + "BERÄKNING   " + str(number_games) + " SPEL  (Normaliserat medelvärde)" + '\n'*2 + "="*60 + '\n')
        
        for string in summary_normal:
            file.write(str(string) + '\n') # Writes the compiled orders and their normalised mean probability weights

        file.write("="*60 + '\n'*2 + "BERÄKNING   " + str(number_games) + " SPEL  (Vanligt Medelvärde)" + '\n'*2 + "="*60 + '\n')
        
        for string in summary:
            file.write(str(string) + '\n') # Writes the compiled orders and their mean probability weights        

        file.write("="*60 + '\n'*2 + "STANDARDAVVIKELSE PÅ ANTAL FÖREKOMSTER" + '\n'*2 + "="*60 + '\n')
         
        for string in standarddeviation_2: # Writes number of action occurences and standard deviation of prob-weights
            file.write(str(string) + '\n')

        file.write("="*60 + '\n'*2 + "STANDARDAVVIKELSE PÅ " + str(number_games) + " SPEL " + '\n'*2 + "="*60 + '\n')
         
        for string in standarddeviation: # Writes number of action occurences and standard deviation of prob-weights
            file.write(str(string) + '\n')




# Info used to read the log file 
file_path = 'log.txt'  # file path
phrase = 'situation_check'   
info, linelist = find_lines_with_phrase(file_path, phrase) # Reads log and extracts all relevant sitcheck-lines, returns info used to label output file


# Info used to extract config info for all sitcheck in the log
config_phrases = ["single_game:", "single_phase:", "single_power:"]
config_filename = "config.txt"
config_list = find_lines_with_config(file_path, config_phrases) # Reads log and extracts all relevant line with config information. Returns list of the power being checked in every sitcheck in the log.


# The following is used to extract  the power, their suggested actions, and number of sticheck-iterations
phrases = ["[situation_check:232]", "[situation_check:237]"] # releveant lines contain these phrases
sitcheck_lines = items_containing_sitcheck_phrases(linelist, phrases) # Reads all sitcheck lines and returns the relevant ones (power and actions)
cleaner_list, number_of_games, countries = cleaner(sitcheck_lines) # Takes sitcheck-lines and cleans them to only output power, action and probability weight, and number of sitcheck iterations
country_string = '-'.join(countries)

print("*"*60,"\n"*2,"ANALYS","\n"*2,"*"*60)
for line in cleaner_list:
    print(line)
print("*"*60)


# The following calculates normalised mean of prob-weights and...
action_dict = action_dictionary(cleaner_list) # Creates dictionary of actions and the sum of their probability weights

action_dict_mean = mean_calculation(action_dict, number_of_games) # Calculates the mean value of the probability weights for each action
action_dict_normal_mean = normalised_mean_calculation(action_dict, number_of_games) # Calculates the normalised mean value of the probability weights for each action

# Creates a dictionary with actions and the standard deviation for corresponding probability weights, also number of action occurences. 
standarddeviation = standard_deviation(cleaner_list, number_of_games) # Standard deviation over "number_of_games" amount of values (weights of 0 are added if number-of_games < 20)
standarddeviation_2 = standard_deviation_2(cleaner_list) # Standard deviation over "number of times the action occurrs" amount of values



# Info to write the output file
document_filename = "FV6-Sitcheck_" + country_string + "_" + info[4]+ "-" + info[5]+ "-" + info[6] + ".txt" # Name of the output file
create_text_document(config_list, sitcheck_lines, cleaner_list, action_dict_mean, action_dict_normal_mean, number_of_games, document_filename, standarddeviation, standarddeviation_2) # Uses extracted and compiled info to write the output file

print(f"Text document '{document_filename}' has been created successfully.")


