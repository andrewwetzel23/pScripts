import mf

dir = mf.browseForDirectory()

subdirs = mf.getSubdirectoriesFromDirectory(dir)

for subdir in subdirs:
    mf.deleteRedFromDirectory(subdir)
    mf.resizeImages(subdir, [576, 352])