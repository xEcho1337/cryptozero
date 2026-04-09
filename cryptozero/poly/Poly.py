class Poly:
    def __init__(self, mod: int, coeffs=None):
        if coeffs is None:
            coeffs = [0]

        self.mod = mod
        self.coeffs = [c % mod for c in coeffs]

    def __call__(self, x):
        res = 0
        power = 1
        for c in self.coeffs:
            res = (res + c * power) % self.mod
            power = (power * x) % self.mod
        return res

    def __add__(self, other):
        n = max(len(self.coeffs), len(other.coeffs))
        res = []
        for i in range(n):
            a = self.coeffs[i] if i < len(self.coeffs) else 0
            b = other.coeffs[i] if i < len(other.coeffs) else 0
            res.append((a + b) % self.mod)
        return Poly(self.mod, res)

    def __mul__(self, other):
        res = [0] * (len(self.coeffs) + len(other.coeffs) - 1)
        for i, a in enumerate(self.coeffs):
            for j, b in enumerate(other.coeffs):
                res[i + j] = (res[i + j] + a * b) % self.mod
        return Poly(self.mod, res)

    def lagrange_interpolate(self, xs: list[int], ys: list[int]):
        n = len(xs)
        result = Poly(self.mod)

        for i in range(n):
            xi, yi = xs[i], ys[i]

            num = Poly(self.mod, [1])
            den = 1

            for j in range(n):
                if i == j:
                    continue
                xj = xs[j]

                # (x - xj)
                num = num * Poly(self.mod, [-xj % self.mod, 1])

                # (xi - xj)
                den = (den * (xi - xj)) % self.mod

            inv_den = pow(den, -1, self.mod)
            term = num * Poly(self.mod, [yi * inv_den % self.mod])

            result = result + term

        return result

    def coefficients(self):
        return self.coeffs.copy()