# Welcome to tetra3!

*tetra3 is a fast lost-in-space plate solver for star trackers written in Python.*

This algorithm is based on the TETRA Star Identification paper, linked [here](https://astroforge.box.com/s/42v7729fymxsjr4arc0ip1f3lnkit2ot).

Use it to identify stars in images and get the corresponding direction (i.e. right ascension and
declination) in the sky which the camera points to and indentification of the stars. tetra3
supports solving distorted images and a wide range of field of view. The default database is
built for 10 to 30 degrees with stars down to magnitude 7, but you can easily build for any
application down to a few degrees.

 **NOTE:**
 In June 2023 the ``master`` branch of tetra3 was updated with a long list of improvements. This may
 cause some compatibility issues. Please use the ``legacy`` branch in the interim and open an issue
 on GitHub to discuss changes and resolve any problems.

The software is available in the `tetra3 GitHub repository <https://github.com/esa/tetra3>`_.
General instructions are available at the
`tetra3 ReadTheDocs website <https://tetra3.readthedocs.io/en/latest/>`_. tetra3 is Free and Open
Source Software released by the European Space Agency under the Apache License 2.0. See LICENSE.txt
in the repository for full licensing details.

Performance will vary, but in general solutions will take 10 milliseconds (excluding time to extract
star positions from images) with 10 arcsecond (50 microradian) accuracy. The algorith is a pure
lost-in-space solver, so it does not require any prior pointing information.

A camera with a field of view (FOV) of about 10 degrees and at least 512 by 512 pixels is a good
starting point for general star tracking applications. Your camera should be able to acquire stars
down to magnitude 7 for best results. (For a narrower FOV camera, you need to be able to capture
dimmer stars.)

To effectively use tetra3 with your camera you may need to build a database optimised for your use
case. The Yale Bright Star Catalog, and the Hipparcos and Tyco Catalogues are supported for
generating databases; see the API documentation.

A real-world set of images acquired with a FLIR Blackfly S BFS-U3-31S4M-C (Sony IMX265 sensor;
binned 2x2) camera and a Fujifilm HF35XA-5M 35mm f/1.9 lens are included as test data (11.4 degrees
FOV).

## Astroforge Updates
1. Cleaned up unused db_props
2. Removed right ascension, declination angle, and magnitude from star table (values are not used in star_id calculations, algorithm only uses the unit vector)
3. Changed default star catalog to tycho2
4. Simplified/removed unused branches in solve_from_centroids()
5. Removed logic that saves largest edge of each pattern, and uses this value to speed up calculations - adds additional complexity that did not meaningfully speed up execution time, so did not implement in flight software. 
6. Added `view_npy.py` utility to open/read npy files
7. Added `read_image.py` utility to read png metadata from image-gen generated images

## Test Image Parameters
**Image-Gen settings:**
Camera: "imager"
resolution_hv_pixel = [5536, 3692]
pixel_size_mm = 2.4e-3
f_no = 4.0
focal_length_mm = 150.0
exposure_time_s = 0.1
analog_gain = 10.0
well_capacity = 15e3
quantum_efficiency = 0.84

## Usage
### Generating New Databases

The `tyc_main.dat` star catalogue is stored in `tetra3/data/` via Git LFS. To fetch it:

```bash
git lfs pull
```

The original source of this file is [Box](https://astroforge.app.box.com/file/1997375061499?s=my1mb5in9vj9hwxiyg9rz2gc1ddoq3xt).

Then use the `tetra3-generate-db` CLI command:

```bash
# Imager database (FOV ~5 deg)
uv run tetra3-generate-db --save-as tycho_fov4-6_mag9 --max-fov 6 --min-fov 4 \
    --star-max-magnitude 9 --star-catalog tyc_main --epoch-proper-motion 2026

# Selfie cam database (FOV ~72 deg)
uv run tetra3-generate-db --star-catalog tyc_main --save-as tycho_fov2-45_mag6.npz --min-fov 2 --max-fov 45 --star-max-magnitude 6 --pattern-stars-per-fov 20 --verification-stars-per-fov 40 --epoch-proper-motion 2026
```

Run `tetra3-generate-db -h` for full usage information.

**Important arguments:**
- `--max-fov, --min-fov`: Select an FOV range +/- 1 degree around the true FOV of the camera (provides error bounds while minimizing database size)
- `--star-max-magnitude`: Dimmest stars to add into the database (default: 9)
- `--star-catalog`: Star catalogue to use: `tyc_main`, `hip_main`, or `BSC5` (default: `tyc_main`)
- `--epoch-proper-motion`: Epoch year for proper motion propagation (default: now)

### Generating Raw Star Files

The `tetra3-generate-stars` command generates a raw binary `.stars` file for use with the `image-gen` tool in `mono`:

```bash
tetra3-generate-stars tetra3/data/tyc_main.dat --year 2026 -o tycho_2026.stars
```

Run `tetra3-generate-stars -h` for full usage information.

### Running Star-ID
`examples/test_tetra3.py` runs the star-ID algorithm on a set of images placed inside `examples/test_images`, using a star database saved into `tetra3/data`. 
The fov of the camera/image gen used to generate the images must match the fov of the database chosen in this script (see `load_database`). 

