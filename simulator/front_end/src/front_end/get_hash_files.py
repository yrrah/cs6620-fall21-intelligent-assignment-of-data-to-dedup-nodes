import os
import ssl
import urllib.request as urlrq

import certifi


def download_file(working_dir: str, web_dir: str, name: str) -> None:
    """
    Download a single trace file [name] to [working_dir] from [web_dir]
    @param working_dir:
    @param web_dir:
    @param name:
    """
    # strip file type
    name, _, suffix = name.partition('.')
    suffix = '.' + suffix

    # download the tar archive
    file = urlrq.urlopen(web_dir + name + '.tar.bz2', context=ssl.create_default_context(cafile=certifi.where()))
    tar_name = os.path.join(working_dir, name + '.tar.bz2')
    with open(tar_name, 'wb') as output:
        output.write(file.read())


def download_files(working_dir: str, web_dir: str, names: [str]):
    print(f'downloading from {web_dir} to {working_dir}')
    print('.' * len(names))
    for name in names:
        download_file(working_dir, web_dir, name)
        print('.', end='', flush=True)
    print()
