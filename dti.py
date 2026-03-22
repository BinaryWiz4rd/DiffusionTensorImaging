import numpy as np
import nibabel as nib
from dipy.io.image import load_nifti, save_nifti
from dipy.io.gradients import read_bvals_bvecs
from dipy.core.gradients import gradient_table
from dipy.reconst.dti import TensorModel
from dipy.tracking.local_tracking import LocalTracking
from dipy.tracking.streamline import Streamlines
from dipy.tracking import utils
from dipy.direction import peaks_from_model
from dipy.data import get_sphere, fetch_stanford_hardi, read_stanford_hardi
from dipy.tracking.stopping_criterion import ThresholdStoppingCriterion


def run_tractography_pipeline(out_prefix="TractoAI_Result"):
    fetch_stanford_hardi()
    img, gtab = read_stanford_hardi()
    data = img.get_fdata()
    affine = img.affine

    print("Fitting Model...")
    tenmodel = TensorModel(gtab)
    tenfit = tenmodel.fit(data)
    fa = tenfit.fa

    print("Cleaning up noise...")
    seed_mask = fa > 0.4
    seeds = utils.seeds_from_mask(seed_mask, affine, density=[1, 1, 1])

    sphere = get_sphere(name='symmetric362')
    pg = peaks_from_model(model=tenmodel, data=data, sphere=sphere,
                          relative_peak_threshold=.5, min_separation_angle=25,
                          mask=seed_mask, return_sh=False)

    stopping_criterion = ThresholdStoppingCriterion(fa, .2)

    streamline_generator = LocalTracking(pg, stopping_criterion, seeds, affine, step_size=.5)
    raw_streamlines = Streamlines(streamline_generator)

    clean_streamlines = Streamlines([s for s in raw_streamlines if len(s) > 40])

    print(f"Final Count: {len(clean_streamlines)} high-quality tracts.")
    return clean_streamlines, fa


if __name__ == "__main__":
    from dipy.viz import window, actor, colormap

    streamlines, fa_map = run_tractography_pipeline()

    scene = window.Scene()

    line_actor = actor.line(streamlines, colors=colormap.line_colors(streamlines), linewidth=0.1)
    scene.add(line_actor)

    vol_actor = actor.slicer(fa_map, opacity=0.5)
    scene.add(vol_actor)

    scene.reset_camera()
    scene.zoom(1.5)

    print("Saving 'Clinical_Tractography_Final.png'...")
    window.record(scene=scene, out_path='Clinical_Tractography_Final.png', size=(1200, 900))

    print("Opening Interactive Window. It's ready for your presentation!")
    window.show(scene)