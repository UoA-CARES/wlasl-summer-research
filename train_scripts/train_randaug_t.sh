cd ..

python mmaction2/tools/train.py experiments/augmentations/configs/i3d/randaug_t/i3d_r50_32x2x1_200e_kinetics400_randaugt_wlasl100_rgb_0.py --validate --deterministic --gpus 1 --seed 0

python mmaction2/tools/train.py experiments/augmentations/configs/i3d/randaug_t/i3d_r50_32x2x1_200e_kinetics400_randaugt_wlasl100_rgb_1.py --validate --deterministic --gpus 1 --seed 1

python mmaction2/tools/train.py experiments/augmentations/configs/i3d/randaug_t/i3d_r50_32x2x1_200e_kinetics400_randaugt_wlasl100_rgb_2.py --validate --deterministic --gpus 1 --seed 2
