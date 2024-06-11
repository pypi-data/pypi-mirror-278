import re

def toCamelCase(string):
    '''
    Returns a string in camelCase
    Example: to_camel_case("hello world") -> "helloWorld"
    '''
    #  split the string into words
    words = re.split(r"\W+", string)
    #  capitalize the first letter of each word except the first one
    return words[0] + "".join(word.capitalize() for word in words[1:] if word)


def to_pascal_case(string):
    '''
    Returns a string in PascalCase
    Example: to_pascal_case("hello world") -> "HelloWorld"
    '''
    if is_pascal_case(string):
        return string

    # split the string into words by non-word characters or underscore
    words = re.split(r"\W+|_", string)

    return "".join(word.capitalize() for word in words if word)


def to_space_case(string):
    '''
    Returns a string in Space Case
    Example: to_space_case("helloWorld") -> "hello world"
    '''
    return " ".join(re.findall(r"[A-Z][a-z]*", string))


def to_pascal_case_with_underscore(string):
    '''
    Returns a string in PascalCase with underscores
    Example: to_pascal_case_with_underscore("hello world") -> "Hello_World"
    '''
    
    string = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", string)
    string = re.sub("([a-z0-9])([A-Z])", r"\1_\2", string)
    string = re.sub(r"[\s]+", "_", string)

    parts = string.split("_")
    return "_".join(part.capitalize() for part in parts)


def is_pascal_case(s):
    return s == "".join(word.capitalize() for word in re.findall(r"[A-Za-z][^A-Z]*", s))


def is_snake_case(s):
    return s == "".join(word.lower() for word in re.findall(r"[A-Za-z][^A-Z]*", s))


def to_snake_case(string):
    '''
    Returns a string in snake_case
    Example: to_snake_case("helloWorld") -> "hello_world"
    '''

    string = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", string)
    string = re.sub("([a-z0-9])([A-Z])", r"\1_\2", string).lower()
    string = re.sub(r"[\s]+", "_", string)
    return string


def to_capitalized(text: str):
    return text.capitalize()
