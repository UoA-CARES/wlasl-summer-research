# wlasl-summer-research

This is a repo that contains the setup for the [WLASL dataset](https://github.com/dxli94/WLASL) to be used with tools available with [MMAction2](https://github.com/open-mmlab/mmaction2). Clone recursively for mmaction2:
```
git clone --recurse https://github.com/UoA-CARES/wlasl-summer-research.git
```

<div align="center">
  <div style="float:left;margin-right:10px;">
  <img src="https://user-images.githubusercontent.com/67076071/206937055-632e2362-140b-440e-b66f-385407550a55.png"
  width=700
  height=auto
  ><br>
    <p style="font-size:1.5vw;">WLASL-2000</p>
  </div>
</div>

## Directory
**After** downloading and extracting the dataset, the directory should look like below:
```
wlasl-summer-research
├── auto_setup.sh
├── data
│   └── wlasl
│       ├── rawframes
│       │   ├── test
│       │   │   └── 00623
│       │   │       ├── img_00001.jpg
│       │   │       └── ...
│       │   ├── train
│       │   │   └── 00623
│       │   │       ├── img_00001.jpg
│       │   │       └── ...
│       │   └── val
│       │       └── 00626
│       │           ├── img_00001.jpg
│       │           └── ...
│       ├── test_annotations.txt
│       ├── train_annotations.txt
│       ├── val_annotations.txt
│       ├── wlasl-processed.zip
│       └── wlasl-uncompressed
│           └── ...
├── LICENSE
├── mmaction2
│   └── ...
├── models
│   ├── c3d
│   │   └── c3d_16x16x1_sports1m_wlasl100_rgb.py
│   └── ...
├── README.md
├── symbolic.sh
├── tools
│   └── wlasl
│       ├── build_labels.py
│       ├── create_annotations.ipynb
│       ├── fix_missing.py
│       ├── json_fixer.ipynb
│       ├── split_videos.ipynb
│       └── split_videos.py
└── work_dirs
    └── ...
```
```data/wlasl/wlasl-processed.zip``` is the dataset downloaded from kaggle. It is unzipped and stored in ```data/wlasl/wlasl-uncompressed```. The dataset is prepared using the scripts under ```tools``` and ```mmaction2```. These are automatically run by ```auto_setup.sh```.

## Requirements
### Setting up a conda environment

#### Install MiniConda
The following instructions are for Linux. For other operating systems, download and install from [here](https://docs.conda.io/en/latest/miniconda.html).
```
curl -sL \
  "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh" > \
 "Miniconda3.sh"
```
Install the .sh file.
```
bash Miniconda3.sh
```
Remove the installer:
```
rm Miniconda3.sh
```
#### Creating a virtual environment
Run the following commands to create a virtual environment and to activate it:
```
conda create -n wlasl python=3.8
conda activate wlasl
```
Make sure to run ```conda activate wlasl``` before running any of the scripts in this repo.

### Installing Dependencies
Install PyTorch by running the following:
```
pip install torch==1.11.0+cu113 torchvision==0.12.0+cu113 torchaudio==0.11.0 --extra-index-url https://download.pytorch.org/whl/cu113
```
**Note:** To fully utilise cuda, make sure to have nvidia graphics drivers installed and running. To check, run ```nvidia-smi```.


Clone the repo if not done already and go inside the repo:
```
git clone --recurse https://github.com/UoA-CARES/wlasl-summer-research.git
cd wlasl-summer-research
````
To install all the other modules, navigate to the root directory of this repo after cloning and run the following:
```
pip install -r requirements.txt
```
Sometimes, kaggle doesn't get installed through requirements.txt, so run the following:
```
pip install kaggle
```
Install mmcv:
```
pip install -U openmim
mim install mmcv-full
```
Assuming mmcv is already installed, install mmaction2:
```
pip install git+https://github.com/open-mmlab/mim.git
mim install mmaction2 -f https://github.com/open-mmlab/mmaction2.git
```
## Setup
### Setting up a symbolic link
This step is optional. If you want to set up an external disk to store the dataset, open ```symbolic.sh``` and change the ```EXTERNALDRIVE``` variable from ```Sadat``` to your drive name. Then, run the script:
```
bash symbolic.sh
```
This will create set up a symbolic link called data in the current to point to the ```EXTERNALDRIVE/wlasl/data```.

### Downloading and extracting the dataset
In order to download the dataset, an existing [kaggle token](https://www.kaggle.com/docs/api#:~:text=From%20the%20site%20header%2C%20click,Create%20New%20API%20Token%E2%80%9D%20button.) needs to be set up.
All the data-acquisition and extraction is handled by ```auto_setup.sh```. From the root of the repo, run:
```
bash auto_setup.sh
```
**Note:** If on other operating system, open the bash file and run each command one by one. The current ```auto_setup.sh``` is set up to create the WLASL-100 dataset for MMAction2. Change the instances to other numbers for other subsets of the WLASL-2000 dataset. Check the different json files under ```data/wlasl/wlasl-uncompressed``` for available options.

This bash script will download the dataset from kaggle (Kaggle token needs to be set up for this), extract and store the dataset under the ```data``` directory.

## Setting up WandB
Log in to WandB account by running the following on terminal:
```
wandb login
```

To link the model training with WandB, copy the following code snippet and paste at the end of the config file.

```python
# Setup WandB
log_config = dict(interval=10, hooks=[
    dict(type='TextLoggerHook'),
    dict(type='WandbLoggerHook',
         init_kwargs={
             'entity': "cares",
             'project': "wlasl-100"
         },
         log_artifact=True)
]
)
```

## Training
Start training by running the following template:
```
python tools/train.py ${CONFIG_FILE} [optional arguments]
```
Example: Train a pretrained 3CD model on wlasl with periodic validation.
```
python mmaction2/tools/train.py models/c3d/c3d_16x16x1_sports1m_wlasl100_rgb.py --validate --seed 0 --deterministic --gpus 1
```

## Testing
Use the following template to test a model:
```
python tools/test.py ${CONFIG_FILE} ${CHECKPOINT_FILE} [optional arguments]
```
Examples and more information can be found [here](https://github.com/open-mmlab/mmaction2/blob/master/docs/en/getting_started.md#test-a-dataset).


## Citations
```
@misc{2020mmaction2,
    title={OpenMMLab's Next Generation Video Understanding Toolbox and Benchmark},
    author={MMAction2 Contributors},
    howpublished = {\url{https://github.com/open-mmlab/mmaction2}},
    year={2020}
}
```
```
@inproceedings{li2020transferring,
 title={Transferring cross-domain knowledge for video sign language recognition},
 author={Li, Dongxu and Yu, Xin and Xu, Chenchen and Petersson, Lars and Li, Hongdong},
 booktitle={Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition},
 pages={6205--6214},
 year={2020}
}
```
