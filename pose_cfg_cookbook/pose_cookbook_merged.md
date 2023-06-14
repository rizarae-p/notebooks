# The `pose_cfg.yaml` Handbook
Hello! Mabuhay! Hola!
In this notebook, we will have a rundown on the following pose config parameters related to data augmentation:


# 1. Goal 
<a id="goal"></a>
By the end of this short lesson, you should have a little bit more understanding of how to tweak the `pose_config.yaml` to fit your dataset and training needws.

# 2. What is *pose_cfg.yml*?
<a id="whatisposecfg"></a>
The `pose_cfg.yaml` file offers easy access to a range of training parameters that the user may want or have to adjust depending on the used dataset and task. We'll go over couple of situations that 
might require those changes or could benefit from some tuning.

# 3. Full parameter list
<a id="fullparamlist"></a>
1. [Training hyperparameters](#hyperparam)
    1. [`max_input_size` and `min_input_size`](#input_size)
    2. [`global_scale`](#global_size)
    3. [`batch_size`](#batch_size)
    4. [`pos_dist_thresh`](#pos)
    5. [`pafwidth`](#paf)
2. [Data augmentation parameters](#data_aug)
    1. [`scale_jitter_lo` and `scale_jitter_up`](#scale_jitter)
    2. [`rotation`](#rot)
    3. [`rotratio`](#rotratio)
    4. [`mirror`](#mirror)
    5. [`crop_size`](#crop_size)
    6. [`crop_raito`](#crop_ratio)
    7. [`max_shift`](#max_shift)
    8. [`crop_sampling`](#crop_sampling)
    9. [`sharpening` and `sharpenratio`](#sharpening)
    10. [`edge`](#edge)

<a id="hyperparam"></a>
## 3.1 Training Hyperparameters 

<a id="input_size"></a>
### 3.1.A `max_input_size` and `min_input_size`
The default values are `1500` and `64` respectively. 

💡Pro-tip:💡
- change `max_input_size` when resolution of the video is higher than 1500x1500 or when `scale_jitter_up` will possibly go over that value
- change `min_input_size` when resolution of the video is smaller than 64x64 or when `scale_jitter_lo` will possibly go below that value

<a id="global_scale"></a>
### 3.1.B `global_scale`
The default value is `0.8`. It's the most basic, first scaling that happens to all images in the training queue.

💡Pro-tip:💡
- With images that are low resolution or lack detail, it may be beneficial to increase the `global_scale` to 1, to keep original size and retain as much information as possible.

### 3.1.C `batch_size`
<a id="batch_size"></a>

The default for single animal projects is 1 and for maDLC projects it's `8`. It's the number of frames used per training iteration.

In both cases you can increase the batchsize up to the limit of your GPU memory and train for a lower number of iterations. The relationship between number of iterations and `batch_size` is not linear so `batch_size: 8` doesn't mean you can train for 8x less iterations, but like with every training, plateauing loss can be treated as an indicator of reaching optimal performance.

💡Pro-tip:💡
- Having a higher `batch_size` can be beneficial in terms of models' generalization

___________________________________________________________________________________

Values mentioned above and the augmenatation parameters are often intuitive and knowing our own data we are able to decide on what will and won't be beneficial. Unfortunately, not all hyperparameters are this simple or intuitive. Two of the parameters that might require some tuning on challanging datasets are `pafwidth` and `pos_dist_thresh`. 

<a id="pos"></a>
### 3.1.D `pos_dist_thresh`
The default value is `17`. It's the size of a window withing which detections are considered positive training samples, meaning they tell the model, that it's going in the right direction. 

<a id="paf"></a>
### 3.1.E `pafwidth`
The default value is `20`. 

<a id="data_aug"></a>
## 3.2 Data augmentation parameters
In the simplest form, we can think of data augmentation as something similar to imagination or dreaming. Humans imagine diferent scenarios based on experience, ultimately allowing us to gain a better understanding of our world. [1,2,3](#references)

In a similar way, we train our models to different types of "imagined" scenarios, which we limit to the foreseeable ones, so we ultimately get a robust model that can more likely handle new data and scenes. 

Classes of data augmentations, characterized by their nature, are given by:
- [**Geometric transformations**](#geometric)
    1. [`scale_jitter_lo` and `scale_jitter_up`](#scale_jitter)
    2. [`rotation`](#rot)
    3. [`rotratio`](#rotratio)
    4. [`mirror`](#mirror)
    5. [`crop size`](#crop_size)
    6. [`crop ratio`](#crop_ratio)
    7. [`max shift`](#max_shift)
    8. [`crop sampling`](#crop_sampling)
- [**Kernel transformations**](#kernel)
    9. [`sharpening` and `sharpen_ratio`](#sharp)
    10. [`edge_enhancement`](#edge)


<a id="geometric"></a>
### Geometric transformations
**Geometric transformations** such as *flipping*, *rotating*, *translating*, *cropping*, *scaling*, and *injecting noise*, which are very good for positional biases present in the training data.

<a id="scale_jitter"></a>
### 3.2.1 `scale_jitter_lo` and `scale_jitter_up`
*Scale jittering* resizes and crops an image within a given resize range. This allows the model to learn from different sizes of objects in the scene, therefore increasing its robustness to generalize especially on newer scenes or object sizes.

The image below, retrieved from [3](#ref3), illustrates the difference between two scale jittering methods.

![scale_jittering.png](pose_cookbook_merged_files/scale_jittering.png)

During training, each image is randomly scaled within the range `[scale_jitter_lo, scale_jitter_up]` to augment training data. The default values for these two parameters are:
- `scale_jitter_lo = 0.5`
- `scale_jitter_up = 1.25`

💡Pro-tips:💡
- ⭐⭐⭐ If the target animal/s do not have an incredibly high variance in size throughout the video (e.g. jumping or moving towards the static camera), keeping the **default** values **unchanged** is **enough** ✅ because the lowest scale jitter value by default is 50% of the original image and the largest scale jitter value by default is 125% of the original image.

- ⭐⭐However, you may want to adjust these parameters if you want your model to:
  - handle new data with possibly **larger (25% bigger than original)** animal subjects ➡️ in this scenario, increase the value of *scale_jitter_up*
  - handle new data with possibly **smaller (50% smaller than the original)** animal subjects ➡️ in this scenario, decrease the value of *scale_jitter_lo*
  - **generalize well in new set-ups/environments** with minimal to no pre-training
  ⚠️ But as a consequence, **training time will take longer**.😔🕒
- ⭐If you have a fully static camera set-up and the sizes of the animals do not vary much, you may also try to **shorten** this range to **reduce training time**.😃🕒(⚠️ but, as a consequence, your model might only fit your data and not generalize well)

<a id="rot"></a>
### 3.1.2 `rotation`
*Rotation augmentations* are done by rotating the image right or left on an axis between $1^{\circ}$ and $359^{\circ}$. Te safety of rotation augmentations is heavily determined by the rotation degree parameter. Slight rotations such as between $+1^{\circ}$ and $+20^{\circ}$ or $-1^{\circ}$ to $-20^{\circ}$ is generally an acceptable range. Keep in mind that as the rotation degree increases, the label of the data is no longer preserved post-transformation.

The image below retreived from [2](#ref2) illustrates the difference between the different rotation degrees.
![augset_rot.png](pose_cookbook_merged_files/augset_rot.png)

During training, each image is rotated $+/-$ the `rotation` degree parameter set. By default, this parameter is set to `25`, which means that the images are augmented with a $+25^{\circ}$ rotation of itself and a $-25^{\circ}$ degree rotation of itself. Should you want to opt out of this augmentation, set the rotation value to `False`.

💡Pro-tips:💡
- ⭐If you have labelled all the possible rotations of your animal/s, keeping the **default** value **unchanged** is **enough** ✅ 

- However, you may want to adjust this parameter if you want your model to:
  - handle new data with new rotations of the animal subjects 
  - handle the possibly unlabelled rotations of your minimally-labelled data 
    - But as a consequence, **the more you increase the rotation degree, the more the original keypoint labels may not be preserved**

<a id="rotratio"></a>
### 3.2.3 `rotratio` (rotation ratio)
This parameter in the DLC module is given by the percentage of sampled data to be augmented from your training data. The default value is set to `0.4` or $40\%$. This means that $40\%$ of the training data is collected randomly for rotation augmentation.

💡Pro-tip:💡
- ⭐ Generally, keeping the **default** value **unchanged** is **enough** ✅ 

<a id="mirror"></a>
### 3.2.4 `mirror` (or a horizontal flip)
**Mirroring** or otherwise called **horizontal axis fipping** is much more common than fipping the vertical axis. This augmentation is one of the easiest to implement and has proven useful on datasets such as CIFAR-10 and ImageNet. However, on datasets involving text recognition such as MNIST or SVHN, this is not a label-preserving transformation.

The image below is an illustration of this property (shown on the right most column).
![augset_flip.png](pose_cookbook_merged_files/augset_flip.png)

This parameter randomly flips an image horizontally to augment training data.
By default, this parameter is set to `False` especially on poses with mirror symmetric joints (for example, so the left  hand and right hand are not swapped).

💡Pro-tip:💡
- ⭐ If you work with labels with symmetric joints, keep the **default** value **unchanged**.✅
- Keeping the default value to `False` will work well in most cases.

<a id ="crop_size"></a>
### 3.2.5 `crop_size`
Cropping consists of removing unwanted pixels from the image, thus selecting a part of the image and discarding the rest, reducing the size of the input. 

In DeepLabCut *pose_config.yaml* file, by default ```crop_size``` is set to (```400,400```), width and height respectively. This means it will crop a set of images getting a size of 400,400 width and height respectively. 

💡Pro-tip:💡
 - If your images are very large, you could consider increasing the crop size. However, be aware that you'll need a strong GPU or you will hit memory errors!
 - If your images are very small, you could consider decreasing the crop size. 


<a id ="cropratio"></a>
### 3.2.6 `crop_ratio`
 Also, the number of frames to be cropped is defined by the variable ```cropratio```, which by default is se to ```0.4```. That means that, from the set of frames, the 40% will be randomnly selected to crop for data augmentation. By default this value works well. 

<a id ="max_shift"></a>
### 3.2.7 `max_shift`

 The cropp shift between each cropped image is defined by ```max_shift``` variable, which explains the max relative shift to the position of the crop centre. By default is set to ```0.4```, which means it will be displaced 40% max from the center of each crop. You'll get one cropped image and the next crop would move max 40% from the previous one. 
 
The image below is modified from [2](#references). 
![cropping.png](pose_cookbook_merged_files/cropping.png)

<a id ="crop_sampling"></a>
### 3.2.8 `crop_sampling`
Likewise, there are different cropping sampling methods (```crop_sampling```), we can use depending on how our image looks like. 

💡Pro-tips💡
- If your keypoints are restricted to one region of the image, you might want to use the variants ```keypoints``` or ```dentisy```. 
- If your animal moves along the whole plane, you could be interested on crop samples uniformly, ```uniform```. 
- You can use an ```hybrid``` method, which means 50% ```density``` and ```uniform```. This is the method chosen by default. 

<a id ="kernel"></a>
### Kernel transformations 
Kernel filters are very popular in image processing to sharpen and blur images. Intuitively, blurring an image might increase the motion blur resistance during testing. Otherwise, sharpening for data enhancement could result in capturing more detail on objects of interest.

<a id ="sharp"></a>
### 3.2.9 `sharpening` and `sharpenratio`
In DeepLabCut *pose_config.yaml* file, by default ```sharpening``` is set to ```False```, but if we want to use this type or data augmentation, we can set it ```True``` and specify a value for ```sharpenratio```, which by default is set to ```0.3```. Blurring is not defined in the *pose_config.yaml*, but if the user finds it convenient, it can be added to add data augmentation. 

The image below is modified from [2](#references). 
![kernelfilter.png](pose_cookbook_merged_files/kernelfilter.png)


<a id ="edge"></a>
### 3.2.10 `edge`
Concerning sharpeness, we have an additional parameter, ```edge``` enhancement, which enhances edge contrast of an image to improve its apparent sharpness. Likewise, by default this parameter is set ```False```, but if you want to include it you just need to set it ```True```.

# References 
<ol id="references">
    We report here relevant references:
    <li id="ref1">Shorten, C., & Khoshgoftaar, T. M. (2019). A survey on Image Data Augmentation for Deep Learning. In Journal of Big Data (Vol. 6, Issue 1). Springer Science and Business Media LLC. <a href="https://doi.org/10.1186/s40537-019-0197-0">https://doi.org/10.1186/s40537-019-0197-0</a> </li>
    <li id="ref2">Mathis, A., Schneider, S., Lauer, J., & Mathis, M. W. (2020). A Primer on Motion Capture with Deep Learning: Principles, Pitfalls, and Perspectives. In Neuron (Vol. 108, Issue 1, pp. 44-65). Elsevier BV. <a href="https://doi.org/10.1016/j.neuron.2020.09.017">https://doi.org/10.1016/j.neuron.2020.09.017</a></li>
    <li id="ref3">Ghiasi, G., Cui, Y., Srinivas, A., Qian, R., Lin, T.-Y., Cubuk, E. D., Le, Q. V., & Zoph, B. (2020). Simple Copy-Paste is a Strong Data Augmentation Method for Instance Segmentation (Version 2). arXiv. <a href="https://doi.org/10.48550/ARXIV.2012.07177">https://doi.org/10.48550/ARXIV.2012.07177</a></li>
    
</ol>


