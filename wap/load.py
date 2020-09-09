from .structs import Technology, Imply, Exclude, Pattern, Category
from typing import Dict, Any, TextIO, Tuple, Union, List
import json
import re


def load_file(
        filepath: str
) -> Tuple[Dict[str, Technology], Dict[str, Category]]:
    """Loads the contents of an technologies.json_ file indicated by the path.

    Args:
        filepath (str): Path of the technologies.json_ file.

    Returns:
        Tuple[Dict[str, Technology], Dict[str, Category]]: A tuple with the
            technologies and the categories defined in technologies.json_.

    Example:
        >>> import wap
        >>> techs, cats = wap.load_file("technologies.json")

    .. _technologies.json: https://github.com/AliasIO/wappalyzer/blob/master/src/technologies.json
    """
    with open(filepath) as json_file:
        return load_stream(json_file)


def load_stream(
        stream: TextIO
) -> Tuple[Dict[str, Technology], Dict[str, Category]]:
    """Loads the contents of an technologies.json_ already opened.

    Args:
        stream (TextIO): A stream of the technologies.json_ content.

    Returns:
        Tuple[Dict[str, Technology], Dict[str, Category]]: A tuple with the
            technologies and the categories defined in technologies.json_.

    Example:
        >>> import wap
        >>> techs, cats = wap.load_stream(open("technologies.json"))

    .. _technologies.json: https://github.com/AliasIO/wappalyzer/blob/master/src/technologies.json
    """
    json_dict = json.load(stream)
    return load_apps(json_dict)


def load_apps(json_dict) -> Tuple[Dict[str, Technology], Dict[str, Category]]:
    """Parses the object generated from the json definition in technologies.json_ and
    returns the technologies and the categories.

    Args:
        json_dict : A object representing the json content of technologies.json_, for
            example loaded with the `json.load` function.

    Returns:
        Tuple[Dict[str, Technology], Dict[str, Category]]: A tuple with the
            technologies and the categories defined in the input object.


    Example:
        >>> import json
        >>> import wap
        >>> techs, cats = wap.load_apps(json.load(open("technologies.json")))

    .. _technologies.json: https://github.com/AliasIO/wappalyzer/blob/master/src/technologies.json
    """
    categories = load_categories(json_dict["categories"])
    technologies = {
        name: Technology(
            name=name,
            categories=[categories[str(c)] for c in techno.get("cats", [])],
            url=_transform_patterns(techno.get("url", None)),
            headers=_transform_patterns(techno.get("headers", None)),
            cookies=_transform_patterns(techno.get("cookies", None)),
            html=_transform_patterns(techno.get("html", None)),
            meta=_transform_patterns(techno.get("meta", None)),
            scripts=_transform_patterns(techno.get("scripts", None)),
            js=_transform_patterns(techno.get("js", None), True),
            implies=[
                Imply(name=pt.value, confidence=pt.confidence)
                for pt in _transform_patterns(techno.get("implies", None))
            ],
            excludes=[
                Exclude(name=pt.value)
                for pt in _transform_patterns(techno.get("excludes", None))
            ],
            icon=techno.get("icon", ""),
            website=techno.get("website", ""),
            cpe=techno.get("cpe", ""),
        )
        for name, techno in json_dict["technologies"].items()
    }

    return (technologies, categories)


def load_categories(json_dict) -> Dict[str, Category]:
    """Parses the object generated from the json definition of the categories
    section of technologies.json_ and returns the categories.

    Args:
        json_dict : A object representing the json content of the categories
            section of technologies.json_, for example loaded with the `json.load`
            function.

    Returns:
        Dict[str, Category]: Categories defined in the input object.

    Example:
        >>> import json
        >>> import wap
        >>> cats = wap.load_categories(json.load(open("technologies.json"))["categories"])

    .. _technologies.json: https://github.com/AliasIO/wappalyzer/blob/master/src/technologies.json
    """
    return {
        id_: Category(
            id_=id_,
            name=cat["name"],
            priority=cat["priority"]
        )
        for id_, cat in json_dict.items()
    }


def _transform_patterns(
        patterns: Any,
        case_sensitive: bool = False
) -> Union[List[Pattern], Dict[str, List[Pattern]]]:
    """Canonicalize the patterns of different sections.
    """
    def to_list(value):
        return value if type(value) is list else [value]

    if not patterns:
        return []

    if type(patterns) is str or type(patterns) is list:
        patterns = {
            "main": patterns
        }

    parsed = {}
    for key in patterns:
        name = key if case_sensitive else key.lower()
        parsed[name] = [
            _parse_pattern(ptrn, key)
            for ptrn in to_list(patterns[key])
        ]

    return parsed["main"] if "main" in parsed else parsed


def _parse_pattern(pattern: str, key: str = "") -> Pattern:
    """Parse the regex pattern and creates a Pattern object.
    It extracts the regex, the version and the confidence values of
    the given string.
    """
    parts = pattern.split("\\;")

    value = parts[0]

    # seems that in js "[^]" is similar to ".", however python
    # re interprets in a diferent way (which leads to an error),
    # so it is better to substitute it
    regex = value.replace("/", "\\/").replace("[^]", ".")

    attrs = {
        "value": value,
        "regex": re.compile(regex, re.I)
    }
    for attr in parts[1:]:
        attr = attr.split(":")
        if len(attr) > 1:
            attrs[attr[0]] = ":".join(attr[1:])

    return Pattern(
        value=attrs["value"],
        regex=attrs["regex"],
        confidence=int(attrs.get("confidence", 100)),
        version=attrs.get("version", ""),
        key=key,
    )
