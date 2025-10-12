"""
Credit for this project : https://basicsr.readthedocs.io/en/latest/_modules/basicsr/data/degradations.html
                         and 
                         RealESRGAN paper https://arxiv.org/abs/2107.10833
"""


from utils import *

"""
same function enforced for both 1st and 2nd order degradation ,
order='first' or 'second' to enforce first order degradation and second order degradation respectively.
"""
def one_order_deg(img,target_size, order='first',second_blur_prob=0.2, second_sinc_prob=0.8):


#----------------------Blur using different random kernels-----------------
    a3= np.arange(7,22,2)
    kernel_size = np.random.choice(a3,replace=True)

    kernel_list = ['iso', 'aniso', 'generalized_iso', 'generalized_aniso', 'plateau_iso', 'plateau_aniso']
    kernel_prob = [0.45, 0.25, 0.12, 0.03, 0.12, 0.03]
    # generate random kernels 
    if order=='second':
        if np.random.uniform() < second_blur_prob:
            sigma_range = [0.2,1.5]
            blur_kernel = random_mixed(kernel_list, kernel_prob, kernel_size=kernel_size,
                                        sinc_prob=0.1,sigma_x_range=sigma_range, sigma_y_range=sigma_range)
            img = cv2.filter2D(img,-1, blur_kernel)
    else:
        blur_kernel = random_mixed(kernel_list, kernel_prob, kernel_size=kernel_size, sinc_prob=0.1)
        img = cv2.filter2D(img,-1, blur_kernel)

    # apply kernel to image
    

#---------------------------------Resize using random interpolation modes-----------------------
    if order== 'first':
        target_size= [target_size[0] * 2, target_size[1] * 2]

    mode = random.choice([cv2.INTER_CUBIC, cv2.INTER_AREA, cv2.INTER_LINEAR])
    img = cv2.resize(img,target_size,interpolation=mode)

#------------------Add random noises in the image--------------------------

    # The original degradation parameters were commented out, and poisson noise was not used in this implementation.
    # noise_prob = [0.5,0.5]
    # noise_type_list = ['gaussian', 'poisson']
    noise_prob = [1.0]
    noise_type_list = ['gaussian']
    gray_noise_prob = 0.4
    img = add_random_noise(img,noise_type_list, noise_prob, gray_noise_prob,order=order)
        

#--------------Add jpeg compression------------------
    quality = np.random.uniform(30,96)
    img = add_jpg_compression(img,quality=quality)


#-------------------If second order degradation add 2d sinc at last-------
    if order=='second':
        if np.random.uniform()< second_sinc_prob:

            # this sinc filter setting is for kernels ranging from [7, 21]
            if kernel_size < 13:
                omega_c = np.random.uniform(np.pi / 3, np.pi)
            else:
                omega_c = np.random.uniform(np.pi / 5, np.pi)

            second_sinc_kernel = deg.circular_lowpass_kernel(cutoff=omega_c, kernel_size=kernel_size, pad_to=False)

            img = cv2.filter2D(img,-1, second_sinc_kernel)
    return img


def degrade_img(img):

    resize_dim = (480,270)

    #first order degradation
    img = one_order_deg(img,target_size=resize_dim)

    #second order degradation
    img = 255 * img
    img = one_order_deg(img,target_size=resize_dim,order='second')

    return img
    