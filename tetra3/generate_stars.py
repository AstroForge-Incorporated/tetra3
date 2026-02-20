"""CLI entrypoint for generating raw binary star catalog files.

Generates a .stars file from the Tycho star catalog (tyc_main.dat).
Each star is stored as 4 little-endian f32 values: [x, y, z, mag]
where (x, y, z) is the unit vector in J2000 ICRF and mag is the visual magnitude.

The output is compatible with the Rust Star struct:
    #[repr(C)]
    pub struct Star {
        pub pos: cgmath::Vector3<f32>,
        pub mag: f32,
    }
"""

import argparse
import csv
import struct
import sys

import numpy as np

# Tycho catalog epoch for proper motion origin
PM_ORIGIN = 1991.25


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Generate a raw binary star file (.stars) from the Tycho star catalog.",
        epilog=(
            "Example usage:\n"
            "  tetra3-generate-stars tyc_main.dat --year 2025\n"
            "  tetra3-generate-stars tyc_main.dat --year 2025 --max-magnitude 9\n"
            "  tetra3-generate-stars tyc_main.dat --year 2025 -o tycho_2025.stars\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "catalog",
        type=str,
        help="Path to the tyc_main.dat catalog file",
    )
    parser.add_argument(
        "--year",
        type=float,
        required=True,
        help="Epoch year for proper motion propagation (e.g. 2025)",
    )
    parser.add_argument(
        "--max-magnitude",
        type=float,
        default=None,
        help="Maximum star magnitude to include (default: no limit)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help="Output file path (default: tycho_YYYY.stars)",
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    output_path = args.output or f"tycho_{int(args.year)}.stars"
    epoch = args.year
    max_mag = args.max_magnitude

    stars = []
    incomplete = 0
    magnitude_filtered = 0

    with open(args.catalog, "r") as f:
        reader = csv.reader(f, delimiter="|")
        for entry in reader:
            # Skip entries with missing essential fields
            if entry[5].isspace() or entry[8].isspace() or entry[9].isspace():
                incomplete += 1
                continue

            mag = float(entry[5])
            if max_mag is not None and mag > max_mag:
                magnitude_filtered += 1
                continue

            alpha = float(entry[8])  # RA in degrees
            delta = float(entry[9])  # Dec in degrees
            cos_delta = np.cos(np.deg2rad(delta))

            # Skip stars without proper motion data when propagating
            # (matches tetra3 generate_database behavior)
            has_pm = not entry[12].isspace() and not entry[13].isspace()
            if epoch != PM_ORIGIN and not has_pm:
                incomplete += 1
                continue

            if epoch != PM_ORIGIN:
                # Proper motion: mas/yr -> deg/yr
                mu_alpha_cos_delta = float(entry[12]) / 1000 / 60 / 60
                mu_delta = float(entry[13]) / 1000 / 60 / 60

                if cos_delta > 0.1:
                    mu_alpha = mu_alpha_cos_delta / cos_delta
                else:
                    mu_alpha = 0
                    mu_delta = 0

                ra = np.deg2rad(alpha + mu_alpha * (epoch - PM_ORIGIN))
                dec = np.deg2rad(delta + mu_delta * (epoch - PM_ORIGIN))
            else:
                ra = np.deg2rad(alpha)
                dec = np.deg2rad(delta)

            # Convert to unit vector in J2000 ICRF
            x = float(np.cos(ra) * np.cos(dec))
            y = float(np.sin(ra) * np.cos(dec))
            z = float(np.sin(dec))

            stars.append((x, y, z, mag))

    print(f"Stars included: {len(stars)}")
    print(f"Skipped (incomplete): {incomplete}")
    if max_mag is not None:
        print(f"Skipped (magnitude > {max_mag}): {magnitude_filtered}")

    # Write as raw little-endian f32 values: [x, y, z, mag] per star
    with open(output_path, "wb") as f:
        for x, y, z, mag in stars:
            f.write(struct.pack("<ffff", x, y, z, mag))

    file_size = len(stars) * 16
    print(f"Wrote {output_path} ({file_size} bytes, {len(stars)} stars)")


if __name__ == "__main__":
    main()
