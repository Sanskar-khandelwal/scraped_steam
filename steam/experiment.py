classes = [
    'platform_img win',
    'platform_img mac',
    'platform_img linux',
    'vr_supported',
]


def get_platforms(classes):
    platforms = []
    for item in classes:
        platform = item.split(' ')[-1]
        if platform == 'win':
            platforms.append('Windows')
        if platform == 'mac':
            platforms.append('Mac Os')
        if platform == 'linux':
            platforms.append('Linux')
        if platform == 'vr_supported':
            platforms.append('VR Supported')

    return platform


get_platforms(classes)
