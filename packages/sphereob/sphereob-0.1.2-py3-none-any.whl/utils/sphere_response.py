

"""
 Main routine used to calculate the sphere-overburden response using the semi-analytical solution described in Desmarais and Smith, 2016. Geophysics 81(4), P. E265-E277
 This script is called by sphereexe when the "plot response" button is clicked in the GUI
"""

#imports
import numpy as np
import math
from scipy.integrate import fixed_quad

class SphereResponse:
    def __init__(self):
        self.mu = 1.256637e-6  # Permeability of free space
        self.dipole_m = 1847300  # Dipole moment of TX
        self.rtx = np.array([0, 0, 120], dtype=np.int64)  # TX coordinates
        self.radar = self.rtx[2]  # Height of transmitter above ground surface
        self.offset_tx_rx = np.array([12.5, 0, 56], dtype=np.int64)  # Offset from transmitter to receiver array

        self.rrx = np.array([
            self.rtx[0] - self.offset_tx_rx[0],
            self.rtx[1] - self.offset_tx_rx[1],
            self.rtx[2] - self.offset_tx_rx[2]
        ], dtype=np.int64)  # Receiver coordinates

        self.rsp = np.array([-200], dtype=np.int64)  # Sphere position
        self.a = 60.0  # Sphere radius
        self.sigma_sp = 0.5  # Sphere conductivity
        self.mtx = np.array([0, 0, 1], dtype=np.int64)  # Unit vector of transmitter dipole moment
        self.interval = 101
        self.profile_length = 1000
        self.profile = np.zeros((1, self.interval))  # Profile position vector
        self.profile_rrx = np.zeros((1, self.interval))
        self.plotting_point = 'Rx'
        self.xsign = "+ve"

        # Default HELITEM window centers
        self.wc = np.array([
            0.0001546, 0.000236, 0.0003337, 0.0004476, 0.0005778, 0.0007406, 0.000944,
            0.0011882, 0.0015137, 0.0019206, 0.0025309, 0.0033447, 0.0045654, 0.006193,
            0.0090143
        ])

        self.nw = len(self.wc)  # Number of windows
        self.P = 3.65e-3  # Pulse length
        self.bfreq = 25  # Frequency of transmitter waveform
        self.T = 1 / self.bfreq  # Period

        self.H_tot_x = np.zeros((self.nw, self.interval))  # Response vectors
        self.H_tot_y = np.zeros((self.nw, self.interval))
        self.H_tot_z = np.zeros((self.nw, self.interval))

        self.C_x = np.zeros((self.nw, self.interval))  # Induced sphere moment vectors
        self.C_z = np.zeros((self.nw, self.interval))

        self.H_ob1 = np.zeros((self.nw, self.interval))  # Overburden response vectors
        self.H_ob2 = np.zeros((self.nw, self.interval))
        self.H_ob3 = np.zeros((self.nw, self.interval))

        self.sigma_ob = 1 / 30  # Conductivity of overburden in S/m
        self.thick_ob = 2  # Thickness of overburden in m

        self.apply_dip = 0  # If 1 then apply dipping sphere model
        self.strike = 90  # Strike of sphere
        self.dip = 135  # Dip of sphere
        self.wave = 1
        self.windows = 1


    def calculate(self):

        def dh_obdt_xyz(mtx, dipole_m, rtx, rrx, O, mu, sigma_ob, thick_ob):
            """
            Function evaluates the time-derivative of the x, y, z component of the overburden field.
            See equations Eq A-5 from Desmarais and Smith, 2016. Geophysics 81(4), P. E265-E277
            """

            m_x = dipole_m * mtx[0]
            m_y = dipole_m * mtx[1]
            m_z = dipole_m * mtx[2]
            rtx_x = rtx[0]
            rtx_y = rtx[1]
            rtx_z = rtx[2]
            rrx_x = rrx[0]
            rrx_y = rrx[1]
            rrx_z = rrx[2]

            def calculate_dh_obx(rrx_z, rtx_z, rrx_x, rtx_x, rrx_y, rtx_y, O, mu, sigma_ob, thick_ob, m_x, m_y, m_z):
                factor = (-1 / (4 * math.pi))
                denominator = ((rrx_x - rtx_x) ** 2 + (rrx_y - rtx_y) ** 2 + (
                            rtx_z - rrx_z + (2 * O) / (mu * sigma_ob * thick_ob)) ** 2)
                if rrx_z > 0:
                    term1 = (m_z * (6 * rrx_x - 6 * rtx_x)) / (mu * sigma_ob * thick_ob * denominator ** (5 / 2))
                    term2 = (6 * m_x * (rrx_z + rtx_z + (2 * O) / (mu * sigma_ob * thick_ob))) / (
                                mu * sigma_ob * thick_ob * denominator ** (5 / 2))
                    term3 = (5 * (6 * rrx_x - 6 * rtx_x) * (rrx_z + rtx_z + (2 * O) / (mu * sigma_ob * thick_ob)) * (
                            m_x * (rrx_x - rtx_x) - m_z * (
                                rrx_z + rtx_z + (2 * O) / (mu * sigma_ob * thick_ob)) + m_y * (rrx_y - rtx_y))) / (
                                    mu * sigma_ob * thick_ob * denominator ** (7 / 2))
                    dh_obx = factor * (term1 - term2 + term3)
                else:
                    term1 = (m_z * (6 * rrx_x - 6 * rtx_x)) / (mu * sigma_ob * thick_ob * denominator ** (5 / 2))
                    term2 = (6 * m_x * (rtx_z - rrx_z + (2 * O) / (mu * sigma_ob * thick_ob))) / (
                                mu * sigma_ob * thick_ob * denominator ** (5 / 2))
                    term3 = (5 * (6 * rrx_x - 6 * rtx_x) * (rtx_z - rrx_z + (2 * O) / (mu * sigma_ob * thick_ob)) * (
                            m_x * (rrx_x - rtx_x) + m_y * (rrx_y - rtx_y) - m_z * (
                                rtx_z - rrx_z + (2 * O) / (mu * sigma_ob * thick_ob)))) / (
                                    mu * sigma_ob * thick_ob * denominator ** (7 / 2))
                    dh_obx = factor * (term1 - term2 + term3)
                return dh_obx

            def calculate_dh_oby(rrx_z, rtx_z, rrx_x, rtx_x, rrx_y, rtx_y, O, mu, sigma_ob, thick_ob, m_x, m_y, m_z):
                factor = (-1 / (4 * math.pi))
                denominator = ((rrx_x - rtx_x) ** 2 + (rrx_y - rtx_y) ** 2 + (
                            rtx_z - rrx_z + (2 * O) / (mu * sigma_ob * thick_ob)) ** 2)
                if rrx_z > 0:
                    term1 = (m_z * (6 * rrx_y - 6 * rtx_y)) / (mu * sigma_ob * thick_ob * denominator ** (5 / 2))
                    term2 = (6 * m_y * (rrx_z + rtx_z + (2 * O) / (mu * sigma_ob * thick_ob))) / (
                                mu * sigma_ob * thick_ob * denominator ** (5 / 2))
                    term3 = (5 * (6 * rrx_y - 6 * rtx_y) * (rrx_z + rtx_z + (2 * O) / (mu * sigma_ob * thick_ob)) * (
                            m_x * (rrx_x - rtx_x) - m_z * (
                                rrx_z + rtx_z + (2 * O) / (mu * sigma_ob * thick_ob)) + m_y * (rrx_y - rtx_y))) / (
                                    mu * sigma_ob * thick_ob * denominator ** (7 / 2))
                    dh_oby = factor * (term1 - term2 + term3)
                else:
                    term1 = (m_z * (6 * rrx_y - 6 * rtx_y)) / (mu * sigma_ob * thick_ob * denominator ** (5 / 2))
                    term2 = (6 * m_y * (rtx_z - rrx_z + (2 * O) / (mu * sigma_ob * thick_ob))) / (
                                mu * sigma_ob * thick_ob * denominator ** (5 / 2))
                    term3 = (5 * (6 * rrx_y - 6 * rtx_y) * (rtx_z - rrx_z + (2 * O) / (mu * sigma_ob * thick_ob)) * (
                            m_x * (rrx_x - rtx_x) + m_y * (rrx_y - rtx_y) - m_z * (
                                rtx_z - rrx_z + (2 * O) / (mu * sigma_ob * thick_ob)))) / (
                                    mu * sigma_ob * thick_ob * denominator ** (7 / 2))
                    dh_oby = factor * (term1 - term2 + term3)
                return dh_oby

            def calculate_dh_obz(rrx_z, rtx_z, rrx_x, rtx_x, rrx_y, rtx_y, O, mu, sigma_ob, thick_ob, m_x, m_y, m_z):
                factor = (-1 / (4 * math.pi))
                denominator = ((rrx_x - rtx_x) ** 2 + (rrx_y - rtx_y) ** 2 + (
                            rtx_z - rrx_z + (2 * O) / (mu * sigma_ob * thick_ob)) ** 2)
                if rrx_z > 0:
                    term1 = (6 * m_z * (rrx_z + rtx_z + (2 * O) / (mu * sigma_ob * thick_ob))) / (
                                mu * sigma_ob * thick_ob * denominator ** (5 / 2))
                    term2 = (6 * (m_x * (rrx_x - rtx_x) - m_z * (
                                rrx_z + rtx_z + (2 * O) / (mu * sigma_ob * thick_ob)) + m_y * (rrx_y - rtx_y))) / (
                                    mu * sigma_ob * thick_ob * denominator ** (5 / 2))
                    term3 = (m_z * (6 * rrx_z + 6 * rtx_z + (12 * O) / (mu * sigma_ob * thick_ob))) / (
                                mu * sigma_ob * thick_ob * denominator ** (5 / 2))
                    term4 = (5 * (6 * rrx_z + 6 * rtx_z + (12 * O) / (mu * sigma_ob * thick_ob)) * (
                                rrx_z + rtx_z + (2 * O) / (mu * sigma_ob * thick_ob)) * (
                                     m_x * (rrx_x - rtx_x) - m_z * (
                                         rrx_z + rtx_z + (2 * O) / (mu * sigma_ob * thick_ob)) + m_y * (
                                                 rrx_y - rtx_y))) / (
                                    mu * sigma_ob * thick_ob * denominator ** (7 / 2))
                    dh_obz = factor * (term1 - term2 + term3 + term4)
                else:
                    term1 = (6 * (m_x * (rrx_x - rtx_x) + m_y * (rrx_y - rtx_y) - m_z * (
                                rtx_z - rrx_z + (2 * O) / (mu * sigma_ob * thick_ob)))) / (
                                    mu * sigma_ob * thick_ob * denominator ** (5 / 2))
                    term2 = (m_z * (6 * rtx_z - 6 * rrx_z + (12 * O) / (mu * sigma_ob * thick_ob))) / (
                                mu * sigma_ob * thick_ob * denominator ** (5 / 2))
                    term3 = (6 * m_z * (rtx_z - rrx_z + (2 * O) / (mu * sigma_ob * thick_ob))) / (
                                mu * sigma_ob * thick_ob * denominator ** (5 / 2))
                    term4 = (5 * (6 * rtx_z - 6 * rrx_z + (12 * O) / (mu * sigma_ob * thick_ob)) * (
                                rtx_z - rrx_z + (2 * O) / (mu * sigma_ob * thick_ob)) * (
                                     m_x * (rrx_x - rtx_x) + m_y * (rrx_y - rtx_y) - m_z * (
                                         rtx_z - rrx_z + (2 * O) / (mu * sigma_ob * thick_ob)))) / (
                                    mu * sigma_ob * thick_ob * denominator ** (7 / 2))
                    dh_obz = factor * (term1 - term2 - term3 - term4)
                return dh_obz

            dh_obx = calculate_dh_obx(rrx_z, rtx_z, rrx_x, rtx_x, rrx_y, rtx_y, O, mu, sigma_ob, thick_ob, m_x, m_y,
                                      m_z)
            dh_oby = calculate_dh_oby(rrx_z, rtx_z, rrx_x, rtx_x, rrx_y, rtx_y, O, mu, sigma_ob, thick_ob, m_x, m_y,
                                      m_z)
            dh_obz = calculate_dh_obz(rrx_z, rtx_z, rrx_x, rtx_x, rrx_y, rtx_y, O, mu, sigma_ob, thick_ob, m_x, m_y,
                                      m_z)

            return np.array([dh_obx, dh_obz, dh_oby])

        def h_ob_xyz(mtx, dipole_m, rtx, rrx, O, mu, sigma_ob, thick_ob):
            """
            Function evaluates the x, y, z component of the overburden field
            See equations Eq A-3 from Desmarais and Smith, 2016. Geophysics 81(4), P. E265-E277
            """

            m_x = dipole_m * mtx[0]
            m_y = dipole_m * mtx[1]
            m_z = dipole_m * mtx[2]
            rtx_x = rtx[0]
            rtx_y = rtx[1]
            rtx_z = rtx[2]
            rrx_x = rrx[0]
            rrx_y = rrx[1]
            rrx_z = rrx[2]

            def calculate_h_obx(rrx_z, rtx_z, rrx_x, rtx_x, rrx_y, rtx_y, O, mu, sigma_ob, thick_ob, m_x, m_y, m_z):
                denominator = ((rrx_x - rtx_x) ** 2 + (rrx_y - rtx_y) ** 2 + (
                            rtx_z - rrx_z + (2 * O) / (mu * sigma_ob * thick_ob)) ** 2)
                factor = (-1 / (4 * math.pi))
                if rrx_z > 0:
                    h_obx = factor * (
                            m_x / (denominator ** (3 / 2)) -
                            (3 * (2 * rrx_x - 2 * rtx_x) * (m_x * (rrx_x - rtx_x) - m_z * (
                                        rrx_z + rtx_z + (2 * O) / (mu * sigma_ob * thick_ob)) + m_y * (
                                                                        rrx_y - rtx_y))) /
                            (2 * denominator ** (5 / 2))
                    )
                else:
                    h_obx = factor * (
                            m_x / (denominator ** (3 / 2)) -
                            (3 * (2 * rrx_x - 2 * rtx_x) * (m_x * (rrx_x - rtx_x) + m_y * (rrx_y - rtx_y) - m_z * (
                                        rtx_z - rrx_z + (2 * O) / (mu * sigma_ob * thick_ob)))) /
                            (2 * denominator ** (5 / 2))
                    )
                return h_obx

            def calculate_h_oby(rrx_z, rtx_z, rrx_x, rtx_x, rrx_y, rtx_y, O, mu, sigma_ob, thick_ob, m_x, m_y, m_z):
                denominator = ((rrx_x - rtx_x) ** 2 + (rrx_y - rtx_y) ** 2 + (
                            rtx_z - rrx_z + (2 * O) / (mu * sigma_ob * thick_ob)) ** 2)
                factor = (-1 / (4 * math.pi))
                if rrx_z > 0:
                    h_oby = factor * (
                            m_y / (denominator ** (3 / 2)) -
                            (3 * (2 * rrx_y - 2 * rtx_y) * (m_x * (rrx_x - rtx_x) - m_z * (
                                        rrx_z + rtx_z + (2 * O) / (mu * sigma_ob * thick_ob)) + m_y * (
                                                                        rrx_y - rtx_y))) /
                            (2 * denominator ** (5 / 2))
                    )
                else:
                    h_oby = factor * (
                            m_y / (denominator ** (3 / 2)) -
                            (3 * (2 * rrx_y - 2 * rtx_y) * (m_x * (rrx_x - rtx_x) + m_y * (rrx_y - rtx_y) - m_z * (
                                        rtx_z - rrx_z + (2 * O) / (mu * sigma_ob * thick_ob)))) /
                            (2 * denominator ** (5 / 2))
                    )
                return h_oby

            def calculate_h_obz(rrx_z, rtx_z, rrx_x, rtx_x, rrx_y, rtx_y, O, mu, sigma_ob, thick_ob, m_x, m_y, m_z):
                denominator = ((rrx_x - rtx_x) ** 2 + (rrx_y - rtx_y) ** 2 + (
                            rtx_z - rrx_z + (2 * O) / (mu * sigma_ob * thick_ob)) ** 2)
                factor = (-1 / (4 * math.pi))
                if rrx_z > 0:
                    h_obz = factor * (
                            -m_z / (denominator ** (3 / 2)) -
                            (3 * (2 * rrx_z + 2 * rtx_z + (4 * O) / (mu * sigma_ob * thick_ob)) * (
                                        m_x * (rrx_x - rtx_x) - m_z * (
                                            rrx_z + rtx_z + (2 * O) / (mu * sigma_ob * thick_ob)) + m_y * (
                                                    rrx_y - rtx_y))) /
                            (2 * denominator ** (5 / 2))
                    )
                else:
                    h_obz = factor * (
                            m_z / (denominator ** (3 / 2)) +
                            (3 * (2 * rtx_z - 2 * rrx_z + (4 * O) / (mu * sigma_ob * thick_ob)) * (
                                        m_x * (rrx_x - rtx_x) + m_y * (rrx_y - rtx_y) - m_z * (
                                            rtx_z - rrx_z + (2 * O) / (mu * sigma_ob * thick_ob)))) /
                            (2 * denominator ** (5 / 2))
                    )
                return h_obz

            h_obx = calculate_h_obx(rrx_z, rtx_z, rrx_x, rtx_x, rrx_y, rtx_y, O, mu, sigma_ob, thick_ob, m_x, m_y, m_z)
            h_oby = calculate_h_oby(rrx_z, rtx_z, rrx_x, rtx_x, rrx_y, rtx_y, O, mu, sigma_ob, thick_ob, m_x, m_y, m_z)
            h_obz = calculate_h_obz(rrx_z, rtx_z, rrx_x, rtx_x, rrx_y, rtx_y, O, mu, sigma_ob, thick_ob, m_x, m_y, m_z)

            return np.array([h_obx, h_obz, h_oby])




        def static(m, r):
            """
            Function calculates the field of a dipole
            see Eq A-5a from Desmarais and Smith, 2016. Geophysics 81(4), P. E265-E277
             m is the magnetic field vector
             r is the vector from the dipole to the field location
             m is the dipole moment vector
             multiply all components of mm by mu0 to get b field
            """
            one_over_4pi = 1 / (4 * math.pi)
            r2 = np.dot(r, r)
            if r2 < 1.e-20:
                h = 0.0
            else:
                a = one_over_4pi / (math.sqrt(r2) * r2)
                b = np.dot(r, m) * 3 / r2
                h = (b * r - m) * a
            return h



        def thetafunction_step(t, O, o, mu, sigma_sp, a, T):

            """
            Function calculates the time-dependant part of a step-response of the sphere alone
            see equations Eq 12-13 from Desmarais and Smith, 2016. Geophysics 81(4), P. E265-E277
            """

            ss = mu * sigma_sp * a * a
            theta = 0
            solver = 0
            k = 0

            while solver < 1:

                k = k + 1

                temp = (1 / (1 + np.exp(-(T/2) * ((k * math.pi) ** 2) / ( self.mu * self.sigma_sp * (self.a ** 2))))) * (
                            (6 / ((k * math.pi) ** 2)) * np.exp((o + O - t) * ((k * math.pi) ** 2) / (self.mu * self.sigma_sp *(self.a**2))))

                theta = theta + temp

                solver = np.linalg.lstsq(np.transpose(np.atleast_2d(temp)),np.transpose(np.atleast_2d(theta)),rcond=-1)[0]


            return theta

        def dh_tot_step(mtx, dipole_m, rtx, rsp, mu, sigma_ob, thick_ob, t, o, sigma_sp, a, T):
            """
            Function calculates the x, y, z component of the first-order induced moment at the sphere.
            See equations Eq 16 from Desmarais and Smith, 2016. Geophysics 81(4), P. E265-E277
            """

            s = 0.0
            b = t
            n = 10
            start_points = np.linspace(s, b, n, endpoint=False)
            h = (b - s) / n
            end_points = start_points + h
            intervals = np.array([start_points, end_points])

            ob_array = h_ob_xyz(mtx, dipole_m, rtx, rsp, -o, mu, sigma_ob, thick_ob)
            thetaz = thetafunction_step(t, 0, o, mu, sigma_sp, a, T)

            def my_function_x(x):
                return -dh_obdt_xyz(mtx, dipole_m, rtx, rsp, x, mu, sigma_ob, thick_ob)[0] * \
                    thetafunction_step(t, x, o, mu, sigma_sp, a, T)

            def my_function_z(x):
                return -dh_obdt_xyz(mtx, dipole_m, rtx, rsp, x, mu, sigma_ob, thick_ob)[1] * \
                    thetafunction_step(t, x, o, mu, sigma_sp, a, T)

            def my_function_y(x):
                return -dh_obdt_xyz(mtx, dipole_m, rtx, rsp, x, mu, sigma_ob, thick_ob)[2] * \
                    thetafunction_step(t, x, o, mu, sigma_sp, a, T)

            resultx, _ = fixed_quad(my_function_x, 0, t - o, n=100)
            resultz, _ = fixed_quad(my_function_z, 0, t - o, n=100)
            resulty, _ = fixed_quad(my_function_y, 0, t - o, n=100)

            return np.array([
                resultx + (ob_array[0] * thetaz),
                resultz + (ob_array[1] * thetaz),
                resulty + (ob_array[2] * thetaz)
            ])

        def h_total_step_1storder(
                mtx, dipole_m, rtx, offset_tx_rx, rsp, t, mu, sigma_ob, thick_ob, sigma_sp, a, P, apply_dip, dip,
                strike, wave, T):
            """
            Function checks if waveform is being convolved and calls previous functions to calculate sphere-overburden response.
            """

            def apply_dip_transform(msp, dip, strike):
                norm = np.array([
                    math.cos((90 - dip) * (math.pi / 180)) * math.cos((strike - 90) * (math.pi / 180)),
                    math.sin((strike - 90) * (math.pi / 180)) * math.cos((90 - dip) * (math.pi / 180)),
                    math.sin((90 - dip) * (math.pi / 180))
                ])
                norm /= np.linalg.norm(norm)
                return np.dot(msp, norm) * norm

            def calculate_statics(msp, offset_tx_rx, rtx, rsp):
                return static(msp, (np.array([-offset_tx_rx[0], -offset_tx_rx[1], rtx[2] - offset_tx_rx[2]]) -
                                    np.array([-rtx[0], -rtx[1], rsp[2]])))

            if hasattr(wave, "__len__"):
                N = len(wave)
                temp_xyz = 0
                tempy_xyz = 0
                H_xyz = 0

                for i in range(0, N - 1, 25):
                    temp_step = dh_tot_step(
                        mtx, dipole_m, [0, 0, rtx[2]], [-rtx[0], -rtx[1], rsp[2]], mu, sigma_ob, thick_ob, t,
                        (-P * (i - 1) / (N - 2)), sigma_sp, a, T
                    )

                    temp_xyz += 2 * math.pi * (a ** 3) * (P / 45) * (temp_step + temp_xyz) * (wave[i + 1] - wave[i]) / (
                                8.14 * 1e-6)
                    tempy_xyz = temp_xyz

                    H_xyz += (P / N) * h_ob_xyz(
                        mtx, dipole_m, [0, 0, rtx[2]], [-offset_tx_rx[0], -offset_tx_rx[1], rtx[2] - offset_tx_rx[2]],
                        t + (P * (i - 1) / (N - 2)), mu, sigma_ob, thick_ob
                    ) * (wave[i + 1] - wave[i]) / (8.14 * 1e-6)

                convo_x, convo_y, convo_z = temp_xyz

                msp = np.array([convo_x, convo_y, convo_z])

                if apply_dip == 1:
                    msp = apply_dip_transform(msp, dip, strike)

                statics = calculate_statics(msp, offset_tx_rx, rtx, rsp)

                H_tot_x = np.dot([1, 0, 0], statics) if self.xsign != "-ve" else -np.dot([1, 0, 0], statics)
                H_tot_z = np.dot([0, 0, 1], statics)
                H_tot_y = np.dot([0, 1, 0], statics)

                final_lst = np.array([
                    (H_tot_x + H_xyz[0]) if self.xsign== "-ve" else (-H_tot_x + H_xyz[0]),
                    -H_tot_z - H_xyz[1],
                    H_tot_y + H_xyz[2]
                ])

            else:
                temp = 2 * math.pi * (a ** 3) * dh_tot_step(
                    mtx, dipole_m, [0, 0, rtx[2]], [-rtx[0], -rtx[1], rsp[2]], mu, sigma_ob, thick_ob, t, 0, sigma_sp,
                    a, T
                )

                msp = np.array([temp[0], temp[2], temp[1]])

                if apply_dip == 1:
                    msp = apply_dip_transform(msp, dip, strike)

                statics = calculate_statics(msp, offset_tx_rx, rtx, rsp)

                H_tot_x = np.dot([1, 0, 0], statics) if self.xsign != "-ve" else -np.dot([1, 0, 0], statics)
                H_tot_z = np.dot([0, 0, 1], statics)
                H_tot_y = np.dot([0, 1, 0], statics)

                H_field = h_ob_xyz(
                    mtx, dipole_m, [0, 0, rtx[2]], [-offset_tx_rx[0], -offset_tx_rx[1], rtx[2] - offset_tx_rx[2]],
                    t, mu, sigma_ob, thick_ob
                )

                final_lst = np.array([
                    -(H_tot_x + H_field[0]) if self.xsign == "-ve" else H_tot_x + H_field[0],
                    H_tot_z - H_field[1],
                    H_tot_y - H_field[2]
                ])

            return final_lst

        if hasattr(self.wave, "__len__"):
            self.wc = self.windows
            self.nw = len(self.wc)
            self.H_tot_x = np.zeros((self.nw, self.interval))  # Response vectors
            self.H_tot_y = np.zeros((self.nw, self.interval))
            self.H_tot_z = np.zeros((self.nw, self.interval))

            self.C_x = np.zeros((self.nw, self.interval))  # Induced sphere moment vectors
            self.C_z = np.zeros((self.nw, self.interval))

            self.H_ob1 = np.zeros((self.nw, self.interval))  # Overburden response vectors
            self.H_ob2 = np.zeros((self.nw, self.interval))
            self.H_ob3 = np.zeros((self.nw, self.interval))

        self.delta_x = math.floor(abs(self.profile_length) / (self.interval - 1))

        for j in range(self.nw):  # iterate time
            i = -1
            t = self.wc[j]
            print(j)
            for x in range(-self.profile_length // 2, (self.profile_length // 2) + self.delta_x,
                           self.delta_x):  # iterate along profile
                i += 1
                if self.PlottingPoint == "Rx":
                    self.profile[0, i] = x - self.offset_tx_rx[0]
                elif self.PlottingPoint == "Tx":
                    self.profile[0, i] = x
                elif self.PlottingPoint == "Mid point":
                    self.profile[0, i] = x - (self.offset_tx_rx[0] / 2)

                self.rtx[0] = x
                self.rrx[0] = self.rtx[0] - self.offset_tx_rx[0]

                # calculate response
                response_array = h_total_step_1storder(
                    self.mtx, self.dipole_m, self.rtx, self.offset_tx_rx, self.rsp, t,
                    self.mu, self.sigma_ob, self.thick_ob, self.sigma_sp, self.a, self.P,
                    self.apply_dip, self.dip, self.strike, self.wave, self.T
                )

                self.H_tot_x[j, i] = (self.mu / 1e-12) * response_array[0]
                self.H_tot_z[j, i] = (self.mu / 1e-12) * response_array[1]
                self.H_tot_y[j, i] = (self.mu / 1e-12) * response_array[2]