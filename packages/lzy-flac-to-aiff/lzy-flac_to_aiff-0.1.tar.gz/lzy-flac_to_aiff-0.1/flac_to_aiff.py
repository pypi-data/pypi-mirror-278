import os
from pydub import AudioSegment


def flac_to_aiff(source_folder, output_folder):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历源文件夹中的所有文件
    for root, dirs, files in os.walk(source_folder):
        for n, file in enumerate(files):
            if file.endswith('.flac'):
                # 构建完整的文件路径
                file_path = os.path.join(root, file)
                # 读取音频文件
                audio = AudioSegment.from_file(file_path, format="flac")
                # 构建输出文件的路径
                output_file_path = os.path.join(output_folder, file[:-4] + 'aiff')
                # 导出为AIFF格式
                audio.export(output_file_path, format="aiff")
                print(n, f'Converted {file_path} to {output_file_path}')
