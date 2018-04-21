from fractions import Fraction
from Polynomials import *
from math import sqrt


def GetFractionFromSet(array):
    x = Fraction(0, 1)
    for i in reversed(array):
        s = Fraction(i, 1) + x
        x = 1 / s
    return x


class ExtFraction:
    def __init__(self):
        self.a = Fraction(0, 1)
        self.denominators = []

    def SetFraction(self, num, den):
        self.a = Fraction(num, den)

    def toString(self):
        print(str(self.a))

    def IsCorrect(self):
        if self.a.numerator * self.a.denominator % 2 == 0:
            return True
        else:
            return False

    def GetSign(self, x):
        if x > 0:
            return 1
        elif x < 0:
            return -1
        else:
            return 0

    def GetPartialDenominators(self, isPrint=False):
        pDens = []
        if self.a.numerator * self.a.denominator == 0:
            if isPrint:
                print("Incorrect fraction")
        elif self.a.numerator * self.a.denominator % 2 == 1:
            if isPrint:
                print("p*q is odd, but should be even")
        else:
            x = Fraction(self.a)
            while not abs(x.numerator) == 1:
                b = x.denominator // abs(x.numerator)
                b = b * self.GetSign(x.numerator)
                if b % 2 == 1:
                    b = b + x.numerator // abs(x.numerator)
                x = Fraction(x.denominator, x.numerator) - Fraction(b, 1)
                pDens.append(b)
            pDens.append(x.denominator * x.numerator)
            if isPrint:
                print(pDens)

            self.denominators = pDens
        return pDens


class BTree:
    def __init__(self):
        self.value = 0
        self.isLeaf = True
        self.leftItem = None
        self.rightItem = None
        self.isRoot = True
        self.rootItem = None
        self.topRoot = self
        self.leafArray = []

    def Init(self, v, topRootLink, isRoot=True, rootLink=None):
        self.topRoot = topRootLink
        self.value = v
        if v == 0 or v == -1:
            self.topRoot.AddLeafLink(self)
        else:
            self.value = v
            self.isLeaf = False
            self.leftItem = BTree()
            self.rightItem = BTree()
            self.leftItem.Init(v - 1, topRootLink, False, self)
            self.rightItem.Init(v - 2, topRootLink, False, self)
        if not isRoot:
            self.isRoot = False
            self.rootItem = rootLink

    def toString(self):
        s = ""
        if self.isLeaf:
            s = str(self.value)
        else:
            s = str(self.value) + " " + self.leftItem.toString() + " " + self.rightItem.toString()
        return s

    def AddLeafLink(self, leafLink):
        self.leafArray.append(leafLink)

    def ReturnAllSets(self):
        toReturn = []

        for l in self.leafArray:
            array = []
            currentBT = l
            while not currentBT.isRoot:
                array.append(currentBT.value)
                currentBT = currentBT.rootItem
            array.append(currentBT.value)
            array.reverse()
            toReturn.append(array)

        return toReturn


class FractionEnumerator:
    def __init__(self, startFraction=None):
        if startFraction is None:
            self.currentDenominator = 2
            self.a = 0
            self.b = 1
            self.c = 1
            self.d = 2
        else:
            self.currentDenominator = startFraction.denominator
            self.a = 0
            self.b = 1
            self.c = startFraction.numerator
            self.d = startFraction.denominator

    def IsHasInverse(self, x, p):
        for i in range(1, x):
            if (x * i) % p == 1:
                return True
        return False

    def IsCorrect(self, r):
        p = r.numerator
        q = r.denominator
        if q % 2 == 1:  # this is a knot
            if p < sqrt(q):
                return True
            else:
                if self.IsHasInverse(p, q):
                    return False
                else:
                    return True

        else:  # this is a link
            if p < sqrt(2*q):
                return True
            else:
                if self.IsHasInverse(p, 2*q):
                    return False
                else:
                    return True
        return True

    def GetNextFraction(self, isCheckCorrect=False):
        isFind = False
        n = self.currentDenominator
        while not isFind:
            k = int((n + self.b)/self.d)
            self.a, self.b, self.c, self.d = self.c, self.d, k*self.c - self.a, k*self.d - self.b
            if not self.b == 1:
                r = Fraction(self.a, self.b)
                if r.denominator == self.currentDenominator:
                    if isCheckCorrect:
                        if self.IsCorrect(r):
                            return r
            if self.c > n:
                self.currentDenominator = self.currentDenominator + 1
                self.a = 0
                self.b = 1
                self.c = 1
                self.d = self.currentDenominator


class HOMFLYCalculator:
    def __init__(self, sFrac=None):
        self.calculatedPolynomials = {}
        if sFrac is None:
            self.startFraction = Fraction(1, 2)
        else:
            self.startFraction = sFrac

    def IsPolynomialNew(self, p):
        for k in self.calculatedPolynomials.keys():
            oldP = self.calculatedPolynomials[k]
            if oldP.IsEqualTo(p):
                return False
        return True

    def RunSeriesCalculation(self, count, isFindEqual=False, isWriteToFile=False, fileName=None):
        if isFindEqual:
            self.calculatedPolynomials = {}
        fe = FractionEnumerator(self.startFraction)
        i = 0
        if isWriteToFile:
            fw = open(fileName, "w")
        while i < count:
            f = fe.GetNextFraction(True)
            if (f.numerator * f.denominator) % 2 == 0:
                print("Calculate for " + str(f))
                p = self.CalculateOnce(f)
                if isFindEqual:
                    if self.IsPolynomialNew(p):
                        self.calculatedPolynomials[f] = p
                    else:
                        self.calculatedPolynomials[f] = p
                        print("Find equal polynomials. Break enumeration.")
                        i = count
                i = i + 1
                if isWriteToFile:
                    fw.write("% " + str(i) + "\n")
                    fw.write("$P(K(\\frac{" + str(f.numerator) + "}{" + str(f.denominator) + "})) = " + p.toString() + "$\n \n")
                else:
                    print(str(f) + ": " + p.toString())
        if isWriteToFile:
            fw.close()

    def MinusPower(self, n):
        if n % 2 == 0:
            return 1
        else:
            return -1

    def GetLambda(self, s):
        toReturn = []
        for i in range(0, len(s)):
            if i < len(s)-1:
                if s[i] - s[i+1] == 1:
                    toReturn.append(s[i])
        return toReturn

    def GetRho(self, s):
        toReturn = []
        for i in range(0, len(s)):
            if i < len(s) - 1:
                if s[i] - s[i + 1] == 2:
                    toReturn.append(s[i])
        return toReturn

    def GetL(self, lSet, dSet):
        toReturn = Polynomial()
        toReturn.GenerateAsMonom(0)
        if len(lSet) == 0:
            return toReturn
        else:
            for i in lSet:
                l = Polynomial()
                l.GenerateAsFN(self.MinusPower(i-1) * dSet[i-1])
                temp = Polynomial()
                temp.MultiplyPolynomials(toReturn, l)

                toReturn = Polynomial(temp)
            return toReturn

    def GetR(self, rSet, dSet):
        toReturn = Polynomial()
        toReturn.GenerateAsMonom(0)
        if len(rSet) == 0:
            return toReturn
        else:
            for i in rSet:
                r = Polynomial()
                r.GenerateAsMonom(self.MinusPower(i-1) * dSet[i-1])
                temp = Polynomial()
                temp.MultiplyPolynomials(toReturn, r)

                toReturn = Polynomial(temp)
            return toReturn

    def GetX(self, cs):
        if cs == 0:
            p = Polynomial()
            p.GenerateAsMonom(0)
            z = ZBasePolynomial()
            z.GenerateAsMonom(0, p)
            return z
        else:  # cs = -1
            p = Polynomial()
            p.GenerateAsSym()
            z = ZBasePolynomial()
            z.GenerateAsMonom(-1, p)
            return z

    def CalculateOnce(self, fraction, isTrace=False):
        result = ZBasePolynomial()

        extFrac = ExtFraction()
        if isTrace:
            print("Start calculations for " + str(fraction))
        if (fraction.numerator * fraction.denominator) % 2 == 0:
            if isTrace:
                print("Fraction correct")
            extFrac.SetFraction(fraction.numerator, fraction.denominator)
        else:
            if fraction.numerator > 0:
                extFrac.SetFraction(fraction.numerator - fraction.denominator, fraction.denominator)
            else:
                extFrac.SetFraction(fraction.numerator + fraction.denominator, fraction.denominator)
            if isTrace:
                print("Fraction is not correct. Set it to " + extFrac.toString())
        if isTrace:
            print("Start calculate denominators")
        denoms = extFrac.GetPartialDenominators()
        if isTrace:
            print("Denominators: " + str(denoms))
        n = len(denoms)
        if isTrace:
            print("Start form the tree")
        t = BTree()
        t.Init(n, t)
        if isTrace:
            print("Tree created. The number of leafs " + str(len(t.leafArray)) + ". Start form sets")
        sets = t.ReturnAllSets()
        if isTrace:
            print("Sets done.")
        for s in sets:
            l = self.GetLambda(s)
            k = len(l)
            r = self.GetRho(s)
            cs = s[len(s) - 1]

            pl = self.GetL(l, denoms)
            pr = self.GetR(r, denoms)
            p = Polynomial()
            p.MultiplyPolynomials(pl, pr)
            xz = self.GetX(cs)
            xz.MultiplyByPolinom(p)
            zkc = ZBasePolynomial()
            p0 = Polynomial()
            p0.GenerateAsMonom(0)
            zkc.GenerateAsMonom(k, p0)

            z = ZBasePolynomial()
            z.Multiply(zkc, xz)

            tRes = ZBasePolynomial()
            tRes.Sum(result, z)
            result = ZBasePolynomial(tRes)
        return result
