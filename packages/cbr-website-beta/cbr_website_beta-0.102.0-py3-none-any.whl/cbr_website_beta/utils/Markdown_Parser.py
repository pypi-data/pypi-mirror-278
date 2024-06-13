import frontmatter
from markdown import Markdown


class Markdown_Parser:
    def __init__(self):
        self.md = Markdown()

    def markdown_to_html(self, markdown_text):
        return self.md.convert(markdown_text)

    def content_to_html(self, content):
        metadata, markdown = frontmatter.parse(content)
        return  self.markdown_to_html(markdown)