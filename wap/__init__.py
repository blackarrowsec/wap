"""
Library to parse wappalyzer technologies.json_ and extracts matches from HTTP responses.


The following examples shows how to use it in conjuction with requests and bs4
in order to get the technologies of "https://www.github.com":

.. highlight:: python
.. code-block:: python

   import requests
   import wap


   technologies, categories = wap.load_file("technologies.json")
   resp = requests.get("https://www.github.com")
   techno_matches = wap.discover_requests_technologies(technologies, resp)

   for t in techno_matches:
       fields = [t.technology.name]
       fields.append(t.version)
       fields.append(str(t.confidence))

       fields.append(",".join(
           [c.name for c in t.technology.categories]
       ))

       print(" ".join(fields))

    if __name__ == '__main__':
        main()


For more examples, look in the `repository examples folder <https://github.com/blackarrowsec/wap/tree/master/examples>`_.

.. _technologies.json: https://github.com/AliasIO/wappalyzer/blob/master/src/technologies.json
"""

from .load import load_file, load_stream, load_apps, load_categories
from .match import match_str, match_list, match_pairs, match_url, \
    match_html, match_scripts, match_cookies, match_metas, match_headers, \
    resolve_techno_matches, extract_techno_matches, resolve_implies, \
    resolve_excludes, discover_technologies, match_all
from .structs import Technology, TechMatch, Category, Pattern, \
    PatternMatch, Imply, Exclude
from .helper import extract_scripts, extract_metas, \
    parse_requests_cookies, parse_requests_headers, \
    parse_requests_response, discover_requests_technologies
