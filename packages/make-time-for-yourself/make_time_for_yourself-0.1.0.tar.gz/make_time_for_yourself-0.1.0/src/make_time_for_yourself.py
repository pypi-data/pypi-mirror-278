import random

def generate_random_numbers(count, min_value, max_value):
    """
    Generate a list of random numbers.
    
    :param count: The number of random numbers to generate
    :param min_value: The minimum value of the random numbers
    :param max_value: The maximum value of the random numbers
    :return: A list of random numbers
    """
    return [random.randint(min_value, max_value) for _ in range(count)]

def main():
    import argparse
    import sys

    def is_integer(value):
        try:
            int(value)
            return True
        except ValueError:
            return False

    parser = argparse.ArgumentParser(description="Generate a list of random numbers.")
    parser.add_argument('count', type=str, help='The number of random numbers to generate.')
    parser.add_argument('min_value', type=str, help='The minimum value of the random numbers.')
    parser.add_argument('max_value', type=str, help='The maximum value of the random numbers.')
    parser.add_argument('--retry', action='store_true', help='Retry generating random numbers.')
    args = parser.parse_args()

    if not (is_integer(args.count) and is_integer(args.min_value) and is_integer(args.max_value)):
        print("Error: All input values must be integers.", file=sys.stderr)
        sys.exit(1)

    count = int(args.count)
    min_value = int(args.min_value)
    max_value = int(args.max_value)

    if min_value > max_value:
        print("Error: Minimum value cannot be greater than maximum value.", file=sys.stderr)
        sys.exit(1)

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
