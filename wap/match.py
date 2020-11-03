import re
import logging
from typing import List, Iterator, Dict, Optional
from .structs import Technology, PatternMatch, Pattern, TechMatch
from functools import partial

logger = logging.getLogger(__name__)


def discover_technologies(
        technologies: Dict[str, Technology],
        url: str = "",
        html: str = "",
        scripts: List[str] = None,
        cookies: Dict[str, List[str]] = None,
        metas: Dict[str, List[str]] = None,
        headers: Dict[str, List[str]] = None
) -> List[TechMatch]:
    """Discover the technologies that matches with the values provided into
    the different parameters. Also resolve the implied/excluded technologies.

    Example:
        >>> import wap
        >>> import requests
        >>> techs, _ = wap.load_file("technologies.json")
        >>> resp = requests.get("https://www.github.com")
        >>> resp_attrs = wap.parse_requests_response(resp)
        >>> techno_matches = wap.discover_technologies(techs, **resp_attrs)
    """
    pattern_matches = match_all(
        technologies,
        url=url,
        html=html,
        scripts=scripts,
        cookies=cookies,
        metas=metas,
        headers=headers,
    )

    return resolve_techno_matches(technologies, pattern_matches)


def match_all(
        technologies: Dict[str, Technology],
        url: Optional[str] = "",
        html: Optional[str] = "",
        scripts: Optional[List[str]] = None,
        cookies: Optional[Dict[str, List[str]]] = None,
        metas: Optional[Dict[str, List[str]]] = None,
        headers: Optional[Dict[str, List[str]]] = None,
        js_vars: Optional[Dict[str, List[str]]] = None,
) -> Iterator[PatternMatch]:
    """For the given parameters, retrieves the technology patterns that match.

    Example:
        >>> import wap
        >>> import requests
        >>> techs, _ = wap.load_file("technologies.json")
        >>> resp = requests.get("https://www.github.com")
        >>> resp_attrs = wap.parse_requests_response(resp)
        >>> pattern_matches = wap.match_all(techs, **resp_attrs)
        >>> techno_matches = wap.resolve_techno_matches(techs, pattern_matches)
    """
    def match_parts(techno, funcs):
        for func in funcs:
            yield from func(techno)

    match_funcs = []

    if url:
        match_funcs.append(partial(match_url, url=url))

    if headers:
        match_funcs.append(partial(match_headers, headers=headers))

    if cookies:
        match_funcs.append(partial(match_cookies, cookies=cookies))

    if html:
        match_funcs.append(partial(match_html, html=html))

    if metas:
        match_funcs.append(partial(match_metas, metas=metas))

    if scripts:
        match_funcs.append(partial(match_scripts, scripts=scripts))

    if js_vars:
        match_funcs.append(partial(match_js_vars, js_vars=js_vars))

    match_techno = partial(match_parts, funcs=match_funcs)

    for technology in technologies.values():
        yield from match_techno(technology)


def match_url(technology: Technology, url: str) -> Iterator[PatternMatch]:
    """Wrapper to search for url matches.

    Example:
        >>> import wap
        >>> import requests
        >>> techs, _ = wap.load_file("technologies.json")
        >>> resp = requests.get("https://www.github.com")
        >>> pattern_matches = []
        >>> for tech in techs.values():
        ...     pattern_matches.extend(wap.match_url(tech, resp.url))
        >>> techno_matches = wap.resolve_techno_matches(techs, pattern_matches)
    """
    return match_str(technology, "url", url)


def match_html(technology: Technology, html: str) -> Iterator[PatternMatch]:
    """Wrapper to search for html matches.

    Example:
        >>> import wap
        >>> import requests
        >>> techs, _ = wap.load_file("technologies.json")
        >>> resp = requests.get("https://www.github.com")
        >>> pattern_matches = []
        >>> for tech in techs.values():
        ...     pattern_matches.extend(wap.match_html(tech, resp.text))
        >>> techno_matches = wap.resolve_techno_matches(techs, pattern_matches)
    """
    return match_str(technology, "html", html)


def match_scripts(
        technology: Technology,
        scripts: List[str]
) -> Iterator[PatternMatch]:
    """Wrapper to search for scripts matches.

    Example:
        >>> import wap
        >>> import requests
        >>> techs, _ = wap.load_file("technologies.json")
        >>> resp = requests.get("https://www.github.com")
        >>> scripts = wap.extract_scripts(resp.text)
        >>> pattern_matches = []
        >>> for tech in techs.values():
        ...     pattern_matches.extend(wap.match_scripts(tech, scripts))
        >>> techno_matches = wap.resolve_techno_matches(techs, pattern_matches)
    """
    return match_list(technology, "scripts", scripts)


def match_js_vars(
        technology: Technology,
        js_vars: Dict[str, List[str]],
) -> Iterator[PatternMatch]:
    """Wrapper to search for matches in javascript variables."""
    return match_pairs(technology, "js", js_vars)


def match_cookies(
        technology: Technology,
        cookies: Dict[str, List[str]]
) -> Iterator[PatternMatch]:
    """Wrapper to search for cookies matches.

    
    Example:
        >>> import wap
        >>> import requests
        >>> techs, _ = wap.load_file("technologies.json")
        >>> resp = requests.get("https://www.github.com")
        >>> cookies = wap.parse_requests_headers(resp.cookies)
        >>> pattern_matches = []
        >>> for tech in techs.values():
        ...     pattern_matches.extend(wap.match_cookies(tech, cookies))
        >>> techno_matches = wap.resolve_techno_matches(techs, pattern_matches)
    """
    return match_pairs(technology, "cookies", cookies)


def match_metas(
        technology: Technology,
        metas: Dict[str, List[str]]
) -> Iterator[PatternMatch]:
    """Wrapper to search for meta matches.

    Example:
        >>> import wap
        >>> import requests
        >>> techs, _ = wap.load_file("technologies.json")
        >>> resp = requests.get("https://www.github.com")
        >>> metas = wap.extract_metas(resp.text)
        >>> pattern_matches = []
        >>> for tech in techs.values():
        ...     pattern_matches.extend(wap.match_metas(tech, metas))
        >>> techno_matches = wap.resolve_techno_matches(techs, pattern_matches)
    """
    return match_pairs(technology, "meta", metas)


def match_headers(
        technology: Technology,
        headers: Dict[str, List[str]]
) -> Iterator[PatternMatch]:
    """Wrapper to search for headers matches.

    Example:
        >>> import wap
        >>> import requests
        >>> techs, _ = wap.load_file("technologies.json")
        >>> resp = requests.get("https://www.github.com")
        >>> headers = wap.parse_requests_headers(resp.headers)
        >>> pattern_matches = []
        >>> for tech in techs.values():
        ...     pattern_matches.extend(wap.match_headers(tech, headers))
        >>> techno_matches = wap.resolve_techno_matches(techs, pattern_matches)
    """
    return match_pairs(technology, "headers", headers)


def match_str(
        tech: Technology,
        field: str,
        value: str
) -> Iterator[PatternMatch]:
    """To match attributes against a string, like an URL or HTML content.

    Args:
        tech (Technology): The technology to search matches
        field (str): The field to look for matches. Must be "url" or "html".
        value (str)

    Returns:
        Iterator[PatternMatch]: An iterator with the found matches.

    """
    return _match_patterns(tech[field], tech, value)


def match_list(
        tech: Technology,
        field: str,
        values: List[str]
) -> Iterator[PatternMatch]:
    """To match against a list of string, like some js scripts URIs.

    Args:
        tech (Technology): The technology to search matches
        field (str): The field to look for matches. Must be "scripts".
        values (List[str])

    Returns:
        Iterator[PatternMatch]: An iterator with the found matches.
    """
    for value in values:
        patterns = tech.get(field, [])
        yield from _match_patterns(patterns, tech, value)


def match_pairs(
        tech: Technology,
        field: str,
        pairs: Dict[str, List[str]]
) -> Iterator[PatternMatch]:
    """To analyze attributes that are a dict with keys and values.
    Such as headers, cookies and meta tags.

    Args:
        tech (Technology): The technology to search matches
        field (str): The field to look for matches. Must be "cookies"
            "headers" or "meta".
        pairs (Dict[str, List[str]])

    Returns:
        Iterator[PatternMatch]: An iterator with the found matches.

    """

    if field in ["cookies"]:
        pairs_local = {}
        for k in pairs:
            pairs_local[k.lower()] = pairs[k]
    else:
        pairs_local = pairs

    for key in tech[field]:
        # get patterns this way since pairs could be a dict or empty list
        patterns = tech[field][key] or []
        values = pairs_local.get(key, [])

        for value in values:
            yield from _match_patterns(patterns, tech, value)


def _match_patterns(
        patterns: List[Pattern],
        technology: Technology,
        value: str
) -> Iterator[PatternMatch]:
    """Check the regexes of the patterns against the value"""
    for pattern in patterns:
        if pattern.regex.search(value):
            yield PatternMatch(
                technology=technology,
                pattern=pattern,
                version=_resolve_version(
                    pattern.version,
                    pattern.regex,
                    value
                )
            )


def _resolve_version(
        version: str,
        regex: re.Pattern,
        value: str
) -> str:
    """Extracts the version from the match, used the matched group
    indicated by an string with format: "\\1" or
    "\\1?value_1:value_2" (ternary version) in the \\;version field
    of the regex
    """
    if not version:
        return version

    matches = regex.search(value)

    if not matches:
        return version

    resolved = version
    matches = [matches.group()] + list(matches.groups())
    for index, match in enumerate(matches):
        ternary = re.search("\\\\{}\\?([^:]+):(.*)$".format(index), version)

        if ternary:
            ternary = [ternary.group()] + list(ternary.groups())

            if len(ternary) == 3:
                resolved = version.replace(
                    ternary[0],
                    ternary[1] if match else ternary[2]
                )

        resolved = resolved.strip().replace(
            "\\{}".format(index),
            match or ""
        )

    return resolved


def resolve_techno_matches(
        technologies: Dict[str, Technology],
        pattern_matches: Iterator[PatternMatch]
) -> List[TechMatch]:
    """Extracts from the pattern matches, the matches in technology and
    resolve the implied and excluded technology.
    """
    pattern_matches = list(set(pattern_matches))
    techno_matches = extract_techno_matches(pattern_matches)
    techno_matches = resolve_implies(techno_matches, technologies)
    techno_matches = resolve_excludes(techno_matches)
    return techno_matches


def extract_techno_matches(
        pattern_matches: List[PatternMatch]
) -> List[TechMatch]:
    """Extracts the technologies in the matches, adjusting the version
    and confidence, and removing duplicates.
    """
    techno_matches = []
    for pattern_match in pattern_matches:
        if pattern_match not in techno_matches:
            version = ""
            confidence = 0

            for pt_match in pattern_matches:
                if pt_match != pattern_match:
                    continue

                confidence = min(100, confidence + pt_match.pattern.confidence)
                version = pt_match.version \
                    if len(version) < len(pt_match.version) <= 10 \
                    else version

            techno_matches.append(TechMatch(
                pattern_match.technology,
                confidence,
                version
            ))
    return techno_matches


def resolve_implies(
        techno_matches: List[TechMatch],
        technologies: Dict[str, Technology],
) -> List[TechMatch]:
    """Generates a list that includes the technology matches and
    the technologies implied by the first ones. Also avoid the duplicates.
    """
    techno_impls = []
    for techno_match in techno_matches:
        _resolve_implies_inner(techno_impls, techno_match, technologies)
    return techno_impls


def _resolve_implies_inner(
        techno_impls: List[TechMatch],
        techno_match: TechMatch,
        technologies: Dict[str, Technology]
):
    if techno_match not in techno_impls:
        techno_impls.append(techno_match)
        implies = [
            TechMatch(
                technology=technologies[imply.name],
                confidence=min(imply.confidence, techno_match.confidence),
                version=''
            )
            for imply in techno_match.technology.implies
        ]
        for implied_techno in implies:
            _resolve_implies_inner(techno_impls, implied_techno, technologies)


def resolve_excludes(
        techno_matches: List[TechMatch],
) -> List[TechMatch]:
    """Generates a list that not includes the technology matches
     that cause conflict with others, by letting only an excludent option.
    """
    # Avoids the destruction of the original list
    techno_matches = techno_matches[:]
    techn_excls = []

    try:
        while True:
            techno_match = techno_matches.pop(0)
            techn_excls.append(techno_match)

            excludes = [ex.name for ex in techno_match.technology.excludes]
            techno_matches = [
                tm for tm in techno_matches
                if tm.technology.name not in excludes
            ]

    except IndexError:
        pass

    return techn_excls
