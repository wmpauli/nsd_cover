import nibabel as nib
import numpy as np

# output of fast tissue seg
tmp_filename = '/home/pauli/Development/CIT_DeepBrain_Atlas/+Release+/CIT168_Amygdala_v1.0.3/CIT168_700um/CIT168_T1w_700um_seg.nii.gz'
# filename out deterministic dope atlas
det_atlas_filename = '/home/pauli/Downloads/det_atlas_bilateral.nii.gz'

# load seg file
tmp = nib.load(tmp_filename)
tmp_data = tmp.get_data()

# load det atlas
det_atlas_nii = nib.load(det_atlas_filename)
det_atlas = det_atlas_nii.get_data()

# remove the front of the brain
tmp_data[:,140:,:] = 0

# remove front left of dope atlas
det_atlas[99:,141:,:] = 0

# combine the two in a nasty/hacky way
det_atlas_flat = det_atlas.flatten() 
idx = np.where(det_atlas_flat > 0)[0]
tmp_data_flat = tmp_data.flatten()
tmp_data_flat[idx] = det_atlas_flat[idx] + 3
tmp_data = tmp_data_flat.reshape(tmp_data.shape)

# save file
out_nii = nib.Nifti1Image(tmp_data, tmp.affine)
out_nii.to_filename('binary_brain.nii.gz')
