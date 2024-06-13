import os
import subprocess
import platform
import psutil

class DrivePy:
    @staticmethod
    def list_usb_drives():
        system = platform.system()
        if system == 'Linux':
            try:
                import pyudev
                context = pyudev.Context()
                drives = []
                for device in context.list_devices(subsystem='block', DEVTYPE='disk'):
                    if 'ID_BUS' in device and device['ID_BUS'] == 'usb':
                        drives.append(device.device_node)
                return drives
            except ImportError:
                return []
        elif system == 'Windows':
            drives = []
            partitions = psutil.disk_partitions()
            for partition in partitions:
                if 'removable' in partition.opts:
                    drives.append(partition.device)
            return drives
        elif system == 'Darwin':  # macOS
            try:
                drives = []
                disks = subprocess.check_output(['diskutil', 'list']).decode('utf-8').split('\n')
                for disk in disks:
                    if '/dev/disk' in disk and 'external' in disk.lower():
                        drives.append(disk.split()[0])
                return drives
            except subprocess.CalledProcessError:
                return []
        else:
            raise NotImplementedError(f"Unsupported platform: {system}")

    @staticmethod
    def unmount_drive(drive):
        system = platform.system()
        if system == 'Linux':
            try:
                subprocess.run(['umount', drive], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except subprocess.CalledProcessError:
                pass
        elif system == 'Windows':
            try:
                diskpart_script = f"""
                select volume {drive.strip(':')}
                remove
                """
                subprocess.run(['diskpart', '/s', diskpart_script.strip()], shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except subprocess.CalledProcessError:
                pass
        elif system == 'Darwin':  # macOS
            try:
                subprocess.run(['diskutil', 'unmountDisk', drive], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except subprocess.CalledProcessError:
                pass

    @staticmethod
    def flash_iso_to_usb(iso_path, usb_drive):
        system = platform.system()
        if system == 'Linux' or system == 'Darwin':
            try:
                subprocess.run(['dd', f'if={iso_path}', f'of={usb_drive}', 'bs=4M', 'status=progress', 'conv=fdatasync'], check=True)
                return True
            except subprocess.CalledProcessError:
                return False
        elif system == 'Windows':
            try:
                subprocess.run(['cmd', '/c', f'xcopy /s /e {iso_path} {usb_drive}'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return True
            except subprocess.CalledProcessError:
                return False

    @staticmethod
    def flash_iso(iso_path, usb_drive):
        DrivePy.unmount_drive(usb_drive)
        return DrivePy.flash_iso_to_usb(iso_path, usb_drive)

    @staticmethod
    def make_bootable(usb_drive):
        system = platform.system()
        if system == 'Linux':
            try:
                subprocess.run(['sudo', 'syslinux', '-i', usb_drive], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return True
            except subprocess.CalledProcessError:
                return False
        elif system == 'Windows':
            try:
                diskpart_script = f"""
                select disk {usb_drive.strip(':')}
                clean
                create partition primary
                select partition 1
                active
                format fs=fat32 quick
                assign
                """
                subprocess.run(['diskpart', '/s', diskpart_script.strip()], shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return True
            except subprocess.CalledProcessError:
                return False
        elif system == 'Darwin':  # macOS
            try:
                efi_dir = os.path.join(usb_drive, 'EFI', 'BOOT')
                os.makedirs(efi_dir, exist_ok=True)
                with open(os.path.join(efi_dir, 'BOOTX64.efi'), 'w') as f:
                    f.write("This is a dummy EFI boot loader file.")
                return True
            except OSError:
                return False

    @staticmethod
    def is_bootable(usb_drive):
        system = platform.system()
        if system == 'Linux':
            try:
                output = subprocess.check_output(['file', '-sL', usb_drive]).decode('utf-8')
                return 'boot sector' in output.lower()
            except subprocess.CalledProcessError:
                return False
        elif system == 'Windows':
            boot_files = ['bootmgr', 'boot.ini', 'boot', 'ntldr']
            return all(os.path.exists(os.path.join(usb_drive, file)) for file in boot_files)
        elif system == 'Darwin':
            efi_boot_files = ['EFI', 'boot']
            return all(os.path.exists(os.path.join(usb_drive, file)) for file in efi_boot_files)
        else:
            return False

    @staticmethod
    def verify_bootability(usb_drive):
        return DrivePy.is_bootable(usb_drive)

    @staticmethod
    def main():
        return DrivePy.list_usb_drives()
                
