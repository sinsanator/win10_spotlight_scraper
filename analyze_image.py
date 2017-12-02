import sys
from PIL import Image

def main(argv):
	''' Use PIL to look at the image and reject it if it doesn't meet our desired requirements (like resolution and layout)'''
	
	with Image.open(argv[1]) as img:
		width, height = img.size
		print("File {} has layout width={} height={}".format(argv[1], 
															 width, 
															 height))
	return True


if __name__ =="__main__":
	main(sys.argv)