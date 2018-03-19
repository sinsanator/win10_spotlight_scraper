import os
import sys
import shutil
import getpass # to get the current user, so we can access his AppData directory. 
from PIL import Image


def spotlight_files_to_jpg(spotlight_dir, target_dir, previously_found=None):
	''' loop through all of the files in the directory. If they don't have an extension, 
	assume they're the windows spotlight files, and give them jpg extensions. '''

	# make sure our input is kosher
	if not os.path.isdir(target_dir):
		print ("Target directory {} doesn't exist, creating it...".format(target_dir))
		os.makedirs(target_dir)

	if not os.path.isdir(spotlight_dir):
		raise Exception("Invalid spotlight directory {}".format(spotlight_dir))

	if previously_found is None:
		previously_found = []

	found = []
	transferred = []
	skip_count = 0

	for file in os.listdir(spotlight_dir):
		# make sure its a file and not a directory
		full_path = os.path.join(spotlight_dir, file)
		if os.path.isfile(full_path):
			if not file in previously_found:
				if "." not in file:
					# DEBUG print("Found new file {}".format(file))
					
					if is_a_wallpaper(full_path):
						# Only copy the file if it passes our wallpaper criteria
						new_found = full_path
						new_transferred = os.path.join(target_dir, "{}.jpg".format(file))
						shutil.copyfile(new_found, new_transferred)
						transferred.append(new_transferred)

					found.append(file)
					
			else:
				# DEBUG print("Skipping already found file {}".format(file))
				skip_count+=1

	print("Found {} new files, skipped {} previously found files, and transferred {} files.".format(len(found), skip_count, len(transferred)))
	return found, transferred

def is_a_wallpaper(image_file_path):
	''' Use PIL to look at the image and reject it if it doesn't meet our desired requirements (like resolution and layout)'''
	valid_image = False
	try:
		with Image.open(image_file_path) as img:
			width, height = img.size
			if width > height and width >= 1920 and height >= 1080:
				# this image meets our requirements for a desktop wallpaper
				valid_image = True
	except Exception as e:
		valid_image = False
		# DEBUG print("Found file {} is not an image file!".format(image_file_path))
	return valid_image


def update_known_images_file(known_list_file, found):
	with open(known_list_file, 'a') as of:

		for found_file in found:
			of.write("{}\n".format(found_file))
	# DEBUG print("Known Images File updated with {} new files".format(len(found)))

def load_known_images(known_images_file):
	known_images = []
	if os.path.isfile(known_images_file):
		with open(known_images_file,"r") as input_file:
			for line in input_file:
				known_images.append(line.strip())

	else:
		print("File {} doesnt exist, it will be created at the end of this run.".format(known_images_file))
	return known_images


def main(argv):

	known_images_file = "known_images.txt"
	user = getpass.getuser()
	spotlight_dir = "C:\Users\{}\AppData\Local\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets".format(user)
	target_dir = "C:\Users\{}\Desktop\potential".format(user)

	known_images = load_known_images(known_images_file)

	found, transferred = spotlight_files_to_jpg(spotlight_dir, target_dir, known_images)
												

	# DEBUG print ("FOUND: \n{}".format(''.join(["{}\n".format(x) for x in found])))
	# DEBUG print ("TRANSFERRED: \n{}".format(''.join(["{}\n".format(x) for x in transferred])))

	update_known_images_file(known_images_file, found)


if __name__ =="__main__":
	main(sys.argv)