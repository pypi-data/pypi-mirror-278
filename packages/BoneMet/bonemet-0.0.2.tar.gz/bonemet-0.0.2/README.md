# MedNerf with BoneMet

## Training Med-Nerf with BoneMet data

See the [mednerf repository](https://github.com/abrilcf/mednerf) for more specific details and instructions on using the medNerf model.

To train mednerf with BoneMet data, first download training data [here](https://huggingface.co/datasets/BoneMet/BoneMet/tree/main/Imagery_Dataset/4.%20Regist-CT). To prepare the data for training, crop each image to a 128x128 .png image that contains each tibia. Store all images in `mednerf/graf-main/data/knee_xrays`. In the graf-main directory, execute this command:

```python train.py configs/knee.yaml``` 

We reccomend training to 100,000 iterations. 

## Generating a reconstruction with Med-Nerf

After training the model you can generate 3D-aware CT projections with a given X-Ray. First, in `render_xray_G.py`, change the file path parameter in variable `target_xray` in line 158 to the path of the desired x-ray. Create a reconstruction with the command:

```python render_xray_G.py configs/knee.yaml / --save_dir="./renderings" / --model model_best.pt / --save_every 25 / --psnr_stop 25```

To change the quality of the reconstruction, increase the psnr threshold.

 The reconstruction output will be in the form of a .mp4 located in `graf-main/results/knee_all_360/renderings`.

##  Acknowledgements
This code orginates from the [mednerf](https://github.com/abrilcf/mednerf) repository. Thank you to the creators who worked hard on this model!


