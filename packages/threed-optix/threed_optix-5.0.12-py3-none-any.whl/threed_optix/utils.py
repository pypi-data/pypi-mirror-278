import numpy as np
from scipy.stats import norm
import cv2
import threed_optix.package_utils.vars as v
# import matlabparser as mpars
# import threed_optix.package_utils.matlab as mt
import re
import matplotlib.pyplot as plt
import plotly.express as px

def wavelengths_normal_distribution(mean_wavelength, std_dev, num_wavelengths):
    wavelengths = {}
    wavelengths_list = np.linspace(mean_wavelength - 3 * std_dev, mean_wavelength + 3 * std_dev, num_wavelengths)
    weights =  norm.pdf(wavelengths_list, mean_wavelength, std_dev)
    sum_of_weights = np.sum(weights)

    for i in range(num_wavelengths):
        wavelength = wavelengths_list[i]
        weight = weights[i] * (v.WEIGHTS_RANGE[1] - v.WEIGHTS_RANGE[0]) / sum_of_weights + v.WEIGHTS_RANGE[0]
        weight = np.maximum(v.WEIGHTS_RANGE[0], np.minimum(v.WEIGHTS_RANGE[1], weight))
        wavelengths[wavelength] = weight

    return wavelengths

def wavelengths_uniform_distribution(min_wavelength, max_wavelength, num_wavelengths):
    wavelengths = {}
    wavelengths_list = np.linspace(min_wavelength, max_wavelength, num_wavelengths)
    weight = 1.0 / num_wavelengths  # Equal weight for each wavelength

    for wavelength in wavelengths_list:
        wavelengths[wavelength] = weight

    return wavelengths

def calculate_spot_size(intensity_matrix):
    # Convert the intensity matrix to uint8 type for processing
    intensity_image = np.array(intensity_matrix, dtype=np.uint8)

    # Apply thresholding to extract the spot
    _, thresholded = cv2.threshold(intensity_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Find contours of the spot
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Assuming the largest contour corresponds to the spot
    if len(contours) > 0:
        largest_contour = max(contours, key=cv2.contourArea)
        # Calculate the minimum enclosing circle around the contour
        (_, _), radius = cv2.minEnclosingCircle(largest_contour)
        # Calculate diameter from radius
        spot_diameter = 2 * radius
        return spot_diameter

    return float('inf')

def center_of_energy_mass(matrix):
    total_mass = sum(sum(row) for row in matrix)

    center_row = sum(i * sum(row) for i, row in enumerate(matrix, start=1)) / total_mass
    center_col = sum(j * matrix[i-1][j-1] for i, row in enumerate(matrix, start=1) for j in range(1, len(row)+1)) / total_mass

    return (center_col, center_row)

def encircled_energy(matrix, percent = 0.9):
    center_point = center_of_energy_mass(matrix)
    # Generate a grid of indices
    indices = np.indices(matrix.shape)

    # Calculate distances from each point in the matrix to the center point
    distances = np.sqrt((indices[0] - center_point[0])**2 + (indices[1] - center_point[1])**2)

    # Flatten the distances and spot matrix for sorting
    flat_distances = distances.flatten()
    flat_spot_matrix = matrix.flatten()

    # Get the indices of the distances within the potential circle
    inside_circle_indices = flat_distances <= flat_distances.max()

    # Sort the relevant distances and corresponding spot matrix values
    sorted_indices = np.argsort(flat_distances[inside_circle_indices])
    sorted_distances = flat_distances[inside_circle_indices][sorted_indices]
    sorted_spot_matrix = flat_spot_matrix[inside_circle_indices][sorted_indices]

    # Calculate cumulative distribution of energy
    cumulative_energy = np.cumsum(sorted_spot_matrix)

    # Find the index where cumulative energy exceeds 90%
    threshold_index = np.argmax(cumulative_energy >= percent * cumulative_energy[-1])

    # Use the distance at the threshold index as the radius
    radius = sorted_distances[threshold_index]

    return radius, center_point

def absolute_pixel_size(resolution, size):
    # Calculate pixel size for width and height
    pixel_size_width = size[0] / resolution[0]
    pixel_size_height = size[1] / resolution[1]

    return (pixel_size_width, pixel_size_height)

def visualize_spot(matrix, center_point, radius):
    plt.figure(figsize=(10, 10))
    plt.imshow(matrix)
    plt.scatter(center_point[1], center_point[0], marker='x', color='red')
    plt.gca().add_patch(plt.Circle((center_point[1], center_point[0]), radius, color='red', fill=False))
    plt.show()

def visualize_matrix(matrix, interactive = False, title = None):

    if not interactive:
        plt.figure(figsize=(10, 10))
        plt.imshow(matrix)
        if title:
            plt.title(title)
        plt.show()

    if interactive:
        fig = px.imshow(matrix, color_continuous_scale = v.COLOR_SCALE)
        if title:
            fig.update_layout(title_text = title)
        fig.show()
