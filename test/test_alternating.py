#!/usr/bin/env python
# module TEST_EMDS

import unittest
import numpy as np
from test_common import BaseCommon

from pylocus.point_set import PointSet
from pylocus.algorithms import reconstruct_dwmds, reconstruct_acd


def call_method(edm, X0, tol, method=''):
    if method == 'ACD':
        print('TestAlternating:call_method',method)
        Xhat, costs = reconstruct_acd(edm, X0=X0, print_out=False, tol=tol)
    elif method == 'dwMDS':
        print('TestAlternating:call_method',method)
        Xhat, costs = reconstruct_dwmds(edm, X0=X0, n=1, print_out=False, tol=tol)
    return Xhat, costs


class TestAlternating(BaseCommon.TestAlgorithms):
    def setUp(self):
        print('TestAlternating:setUp')
        BaseCommon.TestAlgorithms.setUp(self)
        self.n_it = 10
        self.eps = 1e-8
        self.methods = ['dwMDS', 'ACD']

    def create_points(self, N=10, d=3):
        print('TestAlternating:create_points')
        self.pts = PointSet(N, d)
        self.pts.set_points('normal')
        self.X0 = self.pts.points.copy() + \
            np.random.normal(scale=self.eps*0.01, size=self.pts.points.shape)

    def call_method(self, method=''):
        Xhat, __ = call_method(self.pts.edm, X0=self.X0, tol=self.eps, method=method)
        return Xhat

    def test_decreasing_cost(self):
        self.create_points()
        for method in self.methods:
            Xhat, costs = call_method(self.pts.edm, X0=self.X0, tol=self.eps, method=method)
            cprev = np.inf
            for c in costs:
                self.assertTrue(c <= cprev + self.eps,
                                'c: {}, cprev:{}'.format(c, cprev))
                cprev = c


if __name__ == "__main__":
    unittest.main()
