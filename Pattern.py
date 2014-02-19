import subprocess
import os, sys
from PIL import Image, ImageDraw
from IImage import IImage

class IImage2(IImage):

	def makeTriangle(self):
		num = int(self.pil.filename.split('frame')[1].split('.png')[0])
		file ='output/frame{n}.png'.format(n=num)
		self.pil = Image.open(file)
		self.width, self.height = self.pil.size
		im = self.pil
		#first mask
		mask = Image.new('L', im.size, color=255)
		draw = ImageDraw.Draw(mask)

		triangles = [(self.width/2, self.height/2), (0, self.height), (0,0),
					 (self.width, 0), (self.width, self.height),
					 (self.width/2, self.height/2)]

		draw.polygon(triangles, fill=0)
		im.putalpha(mask)

		im.save(file)
		im = Image.open(file)
		self.pil = im
		return self

class Pattern:
	def __init__(self, paths):
		self.folder = os.path.split(paths)[0]
		self.filenames = os.path.split(paths)[1]
		self.imgPaths = paths

		if not os.path.exists(self.folder):
			raise Exception('Directory does not exist')

		self.imgNumber = len(os.listdir(self.folder))

		if self.imgNumber == 0:
			raise Exception('Empty folder')

		if '.' in self.filenames:
			self.extension = self.filenames[self.filenames.rindex('.'):]

	def apply(self, methodList):
		for method in methodList:
			for n in range(0+1, self.imgNumber):
				displayProgress('Applying '+method, n, self.imgNumber-1)
				imgPath = self.imgPaths.format(n)
				iimg = IImage2(imgPath)
				iimg = getattr(iimg, method)()

		return self


def displayProgress(text, n, total):
	sys.stdout.write("\r" + text + " %.2f%%" % (n*100/float(total)))
	sys.stdout.flush()
	if n==total:
		sys.stdout.write("\n")