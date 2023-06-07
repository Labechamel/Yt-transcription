
# Yt-Transcription

## Description

This project is a Python application that allows you to download videos from various websites, with a particular focus on YouTube. It utilizes the yt-dlp library to handle the video downloading process. The program features a graphical user interface (GUI) built with Qt, providing a user-friendly way to download videos.

This project has been designed with the aim of making internet videos accessible to the hearing-impaired community and ensuring worldwide access to online videos, irrespective of the spoken language. By integrating video downloading, transcription, and subtitle generation capabilities, this project empowers individuals with hearing impairments to engage with online video content. 

Additionally, with the inclusion of translation features, it enables users to transcend language barriers and enjoy videos from across the globe. Through these efforts, the project strives to foster inclusivity, break down communication barriers, and create a more inclusive online environment

One of the main functionalities of this application is the ability to select the Whisper speech recognition model's confidence level. By specifying the desired confidence level, the application can transcribe the audio of the downloaded video and generate corresponding subtitle files. These subtitle files are then placed in the same directory as the downloaded video.

The benefit of this approach is that when you play the video using VLC media player, the .str subtitle file is automatically recognized and synchronized with the video based on the correct time codes, providing an enhanced viewing experience.

To utilize this functionality, the application relies on the Whisper library from OpenAI. It is important to note that the project was developed and tested on a computer with a 6 GB NVIDIA GPU and CUDA installed, along with the Whisper library.


## Features

- Download videos from various websites, including YouTube (using the yt-dlp library).
- User-friendly graphical user interface (GUI) created with Qt.
- Select the confidence level of the Whisper speech recognition model.
- Automatically transcribe the audio of the downloaded video.
- Generate subtitle files (.str) corresponding to the transcribed audio.
- Place the subtitle file in the same directory as the downloaded video.
- Subtitle files are recognized by VLC media player and synchronized with the video based on time codes.


## Prerequisites

- Python (version 3.9) installed on your system.
- Whisper and Cuda for NVIDIA GPU installed on your system.
- PyTorch (1.10.1 or above) for Whisper.
- The pip package manager to install Python dependencies.
- The yt-dlp library (version 2023.3.4 or above) for video downloading.
- The PySide6.QtWidgets library (version 6.5.0 or above) for creating the graphical user interface.
- The Whisper library (version 20230314 or above) from OpenAI for speech transcription.
- A computer with an NVIDIA graphics processor and CUDA installed to utilize the Whisper library with GPU acceleration.

Please ensure that you have an active internet connection to download videos from supported websites & Whisper installed on your system and working on your system. 

Please note that while Whisper relies on GPU acceleration, it may also be possible to run the project in CPU mode. However, performance may be significantly reduced without a compatible GPU.


## Prerequisites installation

**To run this project, you'll need to follow these steps:**

Install [Python version 3.9](https://www.python.org/downloads/) on your system.

Set up the pip package manager. If you don't have it installed, follow the instructions at https://pip.pypa.io/en/stable/installing/.

Install the yt-dlp library by running the following command:

```bash
pip install yt-dlp==2023.3.4
```

Install the PySide6.QtWidgets library by executing the following command:
```bash
pip install PySide6==6.5.0
```
Install the [Whisper](https://github.com/openai/whisper) library from Github Whisper OpenAI. Please refer to the official documentation for installation instructions. You can find more information at [Whisper OpenAI on Github](https://github.com/openai/whisper)

Install [CUDA](https://developer.nvidia.com/cuda-downloads?target_os=Windows&target_arch=x86_64&target_version=11) on your computer. CUDA is required for GPU acceleration with Whisper. Please follow the installation instructions provided by NVIDIA for your specific operating system and GPU model.

Install [PyTorch](https://pytorch.org/get-started/locally/) by visiting the PyTorch website and following the installation instructions specific to your platform.


## Configuration

**Before using this project, you need to perform the following configurations:**

Make sure you have a machine with a compatible NVIDIA GPU and CUDA installed. The GPU memory size is important in determining the Whisper level you can effectively utilize.

If your GPU has 6 GB of RAM or more, you can typically use medium Whisper levels for better transcription quality. Here are the recommended levels:

|  Size  | Parameters | Multilingual model | Required VRAM | Relative speed |
|:------:|:----------:|:------------------:|:-------------:|:--------------:|
|  tiny  |    39 M    |       `tiny`       |     ~1 GB     |      ~32x      |
|  base  |    74 M    |       `base`       |     ~1 GB     |      ~16x      |
| small  |   244 M    |       `small`      |     ~2 GB     |      ~6x       |
| medium |   769 M    |      `medium`      |     ~5 GB     |      ~2x       |
| large  |   1550 M   |      `large`       |    ~10 GB     |       1x       |

If your GPU has less than 5 GB of RAM, it is recommended to use lower Whisper levels to ensure optimal performance. Choose one that fits within your GPU's VRAM limitations.

Configure the project to use the desired Whisper level. You can modify the configuration file or the relevant parameter in your project's code to specify the desired level based on your GPU's VRAM size.

For example, if your GPU has 6 GB of RAM, you can choose the "small" level for a good balance between transcription quality and memory usage but you can also choose "medium" for a higher quality.


## Usage

**To use this project, follow these steps:**

- Ensure that you have successfully installed all the dependencies and configured the project as mentioned in the previous sections.

- Download or clone this projet with this command :
```bash
git clone https://github.com/Labechamel/Yt-transcription
```

- Launch the project by running the following command in your terminal or command prompt:
```bash
python main.py
```

- Choose your level of Whiisper, past your Youtube url and then press "enter" or  "start button".


[![Demo Yt-transcription](https://github.com/Labechamel/Yt-transcription/blob/master/github_img/exemple.gif)](https://github.com/Labechamel/Yt-transcription/blob/master/github_img/exemple.gif)


- Go to the folder video and enjoy your video with subtitle. 


## Next step

- [ ]  **Translation Feature :**
Implement a translation feature using services like Google Translate or DeepL to enable users to translate the subtitles into different languages.

- [ ]  **User Interface Enhancements :**
Improve the user interface to enhance usability and provide a more intuitive experience for users.

- [ ]  **Dark Mode :**
Add a dark mode theme option to the user interface, providing a visually pleasing alternative for users who prefer dark backgrounds.

- [ ]  **Download and Transcription Progress :**
Incorporate progress bars or indicators to display the download and transcription progress in real-time. This will provide users with visual feedback on the status of these processes. If translation is implemented, a progress bar for the translation process can also be included.


## Contribution

`Contributions` and `improvements` to this project are welcome. If you have any suggestions, bug fixes, or new features to propose, please feel free to submit a pull request or open an issue on the project's GitHub repository. Your contributions will be reviewed and considered for incorporation into the project.

`I appreciate your help in making this project even better!`


## Author

This project was developed by Labechamel. 

Thank you for your interest in this project!

If you have any more questions, feel free to ask.

- [@Labechamel](https://github.com/Labechamel)
[![portfolio](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://simonbechu.me/)
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/bechu-simon/)
