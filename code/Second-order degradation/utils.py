"""
Credit for this project : https://basicsr.readthedocs.io/en/latest/_modules/basicsr/data/degradations.html
                         and 
                         RealESRGAN paper https://arxiv.org/abs/2107.10833
"""

import os
import cv2
import numpy as np
import random
import degradations as deg
import math
from skimage.util import random_noise


def add_jpg_compression(img, quality=90):
    """Add JPG compression artifacts.
    Args:
        img (Numpy array): Input image, shape (h, w, c), range [0, 1], float32.
        quality (float): JPG compression quality. 0 for lowest quality, 100 for
            best quality. Default: 90.

    Returns:
        (Numpy array): Returned image after JPG, shape (h, w, c), range[0, 1],
            float32.
    """
    img = np.clip(img, 0, 1)
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), int(quality)]
    _, encimg = cv2.imencode('.jpg', img * 255.0, encode_param)
    img = np.float32(cv2.imdecode(encimg, 1)) / 255.
    return img


def random_mixed(kernel_list,
                         kernel_prob,
                         kernel_size,
                         sinc_prob=0.00001,
                         sigma_x_range=(0.2, 3),
                         sigma_y_range=(0.2, 3),
                         rotation_range=(-math.pi, math.pi),
                         betag_range=(0.5, 4),
                         betap_range=(1, 2),
                         noise_range=None):
    """Randomly generate mixed kernels.
    Args:
        kernel_list (tuple): a list name of kernel types,
            support ['iso', 'aniso', 'skew', 'generalized', 'plateau_iso',
            'plateau_aniso']
        kernel_prob (tuple): corresponding kernel probability for each
            kernel type
        kernel_size (int):
        sigma_x_range (tuple): [0.6, 5]
        sigma_y_range (tuple): [0.6, 5]
        rotation range (tuple): [-math.pi, math.pi]
        beta_range (tuple): [0.5, 4] for generalized, [1,2] for plateau
        noise_range(tuple, optional): multiplicative kernel noise,
            [0.75, 1.25]. Default: None

    Returns:
        kernel (ndarray):
    """
    if np.random.uniform() < sinc_prob:

         # this sinc filter setting is for kernels ranging from [7, 21]
        if kernel_size < 13:
            omega_c = np.random.uniform(np.pi / 3, np.pi)
        else:
            omega_c = np.random.uniform(np.pi / 5, np.pi)

        kernel = deg.circular_lowpass_kernel(cutoff=omega_c, kernel_size=kernel_size, pad_to=False)
    
    else:

        kernel_type = random.choices(kernel_list, kernel_prob)[0]
        if kernel_type == 'iso':
            kernel = deg.random_bivariate_Gaussian(
                kernel_size, sigma_x_range, sigma_y_range, rotation_range, noise_range=noise_range, isotropic=True)
        elif kernel_type == 'aniso':
            kernel = deg.random_bivariate_Gaussian(
                kernel_size, sigma_x_range, sigma_y_range, rotation_range, noise_range=noise_range, isotropic=False)
        elif kernel_type == 'generalized_iso':
            kernel = deg.random_bivariate_generalized_Gaussian(
                kernel_size,
                sigma_x_range,
                sigma_y_range,
                rotation_range,
                betag_range,
                noise_range=noise_range,
                isotropic=True)
        elif kernel_type == 'generalized_aniso':
            kernel = deg.random_bivariate_generalized_Gaussian(
                kernel_size,
                sigma_x_range,
                sigma_y_range,
                rotation_range,
                betag_range,
                noise_range=noise_range,
                isotropic=False)
        elif kernel_type == 'plateau_iso':
            kernel = deg.random_bivariate_plateau(
                kernel_size, sigma_x_range, sigma_y_range, rotation_range, betap_range, noise_range=None, isotropic=True)
        elif kernel_type == 'plateau_aniso':
            kernel = deg.random_bivariate_plateau(
                kernel_size, sigma_x_range, sigma_y_range, rotation_range, betap_range, noise_range=None, isotropic=False)
    
    # pad kernel
    pad_size = (21 - kernel_size) // 2
    kernel1 = np.pad(kernel, ((pad_size, pad_size), (pad_size, pad_size)))
    return kernel1


"""
Credit: https://basicsr.readthedocs.io/en/latest/_modules/basicsr/data/degradations.html
"""
def add_random_gaussian_noise(img,sigma_range,gray_prob=0):
    sigma = np.random.uniform(sigma_range[0], sigma_range[1])
    mean=0
    
    if np.random.uniform() < gray_prob:
        noise = np.float32(np.random.normal(mean,sigma,img.shape[0:2])) * sigma / 255.
        noise = np.expand_dims(noise, axis=2).repeat(3, axis=2)

        noisy_image = img + noise
        noisy_image = cv2.normalize(noisy_image, noisy_image, 0, 255, cv2.NORM_MINMAX, dtype=-1)
        noisy_image = noisy_image.astype(np.uint8)

    else:
        gaussian = np.random.normal(0, sigma, img.shape) 

        noisy_image = np.zeros(img.shape, np.float32)

        noisy_image = img + gaussian
        

        noisy_image = cv2.normalize(noisy_image, noisy_image, 0, 255, cv2.NORM_MINMAX, dtype=-1)
        noisy_image = noisy_image.astype(np.uint8)

    return noisy_image/255


def add_random_poisson_noise(image,scale_range,clip=True):
        seed = None
        rng = np.random.default_rng(seed)
        scale = np.random.uniform(scale_range[0], scale_range[1])

        image = image.astype(np.float32)
        image = image/255

        if image.min() < 0:
                low_clip = -1.
        else:
                low_clip = 0.

        vals = len(np.unique(image))
        vals = 2 ** np.ceil(np.log2(vals))

        # Ensure image is exclusively positive
        if low_clip == -1.:
                old_max = image.max()
                image = (image + 1.) / (old_max + 1.)

        # Generating noise for each unique value in image.
        out = rng.poisson(image * vals) / float(vals)

        # Return image to original range if input was signed
        if low_clip == -1.:
                out = out * (old_max + 1.) - 1.

        if clip:
                out = np.clip(out, low_clip, 1.0)
        
        noise = (out - image)
        noise = noise * scale
        image = image + noise

        return image


def add_random_noise(img,
                noise_type_list,
                noise_prob,
                gray_noise_prob,
                sigma_range_gauss = [1.0,30.0],
                scale_range_poiss =[0.05,3.0],
                order='first'
                ):
    
    if order!='first':
        sigma_range_gauss=[1.0,25.0]
        scale_range_poiss=[0.05,2.5]

    noise_type = random.choices(noise_type_list, noise_prob)[0]
    if noise_type =='gaussian':
        img = add_random_gaussian_noise(
            img, sigma_range=sigma_range_gauss,gray_prob=gray_noise_prob)

    elif noise_type == 'poisson':
        img = add_random_poisson_noise(img, scale_range = scale_range_poiss)
        
    return img