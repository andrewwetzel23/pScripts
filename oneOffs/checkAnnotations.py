from tqdm import tqdm
import shutil

import mf

mf.ConfigureLogger("INFO")

def consolidate(idir, sdir):
	tDir = mf.join(idir, "train")
	vDir = mf.join(idir, "val")

	tImages = mf.getImagesFromDirectory(mf.join(tDir, "images"))
	vImages = mf.getImagesFromDirectory(mf.join(vDir, "images"))
	tLabel = mf.getTextFilesFromDirectory(mf.join(tDir, "labels"))
	vLabel = mf.getTextFilesFromDirectory(mf.join(vDir, "labels"))

	dataDirectories = [tImages, vImages, tLabel, vLabel]

	for directory in dataDirectories:
		for file in directory:
			shutil.copy(file, sdir)

Dir = mf.browseForDirectory()
sDir = mf.browseForDirectory()

consolidate(Dir, sDir)
