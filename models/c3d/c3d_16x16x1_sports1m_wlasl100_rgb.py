_base_ = '../../mmaction2/configs/_base_/models/c3d_sports1m_pretrained.py'

# dataset settings
dataset_type = 'RawframeDataset'
data_root = 'data/wlasl/rawframes'
data_root_val = 'data/wlasl/rawframes'
split = 1  # official train/test splits. valid numbers: 1, 2, 3
clip_length = 16
ann_file_train = 'data/wlasl/train_annotations.txt'
ann_file_val = 'data/wlasl/val_annotations.txt'
ann_file_test = 'data/wlasl/test_annotations.txt'
img_norm_cfg = dict(mean=[104, 117, 128], std=[1, 1, 1], to_bgr=False)
train_pipeline = [
    dict(type='SampleFrames', clip_len=16, frame_interval=1, num_clips=1),
    dict(type='RawFrameDecode'),
    dict(type='Resize', scale=(128, 171)),
    dict(type='RandomCrop', size=112),
    dict(type='Flip', flip_ratio=0.5),
    dict(type='Normalize', **img_norm_cfg),
    dict(type='FormatShape', input_format='NCTHW'),
    dict(type='Collect', keys=['imgs', 'label'], meta_keys=[]),
    dict(type='ToTensor', keys=['imgs', 'label'])
]
val_pipeline = [
    dict(
        type='SampleFrames',
        clip_len=16,
        frame_interval=1,
        num_clips=1,
        test_mode=True),
    dict(type='RawFrameDecode'),
    dict(type='Resize', scale=(128, 171)),
    dict(type='CenterCrop', crop_size=112),
    dict(type='Normalize', **img_norm_cfg),
    dict(type='FormatShape', input_format='NCTHW'),
    dict(type='Collect', keys=['imgs', 'label'], meta_keys=[]),
    dict(type='ToTensor', keys=['imgs', 'label'])
]
test_pipeline = [
    dict(
        type='SampleFrames',
        clip_len=16,
        frame_interval=1,
        num_clips=10,
        test_mode=True),
    dict(type='RawFrameDecode'),
    dict(type='Resize', scale=(128, 171)),
    dict(type='CenterCrop', crop_size=112),
    dict(type='Normalize', **img_norm_cfg),
    dict(type='FormatShape', input_format='NCTHW'),
    dict(type='Collect', keys=['imgs', 'label'], meta_keys=[]),
    dict(type='ToTensor', keys=['imgs', 'label'])
]
data = dict(
    videos_per_gpu=16,
    workers_per_gpu=2,
    test_dataloader=dict(videos_per_gpu=1),
    train=dict(
        type=dataset_type,
        ann_file=ann_file_train,
        data_prefix=data_root,
        pipeline=train_pipeline),
    val=dict(
        type=dataset_type,
        ann_file=ann_file_val,
        data_prefix=data_root_val,
        pipeline=val_pipeline),
    test=dict(
        type=dataset_type,
        ann_file=ann_file_test,
        data_prefix=data_root_val,
        pipeline=test_pipeline))
# optimizer
optimizer = dict(
    type='SGD', lr=0.001, momentum=0.9,
    weight_decay=0.0005)  # this lr is used for 8 gpus
optimizer_config = dict(grad_clip=dict(max_norm=40, norm_type=2))
# learning policy
lr_config = dict(policy='step', step=[20, 40])
total_epochs = 45
checkpoint_config = dict(interval=5)
evaluation = dict(
    interval=5, metrics=['top_k_accuracy', 'mean_class_accuracy'])

# # WandB setup
# log_config = dict(interval=10, hooks=[
#     dict(type='TextLoggerHook'),
#     dict(type='WandbLoggerHook',
#          init_kwargs={
#              'entity': "cares",
#              'project': "wlasl-100"
#          },
#          log_artifact=True)
# ]
# )

log_config = dict(
    interval=20,
    hooks=[
        dict(type='TextLoggerHook'),
        # dict(type='TensorboardLoggerHook'),
    ])

# runtime settings
dist_params = dict(backend='nccl')
log_level = 'INFO'
work_dir = f'./work_dirs/c3d_wlasl_{split}_rgb/'
load_from = None
resume_from = None
workflow = [('train', 1)]
