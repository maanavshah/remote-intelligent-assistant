from os import listdir
from os.path import isfile, join, getsize, splitext, isdir

#listing of all the subfolder and files in any directory
class Files:
    file_count = 0

    def __init__(self, name, size, extension, parent):
        self.name = name
        self.size = size
        self.extension = extension
        self.parent = parent
        Files.file_count += 1

    def display(self):
        print ('%-5s' % self.name, "%-4s" % self.size, "%-5s" % self.extension, self.parent)


def display_list(file_list):
    print
    print "Name  Size  Ext  Parent_Directory"
    print
    for files in file_list:
        files.display()
    print
    print "Total Files Scanned : ", Files.file_count


def find(path, listfile):
    for files in listdir(path):
        if isfile(join(path, files)):
            fileparent, fextension = splitext(path + files);
            filename, fextension = splitext(files);
            listfile.append(Files(filename, getsize(path + files), fextension, fileparent))
        elif isdir(join(path, files)):
            find(path + files + "/", listfile)


if __name__ == "__main__":
    file_list = []
    find("/home/", file_list)
    display_list(file_list)

