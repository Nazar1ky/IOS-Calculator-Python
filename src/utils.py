import ast
import logging
import math
import operator

logger = logging.getLogger(__name__)


def safe_eval(s):
    def checkmath(x, *args):
        if x not in [x for x in dir(math) if "__" not in x]:
            msg = f"Unknown func {x}()"
            raise SyntaxError(msg)
        fun = getattr(math, x)
        return fun(*args)

    bin_ops = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.Call: checkmath,
        ast.BinOp: ast.BinOp,
    }

    un_ops = {
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
        ast.UnaryOp: ast.UnaryOp,
    }

    ops = tuple(bin_ops) + tuple(un_ops)

    tree = ast.parse(s, mode="eval")

    def _eval(node):
        if isinstance(node, ast.Expression):
            logger.debug("Expr")
            return _eval(node.body)
        if isinstance(node, ast.Constant):
            logger.info("Const")
            return node.value
        if isinstance(node, ast.BinOp):
            logger.debug("BinOp")
            left = _eval(node.left) if isinstance(node.left, ops) else node.left.value
            if isinstance(node.right, ops):
                right = _eval(node.right)
            else:
                right = node.right.value
            return bin_ops[type(node.op)](left, right)
        if isinstance(node, ast.UnaryOp):
            logger.debug("UpOp")
            if isinstance(node.operand, ops):
                operand = _eval(node.operand)
            else:
                operand = node.operand.value
            return un_ops[type(node.op)](operand)
        if isinstance(node, ast.Call):
            args = [_eval(x) for x in node.args]
            return checkmath(node.func.id, *args)
        msg = f"Bad syntax, {type(node)}"
        raise SyntaxError(msg)

    return _eval(tree)


if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    logger.addHandler(ch)
    assert safe_eval("1+1") == 2
    assert safe_eval("1+-5") == -4
    assert safe_eval("-1") == -1
    assert safe_eval("-+1") == -1
    assert safe_eval("(100*10)+6") == 1006
    assert safe_eval("100*(10+6)") == 1600
    assert safe_eval("2**4") == 2**4
    assert safe_eval("sqrt(16)+1") == math.sqrt(16) + 1
    assert safe_eval("1.2345 * 10") == 1.2345 * 10

    print("Tests pass")
