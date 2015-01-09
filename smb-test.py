# -*- coding: utf-8 -*-

#you need these two modules: pysmb and pyasn1
#extract pysmb-1.1.13/python2/ and copy /smb and /nmb to site-packages
#extract pyasn1-0.1.7/ and copy /pyasn1 to site-packages

from cStringIO import StringIO
from smb.SMBConnection import SMBConnection
from smb import smb_structs
from nmb.NetBIOS import NetBIOS
import os

def getBIOSName(remote_smb_ip, timeout=5):
  try:
    bios = NetBIOS()
    srv_name = bios.queryIPForName(remote_smb_ip, timeout=timeout)
  except:
    print 'getBIOSName: timeout too short?'
  finally:
    bios.close()
    return srv_name[0]

def getServiceName(username, password, my_name, remote_name, remote_ip):
  conn = connect(username, password, my_name, remote_name, remote_ip)
  if conn:
    shares = conn.listShares()
    for s in shares:
      if s.type == 0:  # 0 = DISK_TREE
        return s.name        
    conn.close()
  else:
    return ''

def getRemoteDir(username, password, my_name, remote_name, remote_ip, path, pattern, service_name):
  conn = connect(username, password, my_name, remote_name, remote_ip)
  if conn:
    try:
      files = conn.listPath(service_name, path, pattern=pattern)
      #files = conn.listPath(service_name, path)
      conn.close()
      return files
    except Exception, e:
      print e

def connect(username, password, my_name, remote_name, remote_ip):
  smb_structs.SUPPORT_SMB2 = False
  conn = SMBConnection(username, password, my_name, remote_name, use_ntlm_v2 = True, is_direct_tcp = True)
  try:
    conn.connect(remote_ip, 445) #139=NetBIOS / 445=TCP
  except Exception, e:
    print e
  return conn

def download(username, password, my_name, remote_name, remote_ip, path, filename, service_name):
  conn = connect(username, password, my_name, remote_name, remote_ip)
  if conn:
    print 'Download = ' + path + filename
    attr = conn.getAttributes(service_name, path+filename)
    print 'Size = %.1f kB' % (attr.file_size / 1024.0)
    print 'start download'
    file_obj = StringIO()
    file_attributes, filesize = conn.retrieveFile(service_name, path+filename, file_obj)
    fw = open(filename, 'w')
    file_obj.seek(0)
    for line in file_obj:
      fw.write(line)
    fw.close()
    print 'download finished'
    conn.close()

def upload(username, password, my_name, remote_name, remote_ip, path, filename, service_name):
  conn = connect(username, password, my_name, remote_name, remote_ip)
  if conn:
    print 'Upload = ' + path + filename
    print 'Size = %.1f kB' % (os.path.getsize(filename) / 1024.0)
    print 'start upload'
    with open(filename, 'r') as file_obj:
      filesize = conn.storeFile(service_name, path+filename, file_obj)
    print 'upload finished'
    conn.close()

def delete_remote_file(username, password, my_name, remote_name, remote_ip, path, filename, service_name):
  conn = connect(username, password, my_name, remote_name, remote_ip)
  if conn:
    conn.deleteFiles(service_name, path+filename)
    print 'Remotefile ' + path + filename + ' deleted'
    conn.close()


username = 'admin'
password = 'admin-password'
my_name = 'pythonista'
remote_ip = '192.168.1.100'
remote_name = getBIOSName(remote_ip)
filename = 'guide.pdf'
path = '/share/'
service_name = getServiceName(username, password, my_name, remote_name, remote_ip)
pattern = '*.*'

#download(username, password, my_name, remote_name, remote_ip, path, filename, service_name)
#upload(username, password, my_name, remote_name, remote_ip, path, filename, service_name)
#delete_remote_file(username, password, my_name, remote_name, remote_ip, path, filename, service_name)

'''
#always trouble with listPath() ...
files = getRemoteDir(username, password, my_name, remote_name, remote_ip, path, pattern, service_name)
if files:
  for file in files:
    print file
'''
