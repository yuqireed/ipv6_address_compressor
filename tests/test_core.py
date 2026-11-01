import unittest

from ipv6_address_compressor import compress, expand, is_valid


class CompressTests(unittest.TestCase):
    def test_all_zero(self):
        self.assertEqual(compress("0:0:0:0:0:0:0:0"), "::")

    def test_loopback(self):
        self.assertEqual(compress("0000:0000:0000:0000:0000:0000:0000:0001"), "::1")

    def test_full_address_no_zeros(self):
        self.assertEqual(
            compress("2001:0db8:85a3:0000:0000:8a2e:0370:7334"),
            "2001:db8:85a3::8a2e:370:7334",
        )

    def test_leftmost_longest_run_wins(self):
        # Two runs of two zeros each: the left one must be compressed.
        self.assertEqual(compress("2001:0:0:1:0:0:0:1"), "2001:0:0:1::1")

    def test_single_zero_group_is_not_compressed(self):
        self.assertEqual(
            compress("2001:db8:0:1:1:1:1:1"),
            "2001:db8:0:1:1:1:1:1",
        )

    def test_uppercase_input_is_lowercased(self):
        self.assertEqual(compress("2001:DB8::1"), "2001:db8::1")

    def test_embedded_ipv4_tail(self):
        self.assertEqual(compress("::ffff:192.0.2.128"), "::ffff:192.0.2.128")

    def test_already_canonical_is_idempotent(self):
        canonical = "2001:db8::1"
        self.assertEqual(compress(canonical), canonical)

    def test_malformed_raises_value_error(self):
        with self.assertRaises(ValueError):
            compress("2001:db8:::1")

    def test_non_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            compress(12345)  # type: ignore[arg-type]


class ExpandTests(unittest.TestCase):
    def test_loopback(self):
        self.assertEqual(
            expand("::1"),
            "0000:0000:0000:0000:0000:0000:0000:0001",
        )

    def test_round_trip(self):
        original = "2001:db8:85a3::8a2e:370:7334"
        self.assertEqual(compress(expand(original)), original)


class IsValidTests(unittest.TestCase):
    def test_accepts_valid(self):
        self.assertTrue(is_valid("2001:db8::1"))

    def test_rejects_invalid(self):
        self.assertFalse(is_valid("not an address"))

    def test_rejects_non_string(self):
        self.assertFalse(is_valid(None))


if __name__ == "__main__":
    unittest.main()
