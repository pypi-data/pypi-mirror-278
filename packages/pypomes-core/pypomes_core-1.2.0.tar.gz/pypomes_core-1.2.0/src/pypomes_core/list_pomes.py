from typing import Any

def list_compare(list1: list[Any],
                 list2: list[Any]) -> bool:
    """
    Compare the contents of the two lists *list1* e *list2*.

    Return *True* if all the elements in *list1* are also in *list2*, and vice-versa, with the same cardinality.

    :param list1: the first list
    :param list2: the second list
    :return: True if the two lists contain the same elements, in the same quantity, in any order
    """
    # initialize the return variable
    result: bool = True

    # are the input parameters lists containing the same number of elements ?
    if (isinstance(list1, list) and
        isinstance(list2, list) and
        len(list1) == len(list2)):
        # yes, verify whether all elements in 'list1' are also in 'list2', in the same quantity
        for elem in list1:
            # is 'elem' in both lists, in the same quantity ?
            if list1.count(elem) != list2.count(elem):
                # no, the lists are not equal
                result = False
                break
    else:
        # no, the lists are not equal
        result = False

    return result


def list_flatten(source: list[str]) -> str:
    """
    Buiild and return a *str* by concatenating with "." the elements in *source*.

    Exemples:
        - ['1', '2', '']     -> '1.2.'
        - ['', 'a', 'b']     -> '.a.b'
        - ['x', '', '', 'y'] -> 'x...y'
        - ['z']              -> 'z'

    :param source: the source list
    :return: the concatenated elements of the source list
    """
    result: str = ""
    for item in source:
        result += "." + item
    return result[1:]


def list_unflatten(source: str) -> list[str]:
    """
    Build and return a *list*, by splitting *source* into its components separated by ".".

    This *list* will contain the extracted components. Exemples:
        - '1.2.'  -> ['1', '2', '']
        - '.a.b'  -> ['', 'a', 'b']
        - 'x...y' -> ['x', '', '', 'y']
        - 'z'     -> ['z']

    :param source: string with components concatenated by "."
    :return: the list of strings containing the concatenated components
    """
    # import the needed function
    from .str_pomes import str_split_on_mark

    return str_split_on_mark(source, ".")


def list_find_coupled(coupled_elements: list[tuple[str, str]],
                      primary_element: str) -> str:
    """
    Locate in *coupled_elements*, and return, the element coupled to *primary_element*.

    If *primary_element* contains an index indication (denoted by *[<pos>]*), this indication is removed.
    This function is used in the transformation of *dicts* (*dict_transform*) and *lists* (*list_transform*),
    from sequences of key pairs.

    :param coupled_elements: list of tupl4s containing the pairs of elements
    :param primary_element: the primary element
    :return: the couple element, or 'None' if it is not foundo
    """
    # initialize the return variable
    result: str | None = None

    # remove the list element indication
    pos1: int = primary_element.find("[")
    while pos1 > 0:
        pos2: int = primary_element.find("]", pos1)
        primary_element = primary_element[:pos1] + primary_element[pos2+1:]
        pos1 = primary_element.find("[")

    # traverse the list of coupled elements
    for primary, coupled in coupled_elements:
        # has the primary element been found ?
        if primary == primary_element:
            # yes, return the corresponding coupled element
            result = coupled
            break

    return result


def list_transform(source: list[Any],
                   from_to_keys: list[tuple[str, str]],
                   prefix_from: str = None,
                   prefix_to: str = None) -> list[Any]:
    """
    Construct a new *list*, transforming elements of type *list* and *dict* found in *source*.

    The conversion of *dict* type elements is documented in the *dict_transform* function.

    The prefixes for the source and destination keys, if defined, have different treatments.
    They are added when searching for values in *Source*, and removed when assigning values
    to the return *dict*.

    :param source: the source 'dict' of the values
    :param from_to_keys: the list of tuples containing the source and destination key sequences
    :param prefix_from: prefix to be added to the source keys
    :param prefix_to: prefix to be removed from the target keys
    :return: the new list
    """
    # import the needed function
    from .dict_pomes import dict_transform

    # initialize the return variable
    result: list[Any] = []

    # traverse the source list
    for inx, value in enumerate(source):
        if prefix_from is None:
            from_keys: None = None
        else:
            from_keys: str = f"{prefix_from}[{inx}]"

        # obtain the target value
        if isinstance(value, dict):
            to_value: dict = dict_transform(source=value,
                                            from_to_keys=from_to_keys,
                                            prefix_from=from_keys,
                                            prefix_to=prefix_to)
        elif isinstance(value, list):
            to_value: list = list_transform(source=value,
                                            from_to_keys=from_to_keys,
                                            prefix_from=from_keys,
                                            prefix_to=prefix_to)
        else:
            to_value: Any = value

        # added the value transformed to 'result'
        result.append(to_value)

    return result


def list_elem_starting_with(source: list[str | bytes],
                            prefix: str | bytes,
                            keep_prefix: bool = True) -> str | bytes:
    """
    Locate and return the first element in *source* prefixed by *prefix*.

    Retorna *None* se esse elemento não for encontrado.

    :param source: the list to be inspected
    :param prefix: the data prefixing the element to be returned
    :param keep_prefix: defines whether or not the found element should be returned with the prefix
    :return: the prefixed element, with or without the prefix, or 'None' if not found
    """
    # initialize the return variable
    result: str | bytes | None = None

    # traverse the source list
    for elem in source:
        if elem.startswith(prefix):
            if keep_prefix:
                result = elem
            else:
                result = elem[len(prefix)+1:]
            break

    return result


def list_prune_in(target: list[Any], ref: list[Any]) -> None:
    """
    Remove from *target* all its elements that are also in *ref*.

    :param target: the target list
    :param ref: the reference list
    :return: the target list without the elements also in the reference list
    """
    removals: list[Any] = [item for item in target if item in ref]
    for item in removals:
        target.remove(item)


def list_prune_not_in(target: list[Any], ref: list[Any]) -> None:
    """
    Remove from *target* all its elements that are not also in *ref*.

    :param target: the target list
    :param ref: the reference list
    :return: the target list without the elements not in the reference list
    """
    removals: list[Any] = [item for item in target if item not in ref]
    for item in removals:
        target.remove(item)
