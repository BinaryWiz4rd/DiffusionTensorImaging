# DTI Tractography Pipeline with DIPY

This repository contains a Python-based pipeline for **Diffusion Tensor Imaging (DTI)** reconstruction and **Fiber Tractography**. Using the `DIPY` library, the script processes diffusion-weighted magnetic resonance imaging (dMRI) data, fits a tensor model, and generates 3D streamlines representing white matter pathways.


<img width="675" height="495" alt="obraz" src="https://github.com/user-attachments/assets/768030a8-961d-4e66-a871-3c09ffb5a3fe" />

---

## Overview

The pipeline automates the following neuroimaging steps:
1.  **Data Acquisition**: Automatically fetches the Stanford HARDI dataset for demonstration.
2.  **Tensor Reconstruction**: Fits a `TensorModel` to the diffusion data.
3.  **Fractional Anisotropy (FA)**: Calculates FA maps to identify organized white matter structures.
4.  **Tractography**: 
    * Uses **Seed-based tracking** (masking FA > 0.4).
    * Implements a **Threshold Stopping Criterion** to ensure anatomical accuracy.
    * Filters streamlines by length (min 40 nodes) to remove noise.
5.  **Visualization**: Renders a high-resolution 3D interactive scene with stream tubes and FA slicers.

---

## Requirements

Ensure you have a Python environment (3.8+) with the following dependencies:

```bash
pip install numpy nibabel dipy fury
