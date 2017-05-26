# -*- coding: utf-8 -*-
import helpers

import pyfvm
from pyfvm.form_language import integrate, n_dot, n_dot_grad, dS, dV, Boundary

import pyamg
import meshzoo
from sympy import pi, sin, cos, Matrix
import voropy


def exact_sol(x):
    return sin(pi*x[0]) * sin(pi*x[1]) * sin(pi*x[2])


class Convection(object):
    def apply(self, u):
        a0 = 2
        a1 = 1
        a2 = 3
        a = Matrix([a0, a1, a2])
        return integrate(lambda x: -n_dot_grad(u(x)) + n_dot(a)*u(x), dS) \
            - integrate(
                  lambda x:
                  3*pi**2 * sin(pi*x[0]) * sin(pi*x[1]) * sin(pi*x[2]) +
                  a0 * pi * cos(pi*x[0]) * sin(pi*x[1]) * sin(pi*x[2]) +
                  a1 * pi * sin(pi*x[0]) * cos(pi*x[1]) * sin(pi*x[2]) +
                  a2 * pi * sin(pi*x[0]) * sin(pi*x[1]) * cos(pi*x[2]),
                  dV
                  )

    def dirichlet(self, u):
        return [
            (lambda x: u(x) - exact_sol(x), Boundary())
            ]


def get_mesh(k):
    n = 2**(k+1)
    vertices, cells = meshzoo.cube(
            0.0, 1.0,
            0.0, 1.0,
            0.0, 1.0,
            n+1, n+1, n+1
            )
    return voropy.mesh_tetra.MeshTetra(vertices, cells, mode='algebraic')


def solve(verbose=False):
    def solver(mesh):
        matrix, rhs = pyfvm.discretize_linear(Convection(), mesh)
        ml = pyamg.smoothed_aggregation_solver(matrix)
        u = ml.solve(rhs, tol=1e-10)
        return u

    return helpers.perform_convergence_tests(
        solver,
        exact_sol,
        get_mesh,
        range(4),
        verbose=verbose
        )


def test():
    H, error_norm_1, error_norm_inf, order_1, order_inf = solve()
    expected_order = 2
    tol = 1.0e-1
    assert order_1[-1] > expected_order - tol
    assert order_inf[-1] > expected_order - tol
    return


if __name__ == '__main__':
    H, error_norm_1, error_norm_inf, order_1, order_inf = solve(verbose=True)
    helpers.show_error_data(H, error_norm_1, error_norm_inf)