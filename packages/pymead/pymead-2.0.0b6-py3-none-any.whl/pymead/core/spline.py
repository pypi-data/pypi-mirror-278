import numpy as np

from pymead.core.parametric_curve import ParametricCurve
from pymead.core.bezier import Bezier


class RationalBSpline(ParametricCurve):
    """This code was produced in part by the ChatGPT bot on openai.com"""

    def get_curvature_comb(self, max_k_normalized_scale_factor, interval: int = 1):
        pass

    def __init__(self, P, knots, weights):
        self.P = np.array(P)
        self.knots = knots
        self.weights = weights
        t = np.linspace(0.0, 0.999, 101)
        curve = self.evaluate_vector(t)
        super().__init__(t=t, x=curve[:, 0], y=curve[:, 1], px=None, py=None, ppx=None, ppy=None, R=None, k=None)

    def evaluate(self, t):
        n = len(self.P) - 1
        m = len(self.knots) - 1
        p = m - n - 1

        # Find the span for the given value of t
        span = self._find_span(n, p, t)

        # Compute the basis functions
        basis_functions = self._basis_functions(span, t, p)

        # Evaluate the curve at t
        curve_point = np.zeros(self.P.shape[1])
        for i in range(p + 1):
        # for i in range(n + 1):
            curve_point += basis_functions[i] * self.P[span - p + i] * self.weights[span - p + i]
            # curve_point += self._basis_function(i, p, t) * self.P[i]

        # curve_point2 = self.de_boor(t)
        return curve_point

    def evaluate_vector(self, t_vec):
        """Evaluate the curve along a specified parameter vector"""
        points = []
        for t_val in t_vec:
            point = self.evaluate(t_val)
            points.append(point)
        return np.array([self.evaluate(t_val) for t_val in t_vec])
        # return np.array([self.de_boor(t_val) for t_val in t_vec])

    def _find_span(self, n, p, t):
        """Find the span for the given value of t"""
        # if t == self.knots[n + 1]:
        #     return n
        # low, high = p, n + 1
        # mid = (low + high) // 2
        # while t < self.knots[mid] or t >= self.knots[mid + 1]:
        #     if t < self.knots[mid]:
        #         high = mid
        #     else:
        #         low = mid
        #     mid = (low + high) // 2
        #     print(f"{mid = }")
        # return mid
        interval = 0
        for i in range(len(self.knots) - 1):
            # Modification to account for repeated knots
            if np.isclose(self.knots[i + 1] - self.knots[i], 0.0):
                continue
            if self.knots[i] <= t <= self.knots[i + 1]:
                interval = i
                break
        return interval

    # def _basis_function(self, i: int, p: int, t: float):
    #     """Implementation of the Cox-de Boor recursion formula
    #     (see `this page <https://pages.mtu.edu/~shene/COURSES/cs3621/NOTES/spline/B-spline/bspline-basis.html>`_)"""
    #
    #     def cox_de_boor_recursion(i_, p_):
    #         if p_ == 0:
    #             return 1 if self.knots[i_] <= t < self.knots[i_ + 1] else 0
    #         else:
    #             return (t - self.knots[i_]) / (self.knots[i_ + p_] - self.knots[i_]) * \
    #                    cox_de_boor_recursion(i_, p_ - 1) + \
    #                    (self.knots[i_ + p_ + 1] - t) / (self.knots[i_ + p_ + 1] - self.knots[i_ + 1]) * \
    #                    cox_de_boor_recursion(i_ + 1, p_ - 1)
    #
    #     return cox_de_boor_recursion(i, p)

    def de_boor(self, t):
        """From wikpedia and https://stackoverflow.com/questions/57507696/b-spline-derivative-using-de-boors-algorithm"""
        # Find the knot interval that contains t
        interval = 0
        for i in range(len(self.knots) - 1):
            # Modification to account for repeated knots
            if np.isclose(self.knots[i + 1] - self.knots[i], 0.0):
                continue
            if self.knots[i] <= t <= self.knots[i + 1]:
                interval = i
                break

        p = len(self.knots) - self.P.shape[0] - 1

        d = [self.P[j + interval - p] for j in range(0, p + 1)]

        for r in range(1, p + 1):
            for j in range(p, r - 1, -1):
                print(f"{r = }, {j = }, {p = }, {interval = }")
                alpha = (t - self.knots[j + interval - p]) / (self.knots[j + 1 + interval - r] - self.knots[j + interval - p])
                d[j] = (1.0 - alpha) * d[j - 1] + alpha * d[j]

        return d[p]

    def _basis_functions(self, span, t, p):
        """Compute the non-vanishing basis functions"""
        basis_functions = np.zeros(p + 1)
        basis_functions[0] = 1.0
        left = np.zeros(p + 1)
        right = np.zeros(p + 1)
        for j in range(1, p + 1):
            left[j] = t - self.knots[span + 1 - j]
            right[j] = self.knots[span + j] - t
            saved = 0.0
            for r in range(j):
                temp = basis_functions[r] / (right[r + 1] + left[j - r])
                basis_functions[r] = saved + right[r + 1] * temp
                saved = left[j - r] * temp
            basis_functions[j] = saved
        return basis_functions


class BSpline(RationalBSpline):
    def __init__(self, P, knots):
        weights = np.ones(P.shape[0])
        super().__init__(P=P, knots=knots, weights=weights)


class ClampedBSpline(BSpline):
    def __init__(self, P: np.ndarray, extra_knots: np.ndarray):
        n = P.shape[0] - 1
        multiplicity = n - len(extra_knots) + 1
        knots = np.concatenate((np.zeros(multiplicity), extra_knots, np.ones(multiplicity)))
        super().__init__(P=P, knots=knots)


class BezierCurve(ClampedBSpline):
    def __init__(self, P):
        super().__init__(P=P, extra_knots=np.array([]))


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    P = np.array([[0.0, 0.0], [0.3, 0.1], [0.5, 0.0], [0.7, -0.1], [1.0, 0.0]])
    b = Bezier(P=P, t=np.linspace(0, 1, 101))
    # b2 = BezierCurve(P=P)
    # knots = np.array([0, 0, 0, 0.3, 0.7, 1, 1, 1])
    # knots = np.linspace(0.0, 1.0, 10)
    knots = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1])
    plt.plot(b.x, b.y)
    # plt.plot(b2.x, b2.y)
    # plt.show()
    bspline = BSpline(P=P, knots=knots)
    plt.plot(bspline.x, bspline.y)
    P = np.array([[0.0, 0.0], [0.3, 0.1], [0.5, 0.0], [0.7, -0.1], [1.0, 0.0]])
    # knots = np.linspace(0, 1, 14)
    # bspline = BSpline(P=P, knots=knots)
    # plt.plot(bspline.x, bspline.y)
    plt.show()
    pass
