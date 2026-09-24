import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Unit converter")
    parser.add_argument(
        "category",
        choices=["length", "mass", "temperature"],
    )
    parser.add_argument("value", type=float)
    parser.add_argument("from_unit")
    parser.add_argument("to_unit")
    return parser


def main() -> None:
    args = build_parser().parse_args()

    print(
        f"Requested conversion: "
        f"{args.value} {args.from_unit} -> {args.to_unit} "
        f"({args.category})"
    )
    print("Conversion is not implemented yet.")


if __name__ == "__main__":
    main()
