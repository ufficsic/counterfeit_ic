import os
import argparse
import sys
import zipfile


def create_zip_archive(files_to_zip, zip_root, index):
    with zipfile.ZipFile(zip_root + '_' + str(index) + '.zip', 'w', zipfile.ZIP_DEFLATED) as zf:
        for image_path, arcname in files_to_zip:
            zf.write(image_path, arcname)


def process_files(path):
    total_size = 0.0
    index = 0
    files_to_zip = []
    zip_root = os.path.basename(path)
    for root, dirs, files in os.walk(path):
        sub = root[root.index(zip_root):]
        sub_root = sub.strip('.|./|.\\').replace('\\', '_')
        i = 0
        while i < len(files):
            file = files[i]
            i += 1
            image_path = os.path.join(root, file)
            file_size = os.path.getsize(image_path)
            if ((file_size / 1048576.0) > 100.0):
                continue
            if ((total_size + file_size) / 1048576.0) < 100.0:
                total_size += file_size
                arcname = os.path.join(sub_root, file)
                files_to_zip.append((image_path, arcname))
            elif ((total_size + file_size) / 1048576.0) > 100.0:
                index += 1
                create_zip_archive(files_to_zip, zip_root, index)
                total_size = 0
                i -= 1
                files_to_zip.clear()
    if files_to_zip:
        index += 1
        create_zip_archive(files_to_zip, zip_root, index)
        files_to_zip.clear()


if __name__ == "__main__":
    try:
        path = sys.argv[1]
        process_files(path)
    except Exception as e:
        print('------------------ERROR--------------------------')
        print(e)
        print('Provide absolute Path of the folder to be zipped.')
        print('Example: python pyzip_dataset_builder foldername')
        print('-------------------------------------------------')

