"""This module contains functions which extract the required information for
populating the raga lakshana section in a wiki article. This module defines
those functions which generate information about a raga from its moorchana
alone.

@author: Nikhil Pattisapu, iREL, IIIT-H"""


import re
import json
import argparse
import numpy as np
import tomita.legacy.pysynth_b as psb
from PIL import Image, ImageFont, ImageDraw


# pylint: disable=invalid-name
parser = argparse.ArgumentParser()
parser.add_argument('--ragakb', type=str, default="ragakb.json")
parser.add_argument('--config', type=str, default="resources/config.json")
parser.add_argument('--img_path', type=str, default="raga_images")
# parser.add_argument('--audio_path', type=str)
args = parser.parse_args()

CONF = json.load(open(args.config, 'r'))
FONT = ImageFont.truetype(CONF['font_path'], CONF['font_size'])


def get_img_from_seq(seq, file_name):
    """Saves the keyboard image of the given input swara sequence"""
    keyboard = Image.open(CONF['keyboard_path'])
    drawing = ImageDraw.Draw(keyboard)
    for swm in seq:
        _, _, pos, symbol, color = CONF['map'][swm]
        drawing.text(tuple(pos), symbol, tuple(color), font=FONT)
    keyboard.save(args.img_path + "/" + file_name)


def get_moorchana_audio(aro, ava, file_name):
    """Saves the moorchana audio of the given input arohanam and avarohanam"""
    ar_notes = [CONF['map'][swm][1] for swm in aro]
    av_notes = [CONF['map'][swm][1] for swm in ava]
    ar_dur = [4] * len(ar_notes) # All notes are of fixed duration
    av_dur = [4] * len(av_notes) # All notes are of fixed duration
    ar_dur[-1], av_dur[-1] = 2, 2
    notes, dur = ar_notes + av_notes, ar_dur + av_dur
    moorchana = list(zip(notes, dur))
    # Save file to disk
    psb.make_wav(moorchana, fn=file_name, leg_stac=.7, bpm=90)


def get_raga_image(raga_moorchana):
    """Returns the keyboard image of ragam and its swarasthanams. For image
    generation we have used `pillow library
    <https://code-maven.com/python-write-text-on-images-pil-pillow>`__
    :param raga_name: Name of input ragam
    :param aro: The arohanam of the input ragam
    :param ava: The avarohanam of the input ragam
    :param img_dir: The path of directory where the generated image(s) are
    stored.
    :return: A list of path(s) specifying the locations of generated images.
    """
    raga_name, aro, ava = raga_moorchana
    # aro, ava = aro.split(','), ava.split(',')
    if any([swm not in CONF['map'] for swm in aro + ava]):
        return np.nan
    aro, ava = set(aro), set(ava)
    res_paths = []
    if aro == ava:
        file_path = raga_name + '_kb2wiki.png'
        get_img_from_seq(aro, file_path)
        res_paths.append(file_path)
    else:
        ar_file_path = raga_name + '_ar_kb2wiki.png'
        get_img_from_seq(aro, ar_file_path)
        av_file_path = raga_name + '_av_kb2wiki.png'
        get_img_from_seq(ava, av_file_path)
        res_paths.append(ar_file_path)
        res_paths.append(av_file_path)
    return res_paths


def get_raga_moorchana_audio(raga_moorchana):
    """Produces wav file which plays the moorchana. For moorchana sound
    generataion we have used
    `Pysynth library <https://github.com/mdoege/PySynth>`__
    :param raga_name: Name of input ragam
    :param aro: The arohanam of the input ragam
    :param ava: The avarohanam of the input ragam
    :param sound_dir: The path of directory where the moorchana is stored.
    :return: Path specifying the locations of generated moorchana.
    """
    raga_name, aro, ava = raga_moorchana
    res = args.audio_path + "/" + raga_name + "_kb2wiki.wav"
    if any([swm not in CONF['map'] for swm in aro + ava]):
        return np.nan
    get_moorchana_audio(aro, ava, res)
    return res


ragakb = json.load(open(args.ragakb, 'r'))
for raga in ragakb:
    raga_moorchana = [raga['name'], raga['aro'], raga['ava']]
    get_raga_image(raga_moorchana)
    # get_raga_moorchana_audio(raga_moorchana)
