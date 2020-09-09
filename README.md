# wap
[![](https://img.shields.io/badge/Category-Library-E5A505?style=flat-square)]() [![](https://img.shields.io/badge/Language-Python-E5A505?style=flat-square)]()

Library to parse [Wappalyzer](https://wappalyzer.com) 
[technologies.json](https://github.com/AliasIO/wappalyzer/blob/master/src/technologies.json)
and use its rules to discover web technologies by looking in the HTTP responses.

Functionality is similar to the [wappalyzer core module](https://github.com/AliasIO/wappalyzer/blob/master/src/wappalyzer.js), but in python.


## Installation

From pypi:
```shell
pip3 install wap
```

From repo:
```shell
git clone https://github.com/blackarrowsec/wap
cd wap/
python3 setup.py install
```


## Example

Here is a little example that uses almost all functionalities of wap with regex to retrieve the technologies of github:
```python
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

```

More examples in examples folder.

## Documentation
Documentation can be found in https://wap.readthedocs.io. 


## Adding new technologies

If you want that wap detects a new technology, you can add your rules to the 
[technologies.json](https://github.com/AliasIO/wappalyzer/blob/master/src/technologies.json) 
file and load it with wap. 

Please, consider to do a pull request to 
[Wappalyzer repo](https://github.com/AliasIO/wappalyzer)
and share your rules with the community. Follow the rules in 
[Adding a new technology](https://www.wappalyzer.com/docs/dev/contributing#adding-a-new-technology).

Please do not submit pull requests related to technologies.json, since this repository is 
not related with Wappalyzer.

## Author
Eloy Pérez ([@Zer1t0](https://github.com/Zer1t0)) [ [www.blackarrow.net](http://blackarrow.net/) - [www.tarlogic.com](https://www.tarlogic.com/en/) ]


## License
All the code included in this project is licensed under the terms of the GNU LGPLv3 license.

-----

[![](https://img.shields.io/badge/www-blackarrow.net-E5A505?style=flat-square)](https://www.blackarrow.net) [![](https://img.shields.io/badge/twitter-@BlackArrowSec-00aced?style=flat-square&logo=twitter&logoColor=white)](https://twitter.com/BlackArrowSec) [![](https://img.shields.io/badge/linkedin-@BlackArrowSec-0084b4?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/company/blackarrowsec/)


