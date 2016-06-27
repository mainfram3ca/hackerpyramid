#!/usr/bin/env python
import subprocess, json, os

def getLength(filename):
    result = subprocess.Popen(["avprobe", "-of", "json" ,"-show_streams", "-loglevel", "quiet", filename], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    string = "".join(result.stdout.readlines())
    jobject = json.loads(string)
    try:
	return jobject['streams'][0]['duration']
    except:
	pass

files = [f for f in os.listdir('.') if os.path.isfile(f)]
for f in files:
    if f.find(".mp4") > 0:
	print "%s: %s" %(f,getLength(f))


