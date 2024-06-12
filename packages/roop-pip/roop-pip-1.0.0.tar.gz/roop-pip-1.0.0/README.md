# Roop-pip

[![Build](https://github.com/Konohamaru04/roop-pip/actions/workflows/main.yml/badge.svg)](https://github.com/Konohamaru04/roop-pip/actions/workflows/main.yml) [![Pip](https://github.com/Konohamaru04/roop-pip/actions/workflows/python-publish.yml/badge.svg)](https://github.com/Konohamaru04/roop-pip/actions/workflows/python-publish.yml)

> Take a video and replace the face in it with a face of your choice. You only need one image of the desired face. No dataset, no training.

<!-- [![Build Status](https://img.shields.io/github/actions/workflow/status/s0md3v/roop/ci.yml.svg?branch=main)](https://github.com/s0md3v/roop/actions?query=workflow:ci) -->

<img src="https://i.ibb.co/4RdPYwQ/Untitled.jpg"/>

## Installation

```
pip install roop-pip
```
Be aware, the installation needs technical skills and is not for beginners. Please do not open platform and installation related issues on GitHub.
[Acceleration](https://github.com/s0md3v/roop/wiki/2.-Acceleration) - Unleash the full potential of your CPU and GPU


## Usage

```python
from roop.core import roop_interface

roop_interface(
        source_img=SOURCE_PATH,
        target_path=TARGET_PATH,
        output_file=OUTPUT_PATH
    )

```
## Optional Params

| Parameter                 | Choices                                                                       | Default            |
|---------------------------|-------------------------------------------------------------------------------|--------------------|
| `frame_processor`         | `['face_swapper', 'face_enhancer']`                                           | `['face_swapper']` |
| `keep_fps`                | `True`, `False`                                                               | `True`             |
| `keep_frames`             | `True`, `False`                                                               | `False`            |
| `skip_audio`              | `True`, `False`                                                               | `False`            |
| `many_faces`              | `True`, `False`                                                               | `False`            |
| `reference_face_position` | Number                                                                        | `0`                |
| `reference_frame_number`  | Number                                                                        | `0`                |
| `similar_face_distance`   | Number                                                                        | `0.85`             |
| `temp_frame_format`       | `'jpg', 'png'`                                                                | `'png'`            |
| `temp_frame_quality`      | Range `[0-100]`                                                               | `0`                |
| `output_video_encoder`    | `'libx264', 'libx265', 'libvpx-vp9', 'h264_nvenc', 'hevc_nvenc'`              | `'libx264'`        |
| `output_video_quality`    | Range `[0-100]`                                                               | `35`               |
| `max_memory`              | -                                                                             | -                  |

<!-- ```
python run.py [options]

-h, --help                                                                 show this help message and exit
-s SOURCE_PATH, --source SOURCE_PATH                                       select an source image
-t TARGET_PATH, --target TARGET_PATH                                       select an target image or video
-o OUTPUT_PATH, --output OUTPUT_PATH                                       select output file or directory
--frame-processor FRAME_PROCESSOR [FRAME_PROCESSOR ...]                    frame processors (choices: face_swapper, face_enhancer, ...)
--keep-fps                                                                 keep target fps
--keep-frames                                                              keep temporary frames
--skip-audio                                                               skip target audio
--many-faces                                                               process every face
--reference-face-position REFERENCE_FACE_POSITION                          position of the reference face
--reference-frame-number REFERENCE_FRAME_NUMBER                            number of the reference frame
--similar-face-distance SIMILAR_FACE_DISTANCE                              face distance used for recognition
--temp-frame-format {jpg,png}                                              image format used for frame extraction
--temp-frame-quality [0-100]                                               image quality used for frame extraction
--output-video-encoder {libx264,libx265,libvpx-vp9,h264_nvenc,hevc_nvenc}  encoder used for the output video
--output-video-quality [0-100]                                             quality used for the output video
--max-memory MAX_MEMORY                                                    maximum amount of RAM in GB
--execution-provider {cpu} [{cpu} ...]                                     available execution provider (choices: cpu, ...)
--execution-threads EXECUTION_THREADS                                      number of execution threads
-v, --version                                                              show program's version number and exit
``` -->


<!-- ### Headless

Using the `-s/--source`, `-t/--target` and `-o/--output` argument will run the program in headless mode. -->


## Disclaimer

This software is designed to contribute positively to the AI-generated media industry, assisting artists with tasks like character animation and models for clothing.

We are aware of the potential ethical issues and have implemented measures to prevent the software from being used for inappropriate content, such as nudity.

Users are expected to follow local laws and use the software responsibly. If using real faces, get consent and clearly label deepfakes when sharing. The developers aren't liable for user actions.


## Licenses

Our software uses a lot of third party libraries as well pre-trained models. The users should keep in mind that these third party components have their own license and terms, therefore our license is not being applied.


## Credits

- [deepinsight](https://github.com/deepinsight) for their [insightface](https://github.com/deepinsight/insightface) project which provided a well-made library and models.
- all developers behind the libraries used in this project


## Documentation

Read the [documentation](https://github.com/s0md3v/roop/wiki) for a deep dive.
