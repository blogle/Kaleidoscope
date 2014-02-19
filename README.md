kaleidoscope
============

	from Video import Video
	from Pattern import Pattern

	# open the input video file
	video = Video('video.mp4') 
	# export frames
	video.toFrames() 

	# open the frames as an image pattern
	pattern = Pattern('video_frames/video%d.jpg')
	# apply several filters (the images will be overwritten)
	pattern.apply([
		'makeSquare', 
		'mirrorTopRight', 
		'kaleidoscope',
		'duplicateMirrorV'
	])
	# export the images as a video
	pattern.toVideo(outputPath="output.mpg")

For reference:
[video.mp4](http://www.youtube.com/watch?v=Ng36THlVopY),
[output.mpg](http://www.youtube.com/watch?v=zEO7YMtGUMs)
