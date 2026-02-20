import re
from bs4 import BeautifulSoup


class HTMLBeautifier:
    INLINE_TAGS = {
        "a", "span", "li",
        "b", "i", "u", "em", "strong", "small", "label", "option", "label",
        "code", "kbd", "samp", "sub", "sup", "mark", "q", "cite", "abbr", "time", "var",
        "title", "td", "th", "tr",
    }

    # tags you want forced onto one line when they only contain text/inline stuff
    INLINE_LINE_TAGS = {"a", "i", "b", "u", "span", "li", "title", "td", "th", "tr", "option"}

    # block-ish tags that disqualify inlining when found inside the element
    BLOCKY_INNER_TAGS = {
        "div", "p", "section", "article", "nav", "aside", "header", "footer", "main",
        "ul", "ol", "table", "thead", "tbody", "tfoot",
        "pre", "textarea", "form", "fieldset", "blockquote",
        "h1", "h2", "h3", "h4", "h5", "h6", "code"
    }

    RAW_PRESERVE_TAGS = {"pre", "textarea"}

    @classmethod
    def beautify(cls, html: str, indent_width: int = 1) -> str:
        soup = BeautifulSoup(html, "html.parser")
        pretty = soup.prettify(formatter="minimal")

        # stash <pre>/<textarea> blocks so we don't touch their whitespace
        preserved = []

        def stash(m: re.Match) -> str:
            preserved.append(m.group(0))
            return f"§§PRESERVE{len(preserved)-1}§§"

        pretty = re.sub(
            r"(?is)<(" + "|".join(map(re.escape, cls.RAW_PRESERVE_TAGS)) + r")\b[^>]*>.*?</\1\s*>",
            stash,
            pretty,
        )

        # regex to inline selected tags if their inner html contains no "blocky" tags
        inline_open = r"(?P<open><(?P<tag>" + "|".join(map(re.escape, cls.INLINE_LINE_TAGS)) + r")\b[^>]*>)"
        inline_close = r"(?P<close></(?P=tag)>)"
        inner = r"(?P<inner>.*?)"
        pat = re.compile(r"(?is)" + inline_open + r"\s*" + inner + r"\s*" + inline_close)

        blocky = re.compile(
            r"(?is)<(" + "|".join(map(re.escape, cls.BLOCKY_INNER_TAGS)) + r")\b"
        )

        def squash(m: re.Match) -> str:
            inner_html = m.group("inner")
            if blocky.search(inner_html):
                return m.group(0)

            # remove newlines/indent between inline nodes/text
            inner_html = re.sub(r"\s*\n\s*", "", inner_html)
            # remove spaces between tags
            inner_html = re.sub(r">\s+<", "><", inner_html)
            # collapse leftover runs of spaces
            inner_html = re.sub(r"\s{2,}", " ", inner_html).strip()
            return f"{m.group('open')}{inner_html}{m.group('close')}"

        # iterate until stable (handles nested inline tags)
        last = None
        while last != pretty:
            last = pretty
            pretty = pat.sub(squash, pretty)

        # restore preserved blocks
        for i, blk in enumerate(preserved):
            pretty = pretty.replace(f"§§PRESERVE{i}§§", blk)

        return pretty