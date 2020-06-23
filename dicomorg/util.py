#/usr/bin/env python
# -*- coding : utf-8 -*-

import sys
from enum import Enum

class Operators(Enum):
    QUIT = 0

operator_enums = {
        'q' : Operators.QUIT,
        'quit' : Operators.QUIT 
}

op_takes_group = {
        Operators.QUIT : False
}

op_takes_arg = {
        Operators.QUIT : False
}

def get_argument(wordlist):
    """Gets the argument from a wordlist

    Parameters
    ----------
    wordlist : list
        A list of the words to parse an argument from.

    Returns
    -------
    A string with the argument.

    Raises
    ------
    TypeError
        If wordlist is not a list
    ValueError
        If a valid argument cannot be parsed
    """

    if not isinstance(wordlist, list):
        raise TypeError('wordlist must be of type list')

    if len(wordlist) == 0:
        return None
    if len(wordlist) == 1:
        return wordlist[0]
    if len(wordlist) > 1:
        raise ValueError('Cannot form an argument from multiple words')


def get_srange(word):
    """Gets an srange from a word

    Parameters
    ----------
    word : str
        The word to get an srange from.

    Returns
    -------
    A list of numbers that this word expands to.

    Raises
    ------
    TypeError
        If the word is not a string or if a non-integer number is detected.
    ValueError
        If the word contains non-numerics or has insufficient range 
        arguments.
    """

    if not isinstance(word, str):
        raise TypeError('Words must be strings')

    numbers = word.split(':')
    ncolons = word.count(':')
    integers = [0 for i in numbers]
    for i in range(len(numbers)):
        test = float(numbers[i])
        integers[i] = int(numbers[i])
        if test != integers[i]:
            raise(ValueError, 'Can only range integers')

    nints = len(integers)
    if nints == 0:
        if ncolons == 0:
            return None
        else:
            raise(ValueError, 'Cannot use solitary colon')
    elif nints == 1:
        if ncolons == 0:
            return integers
        else:
            raise(ValueError, 'Hanging colon')
    elif nints == 2:
        if ncolons == 1:
            start = min(integers)
            stop = max(integers)
            if start <= 0:
                raise ValueError('Cannot range negative numbers')
            retlist = [n for n in range(start, stop + 1)]
            retlist.sort()
            return retlist
        else:
            raise ValueError('Hanging colon')
    elif nints == 3:
        if ncolons == 2:
            start = integers[0]
            step = integers[1]
            stop = integers[2]
            if step == 0:
                raise ValueError('Cannot have step size 0')
            if (start <= 0) or (stop <= 0):
                raise ValueError('Indices must be postive integers')
            if step < 0:
                stop = stop - 1
            else:
                stop = stop + 1
            retlist = [n for n in range(start, stop, step)]
            retlist.sort()
            return retlist
    else:
        raise ValueError('Too many numbers for one word')


def get_group(wordlist):
    """Gets a list of numbers from a group wordlist and modifies wordlist.

    Parameters
    ----------
    wordlist : list
        A list of words to parse.

    Returns
    -------
    group : list
        A list of numbers in the group.
    wordlist : list
        The revised wordlist

    Raises
    ------
    TypeError
        If the wordlist is not a list.
    ValueError
        If the wordlist does not make a valid group.

    Notes
    -----
    Modifies the original wordlist to simplify downstream processing.
    """

    if not isinstance(wordlist, list):
        raise ValueError('wordlist must be of type list')
    if not wordlist:
        return None, wordlist

    inwords = ' '.join(wordlist)
    lbracket = -1
    rbracket = -1
    for i in range(len(inwords)):
        if inwords[i] == '[':
            if (lbracket == -1):
                lbracket = i
            else:
                raise ValueError('Can only have one grouping')
        elif inwords[i] == ']':
            if (rbracket == -1):
                rbracket = i
            else:
                raise ValueError('Can only have one grouping')


    if (rbracket < lbracket) or (lbracket >= 0 and rbracket < 0):
        raise ValueError('Unmatched bracket')

    if (lbracket == -1) and (rbracket == -1):
        # Determine if group or command
        c = inwords[0]
        if c.isnumeric():
            # Group should only be the first word in this case
            group = get_srange(wordlist[0])
            wordlist = wordlist[1:]
            return group, wordlist
        else:
            return None, wordlist

    if lbracket != 0:
        raise ValueError('Brackets should begin groups')
    inwords = inwords[1:rbracket]
    srange_words = inwords.split(' ')
    group = []
    for w in srange_words:
        sr = get_srange(w)
        for x in sr:
            group.append(x)

    group = list(set(group))
    # Find the location of the rbracket
    rword = 0
    for i in range(len(wordlist)):
        if ']' in wordlist[i]:
            rword = i

    wordlist = wordlist[rword+1:]
    return group, wordlist


def get_statement(user_input, pad=None):
    """Get statements from an interactive session.

    Parameters
    ----------
    user_input : str
        The current user input. For CLI, iterate over stdin.
    pad : str
        Something to pad the statement with for implied commands.

    Returns
    -------
    operator : str
        The operator to use.
    group : list
        A list of the numbers of interest.
    argument : str
        The argument to the operator.

    Raises
    ------
    ValueError
        If the statement is invalid.
    TypeError
        If the pad or input are not a string.
    """

    if not isinstance(user_input, str):
        raise TypeError('No string was supplied')
    if pad:
        if not isinstance(pad, str):
            raise TypeError('Can only pad with strings')

    user_input = user_input.rstrip()
    input_words = user_input.split()
    if len(input_words) == 0:
        raise ValueError('No statement was given')
    operator_word = input_words[0]

    if operator_word in operator_enums:
        op = operator_enums[operator_word]
    else:
        raise ValueError('No valid operator supplied')
    input_arguments = input_words[1:]

    # Check to make sure that each non-operator word is valid
    group, input_arguments = get_group(input_arguments)
    argument = get_argument(input_arguments)

    if not op_takes_group[op] and group:
        raise ValueError('group not valid for %s' % operator_word)
    if not op_takes_arg[op] and argument:
        raise ValueError('argument not valid for %s' % operator_word)

    return op, group, argument

def group_key_att(indict, attribute, subset=None, sort=True):
    """Group keys by the attribute, sorting the attribute

    Parameters
    ----------
    indict : dict
        The dictionary to search through.
    attribute : str
        The string for the attribute you'd like to group by.
    subset : list
        A list of keys you'd like to search through. Default: None.

    Returns
    -------
    values : list
        A sorted list of the unique values found in the attribute.
    groups : list
        A list of lists, with each sublist the list of keys which match the 
        same index in the returned list of values.

    Raises
    ------
    AttributeError
        If the attribute requested does not exist for one of the items in 
        the dict.
    KeyError
        If one of the keys in the subset is not present in the dict.
    TypeError
        If parameter types are incorrect
    """

    # Type checking
    if not isinstance(indict, dict):
        raise TypeError('indict is not a dict')
    if not isinstance(attribute, str):
        raise TypeError('attribute is not a string')
    if not isinstance(sort, bool):
        raise TypeError('sort is not a boolean')
    if subset:
        if not isinstance(subset, list):
            raise TypeError('subset is not a list')
        # Check list is not empty
        if len(subset) == 0:
            subset = [k for k in indict]
        else:
            # Check for key existence
            extant_keys = [k for k in indict]
            for k in subset:
                if not (k in extant_keys):
                    raise KeyError('Key in subset not present in indict')
    else:
        subset = [k for k in indict]

    # Harvest values and determine unique ones
    test_dict = {}
    for k in subset:
        attribute_value = getattr(indict[k], attribute)
        if not attribute_value in test_dict:
            test_dict[attribute_value] = []
        test_dict[attribute_value].append(k)
    unique_values = [k for k in test_dict]

    groups = [[] for i in unique_values]
    for i in range(len(unique_values)):
        groups[i] = test_dict[unique_values[i]]

    if sort:
        groups = [x for _,x in sorted(zip(unique_values, groups))]
        unique_values.sort()

    return groups, unique_values


def group_key_val(indict, attribute, target_value, subset=None):
    """Return a group of keys which match the desired attribute and value.

    Parameters
    ----------
    indict : dict
        The input dictionary to search through.
    attribute : str
        The attribute to examine for each key.
    target_value : any
        The value you'd like to know which keys match.
    subset : list
        The subset of keys you'd like to explore. Default: None.

    Returns
    -------
    A list of keys which have the desired match.

    Raises
    ------
    AttributeError
        If one of the items keyed does not have the desired attribute.
    KeyError
        If one of the keys in the subset is not present in the dict.
    TypeError
        If the type of a parameter types are incorrect
    """
    # Type checking
    if not isinstance(indict, dict):
        raise TypeError('indict is not a dict')
    if not isinstance(attribute, str):
        raise TypeError('attribute is not a string')
    if subset:
        if not isinstance(subset, list):
            raise TypeError('subset is not a list')
        # Check list is not empty
        if len(subset) == 0:
            subset = [k for k in indict]
        else:
            # Check for key existence
            extant_keys = [k for k in indict]
            for k in subset:
                if not (k in extant_keys):
                    raise KeyError('Key in subset not present in indict')
    else:
        subset = [k for k in indict]

    matching_keys = ['' for i in subset]
    total_matches = 0
    for k in subset:
        current_val = getattr(indict[k], attribute)
        if current_val == target_value:
            matching_keys[total_matches] = k
            total_matches += 1

    return matching_keys[0:total_matches]
