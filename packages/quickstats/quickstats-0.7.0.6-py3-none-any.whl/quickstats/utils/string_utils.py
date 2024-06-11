from typing import Optional, Callable, List, Dict
import re
import ast
import uuid
import string

import numpy as np

def split_lines(s: str, comment_string: Optional[str] = "#", remove_blank: bool = True,
                with_line_number: bool = False, keepends: bool = False):
    """
    Split a multi-line string into individual lines and optionally remove comments and/or blank lines.

    Parameters:
        s (str): The input multi-line string to be split.
        comment_string (Optional[str], optional): The string representing the start of a comment line.
                                                  Lines starting with this string will be considered as comments 
                                                  and removed. Defaults to "#".
        remove_blank (bool, optional): If True, remove blank lines (lines containing only whitespace).
                                       Defaults to True.
        with_line_number (bool, optional): If True, returns a list of tuples with line numbers and lines.
                                           If False, returns a list of lines. Defaults to False.
        keepends (bool, optional): If True, the line breaks are included in each line. If False, line breaks 
                                   are removed. Defaults to False.

    Returns:
        list or list of tuples: A list of lines from the input string. If 'with_line_number' is True, 
                                it returns a list of tuples with line numbers and lines.
    """
    lines = s.splitlines(keepends=keepends)

    if comment_string:
        lines = [line.split(comment_string, 1)[0] for line in lines]

    if remove_blank and with_line_number:
        lines = [(line, i + 1) for i, line in enumerate(lines) if line.strip()]
    elif remove_blank:
        lines = [line for line in lines if line.strip()]
    elif with_line_number:
        lines = [(line, i + 1) for i, line in enumerate(lines)]
        
    return lines


def split_str(s: str, sep: str = None, strip: bool = True, remove_empty: bool = False, cast: Optional[Callable] = None,
              use_paranthesis:bool = False, empty_value:Optional[str]='') -> List:
    """
    Splits a string and applies optional transformations.

    This function splits a string into a list where each element is a substring of the 
    original string. By default, it trims leading and trailing whitespace from each substring. 
    It can also optionally remove empty substrings and apply a casting function to each substring.

    Parameters
    ----------
    s : str
        The string to split.
    sep : str, optional
        The separator according to which the string is split. If not specified or None, 
        the string is split at any whitespace. Defaults to None.
    strip : bool, optional
        Whether to trim leading and trailing whitespace from each substring. Defaults to True.
    remove_empty : bool, default = False
        Whether to remove empty substrings from the list. Defaults to False.
    cast : Callable, optional
        An optional casting function to apply to each substring. It should be a function 
        that takes a single string argument and returns a value. Defaults to None.
    use_paranthesis: bool, default = False
        Whether to ignore separator within paranthesis.
    empty_value: str, optional, default = ''
        Replace empty token with this value.

    Returns
    -------
    list
        A list of substrings (or transformed substrings) obtained by splitting the input string.
    """
    if use_paranthesis:
        if sep is None:
            raise ValueError('separator can not be None when "use_paranthesis" option is set to True')
        items = re.split(sep + r'\s*(?![^()]*\))', s)
    else:
        items = s.split(sep)
    if strip:
        items = [item.strip() for item in items]
    if remove_empty:
        items = [item for item in items if item]
    if cast is None:
        cast = lambda x: x
    items = [cast(item) if item else empty_value for item in items]

    return items
    
whitespace_trans = str.maketrans('', '', " \t\r\n\v")
newline_trans = str.maketrans('', '', "\r\n")

def remove_whitespace(s: str) -> str:
    """
    Removes all whitespace characters from a string.

    The function effectively removes characters like space, tab, carriage return, 
    newline, and vertical tab from the provided string.

    Parameters
    ----------
    s : str
        The input string from which to remove whitespace.

    Returns
    -------
    str
        The string with all whitespace characters removed.
    """
    return s.translate(whitespace_trans)

def remove_newline(s: str):
    """
    Removes newline characters from a string.

    Parameters:
        s (str): The input string from which to remove newline characters.

    Returns:
        str: The input string with all newline characters removed.
    """
    return s.translate(newline_trans)

neg_zero_regex = re.compile(r'(?![\w\d])-(0.[0]+)(?![\w\d])')

def remove_neg_zero(s:str):
    """
    Replaces instances of negative zero in a string with zero.
    
    Parameters:
        string (str): The input string in which to replace negative zeros.

    Returns:
        str: The input string with all instances of negative zero replaced with zero.

    Example:
        string = "The temperature is -0.000 degrees."
        print(remove_neg_zero(string))
        # outputs: "The temperature is 0.000 degrees."
    """
    return neg_zero_regex.sub(r'\1', s)


def parse_as_dict(s:str, item_sep:str=',', key_value_sep:str='='):
    """
    Parse a string into a dictionary based on given item and key-value separators.

    Parameters
    ----------
    s : str
        The input string to be parsed into a dictionary.
    item_sep : (optional) str, default = ','
        The separator between items
    key_value_sep : (optional) str, default = '='
        The separator between keys and values

    Returns
    -------
    dict
        A dictionary containing the parsed key-value pairs.

    Examples
    --------
    >>> parse_as_dict("name='John',age=25")
    {'name': 'John', 'age': 25}
    """
    tokens = split_str(s, sep=item_sep, strip=True, remove_empty=True)
    result = {}
    for token in tokens:
        subtokens = split_str(token, sep=key_value_sep, strip=True)
        if len(subtokens) != 2:
            raise ValueError(f'invalid key-value format: {token}')
        key, value = subtokens
        if key in result:
            raise RuntimeError(f'multiple values specified for the key "{key}"')
        result[key] = ast.literal_eval(value)
    return result
    
    
def make_multiline_text(text:str, max_line_length:int, break_word:bool=True):
    if break_word:
        n = max_line_length
        return '\n'.join(text[i:i+n] for i in range(0, len(text), n))
    #accumulated line length
    acc_length = 0
    words = text.split(" ")
    formatted_text = ""
    for word in words:
        #if ACC_length + len(word) and a space is <= max_line_length 
        if acc_length + (len(word) + 1) <= max_line_length:
            #append the word and a space
            formatted_text = formatted_text + word + " "
            #length = length + length of word + length of space
            acc_length = acc_length + len(word) + 1
        else:
            #append a line break, then the word and a space
            formatted_text = formatted_text + "\n" + word + " "
            #reset counter of length to the length of a word and a space
            acc_length = len(word) + 1
    return formatted_text.lstrip("\n")

def get_field_names(format_str:str):
    """
    Extracting field names from format string
    """
    formatter = string.Formatter()
    field_names = [field_name for _, field_name, _, _ in formatter.parse(format_str) if field_name]
    return field_names

def parse_format_str_with_regex(str_list, format_str, regex_map, mode:str="search"):
    """
    Extract format string field attributes from regex patterns
    """
    if isinstance(str_list, str):
        return parse_format_str_with_regex([str_list], format_str, regex_map)
    if mode not in ["search", "match", "fullmatch"]:
        raise ValueError('mode must be one of "search", "match" or "fullmatch"')
    field_names = get_field_names(format_str)
    unique_fields, counts = np.unique(field_names, return_counts=True)
    field_groupkeys = {}
    duplicate_groupkey_maps = {}
    format_pattern = str(format_str)
    for i, field in enumerate(unique_fields):
        if field not in regex_map:
            raise ValueError(f'missing regex pattern for the field: "{field}"')
        pattern = regex_map[field]
        groupkeys = list(re.compile(pattern).groupindex.keys())
        field_groupkeys[field] = groupkeys
        count = counts[i]
        for j in range(count):
            pattern_ = pattern
            if j > 0:
                suffix = uuid.uuid4().hex
                for groupkey in groupkeys:
                    if groupkey not in duplicate_groupkey_maps:
                        duplicate_groupkey_maps[groupkey] = []
                    new_groupkey = f"{groupkey}_{suffix}"
                    duplicate_groupkey_maps[groupkey].append(new_groupkey)
                    pattern_ = pattern_.replace(f"(?P<{groupkey}>", f"(?P<{new_groupkey}>")
            format_pattern = format_pattern.replace(f"{{{field}}}", pattern_, 1)
    regex = re.compile(format_pattern)
    method = getattr(regex, mode)
    results = []
    for str_ in str_list:
        match = method(str_)
        if not match:
            continue
        groupdict = match.groupdict()
        valid_match = True
        for key, altkeys in duplicate_groupkey_maps.items():
            if not all(groupdict[key] == groupdict[altkey] for altkey in altkeys):
                valid_match = False
                break
            for altkey in altkeys:
                groupdict.pop(altkey)
        if not valid_match:
            continue
        result = (str_, groupdict)
        results.append(result)
    return results


def insert_breaks_preserving_words(text: str, max_width: int, indent: str) -> str:
    """
    Inserts line breaks into a string to ensure it fits within a specified width without breaking words.
    Subsequent lines are indented with the given indent string.

    Args:
        text: The original string to process.
        max_width: The maximum width of each line, in characters.
        indent: The string used to indent lines after the first line.

    Returns:
        The modified string with line breaks and indentation inserted.
    """
    words = text.split()
    if not words:
        return ""

    current_line = words[0]
    formatted_lines = []

    for word in words[1:]:
        # Check if adding the next word would exceed the max width
        if len(current_line) + len(word) + 1 <= max_width:
            current_line += " " + word
        else:
            formatted_lines.append(current_line)
            current_line = indent + word
            max_width = len(indent) + max_width  # Adjust max_width for indentation
    formatted_lines.append(current_line)  # Add the last line

    return "\n".join(formatted_lines)

def format_dict_to_string(dictionary: Dict[str, str], separator: str = " : ",
                          left_margin: int = 0, line_break: int = 100) -> str:
    """
    Formats a dictionary into a neatly aligned string representation, with each key-value pair on a new line. 

    Args:
        dictionary: The dictionary to format. Keys should be strings, and values are expected to be strings that 
                    can contain multiple words.
        separator: The string used to separate keys from their values. Defaults to ": ".
        left_margin: The number of spaces to prepend to each line for indentation. Defaults to 0.
        line_break: The maximum allowed width of each line, in characters, before wrapping the text to a new line. 
                    Defaults to 100.

    Returns:
        A string representation of the dictionary. Each key-value pair is on its own line, with lines broken such 
        that words are not split across lines, respecting the specified `line_break` width.

    Example:
        >>> example_dict = {"Key1": "This is a short value.", "Key2": "This is a much longer value that will be wrapped according to the specified line break width."}
        >>> print(format_dict_to_string(example_dict, left_margin=4, line_break=80))
         Key1: This is a short value.
         Key2: This is a much longer value that will be wrapped according to the
               specified line break width.

    Note:
        The function removes existing newlines in values to prevent unexpected line breaks and treats the entire 
        value as a single paragraph that needs to be wrapped according to `line_break`.
    """
    if not dictionary:
        return ""

    max_key_length = max(len(key) for key in dictionary)
    indent_size = left_margin + max_key_length + len(separator)
    effective_text_width = line_break - indent_size

    if effective_text_width <= 0:
        raise ValueError("Line break width must be greater than the size of indentation and separator.")

    formatted_lines = []
    indent_string = " " * indent_size
    for key, value in dictionary.items():
        cleaned_value = value.replace("\n", " ")
        wrapped_value = insert_breaks_preserving_words(cleaned_value, effective_text_width, indent_string)
        line = f"{' ' * left_margin}{key:{max_key_length}}{separator}{wrapped_value}"
        formatted_lines.append(line)

    return "\n".join(formatted_lines) + "\n"


def str_to_bool(s:str) -> bool:
    """
    Convert a string into a boolean value.
    
    Parameters:
    s (str): The string to convert.

    Returns:
    bool: The boolean value of the string.

    Raises:
    ValueError: If the string does not represent a boolean value.
    """
    s = s.strip().lower()

    true_values = {'true', '1'}
    false_values = {'false', '0'}

    if s in true_values:
        return True
    elif s in false_values:
        return False
    else:
        raise ValueError(f"Invalid literal for boolean: '{s}'")

def remove_cpp_type_casts(expression: str) -> str:
    """
    Removes type casts from a C++ expression based on general structure.

    Parameters:
    expression (str): A string containing a C++ expression.

    Returns:
    str: The expression with type casts removed.
    """
    # Matches a parenthetical that seems like a type (any word potentially followed by pointer/reference symbols),
    # ensuring it's not preceded by an identifier character and is followed by a valid variable name.
    type_cast_pattern = r'(?<![\w_])\(\s*[a-zA-Z_]\w*\s*[\*&]*\s*\)\s*(?=[a-zA-Z_]\w*|[+-]?\s*\d|\.)'
    return re.sub(type_cast_pattern, '', expression)

def extract_variable_names(expression:str)->List[str]:
    """
    Extracts variable names from a C++ expression.

    Parameters:
    expression (str): A string containing a C++ expression.

    Returns:
    list: A list of unique variable names found in the expression.
    """

    expression = remove_cpp_type_casts(expression)

    # Match potential variable names which are not directly followed by a '(' which would indicate a 
    # function call. Use negative lookaheads and positive lookbehinds to refine the match.
    pattern = r'\b[a-zA-Z_]\w*(?:\.\w+)*\b(?!\s*\()'

    matches = re.findall(pattern, expression)

    from quickstats.utils.common_utils import remove_duplicates
    unique_matches = remove_duplicates(matches)
    
    return unique_matches