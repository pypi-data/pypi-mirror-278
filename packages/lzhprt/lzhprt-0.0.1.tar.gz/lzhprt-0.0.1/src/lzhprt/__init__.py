# -*- coding: UTF-8 -*-
# Public package
import os
import math
import numpy
# Private package
# Internal package


class Filler:
    def __init__(self):
        self.block = ' '
        self.loc = 'center'
        self.length = None  # None:不填充, -1:动态填充, >0:固定填充

    def fill(self, value):
        output = value
        if (self.length is not None):
            if (self.loc in ['left', 'l']):
                while (len(output) < self.length):
                    output = output + self.block
            elif (self.loc in ['right', 'r']):
                while (len(output) < self.length):
                    output = self.block + output
            else:
                while (len(output) < self.length):
                    if (len(output) % 2 == 0):
                        output = self.block + output
                    else:
                        output = output + self.block
            if (self.length < len(output)):
                output = output[:self.length]
        return output


class Styler:
    def __init__(self):
        self.effect = '0'
        self.front = ''
        self.back = ''

    def set_effect(self, effect):
        if (effect in ['bold', 'b']):
            self.effect = '1'
        elif (effect in ['underline', 'u']):
            self.effect = '4'
        elif (effect in ['blink', 'l']):
            self.effect = '5'
        elif (effect in ['reverse', 'r']):
            self.effect = '7'
        elif (effect in ['invisible', 'i']):
            self.effect = '8'
        else:
            self.effect = None

    def set_front(self, color):
        if (color in ['black', 'd']):
            self.front = '30'
        elif (color in ['red', 'r']):
            self.front = '31'
        elif (color in ['green', 'g']):
            self.front = '32'
        elif (color in ['yellow', 'y']):
            self.front = '33'
        elif (color in ['blue', 'b']):
            self.front = '34'
        elif (color in ['purple', 'p']):
            self.front = '35'
        elif (color in ['cyan', 'c']):
            self.front = '36'
        elif (color in ['white', 'w']):
            self.front = '37'
        else:
            self.front = None

    def set_back(self, color):
        if (color in ['black', 'd']):
            self.back = '40'
        elif (color in ['red', 'r']):
            self.back = '41'
        elif (color in ['green', 'g']):
            self.back = '42'
        elif (color in ['yellow', 'y']):
            self.back = '43'
        elif (color in ['blue', 'b']):
            self.back = '44'
        elif (color in ['purple', 'p']):
            self.back = '45'
        elif (color in ['cyan', 'c']):
            self.back = '46'
        elif (color in ['white', 'w']):
            self.back = '47'
        else:
            self.back = None

    def set(self, config):
        self.set_effect(config[0])
        self.set_front(config[1])
        self.set_back(config[2])

    def __call__(self, value):
        output = [code for code in [self.effect, self.front, self.back] if code is not None]
        output = ';'.join(output)
        output = '\033[%sm%s\033[0m' % (output, value)
        return output


class Str:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return self.value


class Int:
    def __init__(self, value):
        self.value = value
        self.length = None

    def __repr__(self):
        if (self.length is None):
            return str(self.value)
        else:
            return str(self.value).zfill(self.length)


class Float:
    def __init__(self, value):
        self.value = value
        self.length = None  # total length
        self.inpercent = False  # return in percent

    def float_fix(self, value, length):
        'format float value to string with fixed length'
        return max(0, min(length - 2, length - 2 - int(math.log10(abs(value))))) if value else length - 2

    def __repr__(self):
        if (self.inpercent):
            if (self.length is None):
                return str(self.value * 100) + '%%'
            else:
                return '%.*f%%' % (self.float_fix(self.value * 100, self.length - 1), self.value * 100)
        else:
            if (self.length is None):
                return str(self.value)
            else:
                return '%.*f' % (self.float_fix(self.value, self.length), self.value)


class Unit:
    def __init__(self, value):
        if (type(value) in [str]):
            self.value = Str(value)
        elif (type(value) in [int, numpy.int16, numpy.int32, numpy.int64]):
            self.value = Int(value)
        elif (type(value) in [float, numpy.float16, numpy.float32, numpy.float64]):
            self.value = Float(value)
        else:
            self.value = Str(str(value))
        self.filler = Filler()
        self.styler = Styler()

    def get_str(self):
        return self.value.__repr__()

    def get_filled(self):
        return self.filler.fill(self.get_str())

    def get_unit(self):
        return self.styler(self.get_filled())

    def __repr__(self):
        return self.get_unit()

    def is_dynamic(self):
        return self.filler.length == -1

    def get_length(self):
        return len(self.value.__repr__())


class Line:
    def __init__(self):
        self.units = []
        self.weights = []

    def add(self, unit, weight=None):
        self.units.append(unit)
        if (weight is None):
            self.weights.append(1)
        else:
            self.weights.append(weight)

    def __repr__(self):
        total = os.get_terminal_size().columns
        temp_iunits = []
        temp_weight = []
        for iunit, unit in enumerate(self.units):
            if (unit.is_dynamic()):
                temp_iunits.append(iunit)
                temp_weight.append(self.weights[iunit])
            else:
                total -= unit.get_length()
        total = max(total, 0)
        use_weight = [int(total * weight / sum(temp_weight)) for weight in temp_weight]
        use_weight[-1] += total - sum(use_weight)
        for iunit, weight in zip(temp_iunits, use_weight):
            self.units[iunit].filler.length = weight
        return ''.join([unit.__repr__() for unit in self.units])


def hori():
    line = Line()
    line.add(Unit('|'))
    unit = Unit('')
    unit.filler.length = -1
    unit.filler.block = '-'
    line.add(unit)
    line.add(Unit('|'))
    return line
