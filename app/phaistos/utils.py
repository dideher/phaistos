below_twenty_numwords = ["", # empty in place of μηδέν
                            "μίας", 
                            "δύο", 
                            "τριών", 
                            "τεσσάρων", 
                            "πέντε", 
                            "έξι", 
                            "επτά", 
                            "οκτώ", 
                            "εννέα", 
                            "δέκα",  
                            "ένδεκα", 
                            "δώδεκα",  
                            "δεκατριών", 
                            "δεκατεσσάρων", 
                            "δεκαπέντε", 
                            "δεκαέξι",  
                            "δεκαεπτά", 
                            "δεκαοκτώ", 
                            "δεκαεννέα"]

tens_above_twenty_numwords = [  "είκοσι",
                                "τριάντα",
                                "σαράντα",
                                "πενήντα",
                                "εξήντα", 
                                "εβδομήντα",
                                "ογδόντα", 
                                "ενενήντα"]

hundreds_numwords = [ "εκατό",
                        "διακόσιες",
                        "τριακόσιες",
                        "τετρακόσιες",  
                        "πεντακόσιες",  
                        "εξακόσιες",  
                        "επτακόσιες",  
                        "οκτακόσιες",  
                        "εννιακόσιες"]

thousands_numwords = [(1000, "χίλιες")]


def number_to_word_below_20(number):
    number_in_words = ''
    if number < 20:
        number_in_words = below_twenty_numwords[number]
    return number_in_words

def number_to_word_between_20_and_99(number):
    number_in_words = ''
    if number >= 20 and number < 100:
        list_of_digits = [int(i) for i in str(number)]
        list_of_digits.reverse()
        if list_of_digits[0] == 0: 
            number_in_words = tens_above_twenty_numwords[list_of_digits[1]-2]
        else:
            number_in_words = f'{tens_above_twenty_numwords[list_of_digits[1]-2]} {below_twenty_numwords[list_of_digits[0]]}'
    return number_in_words
    
def number_to_word_between_100_and_999(number):
    number_in_words = ''
    low_part = number % 100
    if low_part < 20:
        low_number_in_words = number_to_word_below_20(low_part)
    else:
        low_number_in_words = number_to_word_between_20_and_99(low_part)

    list_of_digits = [int(i) for i in str(number)]
    hundreds_in_words = hundreds_numwords[list_of_digits[0]-1]
    number_in_words = f'{hundreds_in_words} {low_number_in_words}'

    return number_in_words


def number_to_word_larger_than_1000(number):
    number_in_words = ''
    low_part = number % 1000
    if low_part < 20:
        low_number_in_words = number_to_word_below_20(low_part)
    if low_part >= 200 and low_part < 100:
        low_number_in_words = number_to_word_between_20_and_99(low_part)
    if low_part >= 100 and low_part < 1000:
        low_number_in_words = number_to_word_between_100_and_999(low_part)
    
    list_of_digits = [int(i) for i in str(number)]
    thousands_in_words = ''
    if len(list_of_digits) == 4 and list_of_digits[0] == 1:
        thousands_in_words = "χίλιες"
        number_in_words = f'{thousands_in_words} {low_number_in_words}'
    else:
        high_part = int((number - low_part)/1000)
        high_part_in_words = f'{convert_duration_to_words(high_part)} χιλιάδες'
        number_in_words = f'{high_part_in_words} {low_number_in_words}'

    return number_in_words 

def convert_duration_to_words(number):

    number_in_words = ''
    if number >= 1000000:
        return ('Unsupported duration')
    
    if number < 20:
        number_in_words = number_to_word_below_20(number)

    if number >= 20 and number < 100:
        number_in_words = number_to_word_between_20_and_99(number)

    if number >= 100 and number < 1000:
        number_in_words = number_to_word_between_100_and_999(number)
    
    if number >= 1000:
        number_in_words = number_to_word_larger_than_1000(number)

    return number_in_words


def first_name_to_geniki(first_name):
    geniki = first_name
    name_ends_with = first_name[-4:]
    if name_ends_with == 'ΛΕΩΝ':
        geniki = first_name[:] + 'ΤΑ'
    else:
        name_ends_with = first_name[-2:]
        if name_ends_with == 'ΟΣ':
            geniki = first_name[:-1] + 'Y'
        elif name_ends_with == 'ΑΣ':
            geniki = first_name[:-1]
        elif name_ends_with == 'ΗΣ':
            geniki = first_name[:-1]
        elif name_ends_with == 'ΗΣ':
            geniki = first_name[:-1]
        elif name_ends_with == 'ΩΝ':
            geniki = first_name[:] + 'Α'
        else:
            name_ends_with = first_name[-1]
            if name_ends_with == 'Η':
                geniki = first_name + "Σ"
            elif name_ends_with == 'Α':
                geniki = first_name + "Σ"
            else:
                pass
    return geniki

def first_name_to_accusative(first_name):
    accusative = first_name
    name_ends_with = first_name[-4:]
    if name_ends_with == 'ΛΕΩΝ':
        accusative = first_name[:] + 'ΤΑ'
    else:
        name_ends_with = first_name[-1:]
        if name_ends_with == 'Σ':
            accusative = first_name[:-1]
    return accusative



def last_name_to_geniki(last_name):
    geniki = last_name
    name_ends_with = last_name[-2:]
    if name_ends_with == 'ΟΣ':
        geniki = last_name[:-1] + 'Y'

    elif name_ends_with == 'ΗΣ':
        geniki = last_name[:-1]
    elif name_ends_with == 'ΑΣ':
        geniki = last_name[:-1]
    elif name_ends_with == 'ΕΣ':
        geniki = last_name[:-1]
    elif name_ends_with == 'ΙΣ':
        geniki = last_name[:-1]
    elif name_ends_with == 'ΗΣ':
        geniki = last_name[:-1]
    else:
        pass
    return geniki


def last_name_to_accusative(last_name):
    geniki = last_name
    name_ends_with = last_name[-2:]
    if name_ends_with == 'ΟΣ':
        geniki = last_name[:-1]
    elif name_ends_with == 'ΗΣ':
        geniki = last_name[:-1]
    elif name_ends_with == 'ΑΣ':
        geniki = last_name[:-1]
    elif name_ends_with == 'ΕΣ':
        geniki = last_name[:-1]
    elif name_ends_with == 'ΙΣ':
        geniki = last_name[:-1]
    else:
        pass
    return geniki


# for i in range(0, 900):
#     print (f'{i} -> {convert_duration_to_words(i)}')