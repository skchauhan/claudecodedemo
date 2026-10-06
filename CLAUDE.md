# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a simple Python console calculator application that performs basic arithmetic operations. The codebase is a single-file project with straightforward functionality for addition, subtraction, multiplication, and division.

## Running the Application

**Run the calculator:**
```bash
python calculator.py
```

The calculator runs in an interactive loop, prompting the user for:
1. First number (validated as float)
2. Operation (+, -, *, /)
3. Second number
4. Continue/exit choice

## Code Structure

**calculator.py** contains:
- `get_number(prompt)` — User input validation for numeric values
- `validate_operation(operation)` — Validates operation is in {+, -, *, /}
- `add()`, `subtract()`, `multiply()`, `divide()` — Operation implementations
- `perform_calculation(num1, num2, operation)` — Dispatcher that executes the selected operation and handles errors (e.g., division by zero)
- `display_menu()` — Displays the calculator header/help
- `main()` — Controls the main program loop

## Testing

No formal test suite exists yet. Test manually by running `python calculator.py` and entering various inputs including edge cases (division by zero, invalid operations, non-numeric inputs).

## Architecture Notes

- All operation functions are registered in dictionaries (`valid_operations`, `operations`) for easy extension
- Error handling is centralized in `perform_calculation()` which catches `ValueError` exceptions
- Input validation happens at the point of entry (`get_number()`, `validate_operation()`)
- The main loop continues until the user declines to perform another calculation
