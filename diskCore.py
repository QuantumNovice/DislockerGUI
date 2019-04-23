import os, subprocess, re

DECRYPT_PATH = '/media/bitlocker'
MOUNT_PATH = '/media/mount'
REQUIREMENTS = ['libfuse-dev', 'dislocker']

def isInstalled(pkg, debug=False):
    output = str(subprocess.check_output(['apt', 'search', pkg]))
    if debug:
        print(output)
    if pkg in output:
        return True
    return False

def listDisk():
    output = str(subprocess.check_output(['sudo', 'fdisk', '-l']))
    disks = re.findall(' /dev/(.+?): ', output)
    return disks


class DislockerDecrypt:
    def __init__(self):
        self.RUN = True
        if os.system('sudo -i') != 0:
            self.RUN = False
        DECRYPT_FLAG = os.path.exists(DECRYPT_PATH)
        MOUNT_FLAG = os.path.exists(MOUNT_PATH)
        print('DECRYPT_FLAG:',DECRYPT_FLAG)
        print('MOUNT_FLAG:', MOUNT_FLAG)

        try:
            if not DECRYPT_FLAG:
                os.mkdir(DECRYPT_PATH)
            if not MOUNT_FLAG:
                os.mkdir(MOUNT_PATH)
        except PermissionError:
            self.RUN = False
            print('Run as root!')
            

        for i in REQUIREMENTS:
            if not isInstalled(i):
                print('Try sudo apt-get install libfuse-dev dislocker')
                self.RUN = False
        if not self.RUN:
             raise IOError("Root required. Try sudo python3 dislocker.py")

    def decrypt(self, disk, recovery_pass=None, user_pass=None):
        if recovery_pass != None:
            os.system('sudo dislocker -r -V /dev/'+ disk +' -p'+recovery_pass+' -- '+ DECRYPT_PATH) # recovery pass
        if user_pass != None:
            os.system('sudo dislocker -r -V /dev/'+disk+' -u'+user_pass+' -- '+MOUNT_PATH) # Userpass
        os.system('cd '+DECRYPT_PATH)
        try:
            os.system('mount -r -o loop dislocker-file '+MOUNT_PATH)
        except:
            os.system('sudo dislocker -r -V /dev/sdaX -u -- -o nonempty /media/mount') # Remount

