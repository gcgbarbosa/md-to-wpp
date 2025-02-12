import marko
from marko.renderer import Renderer


class Lhufas(Renderer):
    """
    Custom Renderer that converts Markdown elements into the requested custom format.
    """

    def render(self, element):
        """
        Override the base render method to handle cases where 'element' is a string.
        If 'element' is a string, return it directly. Otherwise, proceed with normal rendering.
        """
        if isinstance(element, str):
            return element
        return super().render(element)

    def render_paragraph(self, element):
        """
        Render a paragraph by concatenating its children and adding a newline.
        """
        return "".join(self.render(child) for child in element.children) + "\n"

    def render_strong_emphasis(self, element):
        """
        **Strong** -> *texto*
        """
        inner = "".join(self.render(child) for child in element.children)
        return f"*{inner}*"

    def render_emphasis(self, element):
        """
        *Italic* -> _texto_
        """
        inner = "".join(self.render(child) for child in element.children)
        return f"_{inner}_"

    def render_strikethrough(self, element):
        """
        ~~Strikethrough~~ -> ~texto~
        """
        inner = "".join(self.render(child) for child in element.children)
        return f"~{inner}~"

    def render_code_span(self, element):
        """
        Inline code -> `texto`
        """
        # element.children can be a list of strings or a single string
        code_text = "".join(self.render(child) for child in element.children)
        return f"`{code_text}`"

    def render_fenced_code(self, element):
        """
        Fenced code block -> ```codigo```
        """
        # Join all lines of the code block
        code_text_joined = "".join(self.render(child) for child in element.children)
        return f"```{code_text_joined}```\n"

    def render_list(self, element):
        """
        Render a bullet or numbered list based on whether it's ordered.
        """
        output = []
        if element.ordered:
            start = element.start if element.start is not None else 1
            for i, child in enumerate(element.children, start):
                child_content = self.render(child).strip()
                lines = child_content.split("\n")
                if lines:
                    lines[0] = f"{i}. {lines[0]}"
                # Indent sub-items if any
                for j in range(1, len(lines)):
                    lines[j] = f"   {lines[j]}"
                output.append("\n".join(lines))
        else:
            for child in element.children:
                child_content = self.render(child).strip()
                lines = child_content.split("\n")
                if lines:
                    lines[0] = f"- {lines[0]}"
                # Indent sub-items if any
                for j in range(1, len(lines)):
                    lines[j] = f"  {lines[j]}"
                output.append("\n".join(lines))

        return "\n".join(output) + "\n"

    def render_list_item(self, element):
        """
        Render the content of a list item by concatenating its children.
        """
        return "".join(self.render(child) for child in element.children)

    def render_quote(self, element):
        """
        Blockquote -> > texto
        """
        content = "".join(self.render(child) for child in element.children).strip()
        lines = content.split("\n")
        quoted = "\n".join([f"> {line}" for line in lines if line.strip()])
        return quoted + "\n"

    def render_heading(self, element):
        """
        Render headings as plain text followed by a newline.
        You can customize this if you want a different representation for headings.
        """
        text = "".join(self.render(child) for child in element.children)
        return "*" + text + "*\n"

    def render_link(self, element):
        """
        Render links in the format: "link text (URL)"
        """
        link_text = "".join(self.render(child) for child in element.children)
        url = element.dest
        return f"{link_text} ({url})" if url else link_text

    def render_image(self, element):
        """
        Render images in the format: "[alt_text] (URL)"
        """
        alt_text = element.alt or ""
        url = element.dest or ""
        return f"[{alt_text}] ({url})"

    def render_text(self, element):
        """
        Render plain text. Handles both string elements and text node objects.
        """
        if isinstance(element, str):
            return element
        return element.children

    def render_line_break(self, element):
        """
        Render a line break as a newline character.
        """
        return "\n"


def markdown_to_whatsapp_format(markdown_text: str) -> str:
    """
    Converts Markdown text to the custom format using the CustomFormatRenderer.
    """
    parser = marko.Markdown(renderer=WahtsappFormatRenderer)  # Pass the class, not an instance
    return parser(markdown_text)
