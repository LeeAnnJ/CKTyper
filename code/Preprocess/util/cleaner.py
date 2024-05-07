import warnings
import re

warnings.filterwarnings(action='ignore', category=UserWarning, module='bs4')

from bs4 import BeautifulSoup

long_code_pstrs = [
    r'<pre.*?>\s*?<code>(.*?\n)*?.*?</code>\s*</pre>',
    r'<pre.*?>\s*?<code>(.*?\n)*?.*?</pre>\s*</code>',
    r'<code>\s*?<pre.*?>(.*?\n)*?.*?</pre>\s*</code>',
    r'<code>\s*?<pre.*?>(.*?\n)*?.*?</code>\s*</pre>',
    r'<pre.*?>(.*?\n)*?.*?</pre>'
]

long_code_patterns = list()
for reg_str in long_code_pstrs:
    long_code_patterns.append(re.compile(reg_str, re.IGNORECASE))

# short_code_pattern = re.compile(r'<code>(.*?\n)*?.*?</code>', re.IGNORECASE)
# link_pattern = re.compile(r'<a .*?href=.*?>', re.IGNORECASE)
blockquote_pattern = re.compile(r'<blockquote>(.*?\n)*?.*?</blockquote>', re.IGNORECASE)


def cleanText(text):
    """
    Clean a text, including the blockquotes,
    long code snippets, short code snippets, and links.
    """
    items = re.finditer(blockquote_pattern, text)
    for item in items:
        s = item.group()
        text = text.replace(s, '')

    for lcp in long_code_patterns:
        items = re.finditer(lcp, text)
        for item in items:
            s = item.group()
            text = text.replace(s, ' ', 1)

    # items = re.finditer(short_code_pattern, text)
    # for item in items:
    #     s = item.group()
    #     rs = s[len('<code>'):len(s) - len('</code>')].strip()
    #     if re.match(r'[^!=;{}+-]+$', rs):
    #         text = text.replace(s, rs, 1)
    #
    # items = re.finditer(link_pattern, text)
    # for item in items:
    #     link = item.group()
    #     i = text.find(link) + len(link)
    #     entity = text[i:text.find('</a>', i)]
    #     text = text.replace(link + entity + '</a>', entity, 1)

    text = cleanHtmlTags(text)
    if text is not None:
        return ' '.join(text.split(' '))
    return ''


def cleanHtmlTags(s):
    """
    Clean html tags in a string.
    """
    try:
        soup = BeautifulSoup(s, 'html.parser', from_encoding='utf-8')
        return soup.get_text()
    except Exception as e:
        print '***** cleanHtmlTags() Error *****', e
        return None


if __name__ == '__main__':

    _s = """ <code>String s = 'abc' + trim();\ni++;</code>
     <a :   href='http://www.baidu.cm/'>http://www.baidu.com</a>"""

    print cleanHtmlTags(_s)
    print cleanText(_s)
