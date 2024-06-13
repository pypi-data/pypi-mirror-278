import unittest

from glom import glom
from levels import levels


class TestLevels(unittest.TestCase):
    def setUp(self):
        self.nested_dict = {
            "a": {"b": {"c": 1, "d": 2}, "e": 3},
            "f": {"g": {"h": [4, 5]}},
        }

    def test_depth_0(self):
        result = list(levels(self.nested_dict, 0))
        self.assertEqual(result, [("['a']", "{...}"), ("['f']", "{...}")])

    def test_depth_1(self):
        result = list(levels(self.nested_dict, 1))
        self.assertEqual(
            result,
            [("['a']['b']", "{...}"), ("['a']['e']", 3), ("['f']['g']", "{...}")],
        )

    def test_depth_2(self):
        result = list(levels(self.nested_dict, 2))
        self.assertEqual(
            result,
            [
                ("['a']['b']['c']", 1),
                ("['a']['b']['d']", 2),
                ("['f']['g']['h']", "[...]"),
            ],
        )

    def test_values_true(self):
        result = list(levels(self.nested_dict, 2, values=True))
        self.assertEqual(
            result,
            [
                ("['a']['b']['c']", 1),
                ("['a']['b']['d']", 2),
                ("['f']['g']['h']", [4, 5]),
            ],
        )

    def test_as_glom_true(self):
        result = list(levels(self.nested_dict, 2, as_glom=True))
        self.assertEqual(result, [("a.b.c", 1), ("a.b.d", 2), ("f.g.h", "[...]")])

    def test_with_glom(self):
        result = list(levels(self.nested_dict, 2, as_glom=True, values=True))
        for path, value in result:
            self.assertEqual(value, glom(self.nested_dict, path))


if __name__ == "__main__":
    unittest.main()
