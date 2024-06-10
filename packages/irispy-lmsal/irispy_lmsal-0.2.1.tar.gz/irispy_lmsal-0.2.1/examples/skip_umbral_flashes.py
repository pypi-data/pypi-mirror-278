"""
=======================
Umbral flashes analysis
=======================

In this example, we are going to work with spectra and slit-jaw
images to study an example of dynamical phenomena called umbral flashes.
"""

import astropy.units as u
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pooch
from astropy.coordinates import SpectralCoord
from astropy.visualization import time_support

from irispy.io import read_files
from irispy.utils import image_clipping

time_support()

###############################################################################
# We start with getting the data. This is done by downloading the data from the IRIS archive.
#
# In this case, we will use ``pooch`` as to keep this example self contained
# but using your browser will also work.
#
# Using the url: http://www.lmsal.com/solarsoft/irisa/data/level2_compressed/2013/09/02/20130902_163935_4000255147/
# we are after the 1400 slit-jaw file and the raster file (~900 MB).

raster_filename = pooch.retrieve(
    "http://www.lmsal.com/solarsoft/irisa/data/level2_compressed/2013/09/02/20130902_163935_4000255147/iris_l2_20130902_163935_4000255147_raster.tar.gz",
    known_hash="e0fdbe63b6ff88856d97dff1fd4c3f62bf0bb4a85c025930c36fd69086ed0533",
)
sji_filename = pooch.retrieve(
    "http://www.lmsal.com/solarsoft/irisa/data/level2_compressed/2013/09/02/20130902_163935_4000255147/iris_l2_20130902_163935_4000255147_SJI_1400_t000.fits.gz",
    known_hash="e04eedbe7fd7e5e173b6a9308db3e45991634a4f8d9b245a334d5c492d85d0ed",
)

###############################################################################
# Now to open the files using ``irispy-lmsal``.

# Note that when ``memmap=True``, the data values are read from the FITS file
# directly without the scaling to Float32, the data values are no longer in DN,
# but in scaled integer units that start at -2$^{16}$/2.
raster = read_files(raster_filename, memmap=True, uncertainty=False)
sji_1400 = read_files(sji_filename, memmap=True, uncertainty=False)

###############################################################################
# We are after the Mg II k and C II lines, which we can select using a key.
# We will produce a space-time image of the Mg II k3 wavelength.

mg_ii = raster["Mg II k 2796"][0]
c_ii = raster["C II 1336"][0]

# Instead of using the pixel index, we can crop the data in wavelength space.
lower_corner = [SpectralCoord(279.63, unit=u.nm), None]
upper_corner = [SpectralCoord(279.63, unit=u.nm), None]
mg_crop = mg_ii.crop(lower_corner, upper_corner)

# The Mg II k3 core is located around wavelength pixel 103.
# Which we will use to clip the data.
vmin, vmax = image_clipping(mg_ii.data[..., 103])
mg_crop.plot(vmin=vmin, vmax=vmax)
plt.xlabel("Solar Y")

plt.show()

###############################################################################
# The middle section between 60"-75" is on the umbra of a sunspot, even though
# it is not obvious from this image. One can see very clearly the umbral oscillations,
# with a clear regular pattern of dark/bright streaks.
#
# Let us now load the 1400 SJI for context.

vmin, vmax = image_clipping(sji_1400[0].data)
sji_1400[0].plot(vmin=vmin, vmax=vmax)

plt.show()

###############################################################################
# The slit pixel 220 is a location on the sunspot's umbra.
# Let us plot the k3 intensity (spectral pixel 103 of ``mg_ii``) and the
# core of the brightest C II line (spectral pixel 90 of ``c_ii``) vs
# time in minutes (showing first ~10 minutes only)

mg_ii_times = mg_ii.axis_world_coords("time", wcs=mg_ii.extra_coords)[0][:200]
c_ii_times = c_ii.axis_world_coords("time", wcs=c_ii.extra_coords)[0][:200]

plt.figure()
plt.plot(mg_ii_times, mg_ii.data[:200, 220, 103], label="Mg II k3")
(ax,) = plt.plot(c_ii_times, c_ii.data[:200, 220, 90], label="C II")
plt.legend()
plt.ylabel("DN (Memory Mapped Value)")
plt.xlabel("Time (UTC)")
ax.axes.xaxis.set_major_formatter(mdates.ConciseDateFormatter(ax.axes.xaxis.get_major_locator()))
# Rotates and right-aligns the x labels so they don't crowd each other.
for label in ax.axes.get_xticklabels(which="major"):
    label.set(rotation=30, horizontalalignment="right")

plt.show()

###############################################################################
# Imagine now you wanted to compare these oscillations with
# the intensity from the SJI. The SJI images are typically
# taken at a different cadence, so you will need to load the corresponding
# time array for the 1400 SJI.

# We will take the first 50 to cut down on the size of the data for this example.
# This is memory intensive and that an upstream bug needs to be fixed.
times_sji = sji_1400.time[:50]

###############################################################################
# Now we can plot both spectral lines and SJI for a pixel close to the slit
# at the same Y position (pre-worked out to be at index 220).

plt.figure()
plt.plot(mg_ii_times, mg_ii.data[:200, 220, 103], label="Mg II k3")
plt.plot(c_ii_times, c_ii.data[:200, 220, 90], label="C II")
(ax,) = plt.plot(times_sji, sji_1400.data[:50, 190, 220], label="1400 SJI")
plt.legend()
plt.ylabel("Counts (Memory Mapped Value)")
plt.xlabel("Time (UTC)")
ax.axes.xaxis.set_major_formatter(mdates.ConciseDateFormatter(ax.axes.xaxis.get_major_locator()))
# Rotates and right-aligns the x labels so they don't crowd each other.
for label in ax.axes.get_xticklabels(which="major"):
    label.set(rotation=30, horizontalalignment="right")

plt.show()

###############################################################################
# You are now ready to explore all the correlations, anti-correlations,
# and phase differences.
