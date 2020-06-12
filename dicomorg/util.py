#/usr/bin/env python
# -*- coding : utf-8 -*-

def group_key_att(indict, attribute, subset=None, sort=True):
    """Groups keys by the attribute, sorting the attribute

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

    return groups, unique_values
