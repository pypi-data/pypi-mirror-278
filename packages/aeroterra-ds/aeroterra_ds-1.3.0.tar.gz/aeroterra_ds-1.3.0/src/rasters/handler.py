import geopandas as gpd
import numpy as np

import os

import rasterio
from rasterio.enums import Resampling
from rasterio.warp import calculate_default_transform, reproject
from rasterio.merge import merge
from rasterio.features import shapes as shapes_rasterio
from rasterio.features import geometry_mask
from rasterio.windows import Window
from rasterio.mask import mask

import shapely
from shapely.geometry import mapping
from shapely.ops import unary_union

from geometry.change_crs import change_crs

from enum import Enum

def is_tiff(file):
    """
    Returns a boolean indicating if a file is a tiff image
    
    Parameters:
        file: (Relative) Path to file wanting to check if a tiff
    """
    filename, file_extension = os.path.splitext(file)
    
    file_extension = file_extension.lower()
    
    return file_extension.find(".tif") == 0


def get_tiffs_from_folder(tiff_folder):
    """
    Return all the tiffs files from the tiff_folder
    
    Parameters:
        file: (Relative) Path to folder wanting to check
    """
    if not os.path.isdir(tiff_folder):
        raise Exception(f"Folder {tiff_folder} Doesn't Exist")

    files = os.listdir(tiff_folder)

    tiff_files = []

    for file in files:
        if is_tiff(file):
            file = f"{tiff_folder}{file}"
            tiff_files.append(file)

    return tiff_files


def join_tiffs(merged_file, rasters_folder=None, rasters_paths=[]):
    """
    Joins all the tiffs present in the rasters_paths or rasters_folder in a merged geo-referenced
    file saved in merged_file
    
    Parameters:
        merged_file: Path where to save the merged tiff file
        rasters_folder (Optional): Path where to read files from (only tiffs file will be read)
        rasters_paths (Optional): List of tiff paths to be joined        
    """
    if rasters_folder is not None:
        rasters_paths = get_tiffs_from_folder(rasters_folder)
        if len(rasters_paths) == 0:
            raise Exception(f"No Tiffs Files Were Found In {rasters_folder}")
    else:
        asked_paths = rasters_paths.copy()
        rasters_paths = []
        for path in asked_paths:
            if is_tiff(path):
                rasters_paths.append(path)
        if len(rasters_paths) == 0:
            raise Exception(f"No Tiffs Files Were Found In Asked List")

    list_raster = []
    for path_raster in rasters_paths:
        raster_file = rasterio.open(path_raster)
        list_raster.append(raster_file)

    mosaic, out_trans = merge(list_raster)

    with rasterio.open(merged_file, 'w', driver = 'GTiff',
            height = mosaic.shape[1],
            width = mosaic.shape[2],
            count = mosaic.shape[0],
            dtype = str(mosaic.dtype),
            crs = raster_file.crs,
            transform = out_trans,
            compress = "deflate") as dest:
        dest.write(mosaic)


def reproject_raster(path_raster_in, path_raster_out, crs_out) -> None:
    """
    Change de CRS of an existing raster.
    
    Note: As squares are not exact from one crs to other, some exact coordinate might change its value.
    
    Parameters:
        - path_raster_in: (Relative) Path to the raster wanted to transform
        - path_raster_out: (Relative) Path where to save the raster with changed crs
        - crs_out: CRS code of the new CRS wanted for the raster
    """
    if not is_tiff(path_raster_in):
        raise Exception(f"Input Raster [{path_raster_in}] Is Not A Raster")
        
    if not is_tiff(path_raster_out):
        raise Exception(f"Output Raster [{path_raster_out}] Is Not A Raster")
    
    if not os.path.isfile(path_raster_in):
        raise Exception(f"Input Raster [{path_raster_in}] Doesn't Exist")
    
    bands = []
    write_file = "aux.tif"
    
    with rasterio.open(path_raster_in) as src:
        transform, width, height = calculate_default_transform(
            src.crs, crs_out, src.width, src.height, *src.bounds)

        kwargs = src.meta.copy()
        kwargs.update({
            'crs': crs_out,
            'transform': transform,
            'width': width,
            'height': height
        })
        tiff_transform = src.transform
        tiff_crs = src.crs
        for i in range(1, src.count + 1):
            band = rasterio.band(src, i)
            bands.append(band)
            
        with rasterio.open(write_file, 'w', **kwargs) as dst:
            for i, band in enumerate(bands):
                reproject(
                    source = band,
                    destination = rasterio.band(dst, i+1),
                    src_transform = tiff_transform,
                    src_crs = tiff_crs,
                    dst_transform = transform,
                    dst_crs = crs_out,
                    resampling = Resampling.nearest
                )
    
    os.rename(write_file, path_raster_out)


def get_image_polygon_aux(image, transform_tif, max_value, min_value, joined):
    """
    Returns a (list of) polygon(s) of the values between 2 extremes values in a raster
    
    Parameters:
        - image: Numpy matrix of the data to analyze
        - transform_tif: The transform function of the tif associated to the image
        - max_value: Max value valid for pixel to be included (<=) in polygon.
        - min_value: Min value valid for pixel to be excluded (>) in polygon.
        - joined: Boolean that indicates if should join all polygons into a multiplyogn or return a list
            of polygons.
    """
    mascara = np.where(image <= max_value, image, min_value)
    mascara = np.where(mascara > min_value, np.uint8(1), np.uint8(0)).astype("uint8")
    if np.sum(mascara) == 0:
        if joined:
            return None
        else:
            return []
    
    results = ({'properties': {'raster_val': v}, 'geometry': s} 
               for i, (s, v) in enumerate(shapes_rasterio(mascara, mask=(mascara==1), transform=transform_tif)))
    sub_mask = [shapely.geometry.shape(v['geometry']) for v in results]
    
    if joined:
        extent = unary_union(sub_mask)
        return extent
    else:
        return sub_mask


def get_polygons_from_tiff(tiff_file, max_value=None, min_value=0, joined=True, raster_band=1):
    """
    Returns a (list of) polygon(s) of the values between 2 extremes values in a raster
    
    Parameters:
        - tiff_file: (Relative) Path to the raster wanted to check.
        - max_value (Optional): Max value valid for pixel to be included (<=) in polygon. By deafult is 
            the max value found there.
        - min_value (Optional): Min value valid for pixel to be excluded (>) in polygon. By default is 0.
        - joined (Optional): Boolean that indicates if should join all polygons into a multiplyogn or return a list
            of polygons. By default is set to True.
        - raster_band (Optional): int indicating what raster to read. By default set to 1.    
    """
    if not is_tiff(tiff_file):
        raise Exception(f"Input Raster [{tiff_file}] Is Not A Raster")
    
    if not os.path.isfile(tiff_file):
        raise Exception(f"Input Raster [{tiff_file}] Doesn't Exist")

    with rasterio.open(tiff_file) as src:
        data = src.read(raster_band)
        transform_tif = src.transform
    
    if max_value is None:
        max_value = np.max(data)
    
    return get_image_polygon_aux(data, transform_tif, max_value, min_value, joined)


def get_total_bound(polygons):
    """
    Returns the bounds (min_x, min_y, max_x, max_y) of a list of polygons
    
    Parameters:
        - polygons: list of polygons to get their total bound from
    """

    min_x = float("inf")
    min_y = float("inf")
    max_x = -float("inf")
    max_y = -float("inf")
    
    for pol in polygons:
        if pol is None:
            continue
        bounds = list(pol.bounds)
        if bounds[0] < min_x:
            min_x = bounds[0]
        if bounds[1] < min_y:
            min_y = bounds[1]
        if bounds[2] > max_x:
            max_x = bounds[2]
        if bounds[3] > max_y:
            max_y = bounds[3]
    
    return [min_x, min_y, max_x, max_y]


def create_tiff_from_polygons(polygons, width, height, tiff_file=None, crs_pol=None, crs_img=None):
    """
    Returns a numpy matrix with ones inside the polygons area and 0 outside. 
    If a file is provided, the image will be saved with georeference
    
    Parameters:
        - polygons: Dict of Polygons wanting to be saved as tiff with the key being the value on the
            tiff and the value being the polygons
        - width: Width of the image wanting to be created
        - height: Height of the image wanting to be created
        - tiff_file (Optional): (Relative) Path where to save the tiff image file.
            If included, crs_pol MUST be included.
        - crs_pol (Optional): CRS in which the data of the polygon is stored
        - crs_img (Optional): What CRS to save the image with. By default it'll
            be saved with the crs of the polygon.
    """
    width = int(width)
    height = int(height)

    shape = (height, width)
    raster_data = np.zeros(shape, dtype=np.uint8)

    if len(polygons) == 0:
        return raster_data
    
    if crs_pol is not None and crs_img is not None:
        if crs_pol != crs_img:
            for tiff_value, polygons_assigned in polygons.items():
                polygons_new = change_crs(polygons_assigned, crs_pol, crs_img)
                polygons[tiff_value] = polygons_new
        crs_pol = crs_img
        
    if tiff_file and not is_tiff(tiff_file):
        raise Exception(f"Input Raster [{tiff_file}] Is Not A Raster File")
    
    if tiff_file and not crs_pol:
        raise Exception("When given a File, a CRS of polygon MUST be provided")

    all_polygons = []
    for pol_aux in polygons.values():
        all_polygons.extend(pol_aux)

    extremes = get_total_bound(all_polygons)
    transform = rasterio.transform.from_bounds(*extremes, width, height)

    for value, polygons_val in polygons.items():
        mask = geometry_mask(polygons_val,
                            out_shape=shape,
                            transform=transform,
                            all_touched=True,
                            invert=True)

        raster_data[mask] = value
    
    if tiff_file:
        with rasterio.open(tiff_file, "w", driver = 'GTiff',
            height = height,
            width = width,
            count = 1,
            dtype = "uint8",
            crs = crs_img,
            transform = transform,
            nodata = 0,
            compress = "deflate") as dest:
            dest.write(raster_data, 1)

    return raster_data


def change_box_crs(bbox, bbox_crs, new_crs):
    """
    Change the CRS of a given bounding box (min_x, min_y, max_x, max_y)

    Parameters:
        - bbox: Bounding Box to change the crs of
        - bbox_crs: CRS of the given bounding box
        - new_crs: CRS to set to the bbox
    """
    if bbox_crs == new_crs:
        return bbox

    lowest_point = (bbox[0], bbox[1])
    lowest_point = change_crs(lowest_point, bbox_crs, new_crs)
    highest_point = (bbox[2], bbox[3])
    highest_point = change_crs(highest_point, bbox_crs, new_crs)

    new_bbox = [lowest_point[0], lowest_point[1], highest_point[0], highest_point[1]]

    return new_bbox


def crop_geotiff(input_paths, output_path, bbox, bbox_crs=None, pad=10):
    """
    Crops geotiffs given a bbox, and creates a pad if asked.

    Parameters:
        - input_paths: Paths to the tiffs to crop
        - output_path: Path where to save the cropped tiff
        - bbox: Bounding Box to cut the geotiff from (min_x, min_y, max_x, max_y)
        - bbox_crs (Optional): CRS of the given bounding box. By default it'll be assumed it matches
            the crs of the input_path.
        - pad (Optional): How many pixels to extend the image by.
    """
    datas = []

    if not is_tiff(output_path):
        raise Exception(f"Save Raster [{output_path}] Is Not A Raster Valid Name")
    
    for input_path in input_paths:
        if not is_tiff(input_path):
            raise Exception(f"Input Raster [{input_path}] Is Not A Raster")
        
        if not os.path.isfile(input_path):
            raise Exception(f"Input Raster [{input_path}] Doesn't Exist")
    
    for i, input_path in enumerate(input_paths):
        with rasterio.open(input_path) as src:
            if i == 0:
                bounds = src.bounds
                tiff_crs = src.crs
                if bbox_crs:
                    bbox = change_box_crs(bbox, bbox_crs, tiff_crs)
                    bbox_crs = tiff_crs

                if bbox[0] < bounds[0]:
                    bbox[0] = bounds[0]

                if bbox[1] < bounds[1]:
                    bbox[1] = bounds[1]
    
                if bbox[2] > bounds[2]:
                    bbox[2] = bounds[2]

                if bbox[3] > bounds[3]:
                    bbox[3] = bounds[3]
                
                print(bbox)

                row_start, col_start = src.index(bbox[0], bbox[3])
                row_start -= pad
                if row_start < 0:
                    row_start = 0
                
                col_start -= pad
                if col_start < 0:
                    col_start = 0
                
                row_stop, col_stop = src.index(bbox[2], bbox[1])
                row_stop += pad
                if row_stop > src.height:
                    row_stop = src.height
                
                col_stop += pad
                if col_stop > src.width:
                    col_stop = src.width

                print(row_start, col_start, row_stop, col_stop)
                
                width = abs(col_stop - col_start)
                height = abs(row_stop - row_start)

            for index in src.indexes:
                data = src.read(window=Window(col_start+1, row_start+1, width, height), indexes=index)
                datas.append(data)

    stacked_data = np.stack(datas)
    num_bands = len(datas)

    # Use metadata from the first input raster
    metadata = src.meta.copy()

    # Update metadata for the output file
    metadata.update({
        'count': num_bands,
        'width': width,
        'height': height,
        'transform': rasterio.windows.transform(window=Window(col_start+1, row_start+1, width, height), transform=src.transform)
    })
    metadata["compress"] = "deflate"

    # Write the data to a new raster file
    with rasterio.open(output_path, 'w', **metadata) as dst:
        for i in range(num_bands):
            band_data = stacked_data[i, :, :]
            dst.write(band_data, i + 1)


def get_bbox(polygons):
    """
    Returns the bounding box of a list of polygons

    Parameters:
        - polygons: List of polygons to get the boudning box from
    """
    current_bound = [float("inf"), float("inf"), -float("inf"), -float("inf")] 
    
    for pol in polygons:
        x_min, y_min, x_max, y_max = pol.bounds
        
        if x_min < current_bound[0]:
            current_bound[0] = x_min
        
        if y_min < current_bound[1]:
            current_bound[1] = y_min
        
        if x_max > current_bound[2]:
            current_bound[2] = x_max
        
        if y_max > current_bound[3]:
            current_bound[3] = y_max
    
    return current_bound


def clip_tiff(save_file, land, tiff_file):
    """
    Clips a geotif given a geodataframe extent.

    Parameters:
        - save_file: Path where to save the clipped tiff
        - land: GeoDataframe where to get the geometries from
        - tiff_file: Path to the tif to clip
    """
    if not is_tiff(tiff_file):
        raise Exception(f"Input Raster [{tiff_file}] Is Not A Raster")
    
    if not is_tiff(save_file):
        raise Exception(f"Save Raster [{save_file}] Is Not A Raster Valid Name")
    
    if not os.path.isfile(tiff_file):
        raise Exception(f"Input Raster [{tiff_file}] Doesn't Exist")

    with rasterio.open(tiff_file) as src:
        crs_tif = src.crs 
        land.to_crs(crs_tif,inplace=True)
        masas_tierra = [mapping(v) for v in land["geometry"].to_list()]
        clip, tansf = mask(src, masas_tierra, invert = False, nodata=None)

        imagen = clip[0, :, :]
        kwargs = src.meta.copy()
        
        land_bbox = get_bbox(land["geometry"].to_list())
    
    kwargs["compress"] = "deflate"

    with rasterio.open(save_file, 'w', **kwargs) as dst:
        dst.write(imagen.astype('uint8'), 1)
    
    crop_geotiff([save_file], save_file, land_bbox)


class Borders(Enum):
    IGNORE = 0
    OVERLAP = 1
    FILL = 2


def create_window(tiff_src, start_x, start_y, size, output_path, ignore_end=False):
    """
    Crop Tiff into a smaller square window

    Parameters:
        - tiff_src: Rasterio Opened File of the tiff to crop
        - start_x: X position where to start the window
        - start_y: Y Position where to start the window
        - size: Size of the square to create
        - output_path: (Relative) Path where to save the clip
        - ignore_end (Optional): Bool indicating if it should create extending over the 
            existing end.
    """
    end_x = start_x + size
    if end_x > tiff_src.width and not ignore_end:
        end_x = tiff_src.width

    end_y = start_y + size
    if end_y > tiff_src.height and not ignore_end:
        end_y = tiff_src.height
    
    window_width = end_x - start_x
    window_height = end_y - start_y

    window = Window(start_x, start_y, window_width, window_height)
    datas = []
    for index in tiff_src.indexes:
        data = tiff_src.read(window=window, indexes=index)
        datas.append(data)
        stacked_data = np.stack(datas)

    num_bands = len(datas)
    metadata = tiff_src.meta.copy()
    metadata.update({
        'count': num_bands,
        'width': window_width,
        'height': window_height,
        'transform': rasterio.windows.transform(window=window, transform=tiff_src.transform)
    })
    metadata["compress"] = "deflate"

    with rasterio.open(output_path, 'w', **metadata) as dst:
        for i in range(num_bands):
            band_data = stacked_data[i, :, :]
            dst.write(band_data, i + 1)


def grid_raster(tiff_file, size, save_folder, overlap=0, extremes = Borders.IGNORE):
    """
    Clips the raster into smaller rasters of size x size
    
    Parameters:
        - tiff_file: (Relative) Path to the raster wanted to grid.
        - size: integer representing the size wanted for the smaller rasters.
        - save_folder: (Relative) Path where to save the smaller rasters.
        - overlap (Optional): Pixels that overlap between neighbours clips. By 
            default set in 0.
        - extremes (Optional): How to handle the extremes. IGNORE = Create smaller clip, OVERLAP = Overlap with previous
            FILL = Fill the missing space with 0s. By defualt set in IGNORE.
    """

    if not is_tiff(tiff_file):
        raise Exception(f"Input Raster [{tiff_file}] Is Not A Raster")
    
    if overlap < 0:
        raise Exception(f"Overlap value can't be negative")
    
    if not os.path.isdir(save_folder):
        os.makedirs(save_folder)

    x_pos = 0
    y_pos = 0

    with rasterio.open(tiff_file) as src:
        height = src.height
        width = src.width
        while x_pos * size - overlap * x_pos < width:
            while y_pos * size - overlap * y_pos < height:
                start_x = x_pos * size
                start_x -= overlap * x_pos
                if extremes == Borders.OVERLAP and start_x + size > width:
                    start_x = width - size
                
                start_y = y_pos * size
                start_y -= overlap * y_pos
                if extremes == Borders.OVERLAP and start_y + size > height:
                    start_y = height - size

                output_path = f"{save_folder}/{x_pos}_{y_pos}.tif"
                create_window(src, start_x, start_y, size, output_path, ignore_end = True)
                y_pos += 1
            y_pos = 0
            x_pos += 1
