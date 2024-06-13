import unittest
from grid_utils.gridder import GribGridder
from grid_utils.exceptions import OutOfGridBound


class TestGribGridder(unittest.TestCase):
    def test_nx_ny(self):
        g1 = GribGridder(resolution='1p00')
        self.assertEqual(g1.nx, 360)
        self.assertEqual(g1.ny, 181)

        g2 = GribGridder(resolution='0p50')
        self.assertEqual(g2.nx, 720)
        self.assertEqual(g2.ny, 361)

        g3 = GribGridder(resolution='0p25')
        self.assertEqual(g3.nx, 1440)
        self.assertEqual(g3.ny, 721)

        g4 = GribGridder(resolution='0p125')
        self.assertEqual(g4.nx, 2880)
        self.assertEqual(g4.ny, 1441)

        g5 = GribGridder(resolution='0p1')
        self.assertEqual(g5.nx, 3600)
        self.assertEqual(g5.ny, 1801)

    def test_i2x(self):
        g1 = GribGridder(resolution='1p00')
        self.assertTupleEqual(g1.i2x(0, 0), (0, 90))
        self.assertTupleEqual(g1.i2x(359, 180), (359, -90))

        with self.assertRaises(OutOfGridBound):
            g1.i2x(-1, 0)

        with self.assertRaises(OutOfGridBound):
            g1.i2x(0, -1)

        with self.assertRaises(OutOfGridBound):
            g1.i2x(360, 0)

        with self.assertRaises(OutOfGridBound):
            g1.i2x(0, 181)

        g2 = GribGridder(resolution='0p25')
        self.assertTupleEqual(g2.i2x(1439, 720), (359.75, -90))

    def test_x2i(self):
        g1 = GribGridder(resolution='1p00')
        self.assertTupleEqual(g1.x2i(359.6, 90-0.499), (0, 0))
        self.assertTupleEqual(g1.x2i(359.4, 90-0.501), (359, 1))

        self.assertTupleEqual(g1.x2i(-0.4, 85.2), (0, 5))
        self.assertTupleEqual(g1.x2i(359, -90), (359, 180))

    def test_copy(self):
        g1 = GribGridder(resolution='0p50')
        g2 = g1.copy()
        self.assertEqual(g1.resolution, g2.resolution)
        self.assertEqual(g1._float_res, g2._float_res)
        self.assertEqual(g1.nx, g2.nx)
        self.assertEqual(g1.ny, g2.ny)


if __name__ == '__main__':
    unittest.main()
