Access Samba/Windows-Shares<br/>
=========================<br/>
<br/>
Small example how to upload, download, delete files (use at your own risk). This worked with my mini WIFI-Router USB-Stick-Share.<br/>
<br/>
First you need to download these two python modules: pysmb-1.1.13 and pyasn1-0.1.7<br/>
Then extract \pysmb-1.1.13\python2\smb, \pysmb-1.1.13\python2\nmb and \pyasn1-0.1.7\pyasn1\ to the side-packages directory.<br/>
After adjusting the parameters (username, password, ...) you might check for NetBIOS support.<br/>
=> Port (139 = NetBIOS), is_direct_tcp=False and SUPPORT_SMB2=True.<br/>
