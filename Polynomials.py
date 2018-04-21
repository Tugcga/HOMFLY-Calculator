class Polynomial:
    def __init__(self, sourceP=None):
        if sourceP is None:
            self.coefficients = {}
        else:
            self.coefficients = {}
            for k in sourceP.coefficients.keys():
                self.coefficients[k] = sourceP.coefficients[k]

    def GenerateAsFN(self, n, isPrint=False):  # -a-a^3-...a^n-1, n>0
        self.coefficients = {}
        if n % 2 == 1:
            if isPrint:
                print("The power of the polynom is wrong. It should be even.")
        else:
            if n > 0:
                for i in range(1, n // 2 + 1):
                    self.coefficients[2*i-1] = -1
            elif n < 0:
                for i in range(1, abs(n) // 2 + 1):
                    self.coefficients[-2 * i + 1] = 1

    def toString(self):
        if len(self.coefficients.keys()) == 0:
            return "0"
        else:
            s = ""
            ks = list(self.coefficients.keys())
            ks.sort()
            isFirst = True
            for k in ks:
                s = s + (("" if isFirst else "+") if self.coefficients[k] == 1 else ("-" if self.coefficients[k] == -1 else (("" if isFirst else "+") + 
                    str(self.coefficients[k]) if self.coefficients[k] > 0 else str(self.coefficients[k])))) + (("1"
                if abs(self.coefficients[k]) == 1 else "") if k == 0 else ("a" + ("" if k == 1 else "^{" + str(k) + "}")))
                isFirst = False
            return s

    def GenerateAsMonom(self, power):  # a^p
        self.coefficients = {}
        self.coefficients[power] = 1

    def GenerateAsSym(self):  # a - a^-1
        self.coefficients = {}
        self.coefficients[1] = 1
        self.coefficients[-1] = -1

    def MultiplyByConstant(self, c):
        for k in self.coefficients.keys():
            self.coefficients[k] = c * self.coefficients[k]

    def MultiplyPolynomials(self, f, g):
        self.coefficients = {}
        for k1 in f.coefficients.keys():
            for k2 in g.coefficients.keys():
                c = f.coefficients[k1] * g.coefficients[k2]
                p = k1 + k2
                if p in self.coefficients.keys():
                    self.coefficients[p] = self.coefficients[p] + c
                else:
                    self.coefficients[p] = c
        self.Filter()

    def SumPolynomials(self, f, g):
        self.coefficients = {}
        for k in f.coefficients.keys():
            self.coefficients[k] = f.coefficients[k]
            if k in g.coefficients.keys():
                self.coefficients[k] = self.coefficients[k] + g.coefficients[k]
        for k in g.coefficients.keys():
            if k not in f.coefficients.keys():
                self.coefficients[k] = g.coefficients[k]

        self.Filter()

    def Filter(self):
        toDeleteKeys = []
        for k in self.coefficients.keys():
            if self.coefficients[k] == 0:
                toDeleteKeys.append(k)
        for k in toDeleteKeys:
            del self.coefficients[k]

    def IsZero(self):
        self.Filter()
        if len(self.coefficients) == 0:
            return True
        else:
            return False

    def IsEqualTo(self, p):
        self.Filter()
        p.Filter()
        if len(self.coefficients.keys()) == len(p.coefficients.keys()):
            for k in self.coefficients.keys():
                if k in p.coefficients.keys():
                    c1 = self.coefficients[k]
                    c2 = p.coefficients[k]
                    if not c1 == c2:
                        return False
                else:
                    return False
            return True
        else:
            return False


class ZBasePolynomial:
    def __init__(self, zPolynomial=None):
        if zPolynomial is None:
            self.pCoefficients = {}
        else:
            self.pCoefficients = {}
            for k in zPolynomial.pCoefficients.keys():
                self.pCoefficients[k] = Polynomial(zPolynomial.pCoefficients[k])

    def GenerateAsMonom(self, pow, pCoef):
        self.pCoefficients = {}
        self.pCoefficients[pow] = pCoef

    def toString(self):
        s = ""
        if len(self.pCoefficients.keys()) == 0:
            return "0"
        else:
            ks = list(self.pCoefficients.keys())
            ks.sort()
            isFirst = True
            for k in ks:
                sign = "+"
                pString = self.pCoefficients[k].toString()
                isAllowBrackets = True
                if len(self.pCoefficients[k].coefficients.keys()) == 1:
                    isAllowBrackets = False
                    if pString[0] == "-":
                        sign = "-"
                        pString = pString[1:]
                startCoeff = ""
                if pString.isdigit():
                    startCoeff = pString
                    if startCoeff == "1":
                        startCoeff = ""
                    pString = ""

                s = s + startCoeff + ("" if k == 0 else (("" if isFirst else sign) + "z" + ("" if k == 1 else "^{" + str(k) + "}") + " ")) + ("(" if isAllowBrackets else "") + pString + (")" if isAllowBrackets else "")
                isFirst = False
            if s[0] == "+":
                s = s[1:]
            return s

    def Filter(self):
        toDelete = []
        for k in self.pCoefficients.keys():
            if self.pCoefficients[k].IsZero():
                toDelete.append(k)
        for k in toDelete:
            del self.pCoefficients[k]

    def Sum(self, z1, z2):
        self.pCoefficients = {}
        for k in z1.pCoefficients.keys():
            p1 = z1.pCoefficients[k]
            if k in z2.pCoefficients.keys():
                p2 = z2.pCoefficients[k]
                p = Polynomial()
                p.SumPolynomials(p1, p2)
                p1 = Polynomial(p)
            self.pCoefficients[k] = p1
        for k in z2.pCoefficients.keys():
            if k not in z1.pCoefficients.keys():
                self.pCoefficients[k] = z2.pCoefficients[k]
        self.Filter()

    def MultiplyByPolinom(self, p):
        for k in self.pCoefficients.keys():
            pCoef = Polynomial(self.pCoefficients[k])
            newCoef = Polynomial()
            newCoef.MultiplyPolynomials(pCoef, p)
            self.pCoefficients[k] = newCoef
        self.Filter()

    def Multiply(self, z1, z2):
        self.pCoefficients = {}
        for k1 in z1.pCoefficients.keys():
            for k2 in z2.pCoefficients.keys():
                prod = Polynomial()
                prod.MultiplyPolynomials(z1.pCoefficients[k1], z2.pCoefficients[k2])
                k = k1 + k2
                if k in self.pCoefficients.keys():
                    oldProd = self.pCoefficients[k]
                    newProd = Polynomial()
                    newProd.SumPolynomials(prod, oldProd)
                    self.pCoefficients[k] = newProd
                else:
                    self.pCoefficients[k] = prod
        self.Filter()

    def IsEqualTo(self, z):
        self.Filter()
        z.Filter()
        if len(self.pCoefficients.keys()) == len(z.pCoefficients.keys()):
            for k in self.pCoefficients.keys():
                if k in z.pCoefficients.keys():
                    p1 = self.pCoefficients[k]
                    p2 = z.pCoefficients[k]
                    if not p1.IsEqualTo(p2):
                        return False
                else:
                    return False
            return True
        else:
            return False
