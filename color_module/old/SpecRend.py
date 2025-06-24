import math

class ColourSystem:
    def __init__(self, name, xRed, yRed, xGreen, yGreen, xBlue, yBlue, xWhite, yWhite, gamma):
        self.name = name
        self.xRed = xRed
        self.yRed = yRed
        self.xGreen = xGreen
        self.yGreen = yGreen
        self.xBlue = xBlue
        self.yBlue = yBlue
        self.xWhite = xWhite
        self.yWhite = yWhite
        self.gamma = gamma

class SpecRend:
    # White point chromaticities.
    IlluminantCx = 0.3101  # for NTSC television
    IlluminantCy = 0.3162
    IlluminantD65x = 0.3127  # for EBU and SMPTE
    IlluminantD65y = 0.3291
    IlluminantEx = 0.333333  # CIE equal-energy illuminant
    IlluminantEy = 0.333333

    # Gamma of nonlinear correction.
    GAMMA_REC709 = 0  # Rec. 709

    # Colour systems
    NTSCsystem = ColourSystem(
        "NTSC", 0.67, 0.33, 0.21, 0.71, 0.14, 0.08,
        IlluminantCx, IlluminantCy, GAMMA_REC709
    )
    EBUsystem = ColourSystem(
        "EBU (PAL/SECAM)", 0.64, 0.33, 0.29, 0.60, 0.15, 0.06,
        IlluminantD65x, IlluminantD65y, GAMMA_REC709
    )
    SMPTEsystem = ColourSystem(
        "SMPTE", 0.630, 0.340, 0.310, 0.595, 0.155, 0.070,
        IlluminantD65x, IlluminantD65y, GAMMA_REC709
    )
    HDTVsystem = ColourSystem(
        "HDTV", 0.670, 0.330, 0.210, 0.710, 0.150, 0.060,
        IlluminantD65x, IlluminantD65y, GAMMA_REC709
    )
    CIEsystem = ColourSystem(
        "CIE", 0.7355, 0.2645, 0.2658, 0.7243, 0.1669, 0.0085,
        IlluminantEx, IlluminantEy, GAMMA_REC709
    )
    Rec709system = ColourSystem(
        "CIE REC 709", 0.64, 0.33, 0.30, 0.60, 0.15, 0.06,
        IlluminantD65x, IlluminantD65y, GAMMA_REC709
    )

    @staticmethod
    def upvp_to_xy(up, vp):
        xc = (9 * up) / ((6 * up) - (16 * vp) + 12)
        yc = (4 * vp) / ((6 * up) - (16 * vp) + 12)
        return xc, yc

    @staticmethod
    def xy_to_upvp(xc, yc):
        up = (4 * xc) / ((-2 * xc) + (12 * yc) + 3)
        vp = (9 * yc) / ((-2 * xc) + (12 * yc) + 3)
        return up, vp

    @staticmethod
    def xyz_to_rgb(cs, xc, yc, zc):
        xr, yr = cs.xRed, cs.yRed
        zr = 1 - (xr + yr)
        xg, yg = cs.xGreen, cs.yGreen
        zg = 1 - (xg + yg)
        xb, yb = cs.xBlue, cs.yBlue
        zb = 1 - (xb + yb)

        xw, yw = cs.xWhite, cs.yWhite
        zw = 1 - (xw + yw)

        rx = (yg * zb) - (yb * zg)
        ry = (xb * zg) - (xg * zb)
        rz = (xg * yb) - (xb * yg)
        gx = (yb * zr) - (yr * zb)
        gy = (xr * zb) - (xb * zr)
        gz = (xb * yr) - (xr * yb)
        bx = (yr * zg) - (yg * zr)
        by = (xg * zr) - (xr * zg)
        bz = (xr * yg) - (xg * yr)

        rw = ((rx * xw) + (ry * yw) + (rz * zw)) / yw
        gw = ((gx * xw) + (gy * yw) + (gz * zw)) / yw
        bw = ((bx * xw) + (by * yw) + (bz * zw)) / yw

        rx /= rw
        ry /= rw
        rz /= rw
        gx /= gw
        gy /= gw
        gz /= gw
        bx /= bw
        by /= bw
        bz /= bw

        r = rx * xc + ry * yc + rz * zc
        g = gx * xc + gy * yc + gz * zc
        b = bx * xc + by * yc + bz * zc

        return r, g, b

    @staticmethod
    def inside_gamut(r, g, b):
        return r >= 0 and g >= 0 and b >= 0

    @staticmethod
    def constrain_rgb(ir, ig, ib):
        r, g, b = ir, ig, ib
        w = min(r, g, b)
        w = min(w, 0)
        w = -w

        if w > 0:
            r += w
            g += w
            b += w
            return (r, g, b, True)
        return (r, g, b, False)

    @staticmethod
    def gamma_correct(cs, c):
        if cs.gamma == SpecRend.GAMMA_REC709:
            cc = 0.018
            if c < cc:
                c *= ((1.099 * (cc ** 0.45)) - 0.099) / cc
            else:
                c = (1.099 * (c ** 0.45)) - 0.099
        else:
            c = math.pow(c, 1.0 / cs.gamma)
        return c

    @staticmethod
    def gamma_correct_rgb(cs, r, g, b):
        r_c = SpecRend.gamma_correct(cs, r)
        g_c = SpecRend.gamma_correct(cs, g)
        b_c = SpecRend.gamma_correct(cs, b)
        return r_c, g_c, b_c

    @staticmethod
    def norm_rgb(ir, ig, ib):
        r, g, b = ir, ig, ib
        greatest = max(r, g, b)
        if greatest > 0:
            r /= greatest
            g /= greatest
            b /= greatest
        return r, g, b

    @staticmethod
    def spectrum_to_xyz(spec_intens, parm):
        X = Y = Z = 0.0
        cie_colour_match = [
            [0.0014,0.0000,0.0065], [0.0022,0.0001,0.0105], [0.0042,0.0001,0.0201],
            [0.0076,0.0002,0.0362], [0.0143,0.0004,0.0679], [0.0232,0.0006,0.1102],
            [0.0435,0.0012,0.2074], [0.0776,0.0022,0.3713], [0.1344,0.0040,0.6456],
            [0.2148,0.0073,1.0391], [0.2839,0.0116,1.3856], [0.3285,0.0168,1.6230],
            [0.3483,0.0230,1.7471], [0.3481,0.0298,1.7826], [0.3362,0.0380,1.7721],
            [0.3187,0.0480,1.7441], [0.2908,0.0600,1.6692], [0.2511,0.0739,1.5281],
            [0.1954,0.0910,1.2876], [0.1421,0.1126,1.0419], [0.0956,0.1390,0.8130],
            [0.0580,0.1693,0.6162], [0.0320,0.2080,0.4652], [0.0147,0.2586,0.3533],
            [0.0049,0.3230,0.2720], [0.0024,0.4073,0.2123], [0.0093,0.5030,0.1582],
            [0.0291,0.6082,0.1117], [0.0633,0.7100,0.0782], [0.1096,0.7932,0.0573],
            [0.1655,0.8620,0.0422], [0.2257,0.9149,0.0298], [0.2904,0.9540,0.0203],
            [0.3597,0.9803,0.0134], [0.4334,0.9950,0.0087], [0.5121,1.0000,0.0057],
            [0.5945,0.9950,0.0039], [0.6784,0.9786,0.0027], [0.7621,0.9520,0.0021],
            [0.8425,0.9154,0.0018], [0.9163,0.8700,0.0017], [0.9786,0.8163,0.0014],
            [1.0263,0.7570,0.0011], [1.0567,0.6949,0.0010], [1.0622,0.6310,0.0008],
            [1.0456,0.5668,0.0006], [1.0026,0.5030,0.0003], [0.9384,0.4412,0.0002],
            [0.8544,0.3810,0.0002], [0.7514,0.3210,0.0001], [0.6424,0.2650,0.0000],
            [0.5419,0.2170,0.0000], [0.4479,0.1750,0.0000], [0.3608,0.1382,0.0000],
            [0.2835,0.1070,0.0000], [0.2187,0.0816,0.0000], [0.1649,0.0610,0.0000],
            [0.1212,0.0446,0.0000], [0.0874,0.0320,0.0000], [0.0636,0.0232,0.0000],
            [0.0468,0.0170,0.0000], [0.0329,0.0119,0.0000], [0.0227,0.0082,0.0000],
            [0.0158,0.0057,0.0000], [0.0114,0.0041,0.0000], [0.0081,0.0029,0.0000],
            [0.0058,0.0021,0.0000], [0.0041,0.0015,0.0000], [0.0029,0.0010,0.0000],
            [0.0020,0.0007,0.0000], [0.0014,0.0005,0.0000], [0.0010,0.0004,0.0000],
            [0.0007,0.0002,0.0000], [0.0005,0.0002,0.0000], [0.0003,0.0001,0.0000],
            [0.0002,0.0001,0.0000], [0.0002,0.0001,0.0000], [0.0001,0.0000,0.0000],
            [0.0001,0.0000,0.0000], [0.0001,0.0000,0.0000], [0.0000,0.0000,0.0000]
        ]

        for i in range(len(cie_colour_match)):
            lambda_val = 380 + i * 5
            Me = spec_intens(lambda_val, parm)
            X += Me * cie_colour_match[i][0]
            Y += Me * cie_colour_match[i][1]
            Z += Me * cie_colour_match[i][2]

        XYZ = X + Y + Z
        if XYZ == 0:
            return (0.0, 0.0, 0.0)
        x = X / XYZ
        y = Y / XYZ
        z = Z / XYZ
        return (x, y, z)
        # return (X, Y, Z)

    @staticmethod
    def bb_spectrum(wavelength, bbTemp):
        wlm = wavelength * 1e-9  # Convert nm to meters
        numerator = 3.74183e-16 * (wlm ** -5.0)
        denominator = math.exp(1.4388e-2 / (wlm * bbTemp)) - 1.0
        return numerator / denominator

    @staticmethod
    def saturate(c, s):
        r, g, b = c
        new_r = (0.213 + 0.787 * s) * r + (0.715 - 0.715 * s) * g + (0.072 - 0.072 * s) * b
        new_g = (0.213 - 0.213 * s) * r + (0.715 + 0.285 * s) * g + (0.072 - 0.072 * s) * b
        new_b = (0.213 - 0.213 * s) * r + (0.715 - 0.715 * s) * g + (0.072 + 0.928 * s) * b
        new_r = max(0.0, min(1.0, new_r))
        new_g = max(0.0, min(1.0, new_g))
        new_b = max(0.0, min(1.0, new_b))
        return (new_r, new_g, new_b)




        