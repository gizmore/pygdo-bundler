import re


class HTMLMinifier:

    @staticmethod
    def minify(s: str) -> str:
        s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
        s = re.sub(r">\s+<", "><", s)
        s = re.sub(r"\s{2,}", " ", s)
        return s.strip()
