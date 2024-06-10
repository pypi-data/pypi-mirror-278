from .app import add_int
import argparse


def main():
    parser = argparse.ArgumentParser(description="Add two integers.")
    parser.add_argument("num1", type=int, help="First integer")
    parser.add_argument("num2", type=int, help="Second integer")
    args = parser.parse_args()

    result = add_int(args.num1, args.num2)
    print(f"The sum of {args.num1} and {args.num2} is {result}")


if __name__ == "__main__":
    main()
