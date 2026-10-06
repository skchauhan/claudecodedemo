def get_number(prompt):
    """Prompt user for a number and validate input."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Error: Please enter a valid number.")


def validate_operation(operation):
    """Validate that the operation is supported."""
    valid_operations = {'+', '-', '*', '/'}
    if operation not in valid_operations:
        return False
    return True


def add(a, b):
    """Add two numbers."""
    return a + b


def subtract(a, b):
    """Subtract two numbers."""
    return a - b


def multiply(a, b):
    """Multiply two numbers."""
    return a * b


def divide(a, b):
    """Divide two numbers with zero division check."""
    if b == 0:
        raise ValueError("Error: Cannot divide by zero.")
    return a / b


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
            operation = input("Enter an operation (+, -, *, /): ").strip()
            if validate_operation(operation):
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
