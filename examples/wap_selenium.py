import wap
from selenium import webdriver
from typing import Dict, List
import argparse


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "url",
        help="Url to request"
    )

    parser.add_argument(
        "--file",
        help="File with apps regexps",
        default="technologies.json"
    )

    return parser.parse_args()


def main():
    args = parse_args()
    technologies, _ = wap.load_file(args.file)

    browser = webdriver.Chrome()
    browser.get(args.url)
    url = browser.current_url
    cookies = parse_cookies_selenium(browser.get_cookies())
    html = browser.page_source
    scripts = extract_scripts_selenium(browser)
    metas = extract_metas_selenium(browser)
    browser.close()

    techno_matches = wap.discover_technologies(
        technologies,
        url=url,
        cookies=cookies,
        html=html,
        scripts=scripts,
        metas=metas
    )

    for t in techno_matches:
        fields = [t.technology.name]
        fields.append(t.version)
        fields.append(str(t.confidence))

        fields.append(",".join(
            [c.name for c in t.technology.categories]
        ))

        print(" ".join(fields))


def parse_cookies_selenium(cookies) -> Dict[str, List[str]]:
    """Helper to parse the cookies retrieved for the 
    selenium browser, and generate cookies to be used 
    by wap.

    Example:
        >>> import wap
        >>> from selenium import webdriver
        >>> browser = webdriver.Chrome()
        >>> browser.get("https://www.github.com")
        >>> cookies = wap.parse_selenium_cookies(browser.get_cookies())
    """
    cks = {}
    for cookie in cookies:
        if cookie["name"] not in cks:
            cks[cookie["name"]] = []
        cks[cookie["name"]].append(cookie["value"])
    return cks


def extract_scripts_selenium(browser) -> List[str]:
    """Helper to extract the javascript scripts paths or URL
    from the selenium browser.

    Example:
        >>> import wap
        >>> from selenium import webdriver
        >>> browser = webdriver.Chrome()
        >>> browser.get("https://www.github.com")
        >>> scripts = wap.extract_scripts_selenium(browser)

    """
    scripts = []
    script_tags = browser.find_elements_by_tag_name("script")
    for script in script_tags:
        src = script.get_attribute("src")
        if src and not src.startswith("data:text/javascript;"):
            scripts.append(src)

    return scripts


def extract_metas_selenium(browser) -> Dict[str, str]:
    """Helper to extract the name and content of the meta tags
    from the selenium browser.

    Example:
        >>> from selenium import webdriver
        >>> browser = webdriver.Chrome()
        >>> browser.get("https://www.github.com")
        >>> metas = extract_metas_selenium(browser)

    """
    meta_tags = browser.find_elements_by_tag_name("meta")

    metas = {}
    for meta in meta_tags:
        key = meta.get_attribute("name") or meta.get_attribute("property")
        content = meta.get_attribute("content")
        if key:
            metas[key.lower()] = [content]

    return metas


if __name__ == '__main__':
    main()
