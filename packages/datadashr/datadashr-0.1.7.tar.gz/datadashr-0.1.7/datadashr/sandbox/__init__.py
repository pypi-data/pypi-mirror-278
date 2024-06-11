import ast
import astor
import pandas as pd
import contextlib
from RestrictedPython import compile_restricted
from RestrictedPython.Guards import safe_builtins, guarded_iter_unpack_sequence
from RestrictedPython.Eval import default_guarded_getattr, default_guarded_getitem, default_guarded_getiter
from datadashr.config import *


class RemoveMethods(ast.NodeTransformer):
    def __init__(self, methods_to_remove):
        self.methods_to_remove = methods_to_remove

    def visit_Expr(self, node):
        # Check if this is a call to one of the methods to remove
        if (isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name)
                and node.value.func.id in self.methods_to_remove):
            return None
        return node


class Sandbox:
    """
    A class that provides a sandboxed environment for executing Python code.
    """

    def __init__(self, verbose=False):
        self._allowed_imports = {}
        self.verbose = verbose
        self.metods_to_remove = ['print', 'input', 'open', 'exec', 'eval', 'compile', 'execfile', 'globals', 'locals']

    def allow_import(self, module_name):
        """
        Allow importing a module in the sandbox
        :param module_name:
        :return:
        """
        with contextlib.suppress(ImportError):
            module = __import__(module_name)
            self._allowed_imports[module_name] = module

    @staticmethod
    def remove_methods(source_code, methods_to_remove):
        tree = ast.parse(source_code)
        transformer = RemoveMethods(methods_to_remove)
        cleaned_tree = transformer.visit(tree)
        return astor.to_source(cleaned_tree)

    def execute(self, code, local_vars=None):
        """
        Execute the code in the sandbox
        :param code: The code to be executed.
        :param local_vars: Local variables to be passed to the execution context.
        :return: Local variables after execution, or error information.
        """
        if local_vars is None:
            local_vars = {}

        allowed_builtins = safe_builtins
        # Add __builtins__, __import__, and allowed imports to the globals
        restricted_globals = {"__builtins__": allowed_builtins}
        restricted_globals |= self._allowed_imports

        builtin_mappings = {
            "__import__": __import__,
            "_getattr_": default_guarded_getattr,
            "_getitem_": default_guarded_getitem,
            "_getiter_": default_guarded_getiter,
            "_iter_unpack_sequence_": guarded_iter_unpack_sequence,
            "list": list,
            "set": set,
            "pd": pd,
        }

        series_methods = [
            "sum", "mean", "any", "argmax", "argmin", "count", "cumsum", "cumprod", "diff",
            "dropna", "fillna", "head", "idxmax", "idxmin", "last", "max", "min", "notna",
            "prod", "quantile", "rename", "round", "tail", "to_frame", "to_list", "to_numpy",
            "to_string", "unique", "sort_index", "sort_values", "aggregate"
        ]

        builtin_mappings |= {
            method: getattr(pd.Series, method) for method in series_methods
        }

        restricted_globals["__builtins__"].update(builtin_mappings)

        # remove methods from the code
        code = self.remove_methods(code, self.metods_to_remove)

        byte_code = compile_restricted(source=code, filename='<inline>', mode='exec')
        if self.verbose:
            logger.info(f"Executing the following code in the sandbox:\n{code}")

        try:
            # Execute the restricted code
            exec(byte_code, restricted_globals, local_vars)
        except Exception as e:
            if self.verbose:
                logger.error(f"Error during code execution: {str(e)}")
            local_vars = {'error': str(e)}
            return local_vars

        return local_vars
