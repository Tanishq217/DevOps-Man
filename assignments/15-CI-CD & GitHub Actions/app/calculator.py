"""
Calculator Core Module
Provides arithmetic operations and interactive CLI mode.
"""

def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def calculate(a, operator, b):
    if operator == '+':
        return add(a, b)
    elif operator == '-':
        return subtract(a, b)
    elif operator == '*':
        return multiply(a, b)
    elif operator == '/':
        return divide(a, b)
    else:
        raise ValueError(f"Unsupported operator: {operator}")


if __name__ == "__main__":
    print("====================================")
    print("  DevOps Calculator CLI Application ")
    print("====================================")
    print("Supported operators: +, -, *, /")
    print("Type 'q' or 'quit' to exit.")
    
    while True:
        try:
            expr = input("\nEnter expression (e.g., 10 + 5): ").strip()
            if expr.lower() in ('q', 'quit', 'exit'):
                print("Exiting application. Goodbye!")
                break
            
            parts = expr.split()
            if len(parts) != 3:
                print("Invalid input format. Use: <number> <operator> <number> (e.g., 20 / 4)")
                continue
                
            num1 = float(parts[0])
            op = parts[1]
            num2 = float(parts[2])
            
            result = calculate(num1, op, num2)
            print(f"Result: {result}")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error occurred: {e}")
