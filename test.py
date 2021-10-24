import unittest

from main import execute_program


class TestPush(unittest.TestCase):

    def test_positive(self):
        program = "42"
        result = execute_program(program)
        self.assertEqual(result, 42, "Could not push positive integer")

    def test_negative(self):
        program = "-13"
        result = execute_program(program)
        self.assertEqual(result, -13, "Could not push negative integer")

    def test_excessive_spaces(self):
        program = "       69       "
        result = execute_program(program)
        self.assertEqual(result, 69, "Could not push integer with excessive spaces")

    def test_extra_on_stack(self):
        program = "42 69"
        self.assertRaises(ValueError, execute_program, program)

    def test_empty(self):
        program = ""
        self.assertRaises(ValueError, execute_program, program)

    def test_nonnum_push(self):
        program = " рофель "
        self.assertRaises(ValueError, execute_program, program)


class TestAddition(unittest.TestCase):

    def test_add_positives(self):
        program = "27 42 +"
        result = execute_program(program)
        self.assertEqual(result, 69, "Could not add two positive integers")

    def test_add_negatives(self):
        program = "-56 -13 +"
        result = execute_program(program)
        self.assertEqual(result, -69, "Could not add two negative integers")

    def test_add_pos_neg(self):
        program = "100 -31 +"
        result = execute_program(program)
        self.assertEqual(result, 69, "Could not add negative to positive integer")

    def test_add_neg_pos(self):
        program = "-42 111 +"
        result = execute_program(program)
        self.assertEqual(result, 69, "Could not add positive to negative integer")

    def test_add_excessive_spaces(self):
        program = " 228  192     + "
        result = execute_program(program)
        self.assertEqual(result, 420, "Could not add integers with excessive spaces")

    def test_add_not_enough_nums(self):
        program = "42 +"
        self.assertRaises(ValueError, execute_program, program)

    def test_add_extra_nums(self):
        program = "228 69 42 +"
        self.assertRaises(ValueError, execute_program, program)


class TestSubtraction(unittest.TestCase):

    def test_sub_positives(self):
        program = "69 27 -"
        result = execute_program(program)
        self.assertEqual(result, 42, "Could not subtract two positive integers")

    def test_sub_negatives(self):
        program = "-111 -69 -"
        result = execute_program(program)
        self.assertEqual(result, -42, "Could not subtract two negative integers")

    def test_sub_pos_neg(self):
        program = "56 -13 -"
        result = execute_program(program)
        self.assertEqual(result, 69, "Could not subtract negative from positive integer")

    def test_sub_neg_pos(self):
        program = "-42 27 -"
        result = execute_program(program)
        self.assertEqual(result, -69, "Could not subtract positive from negative integer")

    def test_sub_excessive_spaces(self):
        program = " 420  192     - "
        result = execute_program(program)
        self.assertEqual(result, 228, "Could not subtract integers with excessive spaces")

    def test_sub_not_enough_nums(self):
        program = "42 -"
        self.assertRaises(ValueError, execute_program, program)

    def test_sub_extra_nums(self):
        program = "228 69 42 -"
        self.assertRaises(ValueError, execute_program, program)


class TestMultiplication(unittest.TestCase):

    def test_mul_positives(self):
        program = "23 3 *"
        result = execute_program(program)
        self.assertEqual(result, 69, "Could not multiply two positive integers")

    def test_mul_negatives(self):
        program = "-21 -2 *"
        result = execute_program(program)
        self.assertEqual(result, 42, "Could not multiply two negative integers")

    def test_mul_pos_neg(self):
        program = "57 -4 *"
        result = execute_program(program)
        self.assertEqual(result, -228, "Could not multiply negative and positive integer")

    def test_mul_neg_pos(self):
        program = "-42 10 *"
        result = execute_program(program)
        self.assertEqual(result, -420, "Could not multiply positive and negative integer")

    def test_mul_excessive_spaces(self):
        program = " 191  7     * "
        result = execute_program(program)
        self.assertEqual(result, 1337, "Could not multiply integers with excessive spaces")

    def test_mul_not_enough_nums(self):
        program = "42 *"
        self.assertRaises(ValueError, execute_program, program)

    def test_mul_extra_nums(self):
        program = "228 69 42 *"
        self.assertRaises(ValueError, execute_program, program)


class TestDivision(unittest.TestCase):

    def test_div_positives(self):
        program = "207 3 //"
        result = execute_program(program)
        self.assertEqual(result, 69, "Could not divide two positive integers")

    def test_div_negatives(self):
        program = "-294 -7 //"
        result = execute_program(program)
        self.assertEqual(result, 42, "Could not divide two negative integers")

    def test_div_pos_neg(self):
        program = "228 -4 //"
        result = execute_program(program)
        self.assertEqual(result, -57, "Could not divide positive by negative integer")

    def test_div_neg_pos(self):
        program = "-420 60 //"
        result = execute_program(program)
        self.assertEqual(result, -7, "Could not divide negative by positive integer")

    def test_div_excessive_spaces(self):
        program = " 621  9     // "
        result = execute_program(program)
        self.assertEqual(result, 69, "Could not divide integers with excessive spaces")

    def test_div_not_enough_nums(self):
        program = "42 //"
        self.assertRaises(ValueError, execute_program, program)

    def test_div_extra_nums(self):
        program = "228 69 42 //"
        self.assertRaises(ValueError, execute_program, program)


class TestPrograms(unittest.TestCase):

    def test_1(self):
        program = "7 2 3 * -"
        result = execute_program(program)
        self.assertEqual(result, 1, "Program-test №1 didn't pass")

    def test_2(self):
        program = "1 2 + 4 * 3 +"
        result = execute_program(program)
        self.assertEqual(result, 15, "Program-test №2 didn't pass")

    def test_complex(self):
        program = "3 6 3 * 1 4 - 2 ^ // +"
        result = execute_program(program)
        self.assertEqual(result, 5, "Program-test complex didn't pass")

    def test_similar(self):
        program = "10 15 - 3 *"
        result1 = execute_program(program)
        program = "3 10 15 - *"
        result2 = execute_program(program)

        self.assertEqual(result1, result2, "Results of similar programs are not equal")
        self.assertEqual(result1,     -15, "test_similar() calculations are invalid")
