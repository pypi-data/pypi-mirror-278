"""
Definition of the Latex2MathML extension.
"""

import re

from latex2mathml import converter

from markdown import Extension
from markdown.blockprocessors import BlockProcessor
from markdown.inlinepatterns import Pattern


# pylint: disable=too-few-public-methods
class LaTeX2MathMLExtension(Extension):
    """
    The Latex2MathMLExtension class.
    """

    _RE_LATEX = r"\$([^$]+)\$"

    # pylint: disable=invalid-name
    def extendMarkdown(self, md):
        """
        Extend the specified markdown instance with a pattern for inline
        LaTex and a parser for blocks of LaTeX, to be converted to MathML.
        """
        md.inlinePatterns.register(
            LatexPattern(self._RE_LATEX), "latex-inline", 100)
        md.parser.blockprocessors.register(
            LatexBlockProcessor(md.parser), 'latex-block', 100)


# pylint: disable=too-few-public-methods
class LatexPattern(Pattern):
    """
    A pattern for inline LaTeX.
    """

    # pylint: disable=invalid-name
    def handleMatch(self, m):
        """
        Convert inline LaTeX to MathML.
        """
        return converter.convert_to_element(m.group(2))


# pylint: disable=too-few-public-methods
class LatexBlockProcessor(BlockProcessor):
    """
    A processor for blocks of LaTeX.
    """

    _RE_LATEX_START = r"^\s*\${2}"
    _RE_LATEX_END = r"\${2}\s*$"

    def test(self, _, block):
        """
        Indicated whether the specified block starts a block of LaTeX.
        """
        return re.search(self._RE_LATEX_START, block)

    def run(self, parent, blocks):
        """
        Convert all subsequent blocks of LaTeX to MathML. Cancel conversion
        in case no ending block is found.
        """
        text = ""

        for i, block in enumerate(blocks):
            text = text + block

            if re.search(self._RE_LATEX_END, block):
                for j in range(0, i + 1):
                    blocks.pop(j)
                break
            if i >= len(blocks) - 1:
                # no ending block is found
                return False

        text = re.sub(self._RE_LATEX_START, "", text)
        text = re.sub(self._RE_LATEX_END, "", text)

        converter.convert_to_element(text, display="block", parent=parent)

        return True
