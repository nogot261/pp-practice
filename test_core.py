"""Короткая проверка основных функций четырех заданий."""
import unittest
from exercise_1 import build_frequency_lines
from exercise_2 import execute, new_accounts
from exercise_3 import calculate_expression
from exercise_4 import build_plan, state_after
from student_config import DISPLAY_ROWS, MEMORY_SLOTS, CALCULATOR_FUNCTIONS, PERCENTAGES

class Tests(unittest.TestCase):
    def test_1(self):
        self.assertEqual(build_frequency_lines(["b", "a", "b"]), ["b 2", "a 1"])

    def test_2(self):
        accounts = new_accounts()
        self.assertEqual(execute(accounts, "BALANCE Stepanova"), ["Stepanova 70205412"])
        with self.assertRaises(ValueError):
            execute(accounts, "deposit A 1")

    def test_3(self):
        self.assertEqual((DISPLAY_ROWS, MEMORY_SLOTS), (5, 7))
        self.assertEqual(CALCULATOR_FUNCTIONS, ["dms", "10^x", "pi", "tanh", "ln"])
        self.assertEqual(calculate_expression("2+3*4"), 14.0)

    def test_4(self):
        moves = build_plan()
        self.assertEqual((PERCENTAGES, len(moves)), ([70, 20, 54, 12], 76))
        end = state_after(76, moves)
        self.assertEqual(len(end[1]), 21)
        self.assertTrue(all(not end[peg] for peg in range(2, 9)))

if __name__ == "__main__":
    unittest.main(verbosity=2)
