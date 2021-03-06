#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
Module is used for visualization of segmentation stored in pkl file.
"""

import logging
import os.path
import sys

logger = logging.getLogger(__name__)
import argparse

if sys.version_info < (3, 0):
    import urllib as urllibr
else:
    import urllib.request as urllibr
import numpy as np
import zipfile
import glob
import os.path as op
import io3d


# you can get hash from command line with:
#  python imtools/sample_data.py -v sliver_training_001
local_dir="~/data/medical/orig/"
# vessels.pkl nejprve vytvoří prázný adresář s názvem vessels.pkl, pak jej při rozbalování zase smaže
__url_home = "http://home.zcu.cz/~mjirik/lisa/testdata/sample-extra-data/"
data_urls= {
    "head": ["http://147.228.240.61/queetech/sample-data/head.zip", "89e9b60fd23257f01c4a1632ff7bb800", "matlab"] ,
    "jatra_06mm_jenjatra": ["http://147.228.240.61/queetech/sample-data/jatra_06mm_jenjatra.zip", "jatra_06mm_jenjatra/*.dcm"],
    "jatra_5mm": ["http://147.228.240.61/queetech/sample-data/jatra_5mm.zip", '1b9039ffe1ff9af9caa344341c8cec03', "jatra_06mm/*.dcm"],
    "exp": ["http://147.228.240.61/queetech/sample-data/exp.zip", '74f2c10b17b6bd31bd03662df6cf884d'],
    "sliver_training_001": ["http://147.228.240.61/queetech/sample-data/sliver_training_001.zip","d64235727c0adafe13d24bfb311d1ed0","liver*001.*"],
    "volumetrie": ["http://147.228.240.61/queetech/sample-data/volumetrie.zip","6b2a2da67874ba526e2fe00a78dd19c9"],
    "vessels.pkl": ["http://147.228.240.61/queetech/sample-data/vessels.pkl.zip","698ef2bc345bb616f8d4195048538ded"],
    "biodur_sample": ["http://147.228.240.61/queetech/sample-data/biodur_sample.zip","d459dd5b308ca07d10414b3a3a9000ea"],
    "gensei_slices": ["http://147.228.240.61/queetech/sample-data/gensei_slices.zip", "ef93b121add8e4a133bb086e9e6491c9"],
    "exp_small": ["http://147.228.240.61/queetech/sample-data/exp_small.zip", "0526ba8ea363fe8b5227f5807b7aaca7"],
    "vincentka": ["http://147.228.240.61/queetech/vincentka.zip", "a30fdabaa39c5ce032a3223ed30b88e3"],
    "vincentka_sample": ["http://147.228.240.61/queetech/sample-data/vincentka_sample.zip"],
    "donut": "http://147.228.240.61/queetech/sample-data/donut.zip",
    "3Dircadb1": ["http://ircad.fr/softwares/3Dircadb/3Dircadb1/3Dircadb1.zip", None, None, "ircad/*[!p]/*[!pfg]"],
    "3Dircadb1.1": "http://ircad.fr/softwares/3Dircadb/3Dircadb1/3Dircadb1.1.zip",
    "3Dircadb1.2": "http://ircad.fr/softwares/3Dircadb/3Dircadb1/3Dircadb1.2.zip",
    "3Dircadb1.3": "http://ircad.fr/softwares/3Dircadb/3Dircadb1/3Dircadb1.3.zip",
    "3Dircadb1.4": "http://ircad.fr/softwares/3Dircadb/3Dircadb1/3Dircadb1.4.zip",
    "3Dircadb1.5": "http://ircad.fr/softwares/3Dircadb/3Dircadb1/3Dircadb1.5.zip",
    "3Dircadb1.6": "http://ircad.fr/softwares/3Dircadb/3Dircadb1/3Dircadb1.6.zip",
    "3Dircadb1.7": "http://ircad.fr/softwares/3Dircadb/3Dircadb1/3Dircadb1.7.zip",
    "3Dircadb1.8": "http://ircad.fr/softwares/3Dircadb/3Dircadb1/3Dircadb1.8.zip",
    "3Dircadb1.9": "http://ircad.fr/softwares/3Dircadb/3Dircadb1/3Dircadb1.9.zip",
    "3Dircadb1.10": "http://ircad.fr/softwares/3Dircadb/3Dircadb1/3Dircadb1.10.zip",
    "3Dircadb1.11": "http://ircad.fr/softwares/3Dircadb/3Dircadb1/3Dircadb1.11.zip",
    "3Dircadb1.12": "http://ircad.fr/softwares/3Dircadb/3Dircadb1/3Dircadb1.12.zip",
    "3Dircadb1.13": "http://ircad.fr/softwares/3Dircadb/3Dircadb1/3Dircadb1.13.zip",
    "3Dircadb1.14": "http://ircad.fr/softwares/3Dircadb/3Dircadb1/3Dircadb1.14.zip",
    "3Dircadb1.15": "http://ircad.fr/softwares/3Dircadb/3Dircadb1/3Dircadb1.15.zip",
    "3Dircadb1.16": "http://ircad.fr/softwares/3Dircadb/3Dircadb1/3Dircadb1.16.zip",
    "3Dircadb1.17": "http://ircad.fr/softwares/3Dircadb/3Dircadb1/3Dircadb1.17.zip",
    "3Dircadb1.18": "http://ircad.fr/softwares/3Dircadb/3Dircadb1/3Dircadb1.18.zip",
    "3Dircadb1.19": "http://ircad.fr/softwares/3Dircadb/3Dircadb1/3Dircadb1.19.zip",
    "3Dircadb1.20": "http://ircad.fr/softwares/3Dircadb/3Dircadb1/3Dircadb1.20.zip",
    
    # není nutné pole, stačí jen string
    # "exp_small": "http://147.228.240.61/queetech/sample-data/exp_small.zip",
}

def get_dataset_meta(label):
    data_url = data_urls[label]
    if type(data_url) == str:
        # back compatibility
        data_url = [data_url]
    if type(data_url) == list:
        data_url.extend([None, None, None])
        data_url = data_url[:4]
        url, expected_hash, hash_path, fnpattern = data_url

        if hash_path is None:
            hash_path = label

        if fnpattern is None and hash_path is not None:
            fnpattern = hash_path


    # elif type(data_url) == dict:



    return data_url, url, expected_hash, hash_path, fnpattern

def download(dataset_label=None, destination_dir=None):
    """
    Download sample data by data label. Labels can be listed by sample_data.data_urls.keys()
    :param dataset_label: label of data. If it is set to None, all data are downloaded
    :param destination_dir: output dir for data
    :return:
    """
    if destination_dir is None:
        destination_dir = local_dir

    destination_dir = op.expanduser(destination_dir)

    if not op.exists(destination_dir):
        os.makedirs(destination_dir)

    if dataset_label is None:
        dataset_label=data_urls.keys()

    if type(dataset_label) == str:
        dataset_label = [dataset_label]

    for label in dataset_label:
        # make all data:url have length 3
        data_url, url, expected_hash, hash_path, fnpattern = get_dataset_meta(label)

        if hash_path is None:
            hash_path = label

        try:
            computed_hash = checksum(os.path.join(destination_dir, hash_path))
        except:
            # there is probably no checksumdir module
            logger.warning("problem with sample_data.checksum()")
            computed_hash = None

        logger.info("dataset '" + label + "'")
        logger.info("expected hash: '" + str(expected_hash) + "'")
        logger.info("computed hash: '" + str(computed_hash) + "'")
        if (computed_hash is not None) and (expected_hash == computed_hash):
            logger.info("match ok - no download needed")
        else:
            logger.info("downloading")
            downzip(url, destination=destination_dir)
            logger.info("finished")
            downloaded_hash = checksum(os.path.join(destination_dir, hash_path))
            logger.info("downloaded hash: '" + str(downloaded_hash) + "'")
            if downloaded_hash != expected_hash:
                logger.warning("downloaded hash is different from expected hash\n" + \
                               "expected hash: '" + str(expected_hash) + "'\n" + \
                               "downloaded hash: '" + str(downloaded_hash) + "'\n")

def get(dataset_label, id, destination_dir=None):
    """
    Get the 3D data from specified dataset with specified id.

    Download data if necessary.

    :param dataset_label:
    :param id: integer or wildcards file pattern
    :param destination_dir:
    :return:
    """
    # @TODO implement
    if destination_dir is None:
        destination_dir = local_dir

    destination_dir = op.expanduser(destination_dir)
    data_url, url, expected_hash, hash_path, fnpattern = get_dataset_meta(dataset_label)
    paths = glob.glob(os.path.join(destination_dir, fnpattern))
    paths.sort()
    import fnmatch
    print(paths)
    print(id)
    pathsf = fnmatch.filter(paths, id)
    print(pathsf
          )
    datap = io3d.read(pathsf[0], dataplus_format=True)
    return datap


def checksum(path, hashfunc='md5'):
    """
    Return checksum given by path. Wildcards can be used in check sum. Function is strongly
    dependent on checksumdir package by 'cakepietoast'.

    :param path:
    :param hashfunc:
    :return:
    """
    import checksumdir
    hash_func = checksumdir.HASH_FUNCS.get(hashfunc)
    if not hash_func:
        raise NotImplementedError('{} not implemented.'.format(hashfunc))

    if os.path.isdir(path):
        return checksumdir.dirhash(path, hashfunc=hashfunc)

    hashvalues = []
    path_list = glob.glob(path)
    logger.debug("path_list " + str(path_list))
    for path in path_list:
        if os.path.isfile(path):
            hashvalues.append(checksumdir._filehash(path, hashfunc=hash_func))
    logger.debug(str(hashvalues))
    hash = checksumdir._reduce_hash(hashvalues, hashfunc=hash_func)
    return hash

def generate_donut():
    """
    Generate donut like shape with stick inside

    :return: datap with keys data3d, segmentation and voxelsize_mm
    """
    import numpy as np
    segmentation = np.zeros([20, 30, 40])
    # generate test data
    segmentation[6:10, 7:24, 10:37] = 1
    segmentation[6:10, 7, 10] = 0
    segmentation[6:10, 23, 10] = 0
    segmentation[6:10, 7, 36] = 0
    segmentation[6:10, 23, 36] = 0
    segmentation[2:18, 12:19, 18:28] = 2

    data3d = segmentation * 100 + np.random.random(segmentation.shape) * 30
    voxelsize_mm=[3,2,1]

    datap = {
        'data3d': data3d,
        'segmentation': segmentation,
        'voxelsize_mm': voxelsize_mm
    }
    # io3d.write(datap, "donut.pklz")
    return datap


def generate_abdominal(size = 100, liver_intensity=100, noise_intensity=20, portal_vein_intensity=130, spleen_intensity=90):
    boundary = int(size/4)
    voxelsize_mm = [1.0, 1.5, 1.5]
    slab = {
        'liver': 1,
        'porta': 2,
        'spleen': 17
    }

    segmentation = np.zeros([size, size, size], dtype=np.uint8)
    segmentation[boundary:-boundary, boundary:-2*boundary, 2*boundary:-boundary] = 1
    segmentation[:, boundary*2:boundary*2+5, boundary*2:boundary*2+5] = 2
    segmentation[:, boundary*2:boundary*2+5, boundary*2:boundary*2+5] = 2
    segmentation[:, -5:, -boundary:] = 17


    seeds = np.zeros([size, size, size], dtype=np.uint8)
    seeds[
    boundary + 1 : boundary + 4,
    boundary + 1 : boundary + 4,
    2 * boundary + 1 : 2 * boundary + 4
    ] = 1

    noise = (np.random.random(segmentation.shape) * noise_intensity).astype(np.int)
    data3d = np.zeros(segmentation.shape, dtype=np.int)
    data3d [segmentation == 1] = liver_intensity
    data3d [segmentation == 2] = portal_vein_intensity
    data3d [segmentation == 17] = spleen_intensity
    data3d += noise


    datap = {
        'data3d': data3d,
        'segmentation': segmentation,
        'voxelsize_mm': voxelsize_mm,
        'seeds': seeds,
        'slab': slab
    }
    return datap


def sliver_reader(filename_end_mask="*[0-9].mhd", sliver_reference_dir="~/data/medical/orig/sliver07/training/", read_orig=True, read_seg=False):
    """
    Generator for reading sliver data from directory structure.

    :param filename_end_mask: file selection can be controlled with this parameter
    :param sliver_reference_dir: directory with sliver .mhd and .raw files
    :param read_orig: read image data if is set True
    :param read_seg: read segmentation data if is set True
    :return: numeric_label, vs_mm, oname, orig_data, rname, ref_data
    """
    sliver_reference_dir = op.expanduser(sliver_reference_dir)
    orig_fnames = glob.glob(sliver_reference_dir + "*orig" +  filename_end_mask)
    ref_fnames = glob.glob(sliver_reference_dir + "*seg"+ filename_end_mask)

    orig_fnames.sort()
    ref_fnames.sort()
    output = []
    for i in range(0, len(orig_fnames)):
        oname = orig_fnames[i]
        rname = ref_fnames[i]
        vs_mm = None
        ref_data= None
        orig_data = None
        if read_orig:
            orig_data, metadata = io3d.datareader.read(oname)
            vs_mm = metadata['voxelsize_mm']
        if read_seg:
            ref_data, metadata = io3d.datareader.read(rname)
            vs_mm = metadata['voxelsize_mm']

        import re
        numeric_label = re.search(".*g(\d+)", oname).group(1)
        out = (numeric_label, vs_mm, oname, orig_data, rname, ref_data)
        yield out


def main():
    logger = logging.getLogger()

    logger.setLevel(logging.WARNING)
    ch = logging.StreamHandler()
    logger.addHandler(ch)

    #logger.debug('input params')

    # input parser
    parser = argparse.ArgumentParser(
        description=
        "Work on dataset")
    parser.add_argument(
        "-l", "--labels", metavar="N", nargs="+",
        default=None,
        help='Get sample data')
    parser.add_argument(
        '-L', '--print_labels', action="store_true",
        default=False,
        help='print all available labels')
    parser.add_argument(
        '-c', '--checksum', # action="store_true",
        default=None,
        help='Get hash for requested path')
    parser.add_argument(
        '-v', '--verbatim', action="store_true",
        default=False,
        help='more messages')
    parser.add_argument(
        '-d', '--debug', # action="store_true",
        default=None,
        help='set debug level')
    parser.add_argument(
        '-o', '--destination_dir',
        default=".",
        help='set output directory')

    args = parser.parse_args()


    #    if args.get_sample_data == False and args.install == False and args.build_gco == False:
    ## default setup is install and get sample data
    #        args.get_sample_data = True
    #        args.install = True
    #        args.build_gco = False
    if args.verbatim:
        # logger.setLevel(logging.DEBUG)
        logger.setLevel(logging.INFO)
    if args.debug is not None:
        logger.setLevel(int(args.debug))

    if args.checksum is not None:
        print(checksum(args.checksum))
        if args.labels is None:
            return

    download(args.labels, destination_dir=args.destination_dir)

    #submodule_update()

def remove(local_file_name):
    try:
        os.remove(local_file_name)
    except Exception as e:
        print ("Cannot remove file '" + local_file_name + "'. Please remove\
        it manually.")
        print (e)


def downzip(url, destination='./sample_data/'):
    """
    Download, unzip and delete.
    """

    # url = "http://147.228.240.61/queetech/sample-data/jatra_06mm_jenjatra.zip"
    logmsg = "downloading from '" + url + "'"
    print(logmsg)
    logger.debug(logmsg)
    local_file_name = os.path.join(destination, 'tmp.zip')
    urllibr.urlretrieve(url, local_file_name)
    datafile = zipfile.ZipFile(local_file_name)
    datafile.extractall(destination)
    remove(local_file_name)


if __name__ == "__main__":
    main()
