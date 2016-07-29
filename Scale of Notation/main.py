from math import modf

class Num:
    Base = 0
    Accuracy = 6

    _decInt = 0
    _decFrac = 0.0
    _digitsInt = []
    _digitsFrac = []

    def _set(self, decInt, decFrac = 0, base = None, accuracy = None):
        if base == None: base = self.Base
        if accuracy == None: accuracy = self.Accuracy

        if base <= 1:
             raise BaseException("")
        if decInt < 0:
            raise BaseException()
        if decFrac < 0:
            raise BaseException()
        if accuracy < 0:
            raise BaseException()

        f, i = modf(decInt)
        F, I = modf(decFrac)

        decInt = I + i
        decFrac = F + f
        f, i = modf(decFrac)
        decFrac = f

        self.Accuracy = accuracy
        self._decInt = decInt
        self._decFrac = decFrac
        self.Base = base

        resultInt = []
        resultFrac = []

        while decInt > 0:
            digit = decInt % base
            decInt //= base
            resultInt.insert(0, int(digit))

        for i in range(accuracy):
            decFrac *= base
            decFrac = round(decFrac, accuracy)
            decFrac, d = modf(decFrac)
            resultFrac.append(int(d))

        for i in range(len(resultFrac) - 1, 0, -1):
            if (resultFrac[i] == 0):
                del resultFrac[i]
            else:
                break

        self._digitsInt = resultInt
        self._digitsFrac = resultFrac

    def __init__(self, base, decInt, decFrac = 0, accuracy = 7):
        self._set(decInt, decFrac, base, accuracy)

    def __call__(self, base, decInt, decFrac = 0, accuracy = 7):
        a = N(base, decInt, decFrac, accuracy)

    def ChangeBase(self, base):
        self._set(self._decInt, self._decFrac, base, accuracy)

    def DecValue(self):
        return self._decFrac + self._decInt

    def __add__(self, y):
        if (isinstance(y, Num)):
            return Num(self.Base, self._decInt + y._decInt, self._decFrac, self.Accuracy)
        else:
            return Num(self.Base, self._decInt + y, self._decFrac, self.Accuracy)

    def __sub__(self, y):
        if (isinstance(y, Num)):
            return Num(self.Base, self._decInt + y._decInt, self._decFrac + y._decFrac, self.Accuracy)
        else:
            return Num(self.Base, self._decInt + y, self._decFrac, self.Accuracy)

    def __mul__(self, y):
        if (isinstance(y, Num)):
            return y * self.DecValue()
        else:
            return Num(self.Base, self._decInt * y, self._decFrac * y, self.Accuracy)

    def __truediv__(self, y):
        if isinstance(y, Num):
            return Num(self.Base, self._decInt / y.DecValue(), self._decFrac / y.DecValue(), self.Accuracy)
        else:
            return Num(self.Base, self._decInt / y, self._decFrac / y, self.Accuracy)

    def __floordiv__(self, y):
        if isinstance(y, Num):
            return Num(self.Base, self.DecValue() // y.DecValue(), 0, self.Accuracy)
        else:
            return Num(self.Base, self.DecValue() // y, 0, self.Accuracy)

    def __mod__(self, y):
        if isinstance(y, Num):
            return Num(self.Base, self.DecValue() % y.DecValue(), 0, self.Accuracy)
        else:
            return Num(self.Base, self.DecValue() % y, 0, self.Accuracy)

    def __pow__(self, y):
        if (isinstance(y, Num)):
            return Num(self.Base, self.DecValue() ** y.DecValue())
        else:
            return Num(self.Base, self.DecValue() ** y)

    def __lt__(self, y):
        if (isinstance(y, Num)):
            return self.DecValue() < y.DecValue()
        else:
            return None

    def __le__(self, y):
        if (isinstance(y, Num)):
            return self.DecValue() <= y.DecValue()
        else:
            return None

    def __eq__(self, y):
        if (isinstance(y, Num)):
            return self.DecValue() == y.DecValue()
        else:
            return None

    def __ne__(self, y):
        if (isinstance(y, Num)):
            return self.DecValue() != y.DecValue()
        else:
            return None

    def __gt__(self, y):
        if (isinstance(y, Num)):
            return self.DecValue() >= y.DecValue()
        else:
            return None

    def _s(self, ls, base):
        result = ""
        if base <= 16:
            for x in ls:
                if x < 10:
                    result += str(x)
                else: result += {
                    10: 'A',
                    11: 'B',
                    12: 'C',
                    13: 'D',
                    14: 'E',
                    15: 'F'
                }[int(x)]
        else:
            for x in ls:
                    result += "(" + str(x) + ")"

        return result

    def __str__(self):
        result = self._s(self._digitsInt, self.Base)
        if (self._decFrac > 0):
            result += "." + self._s(self._digitsFrac, self.Base)

        return result

    def __rshift__(self, y):
        return Num(y, self._decInt, self._decFrac, self.Accuracy)

    def __int__(self):
        return self._decInt

    def __float__(self):
        return self.DecValue()
