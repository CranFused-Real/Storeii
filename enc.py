import cv2
import numpy as np
import os
from tqdm import tqdm

def create_video(output_video_path, inputf, width=1920, height=1080, frame_rate=29, pix=3): # pix=5 (default), Increasing the frame_rate reduces the length, frame_rate=12 (default)
    with open(inputf, 'rb') as file:
        size = os.path.getsize(inputf)
        chunk = int(width * height / (pix * pix))
        width1 = width
        height1 = height
        width = int(width / pix)
        height = int(height / pix)
        add = height * width
        total_bits = size * 8
        if total_bits <= chunk:
            total_bits = chunk
        total_frames = int(np.ceil(total_bits / (width * height)))
        fourcc = cv2.VideoWriter_fourcc(*'png ')
        video_writer = cv2.VideoWriter(output_video_path, fourcc, frame_rate, (width1, height1), isColor=False)

        m = 1
        for _ in tqdm(range(total_frames), desc="Encoding video"):
            if m == 0:
                content = file.read(int(chunk / 8))
                content = ''.join(format(byte, '08b') for byte in content)
                values = np.array([int(content[bit2]) * 255 for bit2 in range(chunk)])
            else:
                size2 = size * 8
                size3 = size2 % chunk
                temp = chunk - size3
                content = file.read(int(size3 / 8))
                binary_data = '0' * (temp - 1)
                binary_data += '1'
                content = ''.join(format(byte, '08b') for byte in content)
                binary_data += content
                values = np.array([int(binary_data[bit]) * 255 for bit in range(chunk)])
                m = 0

            frame = np.zeros((height, width), dtype=np.uint8)
            frame.flat = values
            frame = frame.reshape((height, width))
            frame = cv2.resize(frame, (width1, height1), interpolation=cv2.INTER_NEAREST)
            video_writer.write(frame)

        video_writer.release()

if __name__ == "__main__":
    input_file_path = "/home/cr4nfus3d/Documents/projects/storage-3/storage works/version-2_best/input/mouse.rar"
    output_video_path = "/home/cr4nfus3d/Documents/projects/storage-3/storage works/version-2_best/output/out1.avi"
    create_video(output_video_path, input_file_path)