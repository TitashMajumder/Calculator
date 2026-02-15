import ast, math, operator

class ExpressionEval:
     ALLOWED_OPERATORS = {
          ast.Add: operator.add, ast.Sub: operator.sub,
          ast.Mult: operator.mul, ast.Div: operator.truediv,
          ast.Mod: operator.mod, ast.Pow: operator.pow,
     }

     ALLOWED_FUNCTIONS = {
          'sin' : math.sin, 'cos' : math.cos, 'tan' : math.tan,
          'sqrt' : math.sqrt, 'log' : math.log10, 'ln' : math.log,
          'pi' : math.pi, 'e' : math.e, 'factorial' : math.factorial,
          'abs' : abs, 'rad' : math.radians, 'mod' : operator.mod,
     }

     def safe_eval(self, expr):
          def _eval(node):
               if isinstance(node, ast.Expression):
                    return _eval(node.body)
               elif isinstance(node, ast.BinOp):
                    left = _eval(node.left)
                    right = _eval(node.right)
                    op_type = type(node.op)
                    if op_type in self.ALLOWED_OPERATORS:
                         return self.ALLOWED_OPERATORS[op_type](left, right)
                    else:
                         raise ValueError("Unsupported operator")
               elif isinstance(node, ast.Name):
                    if node.id in self.ALLOWED_FUNCTIONS:
                         return self.ALLOWED_FUNCTIONS[node.id]
                    raise ValueError(f"Name {node.id} not allowed")
               elif isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name) and node.func.id in self.ALLOWED_FUNCTIONS:
                         arg = _eval(node.args[0])
                         return self.ALLOWED_FUNCTIONS[node.func.id](arg)
                    raise ValueError("Function not allowed")
               elif isinstance(node, ast.Constant):
                    if isinstance(node.value, (int, float)):
                         return node.value
                    else:
                         raise ValueError("Invalid constant")
               else:
                    raise ValueError("Invalid expression")
          tree = ast.parse(expr, mode='eval')
          return _eval(tree)