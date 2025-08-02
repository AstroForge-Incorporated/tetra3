"""
This example generates a tetra3 database from a star catalogue. You must have the catalogue file
hip_main.dat in the same directory as tetra3.py to run this example. You can download it from
https://cdsarc.u-strasbg.fr/ftp/cats/I/239/
"""

import sys
sys.path.append('..')

import tetra3

# Create instance without loading any database.
t3 = tetra3.Tetra3(load_database=None)

# Generate and save database - imager
t3.generate_database(save_as='tycho_fov4-6_mag9', max_fov=6, min_fov=4,
                     star_max_magnitude=9, star_catalog='tyc_main')

# Generate and save database - selfie cam
t3.generate_database(save_as='tycho_fov71-73_mag9', max_fov=73, min_fov=71,
                     star_max_magnitude=9, star_catalog='tyc_main')
