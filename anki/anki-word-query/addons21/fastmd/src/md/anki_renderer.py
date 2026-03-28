from typing import Dict, Any
from mistune import BaseRenderer, BlockState
from .anki_tree import AnkiData
# 自定义渲染器来提取标题
class AnkiRenderer(BaseRenderer):
    """A renderer to re-format Markdown text."""
    NAME = 'anki'
    def __init__(self):
        BaseRenderer.__init__(self)
        self.anki = AnkiData()
    def __call__(self, tokens, state: BlockState):
        self.tokens = tokens
        self.state = state
        out = self.render_tokens(tokens, state)
        # special handle for line breaks
        out += '\n\n'.join(self.render_referrences(state)) + '\n'
        return out

    def render_referrences(self, state: BlockState):
        ref_links = state.env['ref_links']
        for key in ref_links:
            attrs = ref_links[key]
            text = '[' + attrs['label'] + ']: ' + attrs['url']
            title = attrs.get('title')
            if title:
                text += ' "' + title + '"'
            yield text

    def render_children(self, token, state: BlockState):
        children = token['children']
        return self.render_tokens(children, state)

    def text(self, token: Dict[str, Any], state: BlockState) -> str:
        return token['raw']

    def emphasis(self, token: Dict[str, Any], state: BlockState) -> str:
        return '*' + self.render_children(token, state) + '*'

    def strong(self, token: Dict[str, Any], state: BlockState) -> str:
        return '**' + self.render_children(token, state) + '**'

    def link(self, token: Dict[str, Any], state: BlockState) -> str:
        label = token.get('label')
        text = self.render_children(token, state)
        out = '[' + text + ']'
        if label:
            return out + '[' + label + ']'

        attrs = token['attrs']
        url = attrs['url']
        title = attrs.get('title')
        if text == url and not title:
            return '<' + text + '>'
        elif 'mailto:' + text == url and not title:
            return '<' + text + '>'

        out += '('
        if '(' in url or ')' in url:
            out += '<' + url + '>'
        else:
            out += url
        if title:
            out += ' "' + title + '"'
        return out + ')'

    def image(self, token: Dict[str, Any], state: BlockState) -> str:
        return '!' + self.link(token, state)

    def codespan(self, token: Dict[str, Any], state: BlockState) -> str:
        return '`' + token['raw'] + '`'

    def linebreak(self, token: Dict[str, Any], state: BlockState) -> str:
        return '  \n'

    def softbreak(self, token: Dict[str, Any], state: BlockState) -> str:
        return '\n'

    def blank_line(self, token: Dict[str, Any], state: BlockState) -> str:
        return ''

    def inline_html(self, token: Dict[str, Any], state: BlockState) -> str:
        return token['raw']

    def paragraph(self, token: Dict[str, Any], state: BlockState) -> str:
        text = self.render_children(token, state)
        return text + '\n\n'

    def heading(self, token: Dict[str, Any], state: BlockState) -> str:
        level = token['attrs']['level']
        marker = '#' * level
        text = self.render_children(token, state)
        self.anki.enterScope(text , level)
        return marker + ' ' + text + '\n\n'

    def thematic_break(self, token: Dict[str, Any], state: BlockState) -> str:
        return '***\n\n'

    def block_text(self, token: Dict[str, Any], state: BlockState) -> str:
        return self.render_children(token, state) + '\n'

    def block_code(self, token: Dict[str, Any], state: BlockState) -> str:
        attrs = token.get('attrs', {})
        info = attrs.get('info', '')
        code = token['raw']
        if code and code[-1] != '\n':
            code += '\n'

        marker = token.get('marker')
        if not marker:
            marker = _get_fenced_marker(code)
        return marker + info + '\n' + code + marker + '\n\n'

    def block_quote(self, token: Dict[str, Any], state: BlockState) -> str:
        text = indent(self.render_children(token, state), '> ')
        return text + '\n\n'

    def block_html(self, token: Dict[str, Any], state: BlockState) -> str:
        return token['raw'] + '\n\n'

    def block_error(self, token: Dict[str, Any], state: BlockState) -> str:
        return ''
    def _render_list_item(self, parent, item, state):
        leading = parent['leading']
        text = ''
        for tok in item['children']:
            if tok['type'] == 'list':
                tok['parent'] = parent
            elif tok['type'] == 'blank_line':
                continue
            text += self.render_token(tok, state)

        lines = text.splitlines()
        text = (lines[0] if lines else '') + '\n'
        self.anki.appendAttr(lines[0] if lines else '')
        prefix = ' ' * len(leading)
        for line in lines[1:]:
            if line:
                text += prefix + line + '\n'
            else:
                text += '\n'
        return leading + text
    def _render_ordered_list(self, token, state):
        attrs = token['attrs']
        start = attrs.get('start', 1)
        for item in token['children']:
            leading = str(start) + token['bullet'] + ' '
            parent = {
                'leading': leading,
                'tight': token['tight'],
            }
            yield self._render_list_item(parent, item, state)
            start += 1
    def _render_unordered_list(self, token, state):
        parent = {
            'leading': token['bullet'] + ' ',
            'tight': token['tight'],
        }
        for item in token['children']:
            yield self._render_list_item(parent, item, state)
    def list(self, token: Dict[str, Any], state: BlockState) -> str:
        attrs = token['attrs']
        if attrs['ordered']:
            children = self._render_ordered_list(token, state)
        else:
            children = self._render_unordered_list(token, state)

        text = ''.join(children)
        parent = token.get('parent')
        if parent:
            if parent['tight']:
                return text
            return text + '\n'
        return text + '\n'