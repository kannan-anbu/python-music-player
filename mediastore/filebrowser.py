import os


def search_files(root, extn, dataqueue):
    for (curdir, subdirs, subfiles) in os.walk(root):
        for file in subfiles:
            if file.endswith(extn):
                absfilepath = curdir + os.sep + file
                dataqueue.put(absfilepath)
    # for i in range(4):
    dataqueue.put('endendend')

