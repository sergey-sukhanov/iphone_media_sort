import glob
import exifread
import os
from shutil import copyfile
import ntpath
import time


def copy_date_folder(file, timestamp, target_dir):
    if timestamp is not None:
        folder_to_copy = timestamp.replace(':', '').split(' ')[0]
        folder_to_copy = os.path.join(target_dir, folder_to_copy)
        if not os.path.exists(folder_to_copy):
            os.mkdir(folder_to_copy)
        copyfile(file, os.path.join(folder_to_copy, ntpath.basename(file)))


if __name__ == '__main__':

    # Source folder with your media files from iphone
    source_path = 'path'

    # Timestamp field from image tag
    timestamp_field = 'Image DateTime'

    # Set tags and corresponding values to comapre with
    compare_dict = {
        'EXIF LensModel': ['iPhone SE back camera 4.15mm f/2.2', 'iPhone SE front camera 2.15mm f/2.4'],
        'Image Software': '10.3.1'
    }

    output_folder = 'ordered'
    other_folder = 'other'

    # Create target directory
    target_dir = os.path.join(source_path, output_folder)
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)

    other_dir = os.path.join(target_dir, other_folder)
    if not os.path.exists(other_dir):
        os.mkdir(other_dir)

    # Get all images
    files_jpeg = glob.glob(source_path + '*.JPG')
    print('Found: {0} jpg files'.format(len(files_jpeg)))

    for i, file in enumerate(files_jpeg):
        print('Processing: {0} out of {1}'.format(i, len(files_jpeg)))
        f = open(file, 'rb')
        # Flag for other folder
        flag_other = False
        # Return Exif tags
        tags = exifread.process_file(f)
        # Go over all compare fields
        for key, value in compare_dict.iteritems():
            if key not in tags:
                flag_other = True
                break
            if type(value) == list:
                if tags[key].printable not in value:
                    flag_other = True
                    break
            if type(value) == str:
                if tags[key].printable != value:
                    flag_other = True
                    break

        # If flag was set, copy to folder 'other'
        if flag_other:
            copyfile(file, os.path.join(other_dir, ntpath.basename(file)))
            continue

        # Copy file to a folder with the date
        copy_date_folder(file, tags.get(timestamp_field, None).values, target_dir)

    # Get all videos
    files_mov = glob.glob(source_path + '*.MOV')
    print('Found: {0} mov files'.format(len(files_mov)))

    files_jpeg = [ntpath.basename(file).split('.')[0] for file in files_jpeg]
    for i, file in enumerate(files_mov):
        print('Processing: {0} out of {1}'.format(i, len(files_mov)))
        if ntpath.basename(file).split('.')[0] in files_jpeg:
            continue
        else:
            copy_date_folder(file, time.strftime('%Y:%m:%d %HH:%MM', time.gmtime(os.path.getmtime(file))), target_dir)