import os
import zipfile
import time
import stat

def zipdir(path, ziph, relpath=None):
    """
    Add files to ZIP handler at path, using relpath as relative path
    Adding readable permissions flag to preserve permissions
    :param path:
    :param ziph:
    :param relpath:
    :return:
    """

    if not relpath:
        relpath = path

    for root, dirs, files in os.walk(path):
        for file in files:
            info = zipfile.ZipInfo(os.path.join(os.path.relpath(root, relpath), file))
            info.date_time = time.localtime()

            st = os.stat(os.path.join(root, file))
            info.external_attr = (st[0] | stat.S_IROTH) << 16
            with open(os.path.join(root, file), 'rb') as f:
                data = f.read()
                ziph.writestr(info, data, zipfile.ZIP_DEFLATED)

                #ziph.write(os.path.join(root, file), arcname=os.path.join(os.path.relpath(root, relpath), file))


def marketplace(extension, output, relpath=None):
    """
    Pack extension to marketplace-compatible zip
    if specified output is dir, gets name from composer.json
    No checks are applied
    :param extension:
    :param output:
    :return:
    """
    if os.path.isdir(output):
        output = os.path.join(output, extension.meta.name.split('/')[1]) + '.zip'

    with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipdir(extension.path, zipf, relpath)
        return zipf
