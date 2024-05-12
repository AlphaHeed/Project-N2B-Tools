import re

# FUNKTION 1: Lista med alla sitchecklines
def find_lines_with_phrase(file_path, phrase):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if phrase in line:
                    # print(line.strip())
                    linelist.append(line.strip())
        
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")

# FUNKTION 2: Lista med config-lines
def find_lines_with_config(file_path, config_phrases):
    matching_config_items = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                for phrase in config_phrases:
                    if phrase in line:
                        matching_config_items.append(line)
                        break  # Exit the inner loop if any phrase is found

            # Print the matching items in the order they appear in the input list
            for matching_item in matching_config_items:
                print(matching_item)
            
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
 
    Country_All = [string.split()[3] for string in matching_config_items]
    Country = list(set(Country_All))
    return Country

# FUNKTION 3: Lista med bara land och ordrar
def print_items_containing_phrases(my_list, phrases):
    matching_items = []
    for item in my_list:
        for phrase in phrases:
            if phrase in item:
                matching_items.append(item)
                break  # Exit the inner loop if any phrase is found

    # Print the matching items in the order they appear in the input list
    for matching_item in matching_items:
        print(matching_item)
    return matching_items

'''
def analyse(datalist):
    pattern = r'\((.*?)\)'
    shortlist = []
    for line in datalist:
        shortlist.append(line.split()[5])
        if "(" in line:
            orderlist = re.findall(pattern, line)
            orderstring = ' '.join(orderlist)
            shortlist.append("("+orderstring+")")

            
    return shortlist
'''
'''
def analyse(datalist):
    shortlist = []
    for line in datalist:
        words = line.split()  # Split the line into words
        if len(words) >= 6:
            shortlist.append(' '.join(words[5:]))  # Join words starting from the fourth word
        else:
            shortlist.append('')  # If there are fewer than 4 words, append an empty string

    for line in shortlist:
        
    return shortlist
'''
def cleaner(datalist):
    shortlist = []
    number_of_games = 0
    countries = []
    
    for line in datalist:
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

    print(number_of_games)
        
    return shortlist, number_of_games, countries

def summarize(shortlist, number_games):
    number_dict = {}
    for line in shortlist:
        parts = line.split()  # Split the line into parts
        if len(parts) >= 2:
            string = ' '.join(parts[1:])  # Join all parts except the first one as the string
            number = float(parts[0])  # Convert the first part to an integer as the number
            if string in number_dict:
                number_dict[string][0] += number  # If the string exists, append the number
            else:
                number_dict[string] = [number]  # Otherwise, create a new list for the string

    # Divide each number in the dictionary by the divisor
    for key, value in number_dict.items():
        if isinstance(key, str):  # Ensuring the key is a number
            number_dict[key] = [num / number_games for num in value]
        else:
            print("ä"*100)

    print(number_dict)
    summary = list(number_dict.items())
           
    return summary



# FUNKTION 4: Skriv txt.dokument
def create_text_document(strings_1, strings_2, analysed, summary, number_games, filename):
    with open(filename, 'w') as file:
        file.write("="*60 + '\n'*2 + "CONFIG" + '\n'*2 + "="*60 + '\n')
        
        for string in strings_1:
            file.write(string + '\n')
            
        file.write("="*60 + '\n'*2 + "SITCHECK" + '\n'*2 + "="*60 + '\n')
        
        for string in strings_2:
            file.write(string + '\n')

        file.write("="*60 + '\n'*2 + "ORDER   " + str(number_games) + " SPEL" + '\n'*2 + "="*60 + '\n')
        
        for string in analysed:
            file.write(string + '\n')

        file.write("="*60 + '\n'*2 + "BERÄKNING   " + str(number_games) + " SPEL" + '\n'*2 + "="*60 + '\n')
        
        for string in summary:
            file.write(str(string) + '\n')


#_____ 1 Sitcheck __________  
linelist = []

file_path = 'log.txt'  # file path
phrase = 'situation_check'  #  desired 'specific phrase' 
find_lines_with_phrase(file_path, phrase)

#print("*"*60,"\n"*3,"*"*60)

#____  2 Config __________
config_phrases = ["single_game:", "single_phase:", "single_power:"]
config_filename = "config.txt"
config_list = find_lines_with_config(file_path, config_phrases)
# create_text_document(config_list, config_filename)


#____  3 Sitcheck Clean __________
phrases = ["[situation_check:232]", "[situation_check:237]"]
clean_list = print_items_containing_phrases(linelist, phrases)

cleaner_list, number_of_games, countries = cleaner(clean_list)
print("*"*60,"\n"*2,"ANALYS","\n"*2,"*"*60)
for line in cleaner_list:
    print(line)

summary = summarize(cleaner_list, number_of_games)

print("*"*150,"\n"*2,"*"*60)

country_string = '-'.join(countries)



#____  4 Write __________
# Name of the text document to create
document_filename = "Sitcheck_" + country_string +".txt"
# Call the function to create the text document
create_text_document(config_list, clean_list, cleaner_list, summary, number_of_games, document_filename)
print("*"*60,"\n"*2,"*"*60)
print(f"Text document '{document_filename}' has been created successfully.")


