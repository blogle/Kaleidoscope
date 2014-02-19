import subprocess
import os, sys

class Video:
	def __init__(self, path=''):
		# TODO: find a video library
		self.path = path
		self.filename = os.path.split(self.path)[1]
		if '.' in self.filename:
			self.filename = self.filename[:self.filename.rindex('.')]

	def toFrames(self, frameRate="24"):
		sys.stdout.write("Warning: exporting frames from a " +
			"video will produce a great ammount of image " + 
			"files (depending on the video duration)\n" +
			"Do you wish to continue? (Y/n)\n")
		response = raw_input()
		if response in ["n","N","no","No","NO"]:
			return

		outputDir = self.filename + '_frames/'
		
		if not os.path.exists(outputDir):
			subprocess.call(['mkdir', outputDir])

		# TODO: Read from file
		frameRate = str(frameRate)
		frameSize = "1280x720"

		sys.stdout.write("Outputting video frames...")
		sys.stdout.flush()
		subprocess.call([
			"ffmpeg",
			"-i", self.path, # Input path
			"-an", # Disable audio
			"-sameq", # Same quality as source
			"-r", frameRate, # Frame rate
			"-s", frameSize , # Frame size
			outputDir + self.filename + "%d.jpg",	#output path
		], stderr=subprocess.PIPE)
		sys.stdout.write("done\n")
