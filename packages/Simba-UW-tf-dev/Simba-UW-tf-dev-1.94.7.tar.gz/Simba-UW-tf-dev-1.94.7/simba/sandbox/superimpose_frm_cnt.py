import functools
import glob
import multiprocessing
import os
import platform
import shutil
import subprocess
import time
from copy import deepcopy
from datetime import datetime
from tkinter import *
from typing import Any, Dict, List, Optional, Tuple, Union

import cv2
import numpy as np
from PIL import Image, ImageTk
from shapely.geometry import Polygon

try:
    from typing import Literal
except:
    from typing_extensions import Literal

import simba
from simba.mixins.config_reader import ConfigReader
from simba.mixins.image_mixin import ImageMixin
from simba.utils.checks import (check_ffmpeg_available,
                                check_file_exist_and_readable, check_float,
                                check_if_dir_exists,
                                check_if_filepath_list_is_empty,
                                check_if_string_value_is_valid_video_timestamp,
                                check_instance, check_int,
                                check_nvidea_gpu_available, check_str,
                                check_that_hhmmss_start_is_before_end,
                                check_valid_lst, check_valid_tuple)
from simba.utils.data import find_frame_numbers_from_time_stamp
from simba.utils.enums import OS, ConfigKey, Formats, Options, Paths
from simba.utils.errors import (CountError, DirectoryExistError,
                                FFMPEGCodecGPUError, FFMPEGNotFoundError,
                                FileExistError, FrameRangeError,
                                InvalidFileTypeError, InvalidInputError,
                                InvalidVideoFileError, NoDataError,
                                NoFilesFoundError, NotDirectoryError)
from simba.utils.lookups import (get_ffmpeg_crossfade_methods, get_fonts,
                                 percent_to_crf_lookup, percent_to_qv_lk)
from simba.utils.printing import SimbaTimer, stdout_success
from simba.utils.read_write import (
    check_if_hhmmss_timestamp_is_valid_part_of_video,
    concatenate_videos_in_folder, find_all_videos_in_directory, find_core_cnt,
    find_files_of_filetypes_in_directory, get_fn_ext, get_video_meta_data,
    read_config_entry, read_config_file, read_frm_of_video)
from simba.utils.warnings import (FileExistWarning, InValidUserInputWarning,
                                  SameInputAndOutputWarning)
from simba.video_processors.extract_frames import video_to_frames
from simba.video_processors.roi_selector import ROISelector
from simba.video_processors.roi_selector_circle import ROISelectorCircle
from simba.video_processors.roi_selector_polygon import ROISelectorPolygon



def superimpose_frame_count(file_path: Union[str, os.PathLike],
                            gpu: Optional[bool] = False,
                            font: Optional[str] = 'Arial',
                            font_color: Optional[str] = 'black',
                            bg_color: Optional[str] = 'white',
                            fontsize: Optional[int] = 20) -> None:
    """
    Superimpose frame count on a video file. The result is stored in the same directory as the
    input file with the ``_frame_no.mp4`` suffix.

    .. image:: _static/img/superimpose_frame_count.png
       :width: 700
       :align: center

    .. image:: _static/img/superimpose_frame_count.gif
       :width: 500
       :align: center

    :parameter Union[str, os.PathLike] file_path: Path to video file.
    :parameter Optional[bool] gpu: If True, use NVIDEA GPU codecs. Default False.
    :parameter Optional[int] fontsize: The size of the font represetnting the current frame. Default: 20.

    :example:
    >>> _ = superimpose_frame_count(file_path='project_folder/videos/Video_1.avi')
    """

    timer = SimbaTimer(start=True)
    check_ffmpeg_available(raise_error=True)
    check_int(name=f'{superimpose_frame_count.__name__} fontsize', value=fontsize, min_value=1)
    font_color = ''.join(filter(str.isalnum, font_color)).lower()
    bg_color = ''.join(filter(str.isalnum, bg_color)).lower()
    font_dict = get_fonts()
    check_str(name='font', value=font, options=tuple(font_dict.keys()))
    font_path = font_dict[font]
    check_file_exist_and_readable(file_path=file_path)
    dir, file_name, ext = get_fn_ext(filepath=file_path)
    save_name = os.path.join(dir, f"{file_name}_frame_no.mp4")
    if gpu:
        cmd = f'''ffmpeg -hwaccel auto -c:v h264_cuvid -i "{file_path}" -vf "drawtext=fontfile='{font_path}':text=%{{n}}:x=(w-tw)/2:y=h-th-10:fontcolor={font_color}:fontsize={fontsize}:box=1:boxcolor={bg_color}@0.5" -c:v h264_nvenc -c:a copy -loglevel error -stats "{save_name}" -y'''
    else:
        cmd = f'''ffmpeg -y -i "{file_path}" -vf "drawtext=fontfile='{font_path}': text='%{{frame_num}}': start_number=0: x=(w-tw)/2: y=h-(2*lh): fontcolor={font_color}: fontsize={fontsize}: box=1: boxcolor={bg_color}: boxborderw=5" -c:a copy -loglevel error -stats "{save_name}" -y'''
    subprocess.call(cmd, shell=True, stdout=subprocess.PIPE)
    timer.stop_timer()
    stdout_success(msg=f"Superimposed video converted! {save_name} generated!", elapsed_time=timer.elapsed_time_str)

superimpose_frame_count(file_path='/Users/simon/Downloads/1_LH_0_3.mp4', font_color='red', bg_color='blue')