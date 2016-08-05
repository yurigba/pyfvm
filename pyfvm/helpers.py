# -*- coding: utf-8 -*-
#
import sympy


def split_affine_linear_nonlinear(expr, variables):
    if isinstance(expr, float):
        return expr, 0, 0

    input_is_list = True
    if not isinstance(variables, list):
        input_is_list = False
        variables = [variables]

    # See <https://github.com/sympy/sympy/issues/11475> on why we need expand()
    # here.
    affine = expr.expand()
    linear = []
    for var in variables:
        linear.append(sympy.diff(expr, var).coeff(var, 0))
        affine = affine.coeff(var, 0)

    # The rest is nonlinear
    nonlinear = expr - affine
    for var, coeff in zip(variables, linear):
        nonlinear -= var * coeff
    nonlinear = sympy.simplify(nonlinear)

    if not input_is_list:
        assert len(linear) == 1
        linear = linear[0]

    return affine, linear, nonlinear


def replace_nosh_functions(expr):
    fks = []
    if isinstance(expr, float) or isinstance(expr, int):
        pass
    else:
        function_vars = []
        for f in expr.atoms(sympy.Function):
            if hasattr(f, 'nosh'):
                function_vars.append(f)

        for function_var in function_vars:
            # Replace all occurences of u(x) by u[k] (the value at the control
            # volume center)
            f = sympy.IndexedBase('%s' % function_var.func)
            k = sympy.Symbol('k')
            try:
                expr = expr.subs(function_var, f[k])
            except AttributeError:
                # 'int' object has no attribute 'subs'
                pass
            fks.append(f[k])

    return expr, fks
