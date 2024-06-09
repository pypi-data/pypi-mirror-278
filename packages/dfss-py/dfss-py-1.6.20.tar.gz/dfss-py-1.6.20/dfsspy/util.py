import paramiko
from progressbar import ProgressBar, Percentage, Bar, FileTransferSpeed, ETA
import socket
import time
from datetime import datetime
import stat
import base64
import os
import io
import sys
import threading
import platform
import subprocess
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

output_buffer = io.StringIO()
error_buffer = io.StringIO()


def lock_output(lock):
    if lock is True:
        sys.stdout = output_buffer
        sys.stderr = error_buffer
    else:
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__


def lock_output_clear():
    output_buffer.truncate(0)
    error_buffer.truncate(0)


def test_ping(host, port):
    try:
        start_time = time.time()
        with socket.create_connection((host, port), timeout=3) as connection:
            pass
        end_time = time.time()
        rtt = (end_time - start_time) * 1000
        return rtt
    except Exception as e:
        print("Error: ", str(e))
        return -1


def speed_sftp(host, port, username, password, timeout=2):
    download_data_ok = 0
    file_content = io.BytesIO()
    lock_output(True)
    start_time = 0
    end_time = 0

    def sftpget(x, y):
        lock_output(True)
        try:
            sftp.getfo(x, y)
        except Exception as e:
            pass
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(10)
            sock.connect((host, port))
            with paramiko.Transport(sock) as transport:
                transport.connect(username=username, password=password)
                sftp = paramiko.SFTPClient.from_transport(transport)
                th = threading.Thread(target=sftpget, args=(
                    ".sophgo_speed", file_content))
                start_time = time.time()
                th.start()
                th.join(timeout)
                end_time = time.time()
                sftp.close()
                transport.close()
                download_data_ok = 1
    except Exception as e:
        print('Error: ', e)
    finally:
        try:
            transport.close()
        except Exception as e:
            print('Error: ', e)
    lock_output(False)
    lock_output_clear()
    if download_data_ok == 1 and (end_time - start_time) != 0:
        data_size = (file_content.getbuffer().nbytes /
                     1024 / (end_time - start_time))
    else:
        data_size = 0
    return data_size


def is_remote_directory(remote_path, sftp):
    try:
        remote_attributes = sftp.stat(remote_path)
        return stat.S_ISDIR(remote_attributes.st_mode)
    except Exception as e:
        print('Failed to determine directory:', str(e))
        return False


def is_remote_reg(remote_path, sftp):
    try:
        remote_attributes = sftp.stat(remote_path)
        return stat.S_ISREG(remote_attributes.st_mode)
    except Exception as e:
        print('Failed to determine reg file:', str(e))
        return False


def is_sftp_supported(index, server, timeout=10):
    host, port, user, passwd, _ = server
    is_sftp = True
    if test_ping(host, port) == -1:
        return (index, False)
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            sock.connect((host, port))
            with paramiko.Transport(sock) as transport:
                transport.banner_timeout = timeout
                transport.connect(username=user, password=passwd)
                if user == None:
                    return (index, True)
                sftp = paramiko.SFTPClient.from_transport(transport)
                if is_remote_reg('.sophgo', sftp) is False:
                    is_sftp = False
                sftp.close()
                transport.close()
    except Exception as e:
        is_sftp = False
        print('is_sftp_supported Error:', e)
    finally:
        try:
            transport.close()
        except Exception as e:
            pass
    return (index, is_sftp)


def format_file_size(file_size_bytes):
    if file_size_bytes < 1024:
        return "{} B".format(file_size_bytes)
    elif file_size_bytes < 1024 ** 2:
        return "{:.2f} KB".format(file_size_bytes / 1024)
    elif file_size_bytes < 1024 ** 3:
        return "{:.2f} MB".format(file_size_bytes / (1024 ** 2))
    elif file_size_bytes < 1024 ** 4:
        return "{:.2f} GB".format(file_size_bytes / (1024 ** 3))
    else:
        return "{:.2f} TB".format(file_size_bytes / (1024 ** 4))


def get_server_info(username, isflag):
    server_info = {'hostname': None, 'port': None,
                   'username': None, 'password': None}
    flagstr = None
    if username.startswith('sophgo'):
        # HDK account
        server_list = [
            ("219.142.246.77", 18822, None, None, 0),
            ("172.29.128.15", 8822, None, None, 0),
        ]
        server_info['hostname'] = None
        server_info['port'] = None
        server_info['username'] = None
        for server in server_list:
            host, port, _, _, _ = server
            lock_output(True)
            (_, ret) = is_sftp_supported(0, server, 10)
            lock_output(False)
            if ret is True:
                server_info['hostname'] = host
                server_info['port'] = port
                server_info['username'] = username
                break
    else:
        # SDK account
        server_list = [
            ("172.26.175.10", 32022, 'oponIn', 'oponIn', 0),
            ("172.26.13.58", 12022, 'oponIn', 'oponIn', 0),
            ("172.26.166.66", 22022, 'oponIn', 'oponIn', 0),
            ("sophgobj.zztweb.top", 32022, 'open', 'open', 0),
            ("sophgohk.zztweb.top", 32022, 'open', 'open', 0),
        ]
        async_res = 0
        print("Finding available servers...")
        lock_output(True)
        with ThreadPoolExecutor(max_workers=10) as t:
            async_res = [t.submit(is_sftp_supported, index, server, 3)
                         for index, server in enumerate(server_list)]
        lock_output(False)
        lock_output_clear()
        for future in as_completed(async_res):
            (index, is_sftp) = future.result()
            if is_sftp is True:
                ip, port_to_check, user, passwd, _ = server_list[index]
                speed = speed_sftp(ip, port_to_check, user, passwd)
                print("connection scheme {} speed: {:.2f} kB/s".format(index, speed))
                server_list[index] = (ip, port_to_check, user, passwd, speed)
        sorted_server_list = sorted(
            server_list, key=lambda x: x[-1], reverse=True)
        host, port, user, passwd, speed = sorted_server_list[0]
        if speed != 0:
            server_info['hostname'] = host
            server_info['port'] = port
            server_info['username'] = user
            server_info['password'] = passwd
            if isflag:
                flagstr = get_flag_text(host, port, user, passwd)
    if server_info['hostname'] != None:
        print('using ip: ', server_info['hostname'])
    return server_info, flagstr


def get_filezilla_installation_path():
    if sys.platform.startswith('win'):
        import winreg
        reg_paths = [r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\FileZilla Client",
                     r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\FileZilla Client"]

        def winreg_find_path_form_uninstall(winreg_root, path):
            try:
                reg_key = winreg.OpenKey(winreg_root, path)
                install_path, _ = winreg.QueryValueEx(
                    reg_key, "InstallLocation")
                return install_path
            except Exception as e:
                return ""
        filezilla_path = ""
        for item in reg_paths:
            filezilla_path = winreg_find_path_form_uninstall(
                winreg.HKEY_LOCAL_MACHINE, item)
            if filezilla_path != "":
                fzpath = os.path.join(filezilla_path, 'filezilla.exe')
                return fzpath
        for item in reg_paths:
            filezilla_path = winreg_find_path_form_uninstall(
                winreg.HKEY_CURRENT_USER, item)
            if filezilla_path != "":
                fzpath = os.path.join(filezilla_path, 'filezilla.exe')
                return fzpath
        return ""
    elif sys.platform.startswith('linux'):
        try:
            process = subprocess.Popen(
                ["which", "filezilla"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            output, _ = process.communicate()
            filezilla_path = output.decode().strip()
            return filezilla_path
        except FileNotFoundError:
            return ""
    elif sys.platform.startswith('darwin'):
        try:
            process = subprocess.Popen(
                ["which", "filezilla"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            output, _ = process.communicate()
            filezilla_path = output.decode().strip()
            return filezilla_path
        except FileNotFoundError:
            return ""
    else:
        return ""


def get_winscp_installation_path():
    if sys.platform.startswith('win'):
        import winreg
        reg_paths = [r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\winscp3_is1",
                     r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\winscp3_is1"]

        def winreg_find_path_form_uninstall(winreg_root, path):
            try:
                reg_key = winreg.OpenKey(winreg_root, path)
                install_path, _ = winreg.QueryValueEx(
                    reg_key, "InstallLocation")
                return install_path
            except Exception as e:
                return ""
        winscp_path = ""
        for item in reg_paths:
            winscp_path = winreg_find_path_form_uninstall(
                winreg.HKEY_LOCAL_MACHINE, item)
            if winscp_path != "":
                fzpath = os.path.join(winscp_path, 'winscp.exe')
                return fzpath
        for item in reg_paths:
            winscp_path = winreg_find_path_form_uninstall(
                winreg.HKEY_CURRENT_USER, item)
            if winscp_path != "":
                fzpath = os.path.join(winscp_path, 'winscp.exe')
                return fzpath
        return ""
    else:
        return ""


def download_file_from_sophon_sftp(remote_path, local_path, isflag):
    server_info, flagstr = get_server_info('open', isflag)

    if server_info['hostname'] is None or server_info['port'] is None \
            or server_info['username'] is None or server_info['password'] is None:
        print("No available servers found.")
        return False

    if isflag:
        flags = json.loads(flagstr)
        if remote_path in flags.keys():
            remote_path = flags[remote_path]['filepath']
        else:
            print('flag "' + remote_path + '" does not exist!')
            return False

    try:
        transport = paramiko.Transport(
            (server_info['hostname'], server_info['port']))
        transport.connect(
            username=server_info['username'], password=server_info['password'])
        sftp = paramiko.SFTPClient.from_transport(transport)

        if is_remote_directory(remote_path, sftp) is True:
            print("cannot find aim")
            return False
        local_path = os.path.normpath(local_path)
        local_item = os.path.basename(remote_path)
        if os.path.isdir(local_path) is True:
            local_path = os.path.join(local_path, local_item)
        directory = os.path.dirname(local_path)
        if os.path.isdir(directory) is False:
            os.makedirs(directory)
        remote_file_size = sftp.stat(remote_path).st_size
        print('download file from', remote_path, '->', local_path, ', size:',
              format_file_size(remote_file_size), '...')
        widgets = [ETA(), ' | ', Percentage(), Bar(), FileTransferSpeed()]
        pbar = ProgressBar(widgets=widgets, maxval=remote_file_size).start()

        def progress_callback(x, y):
            pbar.update(x)
        sftp.get(remote_path, local_path, callback=progress_callback)
        pbar.finish()
        sftp.close()
        transport.close()
        return True
    except Exception as e:
        print('An error occurred in get file:', str(e))
        return False


def upload_file_to_sophon_sftp(remote_path, local_path):
    server_info, _ = get_server_info('open', isflag=False)
    server_info['username'] = 'customerUploadAccount'
    server_info['password'] = '1QQHJONFflnI2BLsxUvA'

    if server_info['hostname'] is None or server_info['port'] is None or server_info['username'] is None or server_info['password'] is None:
        print("No available servers found.")
        return False
    try:
        transport = paramiko.Transport(
            (server_info['hostname'], server_info['port']))
        transport.connect(
            username=server_info['username'], password=server_info['password'])
        sftp = paramiko.SFTPClient.from_transport(transport)
        local_path = os.path.normpath(local_path)
        if not os.path.isfile(local_path):
            print(local_path, 'is not a file.')
            exit(-1)
        remote_file_size = os.path.getsize(local_path)
        print('up file from', local_path, '-> open@sophgo.com:', remote_path, 'size:',
              format_file_size(remote_file_size), '...')
        widgets = [ETA(), ' | ', Percentage(), Bar(), FileTransferSpeed()]
        pbar = ProgressBar(widgets=widgets, maxval=remote_file_size).start()

        def progress_callback(x, y):
            pbar.update(x)
        decoded_bytes = base64.b64decode(remote_path)
        decoded_string = decoded_bytes.decode('utf-8')
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        remote_path = os.path.join(
            decoded_string, current_time + '_' + os.path.basename(local_path))
        sftp.put(local_path, remote_path,
                 callback=progress_callback, confirm=False)
        pbar.finish()
        sftp.close()
        transport.close()
        return True
    except Exception as e:
        print('An error occurred in up file:', str(e))
        return False


def sftp_login(username):
    print('Login sftp server by user: ', username)
    server_info, _ = get_server_info(username, isflag=False)
    if server_info['hostname'] is None or server_info['port'] is None \
            or server_info['username'] is None:
        print("No available servers found.")
        return False
    cmdstr = "echo"
    print('You can use this IP[{}] and port[{}] to login to the server through the SFTP client to download files.'.format(
        server_info['hostname'], server_info['port']))
    print('Currently trying to login using the sftp tool in the system ...')
    print("system platform: ", sys.platform)
    filezilla_path = get_filezilla_installation_path()
    print("filezilla_path ", filezilla_path)
    fzpath = os.path.join(filezilla_path)
    if os.path.exists(fzpath):
        print("find filezilla installed at:", fzpath, " start ...")
        cmdstr = '"{}"'.format(fzpath) + ' sftp://' + username + '@' + \
            server_info['hostname'] + ":" + str(server_info['port'])
    else:
        winscp_path = get_winscp_installation_path()
        print("winscp_path ", winscp_path)
        wcpath = os.path.join(winscp_path, 'winscp.exe')
        if os.path.exists(wcpath):
            print("find winscp installed at:", fzpath, " start ...")
            cmdstr = '"{}"'.format(wcpath) + ' sftp://' + username + '@' + \
                server_info['hostname'] + ":" + str(server_info['port'])
        else:
            print("sftp start ...")
            cmdstr = 'sftp -P ' + \
                str(server_info['port'])+' ' + \
                username + '@'+server_info['hostname']
            print("cmd: ", cmdstr)
    try:
        subprocess.run(cmdstr, check=True, shell=True)
    except Exception as e:
        try:
            cmdstr = 'sftp -P ' + \
                str(server_info['port'])+' ' + \
                username + '@'+server_info['hostname']
            subprocess.run(cmdstr, check=True, shell=True)
        except Exception as _:
            print(
                "Here's the SFTP server information above. Please use it to log in and download the files.")
            return False
    return True


def get_flag_text(host, port, username, password):
    download_data_ok = 0
    file_content = io.BytesIO()
    lock_output(True)

    def sftpget(x, y):
        lock_output(True)
        try:
            sftp.getfo(x, y)
        except Exception as e:
            pass
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(10)
            sock.connect((host, port))
            with paramiko.Transport(sock) as transport:
                transport.connect(username=username, password=password)
                sftp = paramiko.SFTPClient.from_transport(transport)
                th = threading.Thread(target=sftpget, args=(
                    ".dfss_flags", file_content))
                th.start()
                th.join()
                sftp.close()
                transport.close()
                download_data_ok = 1
    except Exception as e:
        print('get_flag_text Error:', e)
    finally:
        try:
            transport.close()
        except Exception as e:
            print('get_flag_text Error:', e)
    lock_output(False)
    lock_output_clear()
    if download_data_ok == 1:
        return file_content.getvalue().decode('utf-8')
    else:
        print("Error: cannot get flag file.")
        return None
