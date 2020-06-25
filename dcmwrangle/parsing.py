#!/usr/bin/env python
# -*- coding : utf-8 -*-

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

    wordlist = wordlist[rword + 1:] 
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
    operator = input_words[0]
    input_arguments = input_words[1:]

    # Check to make sure that each non-operator word is valid
    group, input_arguments = get_group(input_arguments)
    argument = get_argument(input_arguments)

    return operator, group, argument
