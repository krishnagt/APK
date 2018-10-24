#!/usr/bin/env python

import argparse
import glob
import os
import os.path
import subprocess
import tempfile

parser = argparse.ArgumentParser(description='Small script to re-sign Android apk file with different signature.')
parser.add_argument('apkfile', help='Original Apk file')
parser.add_argument('-o', '--output', dest='output', help='Output apk path. Default path is YOUR-ORIGINAL-NAME-signed.apk under the same directory as your original apk file.')

args = parser.parse_args()

# default android debug key
# TODO: make it configurable
keystore = os.path.join(os.path.expanduser("~"), "/Users/mobileopsblr/Desktop/Script-Upload APK/my-release-key.keystore")
keypass = "Philips2011*!"
storepass = "Philips2011*!"
alias = "philips_android_mktplace"

# output apk file
if args.output:
	newapk = os.path.abspath(args.output)
else:
	name, ext = os.path.splitext(args.apkfile)
	newapk = name + "-signed" + ext

print keypass
tempdir = tempfile.mkdtemp()

unzip_command = ['unzip']
unzip_command.extend(['-d', tempdir])
unzip_command.append('-q')
unzip_command.append(args.apkfile)

subprocess.call(unzip_command)

filelist = glob.glob(os.path.join(tempdir, "META-INF/*"))
for f in filelist:
	os.remove(f)

os.chdir(tempdir)
zip_command = ['zip']
zip_command.append('-r')
zip_command.append('-q')
zip_command.append(newapk)
zip_command.append('.')
print zip_command
subprocess.call(zip_command)
zip_align=['zipalign']
zip_align.append('-v')
zip_align.append('-p')
zip_align.append('4')
zip_align.append(newapk)
zip_align.append(newapk)
print zip_align
subprocess.call(zip_align)

jarsigner_command = ['jarsigner']
jarsigner_command.extend(['-keystore', keystore])
jarsigner_command.extend(['-keypass', keypass])
jarsigner_command.extend(['-storepass', storepass])
jarsigner_command.append(newapk)
jarsigner_command.append(alias)
print jarsigner_command
subprocess.call(jarsigner_command)
print "output to " + newapk
