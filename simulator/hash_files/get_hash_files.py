import glob
import ssl
import tarfile

import certifi
import htmllistparse
import os
import urllib.request as urlrq
from tqdm import tqdm


def download_files(web_dir: str, limit: int):
    cwd, listing = htmllistparse.fetch_listing(web_dir, timeout=30)
    names = [f.name.split('.tar.bz2')[0] for f in listing if f.name.endswith('.tar.bz2')]

    # For every line in the file
    for name in tqdm(names[:limit]):
        # Split on the rightmost / and take everything on the right side of that
        url = web_dir + name + '.tar.bz2'

        # Combine the name and the downloads directory to get the local filename
        filename = os.path.join(web_dir, name)

        # Download the file if it does not yet exist
        if not glob.glob(name + '*.hash.anon'):
            file = urlrq.urlopen(url, context=ssl.create_default_context(cafile=certifi.where()))
            with open(name + '.tar.bz2', 'wb') as output:
                output.write(file.read())

            # extract hash file from archive
            tar = tarfile.open(name + '.tar.bz2', "r:bz2")
            hash_files = [m for m in tar.getmembers() if m.name.endswith('.hash.anon')]
            for file in hash_files:
                # get just the file without directory structure
                file.name = os.path.basename(file.name)
            tar.extractall(members=hash_files)
            tar.close()
            os.remove(name + '.tar.bz2')


def main():
    web_dir = "https://tracer.filesystems.org/traces/fslhomes/2011-8kb-only/"
    download_files(web_dir, limit=15)


if __name__ == "__main__":
    main()
