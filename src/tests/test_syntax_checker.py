"""
Tests for syntax_checker class
"""
from main.syntax_checker import Syntax_Checker
import os

#Test 1:
# Tests that do_syntax_check reports an error 
# for a small program containing a syntax error
def test_error():
    checker = Syntax_Checker()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    target_file_path = os.path.join(current_dir, "../../data/syntax_checker/errors.py")
    absolute_file_path = os.path.abspath(target_file_path)
    checker.do_syntax_check(absolute_file_path)
    first_line = checker.message.split("\n")[0]

    assert first_line == "The code contains syntax errors. "

#Test 2:
# Tests that do_syntax_check does not report an error 
# for a small program containing only things giving warnings, not errors
def test_warnings():
    checker = Syntax_Checker()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    target_file_path = os.path.join(current_dir, "../../data/syntax_checker/only_warnings.py")
    absolute_file_path = os.path.abspath(target_file_path)
    checker.do_syntax_check(absolute_file_path)
    lines = checker.message.split("\n")
    first_line = lines[0] 
    second_line = lines[2]

    assert first_line == "The code passed the check with no syntax errors "
    assert second_line == "The following warnings and comments were found for the code "

#Test 3:
# Tests that do_syntax_check does not report an error 
# for a small program containing no syntax errors
def test_no_error():
    checker = Syntax_Checker()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    target_file_path = os.path.join(current_dir, "../../data/syntax_checker/no_error.py")
    absolute_file_path = os.path.abspath(target_file_path)
    checker.do_syntax_check(absolute_file_path)
    lines = checker.message.split("\n")
    first_line = lines[0]
    second_line = lines[2]

    assert first_line == "The code passed the check with no syntax errors "
    assert second_line == "The following warnings and comments were found for the code "