#!/usr/bin/env python
import os,sys

proses = sys.argv[1]

hasiltm = os.popen("ps -ef | grep "+proses).read()[:-1]
namauser = os.popen("whoami").read()[:-1]
prosesid = hasiltm.lstrip(namauser).lstrip(" ")[ :hasiltm.lstrip(namauser).lstrip(" ").find(" ") ]

os.system("kill -9 "+prosesid)
