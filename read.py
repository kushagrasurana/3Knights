import subprocess

proc = subprocess.Popen(['python','out.py'],stdout=subprocess.PIPE) # for python
#proc = subprocess.Popen('a.exe',stdout=subprocess.PIPE) # for c / c++ compiled 
#proc = subprocess.Popen('java','-jar','out.jar',stdout=subprocess.PIPE) # for java
stddata=proc.communicate()
move=stddata[0].decode('ascii')
print(move)