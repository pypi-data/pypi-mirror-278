from ast import (
    AST,
    Assign,
    Attribute,
    Constant,
    Dict,
    List,
    Module,
    Name,
    NodeVisitor,
    UnaryOp,
)
from collections.abc import Mapping, Sequence
from types import GeneratorType
from typing import Any, Literal

from .error import CompileError


type PythonData = str
type ConstantValue = str | int | float | bool | Literal[None]


class Compiler(NodeVisitor):
    '''
    Compile ASTs to Python data structures.
    Effectively does the same as `eval()`.
    '''
    _EXPR_PLACEHOLDER = '_EXPR_PLACEHOLDER'

    def compile(self, node: AST) -> PythonData:
        '''
        Compile an AST, converting it to an equivalent Python data
        structure.
        Effectively does the same as `eval()`.
        '''
        return self.visit(node)

    def visit(self, node: AST) -> PythonData:
        '''
        Use a stack and generators to overcome Python's recursion limit.
        Credit to Dave Beazley (2014).
        '''
        stack = [self.genvisit(node)]
        result = None
        while stack:
            try:
                node = stack[-1].send(result)
                stack.append(self.genvisit(node))
                result = None
            except StopIteration as e:
                stack.pop()
                result = e.value
        return result

    def genvisit(self, node: AST) -> PythonData:
        '''
        Use generators to overcome Python's recursion limit.
        Credit to Dave Beazley (2014).
        '''
        name = 'visit_' + type(node).__name__
        result = getattr(self, name)(node)
        if isinstance(result, GeneratorType):
            result = (yield from result)
        return result

    def visit_Assign(self, node: Assign) -> dict:
        target = (yield (node.targets[-1]))
        value = (yield (node.value))
        if not isinstance(target, str):
            # `target` is an attribute turned into a nested dict
            return self._run_nested_update({}, target, value)
        return {target: value}

    def visit_Attribute(self, node: Attribute) -> dict:
        attrs = self._nested_attr_to_dict(node)
        new_d = self._EXPR_PLACEHOLDER
        for attr in attrs:
            new_d = {attr: new_d}
        return new_d

    @staticmethod
    def _nested_attr_to_dict(
        node: Attribute | Name,
        attrs: Sequence[str] = []
    ) -> list[str]:
        '''
        Convert nested :class:`Attribute`s to a list of attr names.

        :param node: The Attribute to convert
        :type node: :class:`Attribute` | :class:`Name`

        :param attrs: A list of preexisting attribute names
        :type attrs: :class:`Sequence`[:class:`str`]
        '''
        while not isinstance(node, Name):
            if not attrs:
                # A new nested Attribute.
                attrs = [node.attr]
            elif isinstance(node, Attribute):
                attrs.append(node.attr)
            node = node.value

        attrs.append(node.id)
        return attrs

    def visit_Constant(self, node: Constant) -> ConstantValue:
        return node.value

    def _run_nested_update(
        self,
        orig: Mapping | Any,
        upd: Mapping,
        assign: Any = {}
    ) -> dict:
        '''
        Merge two dicts and properly give them their innermost values.
        Use generators and a stack to bypass the Python recursion limit.
        Credit to Dave Beazley (2014).

        :param orig: The original dict
        :type orig: :class:`dict` | :class:`Any`

        :param upd: A dict that updates `orig`
        :type upd: :class:`dict`

        :param assign: A value that will be stored in the innermost dict,
            defaults to ``{}`` for continued attribute parsing.
        :type assign: :class:`Any`
        '''
        stack = [self._nested_update(orig, upd, assign)]
        result = None
        while stack:
            try:
                args = stack[-1].send(result)
                stack.append(self._nested_update(*args))
                result = None
            except StopIteration as e:
                stack.pop()
                result = e.value
        return result

    def _nested_update(
        self,
        orig: dict | Any,
        upd: dict,
        assign: Any = {}
    ) -> dict:
        '''
        Merge two dicts and properly give them their innermost values.
        Use generators and a stack to bypass the Python recursion limit.
        Credit to Dave Beazley (2014).

        :param orig: The original dict
        :type orig: :class:`dict` | :class:`Any`

        :param upd: A dict that updates `orig`
        :type upd: :class:`dict`

        :param assign: A value that will be stored in the innermost dict,
            defaults to ``{}`` for continued attribute parsing.
        :type assign: :class:`Any`
        '''
        for k, v in upd.items():
            if v is self._EXPR_PLACEHOLDER:
                v = assign
            # We cannot use Mapping because its instance check is recursive.
            if not isinstance(orig, dict):
                # Replace the old value with the new:
                return upd

            if isinstance(v, dict):
                # Give parameters to the generator runner:
                updated = (yield (orig.get(k, {}), v, assign))
                if isinstance(updated, GeneratorType):
                    updated = (yield from updated)
                orig[k] = updated
            else:
                orig[k] = v
        return orig

    def visit_Dict(self, node: Dict) -> dict[str]:
        new_d = {}
        for key, val in zip(node.keys, node.values):
            target = (yield key)
            value = (yield val)
            if isinstance(target, dict):
                # An Attribute
                new_d = self._run_nested_update(new_d, target, value)
            else:
                # An assignment
                new_d.update({target: value})
        return new_d

    def visit_List(self, node: List) -> list:
        l = []
        for e in node.elts:
            l.append((yield e))
        return l

    def visit_Module(self, node: Module) -> PythonData:
        config = {}
        for n in node.body:
            assignment = (yield n)
            if isinstance(n, Assign):
                target_node = n.targets[0]
                # Handle dict updates made using attributes:
                if isinstance(target_node, Attribute):
                    (target_name, new) ,= assignment.items()
                    if target_name in config and isinstance(new, dict):
                        old = config[target_name]
                        updated = self._run_nested_update(old, new)
                        assignment = {target_name: updated}
            config.update(assignment)
        return config
        # return [{target: value} for target, value in config.items()]

    def visit_Name(self, node: Name) -> str:
        return node.id

    def visit_UnaryOp(self, node: UnaryOp) -> AST:
        op = node.op
        operand = (yield node.operand)
        try:
            if op == '-':
                return -operand
            elif op == '+':
                return abs(operand)
            elif op == '!':
                return (not operand)
        except TypeError:
            typ = type(operand).__qualname__
            # typ = type(node.operand).__qualname__
            msg = f"Bad operand type for unary {op!r}: {typ!r}"
            raise CompileError.hl_error(node._token, msg)


