import os

def establish_operating_dirs(config):
    assert isinstance(config, dict), 'establish_operating_dirs: configuration data is not a dictionary.'

    fkeys = [ 'download_dir', 'link_files_dir', 'log_dir' ]

    # TODO check for key existence higher up the chain
    assert set(fkeys).issubset(config.keys()), 'establish_operating_dirs: configuration data missing expected values.'

    for d in [config[k] for k in fkeys]:
        if not os.path.exists(d):
            os.makedirs(d)