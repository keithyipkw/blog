import itertools
import ffmpeg
import numpy as np
import cv2
import pytesseract
import pandas as pd
import os

class Bounds:
    def __init__(self, x1, y1, x2, y2) -> None:
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def scale(self, factor) -> None:
        self.x1 = int(self.x1 * factor)
        self.x2 = int(self.x2 * factor)
        self.y1 = int(self.y1 * factor)
        self.y2 = int(self.y2 * factor)

class Result:
    def __init__(self, level, lives, time, video_time) -> None:
        self.level = level
        self.lives = lives
        self.time = time
        self.video_time = video_time
    
    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f'({self.level}, {self.lives}, {self.time}, {self.video_time})'

def frame_to_time(frame, fps) -> str:
    t = float(frame) / fps
    return f'{int(t / 60):02}:{int(t % 60):02}'

video_list = 'C:\\Users\\user\\Downloads\\pangaea\\pangaea-s5-480p\\videos.txt' # a list of paths
output_file = 'output.txt'

height = 480
width = 854
fps = 30

scale = 480.0 / 360
yellow_upper = np.array([255, 220, 20], dtype=np.uint8)
yellow_lower = np.array([230, 190, 0], dtype=np.uint8)
yellow_bounds = Bounds(73, 35, 640 - 73, 43)
yellow_bounds.scale(scale)
yellow_ratio = 0.7

black_upper = np.array([6, 6, 6], dtype=np.uint8)
black_bounds = Bounds(157, 113, 640 - 157, 360 - 113)
black_bounds.scale(scale)
black_ratio = 0.7

skip_intro_frame_count = 10 * fps

time_bounds = Bounds(292, 0, 347, 15)
time_bounds.scale(scale)
level_bounds = Bounds(599, 0, 640, 18)
level_bounds.scale(scale)
level_image_padding = 5
padded_level_image = np.full((level_bounds.y2 - level_bounds.y1 + level_image_padding * 2, level_bounds.x2 - level_bounds.x1 + level_image_padding * 2), 255, dtype=np.uint8)
level_image_buffer = padded_level_image[level_image_padding:-level_image_padding, level_image_padding:-level_image_padding]

lives_bounds = Bounds(335, 184, 425, 259)
lives_bounds.scale(scale)
lives_image_padding = 10
padded_lives_image = np.full((lives_bounds.y2 - lives_bounds.y1 + lives_image_padding * 2, lives_bounds.x2 - lives_bounds.x1 + lives_image_padding * 2), 255, dtype=np.uint8)
lives_image_buffer = padded_lives_image[lives_image_padding:-lives_image_padding, lives_image_padding:-lives_image_padding]

lives_white_bounds = Bounds(335, 184, 380, 259)
lives_white_bounds.scale(scale)
lives_white_ratio = 275.0 * scale * scale / (lives_white_bounds.x2 - lives_white_bounds.x1) / (lives_white_bounds.y2 - lives_white_bounds.y1)
lives_white_lower = np.array([200, 200, 200], dtype=np.uint8)

digits_config = r'--psm 7 -c tessedit_char_whitelist=1234567890 -l digits'
time_config = r'--psm 7 -c tessedit_char_whitelist=1234567890:'

results = []
previous_level = -1

videos = pd.read_csv(video_list, sep='\t')
folder = os.path.dirname(video_list)

output = open(os.path.join(folder, output_file), 'w', encoding='utf-8')

for index, file in zip(videos['index'], videos['file']):
    print(f'{index}: {file}')
    file_path = os.path.normpath(os.path.join(folder, file))
    
    process1 = (
        ffmpeg
        .input(file_path)
        .output('pipe:', format='rawvideo', pix_fmt='rgb24')
        .run_async(pipe_stdout=True)
    )

    i = 0
    current = -skip_intro_frame_count
    for i in itertools.count():
        in_bytes = process1.stdout.read(width * height * 3)
        if not in_bytes:
            break
        if i < current + skip_intro_frame_count:
            continue
        frame = (
            np
            .frombuffer(in_bytes, np.uint8)
            .reshape([height, width, 3])
        )

        intro_yellow = frame[yellow_bounds.y1:yellow_bounds.y2, yellow_bounds.x1:yellow_bounds.x2, :]
        intro_yellow2 = intro_yellow
        intro_yellow = np.logical_and(intro_yellow > yellow_lower, intro_yellow < yellow_upper)
        intro_yellow = intro_yellow.all(-1)
        if np.count_nonzero(intro_yellow) < intro_yellow.size * yellow_ratio:
            continue

        intro_black = frame[black_bounds.y1:black_bounds.y2, black_bounds.x1:black_bounds.x2, :]
        intro_black = intro_black < black_upper
        intro_black = intro_black.all(-1)
        if np.count_nonzero(intro_black) < intro_black.size * black_ratio:
            continue
        
        lives_white = frame[lives_white_bounds.y1:lives_white_bounds.y2, lives_white_bounds.x1:lives_white_bounds.x2, :]
        lives_white = lives_white > lives_white_lower
        lives_white = lives_white.all(-1)
        if np.count_nonzero(lives_white) < lives_white.size * lives_white_ratio:
            continue

        current = i

        frame = 255 - cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        level_image = frame[level_bounds.y1:level_bounds.y2, level_bounds.x1:level_bounds.x2]
        np.copyto(level_image_buffer, level_image)
        level = pytesseract.image_to_string(padded_level_image, config=digits_config).strip()
        if level == previous_level:
            continue
        previous_level = level

        lives_image = frame[lives_bounds.y1:lives_bounds.y2, lives_bounds.x1:lives_bounds.x2]
        np.copyto(lives_image_buffer, lives_image)
        lives = pytesseract.image_to_string(padded_lives_image, config=digits_config).strip()
        
        output.write('\t'.join(str(s) for s  in [index, level, lives, frame_to_time(i, fps), file]))
        output.write('\n')
        output.flush()
