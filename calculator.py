def get_number(prompt, min_value=None, max_value=None, max_retries=3):
    """Prompt user for a valid number with optional range validation."""
    retries = 0
    while retries < max_retries:
        try:
            value = float(input(prompt))

            # Check for invalid float values
            if value != value:  # NaN check
                print("Error: Please enter a valid number (not NaN).")
                retries += 1
                continue
            if value == float('inf') or value == float('-inf'):
                print("Error: Please enter a finite number.")
                retries += 1
                continue

            # Range validation
            if min_value is not None and value < min_value:
                print(f"Error: Number must be >= {min_value}.")
                retries += 1
                continue
            if max_value is not None and value > max_value:
                print(f"Error: Number must be <= {max_value}.")
                retries += 1
                continue

            return value
        except ValueError:
            print("Error: Please enter a valid number.")
            retries += 1

    raise ValueError(f"Failed to get valid input after {max_retries} attempts.")


def validate_operation(operation):
    """Validate and normalize the operation."""
    valid_operations = {'+', '-', '*', '/'}
    operation = operation.strip()  # Sanitize input

    if operation not in valid_operations:
        return False, None
    return True, operation


def add(a, b):
    """Add two numbers."""
    return a + b


def subtract(a, b):
    """Subtract two numbers."""
    return a - b


def multiply(a, b):
    """Multiply two numbers."""
    return a * b


def divide(a, b, epsilon=1e-10):
    """Divide two numbers with zero division check using epsilon comparison."""
    if abs(b) < epsilon:  # Better floating-point comparison
        raise ValueError("Error: Cannot divide by zero.")
    return a / b


def cosine(angle_degrees):
    """Calculate the cosine of an angle in degrees."""
    import math
    angle_radians = math.radians(angle_degrees)
    return math.cos(angle_radians)


def perform_calculation(num1, num2, operation):
    """Perform the selected operation."""
    operations = {
        '+': add,
        '-': subtract,
        '*': multiply,
        '/': divide,
    }

    try:
        result = operations[operation](num1, num2)
        return result
    except ValueError as e:
        print(e)
        return None


def display_menu():
    """Display the calculator menu."""
    print("\n" + "="*40)
    print("       SIMPLE CONSOLE CALCULATOR")
    print("="*40)
    print("Supported operations:")
    print("  + : Addition")
    print("  - : Subtraction")
    print("  * : Multiplication")
    print("  / : Division")
    print("="*40 + "\n")


def main():
    """Main calculator function."""
    display_menu()

    while True:
        # Get first number
        num1 = get_number("Enter the first number: ")

        # Get operation
        while True:
            operation_input = input("Enter an operation (+, -, *, /): ")
            is_valid, operation = validate_operation(operation_input)
            if is_valid:
                break
            print("Error: Please enter a valid operation (+, -, *, /).")

        # Get second number
        num2 = get_number("Enter the second number: ")

        # Perform calculation
        result = perform_calculation(num1, num2, operation)

        if result is not None:
            print(f"\nResult: {num1} {operation} {num2} = {result}\n")

        # Ask if user wants to continue
        continue_choice = input("Would you like to perform another calculation? (yes/no): ").strip().lower()
        if continue_choice not in ['yes', 'y']:
            print("\nThank you for using the calculator. Goodbye!")
            break


if __name__ == "__main__":
    main()
