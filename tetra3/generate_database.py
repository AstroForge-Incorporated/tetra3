"""CLI entrypoint for generating tetra3 star pattern databases.

Wraps the Tetra3.generate_database() method with command-line arguments.
"""

import argparse
import sys


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Generate a tetra3 star pattern database (.npz) from a star catalogue.",
        epilog=(
            "Example usage:\n"
            "  tetra3-generate-db --save-as tycho_fov4-6_mag9 --max-fov 6 --min-fov 4\n"
            "  tetra3-generate-db --save-as tycho_fov71-73_mag9 --max-fov 73 --min-fov 71\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--save-as",
        type=str,
        required=True,
        help="Name for the output database file (without .npz extension)",
    )
    parser.add_argument(
        "--max-fov",
        type=float,
        required=True,
        help="Maximum field of view in degrees",
    )
    parser.add_argument(
        "--min-fov",
        type=float,
        default=None,
        help="Minimum field of view in degrees (default: same as max-fov)",
    )
    parser.add_argument(
        "--star-max-magnitude",
        type=float,
        default=9,
        help="Maximum star magnitude to include (default: 9)",
    )
    parser.add_argument(
        "--star-catalog",
        type=str,
        default="tyc_main",
        help="Star catalogue to use: 'tyc_main', 'hip_main', or 'BSC5' (default: tyc_main)",
    )
    parser.add_argument(
        "--epoch-proper-motion",
        type=str,
        default="now",
        help="Epoch year for proper motion propagation, or 'now' (default: now)",
    )
    parser.add_argument(
        "--pattern-stars-per-fov",
        type=int,
        default=10,
        help="Number of pattern stars per FOV (default: 10)",
    )
    parser.add_argument(
        "--verification-stars-per-fov",
        type=int,
        default=30,
        help="Number of verification stars per FOV (default: 30)",
    )
    parser.add_argument(
        "--pattern-max-error",
        type=float,
        default=0.005,
        help="Maximum pattern error (default: 0.005)",
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    # Parse epoch - allow float or 'now'
    epoch = args.epoch_proper_motion
    if epoch != "now":
        try:
            epoch = float(epoch)
        except ValueError:
            print(f"Error: --epoch-proper-motion must be a number or 'now', got '{epoch}'",
                  file=sys.stderr)
            sys.exit(1)

    import tetra3

    t3 = tetra3.Tetra3(load_database=None)
    t3.generate_database(
        save_as=args.save_as,
        max_fov=args.max_fov,
        min_fov=args.min_fov,
        star_max_magnitude=args.star_max_magnitude,
        star_catalog=args.star_catalog,
        epoch_proper_motion=epoch,
        pattern_stars_per_fov=args.pattern_stars_per_fov,
        verification_stars_per_fov=args.verification_stars_per_fov,
        pattern_max_error=args.pattern_max_error,
    )


if __name__ == "__main__":
    main()
