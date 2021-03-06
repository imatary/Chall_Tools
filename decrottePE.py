#!/usr/bin/python

import pefile
import sys, os

# Extract PE File
# v 0.1

# Need https://code.google.com/p/pefile et on lui doit TOUT
#

# Extract PEFile from "Dump" ... for a EXE not loaded in memory
#

# Copyleft Thanat0s
# http://Thanat0s.trollprod.org
#
# Licence GNU GPL


def decrotte(filearray, text):
  roll = ["|","/","-","\\" ]
  i=0
  dumped = False
  sys.stdout.flush()
  sys.stdout.write( "\r"+int(columns)*" "+"\r")
  for M in range(0,len(filearray)-1):
    if int(filearray[M]) == ord('M') and  int(filearray[M+1]) == ord('Z') :
      i=(i+1) % 4
      sys.stdout.write (" >Seeking %s %s\r" % (roll[i],text))
      sys.stdout.flush()
      try:
        PE = pefile.PE(data="".join(chr(b) for b in filearray[M::]))
        for section in PE.sections:    # va chercher les data la dernierse section fait fois
          location = section.PointerToRawData
          locationadd = section.SizeOfRawData
        Z = location + locationadd
        with open(('PE_%d.exe' % M), 'w') as outfile:
            outfile.write(filearray[M:M+Z])
            dumped = True
        print ('\n[*] Found PE_%d.exe %d bytes saved\n' % (M,Z)),
      except:
        pass
  #sys.stdout.write( "\r"+int(columns)*" "+"\r")
  return dumped

def win():
  print"\n[i] I was victorious..."
  sys.exit(0)

def xor(key,inc, filearray):
  filearrayout = filearray
  for I in range (0,len(filearrayout)): # Pas 0, s'occuppe pas de l'exe host
    filearrayout[I] = filearrayout[I] ^ key
    key = (key+inc) % 256 
  return filearrayout


rows, columns = os.popen('stty size', 'r').read().split()
# Needs two arg if not... help
if len(sys.argv) < 2:
        print ('Extract PE from Dump')
        print 'To Use: '+ sys.argv[0]+  ' filename [-xor]'
        print '         [-xor] enable XOR Bruteforcing'
        sys.exit(1)
FILENAME = sys.argv[1]

XOR = False
# Xor or not ?
if len(sys.argv) == 3:
  if sys.argv[2].upper() == "-XOR":
    print "[i] Ok I Will Brutalizing the XorCipher"
    XOR = True

# Test if file exists
if not os.path.isfile(FILENAME):
    print 'File not found'
    sys.exit(1)
print "[i] Scanning %s" % FILENAME
with open(FILENAME, 'rb') as f:
  filearray = bytearray(f.read())

result = decrotte(filearray,"Searching for PE")
if result:
  win()
if XOR == False:
  print "[!] Sorry nothing.. try with -XOR"
  sys.exit(0)


print("[!] No PE found, will try the chinese style; SIMPLE XOR")
key = 1
while key < 256:
  result = decrotte(xor(key,0,filearray),("8Bits Xor key %d"% key))
  if result:
    win()
  key = key+1

print("[!] No PE found, will try the chinese style; XOR Shifted")
key = 1
while key < 256:
  result = decrotte(xor(key,1,filearray),("8Bits Xor Inc key %d"% key))
  if result:
    win()
  result = decrotte(xor(key,-1,filearray),("8Bits Xor Dec key %d"% key))
  if result:
    win()
  key = key+1

print("[!] No PE found, will try the chinese style; XOR Shifted looking every offsets")
key = 1
while key < 256:
  offset = 0
  while offset < 256:
    key2 = (key + offset) % 256
    result = decrotte(xor(key2,1,filearray),("8Bits Xor Inc key %d offset  %d"% (key,offset)))
    if result:
      win()
    result = decrotte(xor(key2,-1,filearray),("8Bits Xor Dec key %d offset %d"% (key,offset)))
    if result:
      sys.exit(0)
    offset = offset + 1
  key=key+1


print "[!] Sorry nothing.. "
