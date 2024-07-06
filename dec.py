import cv2
import numpy as np
from tqdm import tqdm

def decode_video(video_path, output_file_path, width=1920, height=1080, pix=3):
    video_reader = cv2.VideoCapture(video_path)
    add = int(width * height / (pix * pix))
    m = True
    frame_count = int(video_reader.get(cv2.CAP_PROP_FRAME_COUNT))

    with open(output_file_path, 'ab') as output_file:
        for _ in tqdm(range(frame_count), desc="Decoding video"):
            ret, frame = video_reader.read()
            if not ret:
                break
            frame = cv2.resize(frame, (int(width / pix), int(height / pix)), interpolation=cv2.INTER_NEAREST)
            if frame.size == 0:
                break
            intensity = np.mean(frame, axis=(2 if len(frame.shape) == 3 else 0))

            if not m:
                binary_data = ''.join(np.where(intensity.flatten() > 127, '1', '0').astype(str))
                binary_array = np.array([int(bit) for bit in binary_data])
            else:
                binary_data = ''.join(np.where(intensity.flatten() > 127, '1', '0').astype(str))
                first_one_index = binary_data.find('1')
                binary_array = np.array([int(bit) for bit in binary_data[first_one_index + 1:]])
                m = False

            bytes_array = np.packbits(binary_array)
            output_file.write(bytes_array)

if __name__ == "__main__":
    video_path = "/home/cr4nfus3d/Documents/projects/storage-3/storage works/version-2_best/redgear.mp4"
    output_file_path = "/home/cr4nfus3d/Documents/projects/storage-3/storage works/version-2_best/generated/redgear-mouse-driver-A15.zip"
    decode_video(video_path, output_file_path)