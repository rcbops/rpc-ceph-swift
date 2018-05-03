import hashlib
import os


def get_md5_hash(data, block_size_multiplier=1):
    """
    returns an md5 sum. data is a string or file pointer.
    block size is 512 (md5 msg length).
    """
    hash_ = None
    default_block_size = 2 ** 9
    block_size = block_size_multiplier * default_block_size
    md5 = hashlib.md5()

    if type(data) is file or os.path.isfile(data):
        fh = open(data, 'rb')
        while True:
            read_data = fh.read(block_size)
            if not read_data:
                break
            md5.update(read_data)
        fh.close()
    else:
        md5.update(str(data))

    hash_ = md5.hexdigest()

    return hash_