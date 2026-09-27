import argparse
from pathlib import Path


DEFAULT_ROUND_DIGITS = 2

LENGTH_TO_METERS = {
    "mm": 0.001,
    "cm": 0.01,
    "m": 1.0,
    "km": 1000.0,
}

MASS_TO_KG = {
    "g": 0.001,
    "kg": 1.0,
    "t": 1000.0,
}


def convert_length(value: float, from_unit: str, to_unit: str) -> float:
    if from_unit not in LENGTH_TO_METERS or to_unit not in LENGTH_TO_METERS:
        raise ValueError("Unsupported length unit")

    value_in_meters = value * LENGTH_TO_METERS[from_unit]
    return value_in_meters / LENGTH_TO_METERS[to_unit]


def convert_mass(value: float, from_unit: str, to_unit: str) -> float:
    if from_unit not in MASS_TO_KG or to_unit not in MASS_TO_KG:
        raise ValueError("Unsupported mass unit")

    value_in_kg = value * MASS_TO_KG[from_unit]
    return value_in_kg / MASS_TO_KG[to_unit]


def convert_temperature(
    value: float,
    from_unit: str,
    to_unit: str,
) -> float:
    supported_units = {"c", "f", "k"}

    if from_unit not in supported_units or to_unit not in supported_units:
        raise ValueError("Unsupported temperature unit")

    if from_unit == "c":
        celsius = value
    elif from_unit == "f":
        celsius = (value - 32) * 5 / 9
    else:
        celsius = value - 273.15

    if to_unit == "c":
        return celsius

    if to_unit == "f":
        return celsius * 9 / 5 + 32

    return celsius + 273.15


def convert(
    category: str,
    value: float,
    from_unit: str,
    to_unit: str,
) -> float:
    if category == "length":
        return convert_length(value, from_unit, to_unit)

    if category == "mass":
        return convert_mass(value, from_unit, to_unit)

    if category == "temperature":
        return convert_temperature(value, from_unit, to_unit)

    raise ValueError("Unsupported category")


def convert_batch_file(
    path: str,
    round_digits: int,
) -> list[str]:
    results = []

    lines = Path(path).read_text(encoding="utf-8").splitlines()

    for line_number, line in enumerate(lines, start=1):

        if not line.strip():
            continue

        parts = [part.strip() for part in line.split(";")]

        if len(parts) != 4:
            raise ValueError(f"Invalid format on line {line_number}")

        category, raw_value, from_unit, to_unit = parts

        try:
            value = float(raw_value)
        except ValueError as exc:
            raise ValueError(
                f"Invalid number on line {line_number}"
            ) from exc

        result = convert(
            category,
            value,
            from_unit,
            to_unit,
        )

        results.append(
            f"{category};{value};{from_unit};{to_unit};"
            f"{round(result, round_digits)}"
        )

    return results


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Unit converter")

    parser.add_argument(
        "category",
        nargs="?",
        choices=["length", "mass", "temperature"],
    )
    parser.add_argument("value", nargs="?", type=float)
    parser.add_argument("from_unit", nargs="?")
    parser.add_argument("to_unit", nargs="?")

    parser.add_argument(
        "--file",
        help="Path to a batch input file",
    )

    parser.add_argument(
        "--round-digits",
        type=int,
        default=DEFAULT_ROUND_DIGITS,
        help=(
            "Number of digits after decimal point "
            f"(default: {DEFAULT_ROUND_DIGITS})"
        ),
    )

    return parser


def main() -> None:
    args = build_parser().parse_args()

    try:
        if args.file:
            for result in convert_batch_file(
                args.file,
                args.round_digits,
            ):
                print(result)

            return

        values = (
            args.category,
            args.value,
            args.from_unit,
            args.to_unit,
        )

        if any(value is None for value in values):
            raise ValueError(
                "Single conversion requires: "
                "category value from_unit to_unit"
            )

        result = convert(
            args.category,
            args.value,
            args.from_unit,
            args.to_unit,
        )

        print(round(result, args.round_digits))

    except (ValueError, OSError) as error:
        raise SystemExit(f"Error: {error}")


if __name__ == "__main__":
    main()
