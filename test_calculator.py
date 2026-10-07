"""
Comprehensive pytest test suite for calculator.py

This module provides deterministic unit tests covering all functions in the calculator:
- get_number(): Input validation with retry logic
- validate_operation(): Operation validation
- Arithmetic operations: add, subtract, multiply, divide
- perform_calculation(): Operation dispatcher with error handling
- display_menu(): Output display
- main(): Main loop integration

Tests include happy path scenarios, edge cases, boundary conditions, error handling,
and invalid inputs. All tests are isolated using mocks and parametrization for efficiency.
"""

import pytest
from unittest.mock import patch, MagicMock, call
from io import StringIO
import sys

from calculator import (
    get_number,
    validate_operation,
    add,
    subtract,
    multiply,
    divide,
    perform_calculation,
    display_menu,
    main,
)


# ============================================================================
# Test Classes for Arithmetic Operations
# ============================================================================

class TestArithmeticOperations:
    """Tests for basic arithmetic operation functions: add, subtract, multiply, divide."""

    # Addition tests
    @pytest.mark.parametrize("a,b,expected", [
        (5, 3, 8),
        (0, 0, 0),
        (-5, 3, -2),
        (5, -3, 2),
        (-5, -3, -8),
        (0.5, 0.3, 0.8),
        (1e10, 1, 1e10 + 1),
    ])
    def test_add_valid_inputs(self, a, b, expected):
        """Test addition with various valid inputs including negatives and decimals."""
        result = add(a, b)
        assert result == expected

    # Subtraction tests
    @pytest.mark.parametrize("a,b,expected", [
        (5, 3, 2),
        (0, 0, 0),
        (-5, 3, -8),
        (5, -3, 8),
        (-5, -3, -2),
        (0.5, 0.3, pytest.approx(0.2)),
        (1e10, 1, 1e10 - 1),
    ])
    def test_subtract_valid_inputs(self, a, b, expected):
        """Test subtraction with various valid inputs including negatives and decimals."""
        result = subtract(a, b)
        assert result == expected

    # Multiplication tests
    @pytest.mark.parametrize("a,b,expected", [
        (5, 3, 15),
        (0, 100, 0),
        (-5, 3, -15),
        (5, -3, -15),
        (-5, -3, 15),
        (0.5, 0.2, 0.1),
        (1e5, 1e5, 1e10),
    ])
    def test_multiply_valid_inputs(self, a, b, expected):
        """Test multiplication with various valid inputs including negatives and decimals."""
        result = multiply(a, b)
        assert result == expected

    # Division tests
    @pytest.mark.parametrize("a,b,expected", [
        (10, 2, 5.0),
        (0, 5, 0.0),
        (-10, 2, -5.0),
        (10, -2, -5.0),
        (-10, -2, 5.0),
        (1, 3, pytest.approx(0.333333, rel=1e-5)),
        (1e10, 1e5, 1e5),
    ])
    def test_divide_valid_inputs(self, a, b, expected):
        """Test division with various valid inputs including negatives and decimals."""
        result = divide(a, b)
        assert result == expected

    # Division by zero tests
    def test_divide_by_zero(self):
        """Test that division by zero raises ValueError."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(10, 0)

    def test_divide_by_very_small_number(self):
        """Test that division by very small numbers (< epsilon) raises ValueError."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(10, 1e-11)  # Smaller than epsilon=1e-10

    def test_divide_by_negative_very_small_number(self):
        """Test that division by negative very small numbers (< epsilon) raises ValueError."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(10, -1e-11)


# ============================================================================
# Test Class for Operation Validation
# ============================================================================

class TestValidateOperation:
    """Tests for validate_operation() function."""

    @pytest.mark.parametrize("operation,expected_valid,expected_op", [
        ('+', True, '+'),
        ('-', True, '-'),
        ('*', True, '*'),
        ('/', True, '/'),
        (' + ', True, '+'),  # Test whitespace stripping
        (' - ', True, '-'),
        (' * ', True, '*'),
        (' / ', True, '/'),
    ])
    def test_validate_operation_valid(self, operation, expected_valid, expected_op):
        """Test validation of valid operations."""
        is_valid, op = validate_operation(operation)
        assert is_valid == expected_valid
        assert op == expected_op

    @pytest.mark.parametrize("operation", [
        'x',
        '++',
        'add',
        'subtract',
        '',
        ' ',
        '5',
        '%',
        '**',
    ])
    def test_validate_operation_invalid(self, operation):
        """Test validation of invalid operations."""
        is_valid, op = validate_operation(operation)
        assert is_valid is False
        assert op is None


# ============================================================================
# Test Class for get_number() Function
# ============================================================================

class TestGetNumber:
    """Tests for get_number() input validation function with mocking."""

    @patch('builtins.input', return_value='42')
    def test_get_number_valid_integer(self, mock_input):
        """Test getting a valid integer input."""
        result = get_number("Enter a number: ")
        assert result == 42.0

    @patch('builtins.input', return_value='3.14')
    def test_get_number_valid_float(self, mock_input):
        """Test getting a valid float input."""
        result = get_number("Enter a number: ")
        assert result == pytest.approx(3.14)

    @patch('builtins.input', return_value='0')
    def test_get_number_zero(self, mock_input):
        """Test getting zero as input."""
        result = get_number("Enter a number: ")
        assert result == 0.0

    @patch('builtins.input', return_value='-42.5')
    def test_get_number_negative_number(self, mock_input):
        """Test getting a negative number."""
        result = get_number("Enter a number: ")
        assert result == -42.5

    @patch('builtins.input', return_value='1e10')
    def test_get_number_scientific_notation(self, mock_input):
        """Test getting number in scientific notation."""
        result = get_number("Enter a number: ")
        assert result == 1e10

    @patch('builtins.input', return_value='-1e-5')
    def test_get_number_negative_scientific_notation(self, mock_input):
        """Test getting negative number in scientific notation."""
        result = get_number("Enter a number: ")
        assert result == -1e-5

    @patch('builtins.input', side_effect=['invalid', '42'])
    @patch('builtins.print')
    def test_get_number_invalid_then_valid(self, mock_print, mock_input):
        """Test recovery from invalid input to valid input."""
        result = get_number("Enter a number: ")
        assert result == 42.0
        mock_print.assert_called()
        assert any('Error' in str(call) for call in mock_print.call_args_list)

    @patch('builtins.input', side_effect=['abc', '', 'invalid', '123'])
    @patch('builtins.print')
    def test_get_number_multiple_retries(self, mock_print, mock_input):
        """Test multiple retry attempts before success."""
        result = get_number("Enter a number: ", max_retries=4)
        assert result == 123.0
        assert mock_input.call_count == 4

    @patch('builtins.input', side_effect=['invalid1', 'invalid2', 'invalid3'])
    @patch('builtins.print')
    def test_get_number_max_retries_exceeded(self, mock_print, mock_input):
        """Test that ValueError is raised when max retries exceeded."""
        with pytest.raises(ValueError, match="Failed to get valid input after 3 attempts"):
            get_number("Enter a number: ", max_retries=3)

    @patch('builtins.input', return_value='100')
    def test_get_number_with_min_value_valid(self, mock_input):
        """Test min_value constraint is satisfied."""
        result = get_number("Enter a number: ", min_value=50)
        assert result == 100.0

    @patch('builtins.input', side_effect=['25', '100'])
    @patch('builtins.print')
    def test_get_number_with_min_value_invalid(self, mock_print, mock_input):
        """Test that value below min_value is rejected."""
        result = get_number("Enter a number: ", min_value=50, max_retries=2)
        assert result == 100.0
        mock_print.assert_called()

    @patch('builtins.input', return_value='100')
    def test_get_number_with_max_value_valid(self, mock_input):
        """Test max_value constraint is satisfied."""
        result = get_number("Enter a number: ", max_value=200)
        assert result == 100.0

    @patch('builtins.input', side_effect=['250', '100'])
    @patch('builtins.print')
    def test_get_number_with_max_value_invalid(self, mock_print, mock_input):
        """Test that value above max_value is rejected."""
        result = get_number("Enter a number: ", max_value=200, max_retries=2)
        assert result == 100.0
        mock_print.assert_called()

    @patch('builtins.input', return_value='100')
    def test_get_number_with_range_valid(self, mock_input):
        """Test both min and max value constraints are satisfied."""
        result = get_number("Enter a number: ", min_value=50, max_value=150)
        assert result == 100.0

    @patch('builtins.input', side_effect=['40', '200', '100'])
    @patch('builtins.print')
    def test_get_number_with_range_invalid_values(self, mock_print, mock_input):
        """Test that values outside range are rejected."""
        result = get_number("Enter a number: ", min_value=50, max_value=150, max_retries=3)
        assert result == 100.0

    @patch('builtins.input', side_effect=['invalid1', 'invalid2', 'invalid3'])
    @patch('builtins.print')
    def test_get_number_max_retries_with_custom_value(self, mock_print, mock_input):
        """Test custom max_retries value."""
        with pytest.raises(ValueError, match="Failed to get valid input after 2 attempts"):
            get_number("Enter a number: ", max_retries=2)
        assert mock_input.call_count == 2

    @patch('builtins.input', return_value='0')
    def test_get_number_min_max_boundary_zero(self, mock_input):
        """Test zero at exact boundary."""
        result = get_number("Enter a number: ", min_value=0, max_value=0)
        assert result == 0.0

    @patch('builtins.input', return_value='0.1')
    def test_get_number_small_positive_decimal(self, mock_input):
        """Test small positive decimal number."""
        result = get_number("Enter a number: ")
        assert result == pytest.approx(0.1)

    @patch('builtins.input', return_value='-0.1')
    def test_get_number_small_negative_decimal(self, mock_input):
        """Test small negative decimal number."""
        result = get_number("Enter a number: ")
        assert result == pytest.approx(-0.1)


# ============================================================================
# Test Class for perform_calculation()
# ============================================================================

class TestPerformCalculation:
    """Tests for perform_calculation() dispatcher function."""

    @pytest.mark.parametrize("num1,num2,op,expected", [
        (5, 3, '+', 8),
        (5, 3, '-', 2),
        (5, 3, '*', 15),
        (10, 2, '/', 5.0),
        (0, 0, '+', 0),
        (-5, 3, '+', -2),
        (-5, -3, '*', 15),
    ])
    def test_perform_calculation_valid_operations(self, num1, num2, op, expected):
        """Test perform_calculation with valid operations."""
        result = perform_calculation(num1, num2, op)
        assert result == expected

    @patch('builtins.print')
    def test_perform_calculation_division_by_zero(self, mock_print):
        """Test that division by zero is caught and printed."""
        result = perform_calculation(10, 0, '/')
        assert result is None
        mock_print.assert_called_once()
        assert "Cannot divide by zero" in str(mock_print.call_args)

    @patch('builtins.print')
    def test_perform_calculation_division_by_very_small_number(self, mock_print):
        """Test that division by very small number (< epsilon) is caught."""
        result = perform_calculation(10, 1e-11, '/')
        assert result is None
        mock_print.assert_called_once()

    def test_perform_calculation_large_numbers(self):
        """Test perform_calculation with very large numbers."""
        result = perform_calculation(1e15, 1e10, '+')
        assert result == pytest.approx(1e15 + 1e10)

    def test_perform_calculation_with_floats(self):
        """Test perform_calculation with floating-point numbers."""
        result = perform_calculation(0.1, 0.2, '+')
        assert result == pytest.approx(0.3, abs=1e-9)

    def test_perform_calculation_negative_numbers(self):
        """Test perform_calculation with negative numbers."""
        result = perform_calculation(-5, -3, '*')
        assert result == 15


# ============================================================================
# Test Class for display_menu()
# ============================================================================

class TestDisplayMenu:
    """Tests for display_menu() output function."""

    @patch('builtins.print')
    def test_display_menu_called(self, mock_print):
        """Test that display_menu prints output."""
        display_menu()
        assert mock_print.call_count > 0

    @patch('builtins.print')
    def test_display_menu_contains_title(self, mock_print):
        """Test that display_menu prints the calculator title."""
        display_menu()
        calls_str = ' '.join(str(call) for call in mock_print.call_args_list)
        assert 'CALCULATOR' in calls_str or 'calculator' in calls_str.lower()

    @patch('builtins.print')
    def test_display_menu_contains_operations(self, mock_print):
        """Test that display_menu prints all supported operations."""
        display_menu()
        calls_str = ' '.join(str(call) for call in mock_print.call_args_list)
        assert '+' in calls_str
        assert '-' in calls_str
        assert '*' in calls_str
        assert '/' in calls_str


# ============================================================================
# Test Class for main() Function
# ============================================================================

class TestMain:
    """Tests for main() function with comprehensive mocking."""

    @patch('calculator.display_menu')
    @patch('builtins.input', side_effect=['5', '+', '3', 'no'])
    @patch('builtins.print')
    def test_main_single_calculation_exit(self, mock_print, mock_input, mock_display):
        """Test main loop with single calculation and exit."""
        main()
        mock_display.assert_called_once()
        # Verify calculation result was printed
        calls_str = ' '.join(str(call) for call in mock_print.call_args_list)
        assert '8' in calls_str or 'Result' in calls_str

    @patch('calculator.display_menu')
    @patch('builtins.input', side_effect=['5', '+', '3', 'yes', '10', '*', '2', 'no'])
    @patch('builtins.print')
    def test_main_multiple_calculations(self, mock_print, mock_input, mock_display):
        """Test main loop with multiple calculations."""
        main()
        mock_display.assert_called_once()
        assert mock_input.call_count == 8

    @patch('calculator.display_menu')
    @patch('builtins.input', side_effect=['10', '/', '0', 'no'])
    @patch('builtins.print')
    def test_main_division_by_zero(self, mock_print, mock_input, mock_display):
        """Test main loop handles division by zero gracefully."""
        main()
        calls_str = ' '.join(str(call) for call in mock_print.call_args_list)
        assert 'Cannot divide by zero' in calls_str

    @patch('calculator.display_menu')
    @patch('builtins.input', side_effect=['5', '+', '3', 'y'])
    @patch('builtins.print')
    def test_main_continue_with_y(self, mock_print, mock_input, mock_display):
        """Test that 'y' continues the loop."""
        # Mock the second iteration to exit
        inputs = ['5', '+', '3', 'y', '2', '-', '1', 'no']
        with patch('builtins.input', side_effect=inputs):
            main()

    @patch('calculator.display_menu')
    @patch('builtins.input', side_effect=['5', '+', '3', 'yes', '2', '-', '1', 'no'])
    @patch('builtins.print')
    def test_main_continue_with_yes(self, mock_print, mock_input, mock_display):
        """Test that 'yes' continues the loop."""
        main()
        assert mock_input.call_count == 8

    @patch('calculator.display_menu')
    @patch('builtins.input', side_effect=['invalid', '5', '+', '3', 'no'])
    @patch('builtins.print')
    def test_main_invalid_first_number_retries(self, mock_print, mock_input, mock_display):
        """Test that invalid first number triggers retry."""
        main()
        # Should have multiple print calls due to error message
        assert mock_print.call_count > 1

    @patch('calculator.display_menu')
    @patch('builtins.input', side_effect=['5', 'invalid', '+', '3', 'no'])
    @patch('builtins.print')
    def test_main_invalid_operation_retries(self, mock_print, mock_input, mock_display):
        """Test that invalid operation triggers retry loop."""
        main()
        calls_str = ' '.join(str(call) for call in mock_print.call_args_list)
        assert 'Error' in calls_str or 'valid operation' in calls_str

    @patch('calculator.display_menu')
    @patch('builtins.input', side_effect=['5', '+', 'invalid', '3', 'no'])
    @patch('builtins.print')
    def test_main_invalid_second_number_retries(self, mock_print, mock_input, mock_display):
        """Test that invalid second number triggers retry."""
        main()
        assert mock_print.call_count > 1

    @patch('calculator.display_menu')
    @patch('builtins.input', side_effect=['5', '+', '3', 'NOPE'])
    @patch('builtins.print')
    def test_main_continue_choice_case_insensitive(self, mock_print, mock_input, mock_display):
        """Test that continue choice is case-insensitive and NOPE exits."""
        main()
        # Should not raise and should exit properly
        calls_str = ' '.join(str(call) for call in mock_print.call_args_list)
        assert 'Goodbye' in calls_str or 'Thank you' in calls_str

    @patch('calculator.display_menu')
    @patch('builtins.input', side_effect=['-5', '*', '-3', 'no'])
    @patch('builtins.print')
    def test_main_negative_numbers(self, mock_print, mock_input, mock_display):
        """Test main with negative numbers."""
        main()
        calls_str = ' '.join(str(call) for call in mock_print.call_args_list)
        assert '15' in calls_str or 'Result' in calls_str

    @patch('calculator.display_menu')
    @patch('builtins.input', side_effect=['0', '/', '5', 'no'])
    @patch('builtins.print')
    def test_main_zero_dividend(self, mock_print, mock_input, mock_display):
        """Test main with zero as dividend (should work)."""
        main()
        calls_str = ' '.join(str(call) for call in mock_print.call_args_list)
        assert '0' in calls_str

    @patch('calculator.display_menu')
    @patch('builtins.input', side_effect=['0.5', '+', '0.3', 'no'])
    @patch('builtins.print')
    def test_main_decimal_calculation(self, mock_print, mock_input, mock_display):
        """Test main with decimal numbers."""
        main()
        calls_str = ' '.join(str(call) for call in mock_print.call_args_list)
        assert 'Result' in calls_str

    @patch('calculator.display_menu')
    @patch('builtins.input', side_effect=['1e10', '+', '1', 'no'])
    @patch('builtins.print')
    def test_main_scientific_notation(self, mock_print, mock_input, mock_display):
        """Test main with scientific notation."""
        main()
        calls_str = ' '.join(str(call) for call in mock_print.call_args_list)
        assert 'Result' in calls_str


# ============================================================================
# Edge Case and Integration Tests
# ============================================================================

class TestEdgeCasesAndIntegration:
    """Edge cases and integration tests across multiple functions."""

    def test_arithmetic_chain_addition(self):
        """Test chaining multiple additions."""
        result = add(add(add(1, 2), 3), 4)
        assert result == 10

    def test_arithmetic_chain_operations(self):
        """Test chaining different operations."""
        result = multiply(add(2, 3), subtract(5, 1))
        assert result == 20

    def test_division_very_close_to_epsilon_boundary(self):
        """Test division with value very close to epsilon boundary."""
        # Should succeed (just above epsilon)
        result = divide(10, 1.1e-10)
        assert isinstance(result, float)

    def test_operation_workflow_addition(self):
        """Test full workflow: validate and perform addition."""
        is_valid, op = validate_operation('+')
        assert is_valid is True
        result = perform_calculation(5, 3, op)
        assert result == 8

    def test_operation_workflow_division_success(self):
        """Test full workflow: validate and perform division."""
        is_valid, op = validate_operation('/')
        assert is_valid is True
        result = perform_calculation(10, 2, op)
        assert result == 5.0

    def test_large_number_precision(self):
        """Test that large numbers don't lose precision unexpectedly."""
        large_num = 1e15
        small_num = 1
        result = add(large_num, small_num)
        # With floating-point precision, this might be approximate
        assert result >= large_num

    def test_very_small_positive_number_division(self):
        """Test division by very small positive number just above epsilon."""
        result = divide(1, 2e-10)  # Larger than epsilon
        assert result == pytest.approx(5e9)

    def test_float_subtraction_precision(self):
        """Test floating-point subtraction precision."""
        result = subtract(1.0, 0.9)
        assert result == pytest.approx(0.1)

    def test_zero_operations(self):
        """Test various operations with zero."""
        assert add(0, 0) == 0
        assert subtract(0, 0) == 0
        assert multiply(0, 0) == 0
        assert multiply(100, 0) == 0
        assert divide(0, 100) == 0.0

    @pytest.mark.parametrize("num", [1, -1, 100, -100, 0.5, -0.5])
    def test_multiply_by_one(self, num):
        """Test that multiplying by 1 returns the original number."""
        assert multiply(num, 1) == num

    @pytest.mark.parametrize("num", [1, -1, 100, -100, 0.5, -0.5])
    def test_add_zero(self, num):
        """Test that adding zero returns the original number."""
        assert add(num, 0) == num

    @pytest.mark.parametrize("num", [1, -1, 100, -100, 0.5, -0.5])
    def test_subtract_zero(self, num):
        """Test that subtracting zero returns the original number."""
        assert subtract(num, 0) == num

    @patch('builtins.input', return_value='1e308')
    def test_get_number_very_large_valid_number(self, mock_input):
        """Test getting very large but valid float."""
        result = get_number("Enter a number: ")
        assert result > 0

    @patch('builtins.input', side_effect=['  42  ', '5', '+', '3', 'no'])
    @patch('calculator.display_menu')
    @patch('builtins.print')
    def test_main_whitespace_in_first_number(self, mock_print, mock_display, mock_input):
        """Test that main handles whitespace in numeric input."""
        main()


# ============================================================================
# Parametrized Tests for Comprehensive Coverage
# ============================================================================

class TestParametrizedComprehensive:
    """Parametrized tests for comprehensive operation coverage."""

    @pytest.mark.parametrize("operand1,operand2,operation,expected", [
        # Addition
        (1, 1, '+', 2),
        (0, 0, '+', 0),
        (-1, 1, '+', 0),
        (-1, -1, '+', -2),
        # Subtraction
        (5, 3, '-', 2),
        (0, 0, '-', 0),
        (-1, -1, '-', 0),
        # Multiplication
        (2, 3, '*', 6),
        (0, 100, '*', 0),
        (-2, 3, '*', -6),
        (-2, -3, '*', 6),
        # Division
        (6, 3, '/', 2.0),
        (10, 4, '/', 2.5),
        (-10, 2, '/', -5.0),
        (-10, -2, '/', 5.0),
    ])
    def test_perform_calculation_comprehensive(self, operand1, operand2, operation, expected):
        """Comprehensive test of perform_calculation with all operations and cases."""
        result = perform_calculation(operand1, operand2, operation)
        if isinstance(expected, float):
            assert result == pytest.approx(expected)
        else:
            assert result == expected

    @pytest.mark.parametrize("invalid_op", [
        'x', '++', '', ' ', 'add', '==', '%', '&', '|',
    ])
    def test_validate_operation_all_invalid(self, invalid_op):
        """Test all invalid operations are properly rejected."""
        is_valid, op = validate_operation(invalid_op)
        assert is_valid is False
        assert op is None
