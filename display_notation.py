"""Presentation-only formatting for student practice prompts. Never used to parse answers."""
import re

SUPERSCRIPTS=str.maketrans('0123456789+-','⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻')

def readable_math(text):
    """Convert common Python math syntax to readable Unicode without changing the prompt's meaning.

    This deliberately avoids general expression parsing, since many prompts contain prose,
    units, or multiple mathematical fragments.
    """
    if not isinstance(text,str):
        raise TypeError('Expected a string')
    # Exponents are formatted before multiplication so ** is never confused with *.
    text=re.sub(r'\*\*\s*\(\s*([+-]?\d+)\s*\)',lambda m: ''.join(ch.translate(SUPERSCRIPTS) for ch in m.group(1)),text)
    text=re.sub(r'\*\*\s*([+-]?\d+)(?![\d.])',lambda m: ''.join(ch.translate(SUPERSCRIPTS) for ch in m.group(1)),text)
    # A remaining ** exponent might be symbolic; render it with an explicit caret.
    text=text.replace('**','^')
    # Only remove explicit multiplication between a number/parenthesis and a variable or function.
    text=re.sub(r'(?<=\d)\s*\*\s*(?=[A-Za-z(])','',text)
    text=re.sub(r'(?<=\))\s*\*\s*(?=[A-Za-z(])','',text)
    text=re.sub(r'(?<=[A-Za-z])\s*\*\s*(?=[A-Za-z(])','·',text)
    # Remaining explicit multiplications become readable multiplication symbols.
    text=text.replace('*',' × ')
    return text
