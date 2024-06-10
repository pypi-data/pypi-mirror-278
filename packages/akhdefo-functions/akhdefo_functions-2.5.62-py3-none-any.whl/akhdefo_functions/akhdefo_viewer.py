
import os
import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm, Normalize
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
import rasterio
import rasterio.plot
import earthpy.spatial as es
import earthpy.plot as ep
import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import re
from datetime import datetime
import os
import re
import numpy as np
import rasterio
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize, TwoSlopeNorm
import rasterio.plot
import earthpy.spatial as es
from matplotlib_scalebar.scalebar import ScaleBar

def akhdefo_viewer(path_to_dem_file, raster_file, output_folder, title='', 
                   pixel_resolution_meters=3.125, output_file_name="", 
                   alpha=0.5, unit_conversion=None, no_data_mask=False, 
                   colormap='jet', min_value=None, max_value=None, 
                   normalize=False, colorbar_label=None, show_figure=True , aspect_raster=None, cmap_aspect=None, step=10):
    """
    Overlays a raster file on a DEM hillshade and saves the plot as a PNG image.

    Parameters:
    path_to_dem_file (str): Path to the DEM file.
    raster_file (str): Path to the raster file.
    output_folder (str): Path to the folder where the output image will be saved.
    title (str, optional): Title of the plot. Defaults to the raster file's basename.
    pixel_resolution_meters (float, optional): Pixel resolution of the raster in meters. Default is None get resolution from raster input.
    output_file_name (str, optional): Name of the output PNG image. Defaults to the raster file's basename.
    alpha (float, optional): Alpha value for the raster overlay. Default is 0.5.
    unit_conversion (str, optional): Unit conversion factor for the raster values. For example, '100cm' for meters to centimeters conversion.
    no_data_mask (bool, optional): If True, masks pixels with a value of 0 in the raster. Default is False.
    colormap (str, optional): Colormap to use for the raster. Default is 'jet'.
    min_value (float, optional): Minimum value for normalization. Uses raster's minimum if None.
    max_value (float, optional): Maximum value for normalization. Uses raster's maximum if None.
    normalize (bool, optional): If True, normalizes the raster values. Default is False.
    colorbar_label (str, optional): Label for the colorbar. 
    show_figure (bool, optional): Whether to display the figure. Default is True.
    aspect_raster (str, optional): whetehr to plot displacement vector. Dedulat is None 
    cmap_aspect (str, optional): colormap to sue for the vector arrows
    step (int, optional): density of the aspect vector arraows. Defulat is 10 pixel unit draw 1 arrow

    Returns:
    None
    """
    try:
        
        with rasterio.open(path_to_dem_file) as src:
            # Number of bands
            band_count = src.count
            xres, yres=src.res
            if band_count >2:
                dem = src.read(masked=True)
                dem_transform = src.transform
                hillshade=dem
                
            else:
                dem = src.read(1, masked=True)
                dem_transform = src.transform
            
                hillshade = es.hillshade(dem)
                

        with rasterio.open(raster_file) as src:
            raster = src.read(1, masked=True)
            raster_transform = src.transform
            raster_crs = src.crs
    

        if no_data_mask:
            raster = np.ma.masked_where(raster == 0, raster)

        if unit_conversion:
            unit_type, unit_factor = _separate_floats_letters(unit_conversion)
            raster *= float(unit_factor)

        if pixel_resolution_meters is None:
            pixel_resolution_meters=xres

        # Set the output file name if it's not provided
        if not output_file_name:
            output_file_name = os.path.splitext(os.path.basename(raster_file))[0] + ".png"

        _create_plot(hillshade, raster, dem_transform, raster_transform, raster_crs, alpha, colormap, normalize,
                     title, output_folder, output_file_name, colorbar_label, pixel_resolution_meters, min_value, max_value, aspect_raster, cmap_aspect, step)

        if show_figure:
            plt.show()
        else:
            plt.close()

    except Exception as e:
        raise RuntimeError(f"An error occurred: {e}")

def _separate_floats_letters(input_string):
    """
    Separates floats and letters from a string.
    """
    floats = re.findall(r'\d+\.\d+|\d+', input_string)
    letters = re.findall(r'[a-zA-Z]+', input_string)
    if not floats or not letters:
        raise ValueError("Invalid input string for unit conversion.")
    return letters[0], floats[0]

def _normalize_raster(raster, min_value, max_value):
    """
    Normalizes raster values between given minimum and maximum values.
    """
    if min_value is None and max_value is None:
        min_value = np.nanmin(raster)
        max_value = np.nanmax(raster)
    else:
        min_value=min_value
        max_value=max_value
       

    if np.nanmin(raster) < 0 and np.nanmax(raster) >0:
        norm = TwoSlopeNorm(vmin=min_value, vcenter=0, vmax=max_value)
    else:
        norm = Normalize(vmin=min_value, vmax=max_value)
    
    
    
    return raster, norm


def _create_plot(hillshade, raster, dem_transform, raster_transform, raster_crs, alpha, colormap, normalize,
                 title, output_folder, output_file_name, colorbar_label, pixel_resolution_meters, min_value, max_value , aspect_raster=None, cmap_aspect=None, step=10):
    """
    Creates and saves a plot of hillshade and raster overlay.
    """
    
    basemap_dimensions = hillshade.ndim
    fig, ax = plt.subplots(figsize=(10, 10))

    # Plot the hillshade layer using dem_transform for its extent
    if basemap_dimensions > 2:
        #ep.plot_rgb(hillshade, rgb=(0, 1, 2), str_clip=2, ax=ax, extent=rasterio.plot.plotting_extent(hillshade, transform=dem_transform))
        rasterio.plot.show(hillshade, transform=dem_transform, ax=ax)
    else:
        rasterio.plot.show(hillshade,extent=rasterio.plot.plotting_extent(hillshade, transform=dem_transform), ax=ax , cmap='gray')
        # ep.plot_bands(
        #     hillshade,
        #     ax=ax,
        #     cmap='gray',
        #     scale=False,
        #     cbar=False,
        #     extent=rasterio.plot.plotting_extent(hillshade, transform=dem_transform)  # ensure correct transform
        # )

    if aspect_raster is not None:
        alpha_basemap=0.45
    else:
        alpha_basemap=alpha
    
    if normalize:
        raster, norm = _normalize_raster(raster, min_value, max_value)
        
    if normalize==True:
    # Overlay the raster with alpha for transparency using raster_transform for its extent
        img = ax.imshow(raster, alpha=alpha_basemap, cmap=colormap, norm=norm,
                    extent=rasterio.plot.plotting_extent(raster, transform=raster_transform))  # ensure correct transform
    
    if normalize==False:
        
        if min_value is None and max_value is None:
            min_value = np.nanmin(raster)
            max_value = np.nanmax(raster)
        else:
            min_value=min_value
            max_value=max_value
        
        # Overlay the raster with alpha for transparency using raster_transform for its extent
        img = ax.imshow(raster, alpha=alpha_basemap, cmap=colormap, vmin=min_value , vmax=max_value,
                    extent=rasterio.plot.plotting_extent(raster, transform=raster_transform))  # ensure correct transform
        
    if aspect_raster is not None:
        def aspect_to_uv(aspect):
            """
            Convert aspect data to U and V components for arrows.
            """
            aspect_rad = np.deg2rad(aspect)
            u = np.sin(aspect_rad)
            v = np.cos(aspect_rad)
            return u, v
        # Load the raster file
        with rasterio.open(aspect_raster) as dataset:
            # Read the aspect data
            aspect_data = dataset.read(1)
            
            # Get the geotransformation data
            transform = dataset.transform

            # Get the shape of the data
            data_shape = aspect_data.shape

        # Generate a grid of points every 10 pixels
        step=step
        x_positions = np.arange(0, data_shape[1], step)
        y_positions = np.arange(0, data_shape[0], step)
        x_grid, y_grid = np.meshgrid(x_positions, y_positions)

        # Subset the aspect data to match the grid
        aspect_subset = aspect_data[y_positions[:, None], x_positions]
        aspect_subset, norm = _normalize_raster(aspect_subset, min_value=None, max_value=None)
        u_subset, v_subset = aspect_to_uv(aspect_subset)

        # Convert grid positions to real world coordinates
        x_grid_world, y_grid_world = transform * (x_grid, y_grid)
        if cmap_aspect is None:
            cmap_aspect='hsv'
        quiver = ax.quiver(x_grid_world, y_grid_world, u_subset, v_subset, aspect_subset, scale=20, cmap=cmap_aspect , angles='xy', norm=norm, alpha=alpha)
        # Adding a second colorbar in a horizontal position
        cbar_ax2 = fig.add_axes([0.25, 0.04, 0.5, 0.02])  # Position for the horizontal colorbar
        cbar2 = fig.colorbar(quiver, cax=cbar_ax2, orientation='horizontal',  extend='both')  # Using the ScalarMappable created earlier
        cbar2.set_label('Aspect-Colorbar(degrees)')
            

    # Add colorbar
    if colorbar_label:
        cbar_ax = fig.add_axes([0.92, 0.22, 0.02, 0.5])
        fig.colorbar(img, cax=cbar_ax, label=colorbar_label, extend='both')

    # Set axis labels based on CRS
    if raster_crs.is_geographic:
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
    else:
        ax.set_xlabel('Easting')
        ax.set_ylabel('Northing')

    #ax.grid(True, which='major')
    ax.set_title(title)

   
        
    scalebar = ScaleBar(dx=pixel_resolution_meters, location='lower right', units='m',
                        frameon=True, scale_loc='bottom', dimension='si-length', box_color='white', color='k', border_pad=1, box_alpha=0.65)  # Adjust parameters as needed
   
    ax.add_artist(scalebar)
      
    # Save the plot
    plt.savefig(os.path.join(output_folder, output_file_name), dpi=100, bbox_inches='tight')