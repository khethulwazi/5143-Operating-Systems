import os
from os import listdir
import stat
from pwd import getpwuid
from grp import getgrgid
import datetime
import math

def ls(**kwargs):
	flag = str(kwargs.get('flags')).strip('[]').strip('\'\'')
	flags = []
    #directory = kwargs.get('params')
	for f in flag:
		#print(f)
		flags.append(f)
	#print(*flags)
	files = os.listdir('./')
	if flags:
		if 'l' in flags:
			print("\n")
			longListing(files, flags)
			print("\n")	
		elif 'a' in flags:
			files.sort()
			print(*files, "\n")

	else:
		filelist = [f for f in files if f[0] != '.']
		filelist.sort()
		print('\n',*filelist, "\n")
	return
		
def longListing(files, flags):
	#print(*flags)
    #print(os.getcwd())
	#print(*files)
	for n in files:    
		if 'a' in flags:
			entry = []
			filestats = os.lstat(os.path.abspath(os.path.join(os.getcwd(), n)))
			#permissions
			modes = ['r','w','x']
			mode = ''

			#Establishing the filetype
			if stat.S_ISDIR(filestats.st_mode):
				filetype = 'd'
				entry.append(filetype)
			elif stat.S_ISLNK(filestats.st_mode):
				filetype = 'l'
				entry.append(filetype)
			else:
				filetype = '-'
				entry.append(filetype)
				
			#binary representation for permissions
			#evaluate last 9 bits
			st_perms = bin(filestats.st_mode)[-9:]
			for i, perm in enumerate(st_perms):
				if perm == '0':
					mode += '-'                              
				else:
					mode += modes[i % 3]    
			entry.append(mode)

			mode += " " + str(filestats.st_nlink) + " " 
			entry.append(str(filestats.st_nlink))

			mode += getpwuid(filestats.st_uid).pw_name + " "
			entry.append(getpwuid(filestats.st_uid).pw_name)
			mode += getgrgid(filestats.st_gid).gr_name + " "
			entry.append(getgrgid(filestats.st_gid).gr_name)
			mode += str(filestats.st_size) + " "
			
			#returns human readable or bytes
			if 'h' in flags:
				entry.append(convert_size(filestats.st_size).rjust(9))
			else:
				entry.append(str(filestats.st_size).rjust(7))
				
			mode += str(datetime.datetime.fromtimestamp(filestats.st_mtime).strftime('%b %d %H:%M')) + " "
			entry.append(str(datetime.datetime.fromtimestamp(filestats.st_mtime).strftime('%b %d %H:%M')))
			
			print(*entry, n)
			
		else:
			#default behavior should not show hidden                  
			entry = []
			filestats = os.lstat(os.path.abspath(os.path.join(os.getcwd(), n)))
			#permissions
			modes = ['r','w','x']
			mode = ''

			#Establishing the filetype
			if stat.S_ISDIR(filestats.st_mode):
				filetype = 'd'
				entry.append(filetype)
			elif stat.S_ISLNK(filestats.st_mode):
				filetype = 'l'
				entry.append(filetype)
			else:
				filetype = '-'
				entry.append(filetype)
				
			#binary representation for permissions
			#evaluate last 9 bits
			st_perms = bin(filestats.st_mode)[-9:]
			for i, perm in enumerate(st_perms):
				if perm == '0':
					mode += '-'                              
				else:
					mode += modes[i % 3]    
			entry.append(mode)

			mode += " " + str(filestats.st_nlink) + " " 
			entry.append(str(filestats.st_nlink))

			mode += getpwuid(filestats.st_uid).pw_name + " "
			entry.append(getpwuid(filestats.st_uid).pw_name)
			mode += getgrgid(filestats.st_gid).gr_name + " "
			entry.append(getgrgid(filestats.st_gid).gr_name)
			mode += str(filestats.st_size) + " "
			
			#returns human readable or bytes
			if 'h' in flags:
				entry.append(convert_size(filestats.st_size).rjust(9))
			else:
				entry.append(str(filestats.st_size).rjust(7))
			mode += str(datetime.datetime.fromtimestamp(filestats.st_mtime).strftime('%b %d %H:%M')) + " "
			entry.append(str(datetime.datetime.fromtimestamp(filestats.st_mtime).strftime('%b %d %H:%M')))

			print(*entry, n)
	#return

def convert_size(size_bytes): 
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

if __name__=='__main__':
	ls()
