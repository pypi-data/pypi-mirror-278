import lxml.etree
import requests
import lxml
from requests import Response
from typing import List
class WResponse:
    
    def __init__(self, response: requests.Response):
        self.resp = response
        
        
    def xpath(self, xpath: str) -> List[lxml.etree._Element]:
        html: lxml.etree._Element = lxml.etree.HTML(self.resp.text)
        return html.xpath(xpath)
        