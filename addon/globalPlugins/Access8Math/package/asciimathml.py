# Copyright (c) 2010-2011, Gabriele Favalessa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function

from itertools import chain

import re
import sys

from xml.etree.ElementTree import Element, tostring

__all__ = ['parse']

Element_ = Element
AtomicString_ = lambda s: s

NUMBER_RE = re.compile(r'-?(\d+\.(\d+)?|\.?\d+)')
QUOTED_STRING_RE = re.compile(r'"([^"]*)"')

def text_check(text):
    py2str = (sys.version_info.major == 2 and isinstance(text, basestring))
    py3str = (sys.version_info.major >= 3 and isinstance(text, str))

    return (py3str or py2str)

def element_factory(tag, text=None, *children, **attrib):
    element = Element_(tag, **attrib)

    if not text is None:
        if text_check(text):
            element.text = AtomicString_(text)
        else:
            children = (text, ) + children

    for child in children:
        element.append(child)

    return element

def strip_parens(n):
    if n.tag == 'mrow':
        if n[0].get('_opening', False):
            del n[0]

        if n[-1].get('_closing', False):
            del n[-1]

    return n

def strip_tags(n):
    return ''.join(e.text for e in n)

def is_enclosed_in_parens(n):
    return n.tag == 'mrow' and n[0].get('_opening', False) and n[-1].get('_closing', False)

def binary(operator, operand_1, operand_2, swap=False, o1_attr=None, o2_attr=None):
    operand_1 = strip_parens(operand_1)
    operand_2 = strip_parens(operand_2)

    if swap:
        operand_1, operand_2 = operand_2, operand_1

    if o1_attr is None:
        operator.append(operand_1)
    else:
        operator.attrib[o1_attr] = strip_tags(operand_1)

    if o2_attr is None:
        operator.append(operand_2)
    else:
        operator.attrib[o2_attr] = strip_tags(operand_2)

    return operator

def unary(operator, operand, swap=False, rewrite_lr=None):
    operand = strip_parens(operand)

    if rewrite_lr is None:
        rewrite_lr = []

    if rewrite_lr:
        opener = element_factory("mo", rewrite_lr[0], _opening=True)
        closer = element_factory("mo", rewrite_lr[1], _closing=True)

        if is_enclosed_in_parens(operand):
            operand[0] = opener
            operand[-1] = closer
            return operand
        else:
            operator.append(opener)
            operator.append(operand)
            operator.append(closer)
    else:
        if swap:
            operator.insert(0, operand)
        else:
            operator.append(operand)

    return operator

def frac(num, den):
    return element_factory('mfrac', strip_parens(num), strip_parens(den))

def sub(base, subscript):
    subscript = strip_parens(subscript)

    if base.tag in ('msup', 'mover'):
        children = base.getchildren()
        n = element_factory(
            'msubsup' if base.tag == 'msup' else 'munderover',
            children[0], subscript, children[1]
        )
    else:
        n = element_factory(
            'munder' if base.get('_underover', False) else 'msub',
            base, subscript
        )

    return n

def sup(base, superscript):
    superscript = strip_parens(superscript)

    if base.tag in ('msub', 'munder'):
        children = base.getchildren()
        n = element_factory(
            'msubsup' if base.tag == 'msub' else 'munderover',
            children[0], children[1], superscript
        )
    else:
        n = element_factory(
            'mover' if base.get('_underover', False) else 'msup',
            base, superscript
        )

    return n

def parse(s, element=Element, atomicstring=lambda s: s):
    """
    Translates from ASCIIMathML (an easy to type and highly readable way to
    represent math formulas) into MathML (a w3c standard directly displayable by
    some web browsers).

    The function `parse()` generates a tree of elements:

    >>> import asciimathml
    >>> asciimathml.parse('sqrt 2')
    <Element math at b76fb28c>

    The tree can then be manipulated using the standard python library.  For
    example we can generate its string representation:

    >>> from xml.etree.ElementTree import tostring
    >>> tostring(asciimathml.parse('sqrt 2'))
    '<math><mstyle><msqrt><mn>2</mn></msqrt></mstyle></math>'
    """

    global Element_, AtomicString_

    Element_ = element
    AtomicString_ = atomicstring

    s, nodes = parse_exprs(s)
    remove_invisible(nodes)
    nodes = map(remove_private, nodes)

    return element_factory('math', element_factory('mstyle', *nodes))

delimiters = {'{': '}', '(': ')', '[': ']'}

def parse_string(s):
    opening = s[0]

    if opening in delimiters:
        closing = delimiters[opening]
        end = s.find(closing)

        text = s[1:end]
        s = s[end+1:]

        children = []
        if text.startswith(' '):
            children.append(element_factory('mspace', width='1ex'))
        children.append(element_factory('mtext', text))
        if text.endswith(' '):
            children.append(element_factory('mspace', width='1ex'))

        return s, element_factory('mrow', *children)
    else:
        s, text = parse_m(s)
        return s, element_factory('mtext', text)


tracing_level = 0
def trace_parser(p):
    """
    Decorator for tracing the parser.

    Use it to decorate functions with signature:

      string -> (string, nodes)

    and a trace of the progress made by the parser will be printed to stderr.

    Currently parse_exprs(), parse_expr() and parse_m() have the right signature.
    """

    def nodes_to_string(n):
        if isinstance(n, list):
            result = '[ '
            for m in map(nodes_to_string, n):
                result += m
                result += ' '
            result += ']'

            return result
        else:
            try:
                return tostring(remove_private(copy(n)))
            except Exception as e:
                return n

    def print_trace(*args):
        sys.stderr.write("    " * tracing_level)
        for arg in args:
            sys.stderr.write(str(arg))
            sys.stderr.write(' ')
        sys.stderr.write('\n')
        sys.stderr.flush()

    def wrapped(s, *args, **kwargs):
        global tracing_level

        print_trace(p.__name__, repr(s))

        tracing_level += 1
        s, n = p(s, *args, **kwargs)
        tracing_level -= 1

        print_trace("-> ", repr(s), nodes_to_string(n))

        return s, n

    return wrapped

def parse_expr(s, siblings, required=False):
    s, n = parse_m(s, required=required)

    if not n is None:
        # Being both an _opening and a _closing element is a trait of
        # symmetrical delimiters (e.g. ||).
        # In that case, act as an opening delimiter only if there is not
        # already one of the same kind among the preceding siblings.

        sym_paren = n.get('_opening', False) and n.get('_closing', False)
        prev_sib_pos = find_node_backwards(siblings, n.text)
        parens_nest = (
            n.get('_opening', False)
            and (
                not n.get('_closing', False)
                or (
                    sym_paren is (prev_sib_pos != -1)
                )
            )
        )

        if parens_nest:
            if sym_paren:
                n = element_factory('mrow', *chain(siblings[prev_sib_pos:], [n]))
                del siblings[prev_sib_pos:]
            else:
                s, children = parse_exprs(s, [n], inside_parens=True)
                n = element_factory('mrow', *children)

        if n.tag == 'mtext':
            s, n = parse_string(s)
        elif n.get('_arity', 0) == 1:
            s, m = parse_expr(s, [], True)
            n = unary(n, m, swap=n.get('_swap', False), rewrite_lr=n.get('_rewrite_lr', []))
        elif n.get('_arity', 0) == 2:
            s, m1 = parse_expr(s, [], True)
            s, m2 = parse_expr(s, [], True)
            n = binary(
                n, m1, m2,
                swap=n.get('_swap', False),
                o1_attr=n.get('_o1_attr', None),
                o2_attr=n.get('_o2_attr', None)
            )

    return s, n

def find_node(ns, text):
    for i, n in enumerate(ns):
        if n.text == text:
            return i

    return -1

def find_node_backwards(ns, text):
    for i, n in enumerate(reversed(ns)):
        if n.text == text:
            return len(ns) - (i + 1)

    return -1

def nodes_to_row(row):
    mrow = element_factory('mtr')

    nodes = row.getchildren()

    while True:
        i = find_node(nodes, ',')

        if i > 0:
            mrow.append(element_factory('mtd', *nodes[:i]))

            nodes = nodes[i+1:]
        else:
            mrow.append(element_factory('mtd', *nodes))
            break

    return mrow

def nodes_to_matrix(nodes):
    mtable = element_factory('mtable')

    for row in nodes[1:-1]:
        if row.text == ',':
            continue

        mtable.append(nodes_to_row(strip_parens(row)))

    return element_factory('mrow', nodes[0], mtable, nodes[-1])

def parse_exprs(s, nodes=None, inside_parens=False):
    if nodes is None:
        nodes = []

    inside_matrix = False

    while True:
        s, n = parse_expr(s, nodes)

        if not n is None:
            truly_closing = (
                n.get('_closing', False)
                and (
                    not n.get('_opening', False)
                    or
                    (
                        find_node_backwards(nodes, n.text) != -1
                    )
                )
            )

            neg_number = (
                n.tag == 'mrow'
                and len(n) == 2
                and n[0].text == '-'
                and n[1].tag in {'mn', 'mi'}
            )
            term_before = (
                nodes
                and nodes[-1].tag != 'mo'
            )

            if neg_number and term_before:
                nodes.extend(n)
            else:
                nodes.append(n)

            if truly_closing:
                if not inside_matrix:
                    return s, nodes
                else:
                    return s, nodes_to_matrix(nodes)

            if inside_parens and n.text == ',' and is_enclosed_in_parens(nodes[-2]):
                inside_matrix = True

            len_nodes = len(nodes)
            if len_nodes >= 3 and nodes[-2].get('_special_binary'):
                transform = nodes[-2].get('_special_binary')
                nodes[-3:] = [transform(nodes[-3], nodes[-1])]
            elif s == '' and len_nodes == 2 and nodes[-1].get('_special_binary'):
                transform = nodes[-1].get('_special_binary')
                nodes[-2:] = [transform(nodes[-2], element_factory("mo"))]

        if s == '':
            return '', nodes

def remove_private(n):
    _ks = [k for k in n.keys() if k.startswith('_') or k == 'attrib']

    for _k in _ks:
        del n.attrib[_k]

    for c in n.getchildren():
        remove_private(c)

    return n

def remove_invisible(ns, parent=None):
    for i in range(len(ns)-1, -1, -1):
        if ns[i].get('_invisible', False):
            if parent is None:
                del ns[i]
            else:
                parent.remove(ns[i])
        else:
            remove_invisible(ns[i].getchildren(), parent=ns[i])

def copy(n):
    m = element_factory(n.tag, n.text, **dict(n.items()))

    for c in n.getchildren():
        m.append(copy(c))

    return m

def parse_m(s, required=False):
    s = s.strip()

    if s == '':
        return '', element_factory('mi', u'\u25a1') if required else None

    m = QUOTED_STRING_RE.match(s)
    if m:
        text = m.group(1)

        children = []
        if text.startswith(' '):
            children.append(element_factory('mspace', width='1ex'))
        children.append(element_factory('mtext', text))
        if text.endswith(' '):
            children.append(element_factory('mspace', width='1ex'))

        return s[m.end():], element_factory(
            'mrow',
            *children
        )

    m = NUMBER_RE.match(s)

    if m:
        number = m.group(0)
        if number[0] == '-':
            return s[m.end():], element_factory(
                'mrow',
                element_factory('mo', '-'),
                element_factory('mn', number[1:])
            )
        else:
            return s[m.end():], element_factory('mn', number)

    for y in symbol_names:
        if s.startswith(y):
            n = copy(symbols[y])

            if n.get('_space', False):
                n = element_factory(
                    'mrow',
                    element_factory('mspace', width='1ex'),
                    n,
                    element_factory('mspace', width='1ex')
                )

            return s[len(y):], n

    return s[1:], element_factory('mi' if s[0].isalpha() else 'mo', s[0])

symbols = {}

symbols["alpha"] = element_factory("mi", u"\u03B1")
symbols["beta"] = element_factory("mi", u"\u03B2")
symbols["chi"] = element_factory("mi", u"\u03C7")
symbols["delta"] = element_factory("mi", u"\u03B4")
symbols["Delta"] = element_factory("mo", u"\u0394")
symbols["epsi"] = element_factory("mi", u"\u03B5")
symbols["varepsilon"] = element_factory("mi", u"\u025B")
symbols["eta"] = element_factory("mi", u"\u03B7")
symbols["gamma"] = element_factory("mi", u"\u03B3")
symbols["Gamma"] = element_factory("mo", u"\u0393")
symbols["iota"] = element_factory("mi", u"\u03B9")
symbols["kappa"] = element_factory("mi", u"\u03BA")
symbols["lambda"] = element_factory("mi", u"\u03BB")
symbols["Lambda"] = element_factory("mo", u"\u039B")
symbols["lamda"] = element_factory("mi", u"\u03BB")
symbols["Lamda"] = element_factory("mo", u"\u039B")
symbols["mu"] = element_factory("mi", u"\u03BC")
symbols["nu"] = element_factory("mi", u"\u03BD")
symbols["omega"] = element_factory("mi", u"\u03C9")
symbols["Omega"] = element_factory("mo", u"\u03A9")
symbols["phi"] = element_factory("mi", u"\u03C6")
symbols["varphi"] = element_factory("mi", u"\u03D5")
symbols["Phi"] = element_factory("mo", u"\u03A6")
symbols["pi"] = element_factory("mi", u"\u03C0")
symbols["Pi"] = element_factory("mo", u"\u03A0")
symbols["psi"] = element_factory("mi", u"\u03C8")
symbols["Psi"] = element_factory("mi", u"\u03A8")
symbols["rho"] = element_factory("mi", u"\u03C1")
symbols["sigma"] = element_factory("mi", u"\u03C3")
symbols["Sigma"] = element_factory("mo", u"\u03A3")
symbols["tau"] = element_factory("mi", u"\u03C4")
symbols["theta"] = element_factory("mi", u"\u03B8")
symbols["vartheta"] = element_factory("mi", u"\u03D1")
symbols["Theta"] = element_factory("mo", u"\u0398")
symbols["upsilon"] = element_factory("mi", u"\u03C5")
symbols["xi"] = element_factory("mi", u"\u03BE")
symbols["Xi"] = element_factory("mo", u"\u039E")
symbols["zeta"] = element_factory("mi", u"\u03B6")

symbols["*"] = element_factory("mo", u"\u22C5")
symbols["**"] = element_factory("mo", u"\u2217")
symbols["***"] = element_factory("mo", u"\u22C6")

symbols["/"] = element_factory("mo", u"/", _special_binary=frac)
symbols["^"] = element_factory("mo", u"^", _special_binary=sup)
symbols["_"] = element_factory("mo", u"_", _special_binary=sub)
symbols["//"] = element_factory("mo", u"/")
symbols["\\\\"] = element_factory("mo", u"\\")
symbols["setminus"] = element_factory("mo", u"\\")
symbols["xx"] = element_factory("mo", u"\u00D7")
symbols["|><"] = element_factory("mo", u"\u22C9")
symbols["><|"] = element_factory("mo", u"\u22CA")
symbols["|><|"] = element_factory("mo", u"\u22C8")
symbols["-:"] = element_factory("mo", u"\u00F7")
symbols["@"] = element_factory("mo", u"\u2218")
symbols["o+"] = element_factory("mo", u"\u2295")
symbols["ox"] = element_factory("mo", u"\u2297")
symbols["o."] = element_factory("mo", u"\u2299")
symbols["sum"] = element_factory("mo", u"\u2211", _underover=True)
symbols["prod"] = element_factory("mo", u"\u220F", _underover=True)
symbols["^^"] = element_factory("mo", u"\u2227")
symbols["^^^"] = element_factory("mo", u"\u22C0", _underover=True)
symbols["vv"] = element_factory("mo", u"\u2228")
symbols["vvv"] = element_factory("mo", u"\u22C1", _underover=True)
symbols["nn"] = element_factory("mo", u"\u2229")
symbols["nnn"] = element_factory("mo", u"\u22C2", _underover=True)
symbols["uu"] = element_factory("mo", u"\u222A")
symbols["uuu"] = element_factory("mo", u"\u22C3", _underover=True)

symbols["!="] = element_factory("mo", u"\u2260")
symbols[":="] = element_factory("mo", u":=")
symbols["lt"] = element_factory("mo", u"<")
symbols["gt"] = element_factory("mo", u">")
symbols["<="] = element_factory("mo", u"\u2264")
symbols["lt="] = element_factory("mo", u"\u2264")
symbols["gt="] = element_factory("mo", u"\u2265")
symbols[">="] = element_factory("mo", u"\u2265")
symbols["geq"] = element_factory("mo", u"\u2265")
symbols["-<"] = element_factory("mo", u"\u227A")
symbols["-lt"] = element_factory("mo", u"\u227A")
symbols[">-"] = element_factory("mo", u"\u227B")
symbols["-<="] = element_factory("mo", u"\u2AAF")
symbols[">-="] = element_factory("mo", u"\u2AB0")
symbols["in"] = element_factory("mo", u"\u2208")
symbols["!in"] = element_factory("mo", u"\u2209")
symbols["sub"] = element_factory("mo", u"\u2282")
symbols["sup"] = element_factory("mo", u"\u2283")
symbols["sube"] = element_factory("mo", u"\u2286")
symbols["supe"] = element_factory("mo", u"\u2287")
symbols["-="] = element_factory("mo", u"\u2261")
symbols["~="] = element_factory("mo", u"\u2245")
symbols["~~"] = element_factory("mo", u"\u2248")
symbols["prop"] = element_factory("mo", u"\u221D")

symbols["and"] = element_factory("mtext", u"and", _space=True)
symbols["or"] = element_factory("mtext", u"or", _space=True)
symbols["not"] = element_factory("mo", u"\u00AC")
symbols["=>"] = element_factory("mo", u"\u21D2")
symbols["if"] = element_factory("mo", u"if", _space=True)
symbols["<=>"] = element_factory("mo", u"\u21D4")
symbols["AA"] = element_factory("mo", u"\u2200")
symbols["EE"] = element_factory("mo", u"\u2203")
symbols["_|_"] = element_factory("mo", u"\u22A5")
symbols["TT"] = element_factory("mo", u"\u22A4")
symbols["|--"] = element_factory("mo", u"\u22A2")
symbols["|=="] = element_factory("mo", u"\u22A8")

symbols["("] = element_factory("mo", "(", _opening=True)
symbols[")"] = element_factory("mo", ")", _closing=True)
symbols["["] = element_factory("mo", "[", _opening=True)
symbols["]"] = element_factory("mo", "]", _closing=True)
symbols["{"] = element_factory("mo", "{", _opening=True)
symbols["}"] = element_factory("mo", "}", _closing=True)
symbols["|"] = element_factory("mo", u"|", _opening=True, _closing=True)
# double vertical line
symbols["||"] = element_factory("mo", u"\u2016", _opening=True, _closing=True)
symbols["(:"] = element_factory("mo", u"\u2329", _opening=True)
symbols[":)"] = element_factory("mo", u"\u232A", _closing=True)
symbols["<<"] = element_factory("mo", u"\u2329", _opening=True)
symbols[">>"] = element_factory("mo", u"\u232A", _closing=True)
symbols["{:"] = element_factory("mo", u"{:", _opening=True, _invisible=True)
symbols[":}"] = element_factory("mo", u":}", _closing=True, _invisible=True)

symbols["int"] = element_factory("mo", u"\u222B")
# symbols["dx"] = element_factory("mi", u"{:d x:}", _definition=True)
# symbols["dy"] = element_factory("mi", u"{:d y:}", _definition=True)
# symbols["dz"] = element_factory("mi", u"{:d z:}", _definition=True)
# symbols["dt"] = element_factory("mi", u"{:d t:}", _definition=True)
symbols["oint"] = element_factory("mo", u"\u222E")
symbols["del"] = element_factory("mo", u"\u2202")
symbols["grad"] = element_factory("mo", u"\u2207")
symbols["+-"] = element_factory("mo", u"\u00B1")
symbols["O/"] = element_factory("mo", u"\u2205")
symbols["oo"] = element_factory("mo", u"\u221E")
symbols["aleph"] = element_factory("mo", u"\u2135")
symbols["..."] = element_factory("mo", u"...")
symbols[":."] = element_factory("mo", u"\u2234")
symbols["/_"] = element_factory("mo", u"\u2220")
symbols["/_\\"] = element_factory("mo", u"\u25B3")
symbols["'"] = element_factory("mo", u"\u2032")
# arity of 1
symbols["tilde"] = element_factory("mover", element_factory("mo", u"~"), _arity=1, _swap=True)
symbols["\\ "] = element_factory("mo", u"\u00A0")
symbols["frown"] = element_factory("mo", u"\u2322")
symbols["quad"] = element_factory("mo", u"\u00A0\u00A0")
symbols["qquad"] = element_factory("mo", u"\u00A0\u00A0\u00A0\u00A0")
symbols["cdots"] = element_factory("mo", u"\u22EF")
symbols["vdots"] = element_factory("mo", u"\u22EE")
symbols["ddots"] = element_factory("mo", u"\u22F1")
symbols["diamond"] = element_factory("mo", u"\u22C4")
symbols["square"] = element_factory("mo", u"\u25A1")
symbols["|__"] = element_factory("mo", u"\u230A")
symbols["__|"] = element_factory("mo", u"\u230B")
symbols["|~"] = element_factory("mo", u"\u2308")
symbols["~|"] = element_factory("mo", u"\u2309")
symbols["CC"] = element_factory("mo", u"\u2102")
symbols["NN"] = element_factory("mo", u"\u2115")
symbols["QQ"] = element_factory("mo", u"\u211A")
symbols["RR"] = element_factory("mo", u"\u211D")
symbols["ZZ"] = element_factory("mo", u"\u2124")
symbols["f"] = element_factory("mi", u"f", _func=True) # sample
symbols["g"] = element_factory("mi", u"g", _func=True)

symbols["lim"] = element_factory("mo", u"lim", _underover=True)
symbols["Lim"] = element_factory("mo", u"Lim", _underover=True)
symbols["sin"] = element_factory("mrow", element_factory("mo", "sin"), _arity=1)
symbols["sin"] = element_factory("mrow", element_factory("mo", "sin"), _arity=1)
symbols["cos"] = element_factory("mrow", element_factory("mo", "cos"), _arity=1)
symbols["tan"] = element_factory("mrow", element_factory("mo", "tan"), _arity=1)
symbols["sinh"] = element_factory("mrow", element_factory("mo", "sinh"), _arity=1)
symbols["cosh"] = element_factory("mrow", element_factory("mo", "cosh"), _arity=1)
symbols["tanh"] = element_factory("mrow", element_factory("mo", "tanh"), _arity=1)
symbols["cot"] = element_factory("mrow", element_factory("mo", "cot"), _arity=1)
symbols["sec"] = element_factory("mrow", element_factory("mo", "sec"), _arity=1)
symbols["csc"] = element_factory("mrow", element_factory("mo", "csc"), _arity=1)
symbols["log"] = element_factory("mrow", element_factory("mo", "log"), _arity=1)
symbols["arcsin"] = element_factory("mrow", element_factory("mo", "arcsin"), _arity=1)
symbols["arccos"] = element_factory("mrow", element_factory("mo", "arccos"), _arity=1)
symbols["arctan"] = element_factory("mrow", element_factory("mo", "arctan"), _arity=1)
symbols["coth"] = element_factory("mrow", element_factory("mo", "coth"), _arity=1)
symbols["sech"] = element_factory("mrow", element_factory("mo", "sech"), _arity=1)
symbols["csch"] = element_factory("mrow", element_factory("mo", "csch"), _arity=1)
symbols["exp"] = element_factory("mrow", element_factory("mo", "exp"), _arity=1)

symbols["abs"] = element_factory("mrow", element_factory("mo", "abs", _invisible=True), _arity=1, _rewrite_lr=[u"|", u"|"])
symbols["norm"] = element_factory("mrow", element_factory("mo", "norm", _invisible=True), _arity=1, _rewrite_lr=[u"\u2225", u"\u2225"])
symbols["floor"] = element_factory("mrow", element_factory("mo", "floor", _invisible=True), _arity=1, _rewrite_lr=[u"\u230A", u"\u230B"])
symbols["ceil"] = element_factory("mrow", element_factory("mo", "ceil", _invisible=True), _arity=1, _rewrite_lr=[u"\u2308", u"\u2309"])

symbols["ln"] = element_factory("mrow", element_factory("mo", "ln"), _arity=1)
symbols["det"] = element_factory("mrow", element_factory("mo", "det"), _arity=1)
symbols["gcd"] = element_factory("mrow", element_factory("mo", "gcd"), _arity=1)
symbols["lcm"] = element_factory("mrow", element_factory("mo", "lcm"), _arity=1)
symbols["dim"] = element_factory("mo", u"dim")
symbols["mod"] = element_factory("mo", u"mod")
symbols["lub"] = element_factory("mo", u"lub")
symbols["glb"] = element_factory("mo", u"glb")
symbols["min"] = element_factory("mo", u"min", _underover=True)
symbols["max"] = element_factory("mo", u"max", _underover=True)

symbols["uarr"] = element_factory("mo", u"\u2191")
symbols["darr"] = element_factory("mo", u"\u2193")
symbols["rarr"] = element_factory("mo", u"\u2192")
symbols["->"] = element_factory("mo", u"\u2192")
symbols["|->"] = element_factory("mo", u"\u21A6")
symbols["larr"] = element_factory("mo", u"\u2190")
symbols["harr"] = element_factory("mo", u"\u2194")
symbols["rArr"] = element_factory("mo", u"\u21D2")
symbols["lArr"] = element_factory("mo", u"\u21D0")
symbols["hArr"] = element_factory("mo", u"\u21D4")

symbols["hat"] = element_factory("mover", element_factory("mo", u"\u005E"), _arity=1, _swap=1)
symbols["bar"] = element_factory("mover", element_factory("mo", u"\u00AF"), _arity=1, _swap=1)
symbols["vec"] = element_factory("mover", element_factory("mo", u"\u2192"), _arity=1, _swap=1)
symbols["dot"] = element_factory("mover", element_factory("mo", u"."), _arity=1, _swap=1)
symbols["ddot"] = element_factory("mover", element_factory("mo", u".."), _arity=1, _swap=1)
symbols["ul"] = element_factory("munder", element_factory("mo", u"\u0332"), _arity=1, _swap=1)
symbols["ubrace"] = element_factory("munder", element_factory("mo",  "\u23DF"), _swap=True, _arity=1)
symbols["obrace"] = element_factory("mover", element_factory("mo", "\u23DE"), _swap=True, _arity=1)

symbols["sqrt"] = element_factory("msqrt", _arity=1)
symbols["root"] = element_factory("mroot", _arity=2, _swap=True)
symbols["frac"] = element_factory("mfrac", _arity=2)

# the base is the first argument
# the second argument is where effect applies
symbols["stackrel"] = element_factory("mover", _arity=2, _swap=True)
symbols["overset"] = element_factory("mover", _arity=2, _swap=True)
symbols["underset"] = element_factory("munder", _arity=2, _swap=True)

symbols["text"] = element_factory("mtext", _arity=1)
symbols["mbox"] = element_factory("mtext", _arity=1)

# sets mathcolor attrib

symbols["color"] = element_factory("mstyle", _arity=2, _o1_attr="mathcolor")
symbols["cancel"] = element_factory("menclose", _arity=1, notation="updiagonalstrike")

# new style tags
## bold
symbols["bb"] = element_factory("mstyle", _arity=1, fontweight="bold")
symbols["mathbf"] = element_factory("mstyle", _arity=1, fontweight="bold")

## sans
symbols["sf"] = element_factory("mstyle", _arity=1, fontfamily="sans")
symbols["mathsf"] = element_factory("mstyle", _arity=1, fontfamily="sans")

## double-struck
symbols["bbb"] = element_factory("mstyle", _arity=1, mathvariant="double-struck")
symbols["mathbb"] = element_factory("mstyle", _arity=1, mathvariant="double-struck")

## script
symbols["cc"] = element_factory("mstyle", _arity=1, mathvariant="script")
symbols["mathcal"] = element_factory("mstyle", _arity=1, mathvariant="script")

## monospace
symbols["tt"] = element_factory("mstyle", _arity=1, fontfamily="monospace")
symbols["mathtt"] = element_factory("mstyle", _arity=1, fontfamily="monospace")

## fraktur
symbols["fr"] = element_factory("mstyle", _arity=1, mathvariant="fraktur")
symbols["mathfrak"] = element_factory("mstyle", _arity=1, mathvariant="fraktur")
# {input:"mbox", tag:"mtext", output:"mbox", tex:null, ttype:TEXT},
# {input:"\"",   tag:"mtext", output:"mbox", tex:null, ttype:TEXT};

symbol_names = sorted(symbols.keys(), key=lambda s: len(s), reverse=True)

def main(args=None):
    if args is None:
        args = sys.argv[1:]

    from argparse import ArgumentParser

    aparser = ArgumentParser(
        usage='Test asciimathml with different etree elements'
    )
    text_modes = aparser.add_mutually_exclusive_group()
    text_modes.add_argument(
        '-m', '--markdown',
        default=False, action='store_true',
        help="Use markdown's etree element"
    )
    text_modes.add_argument(
        '-c', '--celement',
        default=False, action='store_true',
        help="Use cElementTree's element"
    )

    aparser.add_argument(
        'text',
        nargs='+',
        help='asciimath text to turn into mathml'
    )
    args_ns = aparser.parse_args(args)

    if args_ns.markdown:
        import markdown
        try:
            element = markdown.etree.Element
        except AttributeError as e:
            element = markdown.util.etree.Element
    elif args_ns.celement:
        from xml.etree.cElementTree import Element
        element = Element
    else:
        element = Element

    print("""\
<?xml version="1.0"?>
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <meta http-equiv="Content-Type" content="application/xhtml+xml" />
        <title>ASCIIMathML preview</title>
    </head>
    <body>
""")
    result = parse(' '.join(args_ns.text), element)
    if sys.version_info.major >= 3:
        encoding = 'unicode'
    else:
        encoding = 'utf-8'
    print(tostring(result, encoding=encoding))
    print("""\
    </body>
</html>
""")

if __name__ == '__main__':
    main()
