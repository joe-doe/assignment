"""
``numpy`` is for numerical computation

"""
import numpy as np

"""
``nibabel`` is for loading imaging datasets
"""

import nibabel as nib

"""
``dipy.reconst`` is for the reconstruction algorithms which we use to create
voxel models from the raw data.
"""

import dipy.reconst.dti as dti


from dipy.core.gradients import gradient_table
from dipy.io.gradients import read_bvals_bvecs
from dipy.segment.mask import median_otsu
from dipy.reconst.dti import fractional_anisotropy, color_fa, lower_triangular

from os.path import join as pjoin


class Reconstruction(object):
    def __init__(self):

        self.folder = '/home/giskard/.dipy/stanford_hardi'
        # self.folder = '/home/giskard/PycharmProjects/assignment/data/'

        # read nibabel Nifti1 Image object as img
        # and GradientTable object as gtab
        self.img, self.gtab = self.read_data()

        # test data
        self.data = self.img.get_data()
        print('data.shape (%d, %d, %d, %d)' % self.data.shape)

        # mask and crop
        self.maskdata, self.mask = self.mask_and_crop()

        # reconstruct voxel
        self.tenmodel, self.tenfit = self.reconstruct_voxel()

        # calculate
        self.fa = self.calculate_fa()

        # save FA image
        self.save_fa_image()

        # compute colored FA
        self.colored_fa = self.compute_colored_fa()

        # save png
        self.save_png()

    def read_data(self):
        fraw = pjoin(self.folder, 'dti.nii')
        fbval = pjoin(self.folder, 'dti.bval')
        fbvec = pjoin(self.folder, 'dti.bvec')
        bvals, bvecs = read_bvals_bvecs(fbval, fbvec)
        gtab = gradient_table(bvals, bvecs)
        img = nib.load(fraw)
        return img, gtab

    def mask_and_crop(self):
        maskdata, mask = median_otsu(self.data, 3, 1, True,
                                     vol_idx=range(10, 50), dilate=2)
        print('maskdata.shape (%d, %d, %d, %d)' % maskdata.shape)
        return maskdata, mask

    def reconstruct_voxel(self):
        # instantiate the Tensor model
        tenmodel = dti.TensorModel(self.gtab)

        # fit the data
        tenfit = tenmodel.fit(self.maskdata)

        return tenmodel, tenfit

    def calculate_fa(self):
        print('Computing anisotropy measures (FA, MD, RGB)')

        fa = fractional_anisotropy(self.tenfit.evals)

        # remove NaNs from fa
        fa[np.isnan(fa)] = 0

        return fa

    def save_fa_image(self):
        print('Saving FA image')

        fa_img = nib.Nifti1Image(self.fa.astype(np.float32), self.img.affine)
        nib.save(fa_img, 'tensor_fa.nii.gz')

    def compute_colored_fa(self):
        print('Computing colored FA')

        fa = np.clip(self.fa, 0, 1)
        rgb = color_fa(fa, self.tenfit.evecs)
        nib.save(nib.Nifti1Image(np.array(255 * rgb, 'uint8'), self.img.affine), 'tensor_rgb.nii.gz')

        return rgb

    def save_png(self):
        pass