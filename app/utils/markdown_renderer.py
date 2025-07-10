from markdown2 import Markdown
import bleach
from markupsafe import Markup


class SafeMarkdownRenderer:
    def __init__(self):
        self.allowed_tags = [
            "p",
            "br",
            "strong",
            "em",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "ul",
            "ol",
            "li",
            "blockquote",
            "code",
            "pre",
            "a",
            "img",
            "hr",
            "table",
            "thead",
            "tbody",
            "tr",
            "th",
            "td",
            "del",
            "strike",
            "s",
            "ins",
            "mark",
            "sub",
            "sup",
            "input",
            "label",
            "span",
            "div",
        ]
        self.allowed_attributes = {
            "a": ["href", "title", "id"],
            "img": ["src", "alt", "title", "width", "height"],
            "h1": ["id"],
            "h2": ["id"],
            "h3": ["id"],
            "h4": ["id"],
            "h5": ["id"],
            "h6": ["id"],
            "input": ["type", "checked", "disabled"],
            "span": ["class"],
            "div": ["class"],
            "table": ["class"],
            "thead": ["class"],
            "tbody": ["class"],
            "tr": ["class"],
            "th": ["class"],
            "td": ["class"],
        }
        self.allowed_protocols = ["http", "https", "mailto"]
        self.md = Markdown(
            extras=[
                "fenced-code-blocks",
                "strike",
                "tables",
                "task_list",
                "code-friendly",
                "footnotes",
                "header-ids",
                "spoiler",
            ]
        )

    def render(self, text: str) -> Markup:
        html = self.md.convert(text or "")
        clean_html = bleach.clean(
            html,
            tags=self.allowed_tags,
            attributes=self.allowed_attributes,
            protocols=self.allowed_protocols,
            strip=True,
        )
        return Markup(clean_html)
