# https://github.com/hkurhinen/etrs-tm35fin-to-wgs84-converter/blob/master/src/fi/elemmings/converter/Etrs35fin2wgs84Converter.java

import math


def etrs_to_wgs84(x, y):

    Ca = 6378137.0
    Cf = 1.0 / 298.257223563
    Ck0 = 0.9996
    Clo0 = math.radians(27.0)
    CE0 = 500000.0
    Cn = Cf / (2.0 - Cf)
    CA1 = Ca / (1.0 + Cn) * (1.0 + (math.pow(Cn, 2.0)) /
                             4.0 + (math.pow(Cn, 4.0)) / 64.0)
    Ce = math.sqrt((2.0 * Cf - math.pow(Cf, 2.0)))
    Ch1 = 1.0 / 2.0 * Cn - 2.0 / 3.0 * \
        (math.pow(Cn, 2.0)) + 37.0 / 96.0 * \
        (math.pow(Cn, 3.0)) - 1.0 / 360.0 * (math.pow(Cn, 4.0))
    Ch2 = 1.0 / 48.0 * (math.pow(Cn, 2.0)) + 1.0 / 15.0 * \
        (math.pow(Cn, 3.0)) - 437.0 / 1440.0 * (math.pow(Cn, 4.0))
    Ch3 = 17.0 / 480.0 * (math.pow(Cn, 3.0)) - 37.0 / \
        840.0 * (math.pow(Cn, 4.0))
    Ch4 = 4397.0 / 161280.0 * (math.pow(Cn, 4.0))

    E = x / (CA1 * Ck0)
    nn = (y - CE0) / (CA1 * Ck0)
    E1p = Ch1 * math.sin(2.0 * E) * math.cosh(2.0 * nn)
    E2p = Ch2 * math.sin(4.0 * E) * math.cosh(4.0 * nn)
    E3p = Ch2 * math.sin(6.0 * E) * math.cosh(6.0 * nn)
    E4p = Ch3 * math.sin(8.0 * E) * math.cosh(8.0 * nn)

    nn1p = Ch1 * math.cos(2.0 * E) * math.sinh(2.0 * nn)
    nn2p = Ch2 * math.cos(4.0 * E) * math.sinh(4.0 * nn)
    nn3p = Ch3 * math.cos(6.0 * E) * math.sinh(6.0 * nn)
    nn4p = Ch4 * math.cos(8.0 * E) * math.sinh(8.0 * nn)

    Ep = E - E1p - E2p - E3p - E4p

    nnp = nn - nn1p - nn2p - nn3p - nn4p
    be = math.asin(math.sin(Ep) / math.cosh(nnp))

    Q = asinh(math.tan(be))
    Qp = Q + Ce * atanh(Ce * math.tanh(Q))
    Qp = Q + Ce * atanh(Ce * math.tanh(Qp))
    Qp = Q + Ce * atanh(Ce * math.tanh(Qp))
    Qp = Q + Ce * atanh(Ce * math.tanh(Qp))

    latitude = math.degrees(math.atan(math.sinh(Qp)))

    longitude = math.degrees(Clo0 + math.asin(math.tanh(nnp) / math.cos(be)))

    return [latitude, longitude]


def atanh(value):
    return math.log((1 / value + 1) / (1 / value - 1)) / 2


def asinh(value):
    return math.log(value + math.sqrt(value * value + 1))
