some tools I used to help my girlfriend apply a kaleidoscope like effect to a video.
Requires PIL and ~opencv
The pieces are fairly scattered:
the block to convert the video to frames is in the notebook, however you need to monitor it as it will loop back to the
beginning indefinitely (requires opencv). Once you have frames in the input folder, run the process script to apply the
effects. It's up to you to stitch the images back together, I have no experience with ffmpeg so I opted for
Quicktime Pro 7 (not bundled in OS X) then opened the directory as an image sequence/
