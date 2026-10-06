# Simple Console Calculator

A straightforward Python command-line calculator that supports basic arithmetic operations.

## Features

- **Basic Operations**: Addition (+), Subtraction (-), Multiplication (*), Division (/)
- **Input Validation**: Ensures valid numbers and operations are entered
- **Error Handling**: Handles division by zero and invalid inputs gracefully
- **Interactive Loop**: Perform multiple calculations in one session

## How to Use

Run the calculator from the command line:

```bash
python calculator.py
```

### Example Session

```
========================================
       SIMPLE CONSOLE CALCULATOR
========================================
Supported operations:
  + : Addition
  - : Subtraction
  * : Multiplication
  / : Division
========================================

Enter the first number: 10
Enter an operation (+, -, *, /): +
Enter the second number: 5

Result: 10.0 + 5 = 15.0

Would you like to perform another calculation? (yes/no): no

Thank you for using the calculator. Goodbye!
```

## Requirements

- Python 3.x

## Installation

No additional dependencies required. Just clone the repository and run the script.

```bash
git clone <repository-url>
cd claudecodedemo
python calculator.py
```

## Features Explained

- **get_number()**: Prompts the user for a number with validation
- **validate_operation()**: Ensures only valid operations are accepted
- **perform_calculation()**: Executes the calculation with error handling
- **display_menu()**: Shows the calculator interface and available operations
- **main()**: Controls the main program loop

## License

Open source project
