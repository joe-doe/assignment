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


class Transform(object):
    def __init__(self):

        self.folder = '/home/giskard/PycharmProjects/assignment/data/'

        # read nibabel Nifti1 Image object as img
        # and GradientTable object as gtab
        self.img_dti, self.gtab_dti = self.read_data('dti')
        self.img_T1, self.gtab_T1 = self.read_data('t1')

        print (self.img_dti.header.get_sform())
        print (self.img_T1.header.get_sform())

        t1_header_affine = self.img_T1.header.get_sform()
        self.img_dti.header.set_sform(t1_header_affine)

        print (self.img_dti.header.get_sform())
        print (self.img_T1.header.get_sform())


    def read_data(self, name):
        fraw = pjoin(self.folder, name+'.nii')
        fbval = pjoin(self.folder, 'dti.bval')
        fbvec = pjoin(self.folder, 'dti.bvec')
        bvals, bvecs = read_bvals_bvecs(fbval, fbvec)
        gtab = gradient_table(bvals, bvecs)
        img = nib.load(fraw)
        return img, gtab