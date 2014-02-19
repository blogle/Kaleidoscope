from PIL import Image, ImageDraw, ImageOps

class IImage(object):

	def __init__(self, arg):
		if type(arg) == type('path'):
			self.pil = Image.open(arg, 'r')
		elif type(arg) == type(('size', 'tuple')):
			self.pil = Image.new('RGBA', arg, 'black')
		else:
			self.pil = arg

		self.width, self.height = self.pil.size

	def save(self, path, extension='PNG', quality=80):
		self.pil.save(path, extension, quality=quality)
		return self

	def flipH(self):
		im = self.pil
		print self.pil.info
		num = int(self.pil.filename.split('frame')[1].split('.png')[0])
		data = (self.width, 0, 0, self.height)
		im = im.transform((self.width,self.height), Image.EXTENT, data)

		file ='output/frame{n}.png'.format(n=num)
		im.save(file)
		im = Image.open(file)
		self.pil = im
		return self

	def flipV(self):
		im = self.pil
		num = int(self.pil.filename.split('frame')[1].split('.png')[0])
		data = (0, self.height, self.width, 0)
		im = im.transform((self.width,self.height), Image.EXTENT, data)

		file ='output/frame{n}.png'.format(n=num)
		im.save(file)
		im = Image.open(file)
		self.pil = im
		return self

	def flipHV(self):
		return self.flipH().flipV()

	def flipVH(self):
		return self.flipV().flipH()

	def duplicateMirrorV(self):
		canvas = IImage((self.width*2, self.height))
		return canvas.paste(self, 0, 0).paste(self.flipV(), self.width, 0)

	def rotate(self, angle):
		self.pil = self.pil.rotate(angle)
		return self

	def paste(self, iimg, x, y):
		self.pil.paste(iimg.pil, (x,y))
		return self

	def thumbnail(self, width, height, mode):
		self.pil.thumbnail((width,height), mode)
		self.width, self.height = self.pil.size
		return self

	def compositeWith(self, iimg, mask):
		self.pil = Image.composite(self.pil, iimg.pil, mask.pil.convert('L'))
		return self

	def fillPolygon(self, points, color):
		maskdraw = ImageDraw.Draw(self.pil)
		maskdraw.polygon(points, color)
		return self

	def copy(self):
		print self.pil.filename
		return IImage(self.pil.copy())

	def makeSquare(self):
		side = min(self.width, self.height)
		box = (
			(self.width - side) // 2,
			(self.height - side) // 2,
			(self.width + side) // 2,
			(self.height + side) // 2
		)
		num = int(self.pil.filename.split('frame')[1].split('.png')[0])
		file ='output/frame{n}.png'.format(n=num)

		self.pil = self.pil.crop(box)
		self.pil.save(file)
		self.pil = Image.open(file)
		self.width, self.height = self.pil.size

		return self

	def mirrorTopLeft(self):

		points = [
			(0, 0),
			(0, self.height),
			(self.width, 0)
		]
		mask = IImage((self.width, self.height))
		mask.fillPolygon(points, "white")
		rotated = self.copy().rotate(-90).flipV()
		self.compositeWith(rotated, mask)

		return self

	def mirrorTopRight(self):
		points = [
			(0, 0),
			(self.width, 0),
			(self.width, self.height)
		]
		mask = IImage((self.width, self.height))
		mask.fillPolygon(points, "white")
		rotated = self.copy().rotate(90).flipV()
		self.compositeWith(rotated, mask)

		self.pil.show()

		return self

	def mirrorBottomLeft(self):
		points = [
			(0, 0),
			(0, self.height),
			(self.width, self.height)
		]
		mask = IImage((self.width, self.height))
		mask.fillPolygon(points, "white")
		rotated = self.copy().rotate(90).flipV()
		self.compositeWith(rotated, mask)
		return self

	def mirrorBottomRight(self):
		points = [
			(0, self.height),
			(self.width, self.height),
			(self.width, 0)
		]
		mask = IImage((self.width, self.height))
		mask.fillPolygon(points, "white")
		rotated = self.copy().rotate(-90).flipV()
		self.compositeWith(rotated, mask)
		return self

	def blendWith(self, iimg, alpha=0.5):
		self.pil = Image.blend(self.pil, iimg.pil, alpha)
		return self

	def kaleidoscope(self, keepOriginalSize=True):
		self.pil = Image.open('output/' + self.pil.filename.split('input/')[1])
		filename = self.pil.filename
		img0 = self.copy().rotate(180)
		img1 = self.copy().rotate(45)
		img2 = self.copy().rotate(135 + 180)


		im = self.combine(img0, img1, img2)

		im = self.mirror(im, 2)
		im = self.mirror(im.rotate(90))

		im.save(filename)
		self.pil = Image.open( filename)


		return self
	def mirror(self, img, n=2):
		x,y = img.size
		mirror_img = Image.new("RGB", (x*n,y), "White")
		for i in range(0, n):
			mirror_img.paste(img, (i*x,0))
		return mirror_img
	#@classmethod
	def combine(self, iimg0, iimg1, iimg2):
		width, height = iimg0.width, iimg0.height
		newSize = (width*2, height*2)
		width, height = newSize

		canvas = Image.new("RGB", newSize, color='black')

		canvas.paste(self.pil, (width/4,height/2), self.pil)
		canvas.paste(iimg0.pil, (width/4,0), iimg0.pil)

		canvas.paste(self.pil.rotate(270), (0, height/4), self.pil.rotate(270))
		canvas.paste(iimg0.pil.rotate(-90), (width/2, height/4), iimg0.pil.rotate(-90))

		canvas.paste(iimg1.pil.rotate(180), (108, 108), iimg1.pil.rotate(180))
		canvas.paste(iimg1.pil.rotate(90), (int(width/2.35), 108), iimg1.pil.rotate(90))

		canvas.paste(iimg2.pil, (108, int(height/2.35)), iimg2.pil)
		canvas.paste(iimg2.pil.rotate(90), (int(width/2.35), int(height/2.35)), iimg2.pil.rotate(90))

		self.pil = canvas

		return self.pil
