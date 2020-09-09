"""
This module defines the structures used by the package.
"""

import re
from typing import List, Dict


class Category:
    """A category to classify technologies in groups. Examples or categories
    are "CMS", "Javascript frameworks", "Web servers", etc.

    The exhaustive list of categories is defined in the technologies.json_ file in
    the wappalyzer repository.

    Attributes:
        id_ (str): The identifier of category in technologies.json_.
        name (str): The name of the category (e.g CMS).
        priority (int)

    .. _technologies.json: https://github.com/AliasIO/wappalyzer/blob/master/src/technologies.json

    """

    def __init__(self, id_: str, name: str, priority: int):
        self.id_ = id_
        self.name = name
        self.priority = priority


class Imply:
    """Structure to define a technology that is implied by the use of another
    one.

    Attributes:
        name (str): Name of the implied technology.
        confidence (int): Confidence of the implied technology.

    """

    def __init__(self, name: str, confidence: int):
        self.name = name
        self.confidence = confidence


class Exclude:
    """Structure to define a technology that is incompatible with another
    one.

    Attributes:
        name (str): Name of the excluded technology.

    """

    def __init__(self, name: str):
        self.name = name


class Pattern:
    """Holds the pattern definition that allows to identify a technology.

    Attributes:
        value (str): The pattern string.
        regex (re.Pattern): The regex used to identify the pattern.
        confidence (int): The confidence given by the value matched by this
            pattern.
        version (str): String that indicates how to identify the version in
            the matched value.
        key (str): Key to identified the element to apply the pattern
            (e.g a cookie or header name).
    """

    def __init__(
            self,
            value: str,
            regex: re.Pattern,
            confidence: int,
            version: str,
            key: str
    ):
        self.value = value
        self.regex = regex
        self.confidence = confidence
        self.version = version
        self.key = key

    def __getitem__(self, k):
        return self.__dict__[k]

    def __repr__(self):
        return repr(self.__dict__)


class Technology:
    """Definition of a technology and all of its rules that is extracted
    from technologies.json_ file.

    Attributes:
        name (str)

        categories (List[Category]): Categories to which the technology
            belongs.

        url (List[Pattern]): List of patterns to identify urls of the
            technology.

        headers (Dict[str, List[Pattern]]): List of headers patterns identified
            by the name of the header.

        cookies (Dict[str, List[Pattern]]): List of cookies patterns identified
            by the name of the cookie.

        html (List[Pattern]): List of patterns to match HTML content.

        meta (Dict[str, List[Pattern]]): List of patterns to match meta tags
            in HTML content, identified by the name of the each tag.

        scripts (List[Pattern]): List of patterns to match scripts URLs.

        js (Dict[str, List[Pattern]]): Dictionary that identifies javascript
            variables and regex for the values.

        implies (List[Imply]): List of technology names that are used in
            conjuction with the current technology.

        excludes (List[Exclude]): List of technologies that are incompatible
            with the current technology.

        icon (str): Indicates the file with the icon (in Wappalyzer icons_
            folder).

        website (str): Indicates the url of the technology website.

        cpe (str):


    .. _technologies.json: https://github.com/AliasIO/wappalyzer/blob/master/src/technologies.json
    .. _icons: https://github.com/AliasIO/wappalyzer/tree/master/src/drivers/webextension/images/icons
    """

    def __init__(
            self,
            name: str,
            categories: List[Category],
            url: List[Pattern],
            headers: Dict[str, List[Pattern]],
            cookies: Dict[str, List[Pattern]],
            html: List[Pattern],
            meta: Dict[str, List[Pattern]],
            scripts: List[Pattern],
            js: Dict[str, List[Pattern]],
            implies: List[Imply],
            excludes: List[Exclude],
            icon: str,
            website: str,
            cpe: str,
    ):
        self.name = name
        self.categories = categories
        self.url = url
        self.headers = headers
        self.cookies = cookies
        self.html = html
        self.meta = meta
        self.scripts = scripts
        self.js = js
        self.implies = implies
        self.excludes = excludes
        self.icon = icon
        self.website = website
        self.cpe = cpe

    def __getitem__(self, k):
        return self.__dict__[k]

    def get(self, *args, **kwargs):
        return self.__dict__.get(*args, **kwargs)

    def __repr__(self):
        return repr(self.__dict__)


class PatternMatch:
    """Identifies a match in a technology pattern.

    Attributes:
        technology (Technology): Technology identified by the pattern.
        pattern (Pattern): Pattern that cause the match.
        version (str): Version identified by the pattern in the match.
    """

    def __init__(self, technology: Technology, pattern: Pattern, version: str):
        self.technology = technology
        self.pattern = pattern
        self.version = version

    def __getitem__(self, k):
        return self.__dict__[k]

    def __repr__(self):
        return repr(self.__dict__)

    def __eq__(self, o):
        return self.technology.name == o.technology.name \
            and self.pattern.key == self.pattern.key \
            and self.pattern.value == self.pattern.value

    def __hash__(self):
        return hash(
            (self.technology.name, self.pattern.key, self.pattern.value)
        )


class TechMatch:
    """Identifies a match in a technology.

    Attributes:
        technology (Technology): Technology identified.
        confidence (int): Confidence in the match, is derivated from all the
            patterns of this technology that matched.
        version (str): Version identified by the patterns.
    """

    def __init__(self, technology: Technology, confidence: int, version: str):
        self.technology = technology
        self.confidence = confidence
        self.version = version

    def __getitem__(self, k):
        return self.__dict__[k]

    def __repr__(self):
        return repr(self.__dict__)

    def __eq__(self, o):
        return self.technology.name == o.technology.name
