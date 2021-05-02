import os
import subprocess
import shutil
from datetime import datetime


class FileOrganizer:


    extensionsPhotos = ['jpg', 'png', 'jpeg', 'JPG', 'PNG', 'JPEG', 'gif', 'GIF']
    extensionsVideos = ['mp4', 'MP4', '3gp', '3GP']
    exe = 'exiftool.exe'


    def folder_path_from_file_date(self,file, extension=''):
        date = self.file_shooting_date(file)
        return extension + date.strftime('%Y') + '/' + date.strftime('%B')


    def file_shooting_date(self,file):
        archive = subprocess.Popen(
            [self.exe, file], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        metadata = []
        for output in archive.stdout:
            line = output.decode('utf-8').splitlines()[0].split(": ")
            if line[0].strip() == 'File Modification Date/Time':
                break
            info = (line[0].strip(), line[1])
            metadata.append(info)
        infors = dict(metadata)

        if 'File Modification Date/Time' in infors:
            date = infors['File Modification Date/Time'][0:19]
            date = datetime.strptime(date, '%Y:%m:%d %H:%M:%S')
        else:
            date = datetime.fromtimestamp(os.path.getmtime(file))
        return date


    def move_file(self,file, extension=''):
        new_folder = self.folder_path_from_file_date(file, extension)
        if not os.path.exists(new_folder):
            os.makedirs(new_folder)
        shutil.move(file, new_folder + '/' + file)
        print(new_folder + '/' + file)


    def organize(self):
        photos = [
            filenamePhotos for filenamePhotos in os.listdir('.') if any(filenamePhotos.endswith(ext) for ext in self.extensionsPhotos)
        ]
        videos = [
            filenameVideos for filenameVideos in os.listdir('.') if any(filenameVideos.endswith(ext) for ext in self.extensionsVideos)
        ]

        for filenamePhotos in photos:
            self.move_file(filenamePhotos, 'Images/')

        for filenameVideos in videos:
            self.move_file(filenameVideos, 'Videos/')

FO = FileOrganizer()
FO.organize()