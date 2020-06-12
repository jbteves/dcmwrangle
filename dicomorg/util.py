#/usr/bin/env python
# -*- coding : utf-8 -*-

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
