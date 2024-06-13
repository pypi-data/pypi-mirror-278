import random
import argparse
import sys
from typing import List

def generate_random_numbers(count: int, min_value: int, max_value: int) -> List[int]:
    """
    Generate a list of random numbers.
    
    :param count: The number of random numbers to generate
    :param min_value: The minimum value of the random numbers
    :param max_value: The maximum value of the random numbers
    :return: A list of random numbers
    """
    return [random.randint(min_value, max_value) for _ in range(count)]

def is_integer(value: str) -> bool:
    """
    Check if a string can be converted to an integer.
    
    :param value: The string to check
    :return: True if the string can be converted to an integer, False otherwise
    """
    try:
        int(value)
        return True
    except ValueError:
        return False

def parse_arguments() -> argparse.Namespace:
    """
    Parse command line arguments.
    
    :return: The parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Generate a list of random numbers.",
        epilog="Example usage: make_time_for_yourself 10 1 100 --retry"
    )
    parser.add_argument(
        'count',
        type=str,
        help='The number of random numbers to generate (e.g., 10).'
    )
    parser.add_argument(
        'min_value',
        type=str,
        help='The minimum value of the random numbers (e.g., 1).'
    )
    parser.add_argument(
        'max_value',
        type=str,
        help='The maximum value of the random numbers (e.g., 100).'
    )
    parser.add_argument(
        '--retry',
        action='store_true',
        help='Allow retrying the generation of random numbers.'
    )
    return parser.parse_args()

def validate_arguments(args: argparse.Namespace) -> None:
    """
    Validate command line arguments.
    
    :param args: The parsed arguments
    :raises ValueError: If any of the arguments are invalid
    """
    if not (is_integer(args.count) and is_integer(args.min_value) and is_integer(args.max_value)):
        raise ValueError("All input values must be integers.")
    
    count = int(args.count)
    min_value = int(args.min_value)
    max_value = int(args.max_value)

    if min_value > max_value:
        raise ValueError("Minimum value cannot be greater than maximum value.")

def main() -> None:
    """
    The main function.
    """
    args = parse_arguments()

    try:
        validate_arguments(args)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    count = int(args.count)
    min_value = int(args.min_value)
    max_value = int(args.max_value)

    while True:
        random_numbers = generate_random_numbers(count, min_value, max_value)
        print(f"Generated {count} random numbers between {min_value} and {max_value}:")
        print(random_numbers)

        if not args.retry:
            break

        retry_input = input("Do you want to generate new random numbers? (yes/no): ").strip().lower()
        if retry_input != 'yes':
            break

if __name__ == "__main__":
    main()
