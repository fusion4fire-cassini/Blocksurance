import numpy as np
import rasterio
from rasterio.plot import show
from rasterio.warp import Resampling
import matplotlib.pyplot as plt

Jun_04_10m = 'C:\\Users\\Dfran\\.spyder-py3\\S2A_MSIL2A_20170604T112121_N0205_R037_T29TNE_20170604T112755.SAFE\\GRANULE\\L2A_T29TNE_A010187_20170604T112755\\IMG_DATA\\R10m\\'
Jun_04_20m = 'C:\\Users\\Dfran\\.spyder-py3\\S2A_MSIL2A_20170604T112121_N0205_R037_T29TNE_20170604T112755.SAFE\\GRANULE\\L2A_T29TNE_A010187_20170604T112755\\IMG_DATA\\R20m\\'
Jun_04_60m = 'C:\\Users\\Dfran\\.spyder-py3\\S2A_MSIL2A_20170604T112121_N0205_R037_T29TNE_20170604T112755.SAFE\\GRANULE\\L2A_T29TNE_A010187_20170604T112755\\IMG_DATA\\R60m\\'

# NDVI ---------------------------------------------------#

b4=rasterio.open(Jun_04_10m + "L2A_T29TNE_20170604T112121_B04_10m.jp2")
b8=rasterio.open(Jun_04_10m + "L2A_T29TNE_20170604T112121_B08_10m.jp2")

red = b4.read()
nir = b8.read()

ndvi = (nir.astype(float)-red.astype(float))/(nir+red)

meta = b4.meta
meta.update(driver='GTiff')
meta.update(dtype=rasterio.float32)

with rasterio.open('C:\\Users\\Dfran\\.spyder-py3\\2017-06-04_S2_NDVI.tif', 'w', **meta) as dest:
    dest.write(ndvi.astype(rasterio.float32))

img = rasterio.open('C:\\Users\\Dfran\\.spyder-py3\\2017-06-04_S2_NDVI.tif')
img_r = img.read()
image = np.asarray(img_r)

fig = plt.figure(figsize=(20,12))

# Show the figure
show(image)

# NDMI ---------------------------------------------------#

b11=rasterio.open(Jun_04_20m + "L2A_T29TNE_20170604T112121_B11_20m.jp2")

upscale_factor = 2

with rasterio.open(Jun_04_20m + "L2A_T29TNE_20170604T112121_B11_20m.jp2") as dataset:

    # resample data to target shape
    swir11 = dataset.read(
        out_shape=(
            dataset.count,
            int(dataset.height*upscale_factor),
            int(dataset.width*upscale_factor)
        ),
        resampling=Resampling.bilinear
    )

ndmi = (nir.astype(float)-swir11.astype(float))/(nir+swir11)

meta = b8.meta
meta.update(driver='GTiff')
meta.update(dtype=rasterio.float32)

with rasterio.open('C:\\Users\\Dfran\\.spyder-py3\\2017-06-04_S2_NDMI.tif', 'w', **meta) as dest:
    dest.write(ndmi.astype(rasterio.float32))

# MYVI ---------------------------------------------------#

b3=rasterio.open(Jun_04_10m + "L2A_T29TNE_20170604T112121_B03_10m.jp2")

green = b3.read()

upscale_factor = 2

with rasterio.open(Jun_04_20m + "L2A_T29TNE_20170604T112121_B06_20m.jp2") as dataset:

    # resample data to target shape
    b6 = dataset.read(
        out_shape=(
            dataset.count,
            int(dataset.height*upscale_factor),
            int(dataset.width*upscale_factor)
        ),
        resampling=Resampling.bilinear
    )

upscale_factor_9 = 6

with rasterio.open(Jun_04_60m + "L2A_T29TNE_20170604T112121_B09_60m.jp2") as dataset:

    # resample data to target shape
    b9 = dataset.read(
        out_shape=(
            dataset.count,
            int(dataset.height*upscale_factor_9),
            int(dataset.width*upscale_factor_9)
        ),
        resampling=Resampling.bilinear
    )

myvi = 0.723 * green.astype(float) - 0.597 * red.astype(float) + 0.206 * b6.astype(float) - 0.278 * b9.astype(float)

meta = b3.meta
meta.update(driver='GTiff')
meta.update(dtype=rasterio.float32)

with rasterio.open('C:\\Users\\Dfran\\.spyder-py3\\2017-06-04_S2_MYVI.tif', 'w', **meta) as dest:
    dest.write(myvi.astype(rasterio.float32))

# # Prefire NBR--------------------------------------------------------------#

upscale_factor = 2

with rasterio.open(Jun_04_20m + "L2A_T29TNE_20170604T112121_B8A_20m.jp2") as dataset:

    # resample data to target shape
    b8a = dataset.read(
        out_shape=(
            dataset.count,
            int(dataset.height*upscale_factor),
            int(dataset.width*upscale_factor)
        ),
        resampling=Resampling.bilinear
    )

with rasterio.open(Jun_04_20m + "L2A_T29TNE_20170604T112121_B12_20m.jp2") as dataset:

    # resample data to target shape
    b12 = dataset.read(
        out_shape=(
            dataset.count,
            int(dataset.height*upscale_factor),
            int(dataset.width*upscale_factor)
        ),
        resampling=Resampling.bilinear
    )

# Calculate NBR
nbr = (b8a.astype(float)-b12.astype(float))/(b8a+b12)

# Extract and update the metadata
meta = b3.meta
meta.update(driver='GTiff')
meta.update(dtype=rasterio.float32)

# Write the NBR image with metadata

with rasterio.open('C:\\Users\\Dfran\\.spyder-py3\\2017-06-04_S2_NBR.tif', 'w', **meta) as dest:
    dest.write(nbr.astype(rasterio.float32))
    
# # Postfire NBR ------------------------------------------------------------#

Jul_04_20m = 'C:\\Users\\Dfran\\.spyder-py3\\S2A_MSIL2A_20170704T112111_N0205_R037_T29TNE_20170704T112431.SAFE\\GRANULE\\L2A_T29TNE_A010616_20170704T112431\\IMG_DATA\\R20m\\'
    
with rasterio.open(Jul_04_20m + "L2A_T29TNE_20170704T112111_B8A_20m.jp2") as dataset:

    # resample data to target shape
    b8a = dataset.read(
        out_shape=(
            dataset.count,
            int(dataset.height*upscale_factor),
            int(dataset.width*upscale_factor)
        ),
        resampling=Resampling.bilinear
    )

with rasterio.open(Jul_04_20m + "L2A_T29TNE_20170704T112111_B12_20m.jp2") as dataset:

    # resample data to target shape
    b12 = dataset.read(
        out_shape=(
            dataset.count,
            int(dataset.height*upscale_factor),
            int(dataset.width*upscale_factor)
        ),
        resampling=Resampling.bilinear
    )
    
nbr = (b8a.astype(float)-b12.astype(float))/(b8a+b12)

# Extract and update the metadata
meta = b3.meta
meta.update(driver='GTiff')
meta.update(dtype=rasterio.float32)

# Write the NBR image with metadata

with rasterio.open('C:\\Users\\Dfran\\.spyder-py3\\2017-07-04_S2_NBR.tif', 'w', **meta) as dest:
    dest.write(nbr.astype(rasterio.float32))   
    
pre_nbr = rasterio.open('C:\\Users\\Dfran\\.spyder-py3\\2017-06-04_S2_NBR.tif')
post_nbr = rasterio.open('C:\\Users\\Dfran\\.spyder-py3\\2017-07-04_S2_NBR.tif')

# RBR ------------------------------------------------------------#

# Read the images in as arrays
pre = pre_nbr.read()
post = post_nbr.read()

RBR = (pre.astype(rasterio.float32)-post.astype(rasterio.float32))/(pre.astype(rasterio.float32) +1001)

with rasterio.open('C:\\Users\\Dfran\\.spyder-py3\\2017-06-04_to_07-04_S2_RBR.tif', 'w', **meta) as dest:
    dest.write(RBR.astype(rasterio.float32))    
