"""Normalize a small, explicit set of familiar math notations; no eval."""
import re

def normalize_math(text):
    text = text.strip().translate(str.maketrans({'²':'^2','³':'^3','⁴':'^4','⁵':'^5','⁶':'^6','⁷':'^7','⁸':'^8','⁹':'^9','⁰':'^0','¹':'^1','−':'-','×':'*','÷':'/','π':'pi','√':'sqrt'}))
    text = text.replace('**','^').replace('\u00a0',' ')
    text = re.sub(r'\bln\s*\(', 'log(', text)
    # e^(...) is interpreted as exp(...); e^x and e^2 are valid as E^x / E^2.
    text = re.sub(r'(?<![A-Za-z_])e\s*\^', 'E^', text)
    # Support the most common textbook implicit products without rewriting function calls.
    text = re.sub(r'(?<=\d)\s*(?=[xyE(])', '*', text)
    text = re.sub(r'(?<=\))\s*(?=[xyE(])', '*', text)
    text = re.sub(r'(?<=[xy])\s*(?=\()', '*', text)
    text = re.sub(r'(?<=\d)\s+(?=\d)', '', text)
    return text
