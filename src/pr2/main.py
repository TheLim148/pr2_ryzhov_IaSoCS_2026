import argparse


LENGTH_TO_METERS = {
    "mm": 0.001,
    "cm": 0.01,
    "m": 1.0,
    "km": 1000.0,
}


def convert_length(value: float, from_unit: str, to_unit: str) -> float:
    if from_unit not in LENGTH_TO_METERS or to_unit not in LENGTH_TO_METERS:
        raise ValueError("Unsupported length unit")

    value_in_meters = value * LENGTH_TO_METERS[from_unit]
    return value_in_meters / LENGTH_TO_METERS[to_unit]


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

    try:
        if args.category != "length":
            print("Conversion is not implemented yet.")
            return

        result = convert_length(
            args.value,
            args.from_unit,
            args.to_unit,
        )
        print(result)
    except ValueError as error:
        raise SystemExit(f"Error: {error}")


if __name__ == "__main__":
    main()
