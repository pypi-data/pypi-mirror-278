import ast

class SafeEval(ast.NodeVisitor):
    def __init__(self):
        self.allowed_functions = ['compare', 'regexp']
        self.allowed_operators = [ast.And, ast.Or, ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE]

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id in self.allowed_functions:
            self.generic_visit(node)
            return node
        raise ValueError("Function not allowed")

    def visit_BinOp(self, node):
        if isinstance(node.op, self.allowed_operators):
            self.generic_visit(node)
            return node
        raise ValueError("Operator not allowed")

    def visit_Name(self, node):
        if node.id == 'data' and isinstance(node.ctx, ast.Load):
            return node
        print(node.id)
        raise ValueError("Variable not allowed")

    def visit_Import(self, node):
        raise ValueError("Import not allowed")

    def visit_ImportFrom(self, node):
        raise ValueError("Import from not allowed")

    def visit_Expr(self, node):
        if not isinstance(node.value, (ast.Call, ast.BinOp, ast.Name, ast.Subscript)):
            raise ValueError("Expression not allowed")
        self.generic_visit(node)
        return node

    def visit_Load(self, node):
        return node

    def generic_visit(self, node):
        if isinstance(node, ast.AST):
            for field in node._fields:
                if isinstance(getattr(node, field), list):
                    for item in getattr(node, field):
                        if isinstance(item, ast.AST):
                            self.visit(item)
                elif isinstance(getattr(node, field), ast.AST):
                    self.visit(getattr(node, field))

def safe_condition_eval(expr, data):
    tree = ast.parse(expr, mode='eval')
    SafeEval().visit(tree)
    try:
        return eval(compile(tree, '', 'eval'), {'data': data})
    except Exception as e:
        print(e)
        return None

if __name__ == "__main__":
    data = {'platform': 'slack', 'event_id': '1717004222.968299', 'user': 'U06UFES01RR', 'user_friendly_name': 'Dev Singh', 'team': 'T06U11UCK0F', 'channel': 'C0739CF73U6', 'channel_friendly_name': 'testing', 'text': '@DeplyAI test', 'ts': '1717004222.968299', 'attachments': None, 'thread_ts': None, 'thread_status': 1, 'edited': None, 'hidden': False, 'deleted': None, 'reactions': None}
    assert safe_condition_eval("'fds' in data['text'] and data['user_friendly_name'] in ['Dev Singh', 'Ishaan Singh']", data) == False
    assert safe_condition_eval("('Migration Project' in data['text'] or 'test' in data['text']) and data['user_friendly_name'] in ['Dev Singh', 'Ishaan Singh']", data) == True
    print("Tests passed!")