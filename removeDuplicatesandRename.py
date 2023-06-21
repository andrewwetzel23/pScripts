import os
import hashlib
from pathlib import Path
from tqdm import tqdm
import shutil


from funcs import browse_for_dir, get_subdirectories, get_images_from_dir, get_extension, convert_name_to_text


# Dialog box for selecting a folder.
file_path = browse_for_dir()
dir = file_path

# Listing out all the files
# inside our root folder.
list_of_files = os.walk(file_path)

# In order to detect the duplicate
# files we are going to define an empty dictionary.
unique_files = dict()
count = 0
for root, folders, files in list_of_files:


	# Running a for loop on all the files
	for file in tqdm(files, 'Removing duplicates...'):
		if get_extension(file) != '.txt':

			# Finding complete file path
			file_path = Path(os.path.join(root, file))

			# Converting all the content of
			# our file into md5 hash.
			Hash_file = hashlib.md5(open(file_path, 'rb').read()).hexdigest()

			# If file hash has already #
			# been added we'll simply delete that file
			if Hash_file not in unique_files:
				unique_files[Hash_file] = file_path
			else:
				os.remove(file_path)
				try:
					os.remove(os.path.join(dir, convert_name_to_text(file)))
				except:
					pass
				count += 1
				# print(f"{file_path} has been deleted")

# print(f'Removed {count} duplicates')



images = get_images_from_dir(dir)
i = 0
for image in tqdm(images, desc=f'Renaming images...'):
		ext = get_extension(image)
		shutil.move(os.path.join(dir, image), os.path.join(dir, f'ch_image_{i}{ext}'))
		try:
			shutil.move(os.path.join(dir, convert_name_to_text(image)), os.path.join(dir, f'ch_image_{i}.txt'))
		except:
			pass
		i += 1