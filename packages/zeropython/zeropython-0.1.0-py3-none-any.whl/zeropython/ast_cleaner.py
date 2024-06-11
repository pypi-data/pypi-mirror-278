import ast
from ast import NodeTransformer, parse, dump, unparse

import zeropython.report

AUTHORIZED_MODULES = set()
AUTHORIZED_BUILTINS_NAMES = {
    "int",
    "list",
    "dict",
    "bool",
    "str",
    "float",
    "tuple",
    "type",
    "Ellipsis",
}
FORBIDDEN_BUILTINS = {
    "ArithmeticError",
    "AssertionError",
    "AttributeError",
    "BaseException",
    "BlockingIOError",
    "BrokenPipeError",
    "BufferError",
    "BytesWarning",
    "ChildProcessError",
    "ConnectionAbortedError",
    "ConnectionError",
    "ConnectionRefusedError",
    "ConnectionResetError",
    "DeprecationWarning",
    "EOFError",
    "Ellipsis",
    "EncodingWarning",
    "EnvironmentError",
    "Exception",
    "False",
    "FileExistsError",
    "FileNotFoundError",
    "FloatingPointError",
    "FutureWarning",
    "GeneratorExit",
    "IOError",
    "ImportError",
    "ImportWarning",
    "IndentationError",
    "IndexError",
    "InterruptedError",
    "IsADirectoryError",
    "KeyError",
    "KeyboardInterrupt",
    "LookupError",
    "MemoryError",
    "ModuleNotFoundError",
    "NameError",
    "None",
    "NotADirectoryError",
    "NotImplemented",
    "NotImplementedError",
    "OSError",
    "OverflowError",
    "PendingDeprecationWarning",
    "PermissionError",
    "ProcessLookupError",
    "RecursionError",
    "ReferenceError",
    "ResourceWarning",
    "RuntimeError",
    "RuntimeWarning",
    "StopAsyncIteration",
    "StopIteration",
    "SyntaxError",
    "SyntaxWarning",
    "SystemError",
    "SystemExit",
    "TabError",
    "TimeoutError",
    "True",
    "TypeError",
    "UnboundLocalError",
    "UnicodeDecodeError",
    "UnicodeEncodeError",
    "UnicodeError",
    "UnicodeTranslateError",
    "UnicodeWarning",
    "UserWarning",
    "ValueError",
    "Warning",
    "WindowsError",
    "ZeroDivisionError",
    "_",
    "__build_class__",
    "__builtins__",
    "__debug__",
    "__doc__",
    "__import__",
    "__loader__",
    "__name__",
    "__package__",
    "__spec__",
    "abs",
    "aiter",
    "all",
    "anext",
    "any",
    "ascii",
    "bin",
    "bool",
    "breakpoint",
    "bytearray",
    "bytes",
    "callable",
    "chr",
    "classmethod",
    "compile",
    "complex",
    "copyright",
    "credits",
    "delattr",
    "dict",
    "dir",
    "divmod",
    "enumerate",
    "eval",
    "exec",
    "execfile",
    "exit",
    "filter",
    "float",
    "format",
    "frozenset",
    "getattr",
    "globals",
    "hasattr",
    "hash",
    "help",
    "hex",
    "id",
    "input",
    "int",
    "isinstance",
    "issubclass",
    "iter",
    "len",
    "license",
    "list",
    "locals",
    "map",
    "max",
    "memoryview",
    "min",
    "next",
    "object",
    "oct",
    "open",
    "ord",
    "pow",
    "print",
    "property",
    "quit",
    "range",
    "repr",
    "reversed",
    "round",
    "runfile",
    "set",
    "setattr",
    "slice",
    "sorted",
    "staticmethod",
    "str",
    "sum",
    "super",
    "tuple",
    "type",
    "vars",
    "zip",
}


def is_authorized(import_: ast.Import | ast.ImportFrom) -> bool:
    """
    Function that checks if the import node is authorized
    """
    forbidden_modules = [
        alias.name for alias in import_.names if alias.name not in AUTHORIZED_MODULES
    ]
    return not forbidden_modules


class ASTCleaner(NodeTransformer):
    """
    AST visitor that deletes forbidden nodes
    """

    def __init__(self, report: zeropython.report.Report):
        self.report = report

        self.forbidden_imports = list()
        self.forbidden_from_imports = list()
        self.forbidden_func_calls = list()
        self.forbidden_method_calls = list()
        self.forbidden_func_definitions = list()
        self.forbidden_try_clauses = 0
        self.forbidden_break_statements = 0
        self.forbidden_continue_statements = 0
        self.forbidden_names = list()
        self.forbidden_for_loops = 0
        self.forbidden_list_comprehensions = 0
        self.forbidden_dict_comprehensions = 0
        self.forbidden_set_comprehensions = 0
        self.forbidden_generator_expressions = 0
        self.forbidden_yield_statements = 0
        self.forbidden_yield_from_statements = 0
        self.forbidden_raise_statements = 0
        self.forbidden_assignments = list()
        self.forbidden_assert_statements = 0
        self.forbidden_while_else_clauses = 0
        self.forbidden_global_statements = 0
        self.forbidden_nonlocal_statements = 0
        self.forbidden_class_definitions = 0
        self.forbidden_in_operators = 0
        self.forbidden_arguments = 0
        self.forbidden_attributes = list()
        self.forbidden_is_operators = 0
        self.forbidden_is_not_operators = 0
        self.forbidden_slices = 0
        self.forbidden_starred_expressions = list()
        self.forbidden_not_in_operators = 0

    @staticmethod
    def _visit_import_generic(
        node: ast.Import | ast.ImportFrom, forbidden_import_buffer: list
    ) -> ast.Import | ast.ImportFrom | None:
        if not is_authorized(node):
            forbidden_import_buffer.extend([alias.name for alias in node.names])
            return None
        return node

    def visit_Import(self, node: ast.Import) -> ast.Import | None:
        """AST visitor that deletes forbidden imports"""
        return self._visit_import_generic(node, self.forbidden_imports)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> ast.ImportFrom | None:
        """AST visitor that deletes forbidden imports from"""
        return self._visit_import_generic(node, self.forbidden_from_imports)

    def visit_Call(self, node: ast.Call) -> ast.Call | None:
        """AST visitor that deletes forbidden calls"""
        if isinstance(node.func, ast.Name) and node.func.id == "type" and len(node.args) == 3:
            self.forbidden_func_calls.append("3 args form of type")
            return None

        self.generic_visit(node)
        if not hasattr(node, "func"):
            return None
        return node

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef | None:
        """AST visitor that deletes forbidden functions"""
        if node.name in FORBIDDEN_BUILTINS:
            self.forbidden_func_definitions.append(node.name)
            return None
        self.generic_visit(node)
        return node

    def visit_Try(self, node: ast.Try) -> None:
        """AST visitor that deletes forbidden try clauses"""
        self.forbidden_try_clauses += 1
        return None

    def visit_Break(self, node: ast.Break) -> None:
        """AST visitor that deletes forbidden break statements"""
        self.forbidden_break_statements += 1
        return None

    def visit_Continue(self, node: ast.Continue) -> None:
        """AST visitor that deletes forbidden continue statements"""
        self.forbidden_continue_statements += 1
        return None

    def visit_Expr(self, node: ast.Expr) -> ast.Expr | None:
        """AST visitor that deletes forbidden expressions"""
        self.generic_visit(node)
        if not hasattr(node, "value"):
            return None
        return node

    def visit_Name(self, node: ast.Name) -> ast.Name | None:
        """AST visitor that deletes forbidden names"""
        if node.id in FORBIDDEN_BUILTINS - AUTHORIZED_BUILTINS_NAMES or node.id.endswith("_"):
            self.forbidden_names.append(node.id)
            return None
        self.generic_visit(node)
        return node

    def visit_Assign(self, node: ast.Assign) -> ast.Assign | None:
        self.generic_visit(node)
        if not hasattr(node, "value"):
            return None
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id in FORBIDDEN_BUILTINS:
                self.forbidden_assignments.append(target.id)
                return None
        return node

    def visit_For(self, node: ast.For) -> None:
        """AST visitor that deletes forbidden for loops"""
        self.forbidden_for_loops += 1
        return None

    def visit_ListComp(self, node: ast.ListComp) -> None:
        """AST visitor that deletes forbidden list comprehensions"""
        self.forbidden_list_comprehensions += 1
        return None

    def visit_DictComp(self, node: ast.DictComp) -> None:
        """AST visitor that deletes forbidden dict comprehensions"""
        self.forbidden_dict_comprehensions += 1
        return None

    def visit_SetComp(self, node: ast.SetComp) -> None:
        """AST visitor that deletes forbidden set comprehensions"""
        self.forbidden_set_comprehensions += 1
        return None

    def visit_GeneratorExp(self, node: ast.GeneratorExp) -> None:
        """AST visitor that deletes forbidden generator expressions"""
        self.forbidden_generator_expressions += 1
        return None

    def visit_Yield(self, node: ast.Yield) -> None:
        """AST visitor that deletes forbidden yield statements"""
        self.forbidden_yield_statements += 1
        return None

    def visit_YieldFrom(self, node: ast.YieldFrom) -> None:
        """AST visitor that deletes forbidden yield from statements"""
        self.forbidden_yield_from_statements += 1
        return None

    def visit_Raise(self, node: ast.Raise) -> None:
        """AST visitor that deletes forbidden raise statements"""
        self.forbidden_raise_statements += 1
        return None

    def visit_BinOp(self, node: ast.BinOp) -> ast.BinOp | None:
        """AST visitor that deletes forbidden binary operators"""
        self.generic_visit(node)
        if not hasattr(node, "right") or not hasattr(node, "left"):
            return None
        return node

    def visit_Assert(self, node: ast.Assert) -> None:
        """AST visitor that deletes forbidden assert statements"""
        self.forbidden_assert_statements += 1
        return None

    def visit_While(self, node: ast.While) -> ast.While | None:
        """AST visitor that deletes forbidden while statements"""
        if node.orelse:
            self.forbidden_while_else_clauses += 1
            node.orelse.clear()
        self.generic_visit(node)
        if not hasattr(node, "test"):
            return None
        return node

    def visit_Global(self, node: ast.Global) -> None:
        """AST visitor that deletes forbidden global statements"""
        self.forbidden_global_statements += 1
        return None

    def visit_Nonlocal(self, node: ast.Nonlocal) -> None:
        """AST visitor that deletes forbidden nonlocal statements"""
        self.forbidden_nonlocal_statements += 1
        return None

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """AST visitor that deletes forbidden class definitions"""
        self.forbidden_class_definitions += 1
        return None

    def visit_In(self, node: ast.In) -> None:
        """AST visitor that deletes forbidden in operators"""
        self.forbidden_in_operators += 1
        return None

    def visit_NotIn(self, node: ast.NotIn) -> None:
        """AST visitor that deletes forbidden not in operators"""
        self.forbidden_not_in_operators += 1
        return None

    def visit_arguments(self, node: ast.arguments) -> ast.arguments:
        """AST visitor that deletes forbidden arguments"""
        if (
            node.kwonlyargs
            or node.kw_defaults
            or node.defaults
            or node.vararg
            or node.kwarg
            or node.posonlyargs
        ):
            self.forbidden_arguments += 1
            node.kwonlyargs.clear()
            node.kw_defaults.clear()
            node.defaults.clear()
            node.posonlyargs.clear()
            node.vararg = None
            node.kwarg = None
        return node

    def visit_Attribute(self, node: ast.Attribute) -> None:
        """AST visitor that deletes forbidden attributes"""
        self.forbidden_attributes.append(node.attr)
        return None

    def visit_Is(self, node: ast.Is) -> None:
        """AST visitor that deletes forbidden is operators"""
        self.forbidden_is_operators += 1
        return None

    def visit_IsNot(self, node: ast.IsNot) -> None:
        """AST visitor that deletes forbidden is not operators"""
        self.forbidden_is_not_operators += 1
        return None

    def visit_Slice(self, node: ast.Slice) -> None:
        """AST visitor that deletes forbidden slices"""
        self.forbidden_slices += 1
        return None

    def visit_Subscript(self, node: ast.Subscript) -> ast.Subscript | None:
        """AST visitor that deletes forbidden subscripts"""
        self.generic_visit(node)
        if not hasattr(node, "slice"):
            return None
        return node

    def visit_Compare(self, node: ast.Compare) -> ast.Compare | None:
        """AST visitor that deletes forbidden comparisons"""
        self.generic_visit(node)
        if not hasattr(node, "left"):
            return None
        return node

    def visit_Starred(self, node: ast.Starred) -> None:
        """AST visitor that deletes forbidden starred expressions"""
        self.forbidden_starred_expressions += 1
        return None

    def fill_report(self) -> None:
        """Fills the report with the results of the analysis"""
        buffer_analysis = [
            (self.forbidden_imports, "Forbidden imports:"),
            (self.forbidden_from_imports, "Forbidden imports from:"),
            (self.forbidden_func_calls, "Forbidden function calls:"),
            (self.forbidden_method_calls, "Forbidden method calls:"),
            (self.forbidden_func_definitions, "Forbidden function definitions:"),
            (self.forbidden_names, "Forbidden names:"),
            (self.forbidden_assignments, "Forbidden assignments:"),
            (self.forbidden_attributes, "Forbidden attributes:"),
            (self.forbidden_starred_expressions, "Forbidden starred expressions:"),
        ]

        for buffer, msg in buffer_analysis:
            if buffer:
                self.report.add_note(msg)

        counter_analysis = [
            (self.forbidden_try_clauses, f"Forbidden try clauses: {self.forbidden_try_clauses}"),
            (
                self.forbidden_break_statements,
                f"Forbidden break statements: {self.forbidden_break_statements}",
            ),
            (
                self.forbidden_continue_statements,
                f"Forbidden continue statements: {self.forbidden_continue_statements}",
            ),
            (self.forbidden_for_loops, f"Forbidden for loops: {self.forbidden_for_loops}"),
            (
                self.forbidden_list_comprehensions,
                f"Forbidden list comprehensions: {self.forbidden_list_comprehensions}",
            ),
            (
                self.forbidden_dict_comprehensions,
                f"Forbidden dict comprehensions: {self.forbidden_dict_comprehensions}",
            ),
            (
                self.forbidden_set_comprehensions,
                f"Forbidden set comprehensions: {self.forbidden_set_comprehensions}",
            ),
            (
                self.forbidden_generator_expressions,
                f"Forbidden generator expressions: {self.forbidden_generator_expressions}",
            ),
            (
                self.forbidden_yield_statements,
                f"Forbidden yield statements: {self.forbidden_yield_statements}",
            ),
            (
                self.forbidden_yield_from_statements,
                f"Forbidden yield from statements: {self.forbidden_yield_from_statements}",
            ),
            (
                self.forbidden_raise_statements,
                f"Forbidden raise statements: {self.forbidden_raise_statements}",
            ),
            (
                self.forbidden_assert_statements,
                f"Forbidden assert statements: {self.forbidden_assert_statements}",
            ),
            (
                self.forbidden_while_else_clauses,
                f"Forbidden while else clauses: {self.forbidden_while_else_clauses}",
            ),
            (
                self.forbidden_global_statements,
                f"Forbidden global statements: {self.forbidden_global_statements}",
            ),
            (
                self.forbidden_nonlocal_statements,
                f"Forbidden nonlocal statements: {self.forbidden_nonlocal_statements}",
            ),
            (self.forbidden_in_operators, f"Forbidden in operator: {self.forbidden_in_operators}"),
            (self.forbidden_arguments, f"Forbidden arguments: {self.forbidden_arguments}"),
            (self.forbidden_is_operators, f"Forbidden is operator: {self.forbidden_is_operators}"),
            (
                self.forbidden_is_not_operators,
                f"Forbidden is not operator: {self.forbidden_is_not_operators}",
            ),
            (self.forbidden_slices, f"Forbidden slices: {self.forbidden_slices}"),
            (
                self.forbidden_class_definitions,
                f"Forbidden class definitions: {self.forbidden_class_definitions}",
            ),
            (
                self.forbidden_not_in_operators,
                f"Forbidden not in operator: {self.forbidden_not_in_operators}",
            ),
        ]
        for counter, msg in counter_analysis:
            if counter:
                self.report.add_note(msg)


def ast_clean(code: str, report: zeropython.report.Report) -> tuple[ast.AST | None, zeropython.report.Report]:
    """
    Function that return the cleaned code and the report.
    """
    try:
        original_node = parse(code)
    except Exception as e:
        report.add_note(f"Parse error: {e}")
        return None, report
    # print(dump(original_node, indent=4))
    cleaner = ASTCleaner(report)
    cleaned_node = cleaner.visit(original_node)
    # print('=' * 80)
    # print(dump(cleaned_node, indent=4))
    # print('=' * 80)
    # print(unparse(cleaned_node))
    cleaner.fill_report()
    try:
        return cleaned_node, report
    except Exception as e:
        report.add_note(f"Unparse error: {e}")
        return None, report
