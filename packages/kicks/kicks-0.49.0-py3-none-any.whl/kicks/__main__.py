import requests
import time
import os
import subprocess

import rich
from rich.pretty import pprint as PP
from rich.console import Console
from rich.table import Table
CONSOLE = Console()


# curl -o p.exe -L https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe
# p.exe PrependPath=1 /passive
# cmd reopen
# pip install kicks
# python -m kicks


# written by robert degen
# 2015-2024
# notes:
# c:\cygwin64\bin\mintty.exe -w max -s 80x25  -e python -m dcx
# vs code / xdebug php extension + devsense php extension
# windows server 2022:
# https://www.microsoft.com/en-us/evalcenter/evaluate-windows-server-2022
# https://info.microsoft.com/ww-landing-windows-server-2022.html
# https://www.microsoft.com/de-de/evalcenter/download-windows-server-2022
# US ISO https://software-static.download.prss.microsoft.com/sg/download/888969d5-f34g-4e03-ac9d-1f9786c66749/SERVER_EVAL_x64FRE_en-us.iso


home = os.getenv("USERPROFILE")

OP=os.path.join(home, "_kicks")
OD=os.makedirs(OP, exist_ok=True)


def tryversion(pkg):
    import importlib.metadata
    try:
        res = pkg + '-' + importlib.metadata.version(pkg)
    except:
        res = pkg + '-dev'
    return res


def generic_pip_install(pkg_name, rcon):
    install_command = 'pip install "%s"' % pkg_name
    confirm = CONSOLE.input("run '%s' ? # 'y' to continue... " % install_command)
    if confirm == "y":
        subprocess.call(install_command, shell=True)


t = Table(title=tryversion("kicks"))
t.add_column("#")
t.add_column("File")
t.add_column("#")
t.add_column("File")
t.add_row("u", "update kicks", "id", "install dcx")
t.add_row("ud", "update dcx")
t.add_row("b", ".BAT->/AppData/Local/Microsoft/WindowsApps")
t.add_section()
t.add_row("1", "firefox windows 64", "3", "docker windows")
t.add_row("2", "chrome windows 64", "6", "virtualbox")
t.add_section()
t.add_row("4", "process explorer", "wp", "latest wordpress")
t.add_row("5", "vc_redist", "www", "WP->htdocs (req:wp)")
t.add_row("7", "grml small iso", "2k22", "windows server 2022 en iso")
t.add_row("8", "fpc win64 laz-3.4", "j", "jenkins")
t.add_row("jc", "jenkins configuration as code plugin")
t.add_row("9", "sublime", "npp", "notepad plus plus")
t.add_row("10", "emacs", "j21", "Java JDK v21 Oracle")
t.add_row("11", "cygwin", "j22", "Java JDK v22 Oracle")
t.add_row("12", "git", "is", "inno setup")
t.add_row("13", "xampp", "sshd1-6", "Set Up SSHd with key auth")
t.add_row("14", "visual studio code", "15", "LibreOffice")
t.add_section()
t.add_row("q", "QUIT")

while True:
    CONSOLE.print("")
    CONSOLE.print("")
    CONSOLE.print("")
    CONSOLE.print("")
    CONSOLE.print(t)

    x = CONSOLE.print()
    x = CONSOLE.input(' (q=QUIT) # ')



    if x == "u":
        while True:
            kicks_online = requests.get('https://pypi.org/pypi/kicks/json').json()["info"]["version"]
            lines = subprocess.check_output("pip freeze", shell=True, universal_newlines=True).strip().replace("\r", "").split("\n")
            kicks_local = [x for x in lines if x.find('kicks==') >= 0]
            CONSOLE.print("Latest ONLINE Version of kicks is %s" % kicks_online)
            CONSOLE.print("Local Version is %s" % str(kicks_local))
            update_loop_confirm = CONSOLE.input('u for UNINSTALL | i for INSTALL | q for QUIT | EMPTY for RE-CHECK # ')
            if update_loop_confirm == "u":
                uninstall_command = "pip uninstall -y kicks"
                subprocess.call(uninstall_command, shell=True)
            if update_loop_confirm == "i":
                install_command = 'pip install "kicks==%s"' % kicks_online
                update_loop_confirm = CONSOLE.input("run '%s' ? # " % install_command)
                subprocess.call(install_command, shell=True)
            if update_loop_confirm == "q":
                break

    if x == "id":
        generic_pip_install("dcx", CONSOLE)

    if x == "ud":
        while True:
            dcx_online = requests.get('https://pypi.org/pypi/dcx/json').json()["info"]["version"]
            lines = subprocess.check_output("pip freeze", shell=True, universal_newlines=True).strip().replace("\r", "").split("\n")
            dcx_local = [x for x in lines if x.find('dcx==') >= 0]
            CONSOLE.print("Latest ONLINE Version of dcx is %s" % dcx_online)
            CONSOLE.print("Local Version is %s" % str(dcx_local))
            update_loop_confirm = CONSOLE.input('u for UNINSTALL | i for INSTALL | q for QUIT | EMPTY for RE-CHECK # ')
            if update_loop_confirm == "u":
                uninstall_command = "pip uninstall -y dcx"
                subprocess.call(uninstall_command, shell=True)
            if update_loop_confirm == "i":
                install_command = 'pip install "dcx==%s"' % dcx_online
                update_loop_confirm = CONSOLE.input("run '%s' ? # " % install_command)
                subprocess.call(install_command, shell=True)
            if update_loop_confirm == "q":
                break


    if x == "b":
        bindir = os.path.join(home, 'AppData', 'Local', 'Microsoft', 'WindowsApps')
        
        #dcx / python: daisy chain xpath
        with open(os.path.join(bindir, 'dcx.bat'), 'w') as f:
            f.write('python -m dcx %*')

        #eppu
        with open(os.path.join(bindir, 'eppu.bat'), 'w') as f:
            f.write('python -m eppu %*')

        #dcxc / python: daisy chain xpath CHROME
        with open(os.path.join(bindir, 'dcxc.bat'), 'w') as f:
            f.write('python -m dcx --local-chrome %*')

        #dcxe / python: daisy chain xpath EDGE
        with open(os.path.join(bindir, 'dcxe.bat'), 'w') as f:
            f.write('python -m dcx --local-edge %*')

        #kicks / python: kickstarter for windows64
        with open(os.path.join(bindir, 'kicks.bat'), 'w') as f:
            f.write('python -m kicks')

        #ee / emacs
        with open(os.path.join(bindir, 'ee.bat'), 'w') as f:
            f.write('set SHELL=c:\\windows\\system32\\cmdproxy.exe\r\n%s -nw %%*' % (os.path.join(home, '_kicks', 'e', 'bin', 'emacs')))

        #e / sublime
        with open(os.path.join(bindir, 'e.bat'), 'w') as f:
            f.write('%s %%*' % (os.path.join(home, '_kicks', 'sub', 'sublime_text')))

        #cw / cygwin mintty
        with open(os.path.join(bindir, 'cw.bat'), 'w') as f:
            f.write('%s %%*' % (os.path.join('C:\\', 'Cygwin64', 'bin', 'mintty.exe')))

        #lbu / lazarus build
        with open(os.path.join(bindir, 'lbu.bat'), 'w') as f:
            f.write('%s %%*' % (os.path.join('C:\\', 'lazarus', 'lazbuild.exe')))

        #ff / firefox
        with open(os.path.join(bindir, 'ff.bat'), 'w') as f:
            f.write('"%s" %%*' % (os.path.join('C:\\', 'Program Files', 'Mozilla Firefox', 'firefox.exe')))

        #pe / process explorer
        with open(os.path.join(bindir, 'pe.bat'), 'w') as f:
            f.write('"%s" %%*' % (os.path.join(home, '_kicks', 'pe', 'procexp.exe')))

    if x == "1":
        outfile = os.path.join(OP, "firefox-setup.exe")
        cmd = 'curl -C - -L -o "%s" "https://download.mozilla.org/?product=firefox-latest-ssl&os=win64&lang=en-US"' % outfile
        subprocess.call(cmd, shell=True)
        run_confirm = CONSOLE.input('run it? type "run" to execute or anything else to exit # ')
        if run_confirm == "run":
            subprocess.call("%s /S" % outfile, shell=True)

    if x == "2":
        outfile = os.path.join(OP, "chrome.zip")
        outzipdir = os.path.join(OP, "chrome")
        cmd = 'curl -C - -L -o "%s" "https://dl.google.com/chrome/install/GoogleChromeEnterpriseBundle64.zip"' % outfile
        subprocess.call(cmd, shell=True)
        run_confirm = CONSOLE.input('run it? type "run" to execute or anything else to exit # ')
        if run_confirm == "run":
            subprocess.call("""powershell -Command Expand-Archive -Path '%s' -DestinationPath '%s'""" % (outfile, outzipdir), shell=True)
            subprocess.call("""%s""" % os.path.join(outzipdir, "Installers", "GoogleChromeStandaloneEnterprise64.msi"), shell=True)
            #subprocess.call("""explorer %s""" % (outzipdir), shell=True)

    if x == "j":
        #https://www.jenkins.io/download/
        outfile = os.path.join(OP, "jenkins.msi")
        cmd = 'curl -C - -L -o "%s" "https://get.jenkins.io/windows-stable/2.440.3/jenkins.msi"' % outfile
        subprocess.call(cmd, shell=True)
        run_confirm = CONSOLE.input('run it? type "run" to execute or anything else to exit # ')
        if run_confirm == "run":
            subprocess.call("""msiexec.exe /i %s /passive JENKINSDIR="C:\\Program Files\\Jenkins\\" PORTNUMBER=18080 JENKINS_ROOT="%%ProgramData%%\\Jenkins\\" JAVA_HOME="C:\\Program Files\\Java\\jdk-21\\" SERVICE_LOGON_TYPE=ServiceLocalSystem ALLUSERS=1""" % outfile, shell=True)

    if x == "jc":
        pass
        #https://plugins.jenkins.io/configuration-as-code/
        # outfile = os.path.join(OP, "jenkins.msi")
        # cmd = 'curl -C - -L -o "%s" "https://get.jenkins.io/windows-stable/2.440.3/jenkins.msi"' % outfile
        # subprocess.call(cmd, shell=True)
        # run_confirm = CONSOLE.input('run it? type "run" to execute or anything else to exit # ')
        # if run_confirm == "run":
        #     subprocess.call("""msiexec.exe /i %s /passive JENKINSDIR="C:\\Program Files\\Jenkins\\" PORTNUMBER=18080 JENKINS_ROOT="%%ProgramData%%\\Jenkins\\" JAVA_HOME="C:\\Program Files\\Java\\jdk-21\\" SERVICE_LOGON_TYPE=ServiceLocalSystem ALLUSERS=1""" % outfile, shell=True)

    if x == "j21":
        outfile = os.path.join(OP, "j21.msi")
        cmd = 'curl -C - -L -o "%s" "https://download.oracle.com/java/21/latest/jdk-21_windows-x64_bin.msi"' % outfile
        subprocess.call(cmd, shell=True)
        run_confirm = CONSOLE.input('run it? type "run" to execute or anything else to exit # ')
        if run_confirm == "run":
            subprocess.call("msiexec.exe /i %s /qn" % outfile, shell=True)

    if x == "j22":
        outfile = os.path.join(OP, "j22.msi")
        cmd = 'curl -C - -L -o "%s" "https://download.oracle.com/java/22/latest/jdk-22_windows-x64_bin.msi"' % outfile
        subprocess.call(cmd, shell=True)
        run_confirm = CONSOLE.input('run it? type "run" to execute or anything else to exit # ')
        if run_confirm == "run":
            subprocess.call("msiexec.exe /i %s /qn" % outfile, shell=True)

    if x == "wp":
        outfile = os.path.join(OP, "wp.zip")
        outzipdir = os.path.join(OP, "wp")
        cmd = 'curl -C - -L -o "%s" "https://wordpress.org/latest.zip"' % outfile
        subprocess.call(cmd, shell=True)
        run_confirm = CONSOLE.input('run it? type "run" to execute or anything else to exit # ')
        if run_confirm == "run":
            subprocess.call("""powershell -Command Expand-Archive -Path '%s' -DestinationPath '%s'""" % (outfile, outzipdir), shell=True)
            subprocess.call("""explorer %s""" % (outzipdir), shell=True)

    #todo:
    if x == "www":
        outfile = os.path.join(OP, "wp.zip")
        outzipdir = os.path.join(OP, "wp", "wordpress")
        htdir = os.path.join('C:\\', 'xampp', 'htdocs')
        subprocess.call("""robocopy %s %s /MIR""" % (outzipdir, htdir), shell=True)

    if x == "3":
        outfile = os.path.join(OP, "docker-setup.exe")
        cmd = 'curl -C - -L -o "%s" "https://desktop.docker.com/win/main/amd64/Docker%%20Desktop%%20Installer.exe"' % outfile
        subprocess.call(cmd, shell=True)
        run_confirm = CONSOLE.input('run it? type "run" to execute or anything else to exit # ')
        if run_confirm == "run":
            subprocess.call(outfile, shell=True)

    if x == "4":
        #https://learn.microsoft.com/en-us/sysinternals/downloads/process-explorer
        outfile = os.path.join(OP, "pe.zip")
        outzipdir = os.path.join(OP, "pe")
        cmd = 'curl -C - -L -o "%s" "https://download.sysinternals.com/files/ProcessExplorer.zip"' % outfile
        subprocess.call(cmd, shell=True)
        run_confirm = CONSOLE.input('run it? type "run" to execute or anything else to exit # ')
        if run_confirm == "run":
            subprocess.call("""powershell -Command Expand-Archive -Path '%s' -DestinationPath '%s'""" % (outfile, outzipdir), shell=True)
            subprocess.call("""explorer %s""" % (outzipdir), shell=True)

    if x == "5":
        outfile = os.path.join(OP, "vc_redist.exe")
        cmd = 'curl -C - -L -o "%s" "https://aka.ms/vs/17/release/vc_redist.x64.exe"' % outfile
        subprocess.call(cmd, shell=True)
        run_confirm = CONSOLE.input('run it? type "run" to execute or anything else to exit # ')
        if run_confirm == "run":
            subprocess.call("%s /install /passive" % outfile, shell=True)

    if x == "6":
        #https://www.virtualbox.org/wiki/Downloads
        outfile = os.path.join(OP, "vbox-setup.exe")
        cmd = 'curl -C - -L -o "%s" "https://download.virtualbox.org/virtualbox/7.0.14/VirtualBox-7.0.14-161095-Win.exe"' % outfile
        subprocess.call(cmd, shell=True)
        run_confirm = CONSOLE.input('run it? type "run" to execute or anything else to exit # ')
        if run_confirm == "run":
            subprocess.call(outfile, shell=True)

    if x == "7":
        #https://download.grml.org/grml64-small_2024.02.iso
        outfile = os.path.join(OP, "grml.iso")
        cmd = 'curl -C - -L -o "%s" "https://download.grml.org/grml64-small_2024.02.iso"' % outfile
        subprocess.call(cmd, shell=True)
        subprocess.call("""explorer %s""" % (OP), shell=True)

    if x == "2k22":
        outfile = os.path.join(OP, "grml.iso")
        cmd = 'curl -C - -L -o "%s" "https://go.microsoft.com/fwlink/p/?LinkID=2195280&clcid=0x409&culture=en-us&country=US"' % outfile
        subprocess.call(cmd, shell=True)
        subprocess.call("""explorer %s""" % (OP), shell=True)

    if x == "8":
        #https://sourceforge.net/projects/lazarus/files/
        outfile = os.path.join(OP, "laz-setup.exe")
        cmd_3_2 = 'curl -C - -L -o "%s" "https://deac-riga.dl.sourceforge.net/project/lazarus/Lazarus%%20Windows%%2064%%20bits/Lazarus%%203.2/lazarus-3.2-fpc-3.2.2-win64.exe"' % outfile
        cmd = 'curl -C - -L -o "%s" "https://kumisystems.dl.sourceforge.net/project/lazarus/Lazarus%%20Windows%%2064%%20bits/Lazarus%%203.4/lazarus-3.4-fpc-3.2.2-win64.exe"' % outfile
        subprocess.call(cmd, shell=True)
        run_confirm = CONSOLE.input('run it? type "run" to execute or anything else to exit # ')
        if run_confirm == "run":
            subprocess.call(outfile, shell=True)

    if x == "9":
        outfile = os.path.join(OP, "sub.zip")
        outzipdir = os.path.join(OP, "sub")
        cmd = 'curl -C - -L -o "%s" "https://download.sublimetext.com/sublime_text_build_4169_x64.zip"' % outfile
        subprocess.call(cmd, shell=True)
        run_confirm = CONSOLE.input('run it? type "run" to execute or anything else to exit # ')
        if run_confirm == "run":
            subprocess.call("""powershell -Command Expand-Archive -Path '%s' -DestinationPath '%s'""" % (outfile, outzipdir), shell=True)
            subprocess.call("""explorer %s""" % (outzipdir), shell=True)

    if x == "10":
        outfile = os.path.join(OP, "e.zip")
        outzipdir = os.path.join(OP, "e")
        cmd = 'curl -C - -L -o "%s" "http://ftp.gnu.org/gnu/emacs/windows/emacs-29/emacs-29.2_1.zip"' % outfile
        subprocess.call(cmd, shell=True)
        run_confirm = CONSOLE.input('run it? type "run" to execute or anything else to exit # ')
        if run_confirm == "run":
            subprocess.call("""powershell -Command Expand-Archive -Path '%s' -DestinationPath '%s'""" % (outfile, outzipdir), shell=True)
            subprocess.call("""explorer %s""" % (outzipdir), shell=True)

    if x == "11":
        outfile = os.path.join(OP, "cygwinsetup.exe")
        cmd = 'curl -C - -L -o "%s" "https://www.cygwin.com/setup-x86_64.exe"' % outfile
        subprocess.call(cmd, shell=True)
        run_confirm = CONSOLE.input('run it? type "run" to execute or anything else to exit # ')
        if run_confirm == "run":
            cy_dir=os.makedirs(os.path.join(home, '_kicks', 'cy'), exist_ok=True)
            subprocess.call("""%s -l %s -P %s""" % (outfile, cy_dir, "nc,mc,ncdu"), shell=True)

    if x == "12":
        outfile = os.path.join(OP, "gitsetup.exe")
        cmd = 'curl -C - -L -o "%s" "https://github.com/git-for-windows/git/releases/download/v2.44.0.windows.1/Git-2.44.0-64-bit.exe"' % outfile
        subprocess.call(cmd, shell=True)
        run_confirm = CONSOLE.input('run it? type "run" to execute or anything else to exit # ')
        if run_confirm == "run":
            subprocess.call(outfile, shell=True)

    if x == "is":
        outfile = os.path.join(OP, "innosetup.exe")
        cmd = 'curl -C - -L -o "%s" "https://jrsoftware.org/download.php/is.exe?site=2"' % outfile
        subprocess.call(cmd, shell=True)
        run_confirm = CONSOLE.input('run it? type "run" to execute or anything else to exit # ')
        if run_confirm == "run":
            subprocess.call(outfile, shell=True)

    if x == "npp":
        outfile = os.path.join(OP, "nppsetup.exe")
        cmd = 'curl -C - -L -o "%s" "https://github.com/notepad-plus-plus/notepad-plus-plus/releases/download/v8.6.4/npp.8.6.4.Installer.x64.exe"' % outfile
        subprocess.call(cmd, shell=True)
        run_confirm = CONSOLE.input('run it? type "run" to execute or anything else to exit # ')
        if run_confirm == "run":
            subprocess.call(outfile, shell=True)

    if x == "13":
        outfile = os.path.join(OP, "xamppsetup.exe")
        cmd = 'curl -C - -L -o "%s" "https://sourceforge.net/projects/xampp/files/XAMPP%%20Windows/8.2.12/xampp-windows-x64-8.2.12-0-VS16-installer.exe"' % outfile
        subprocess.call(cmd, shell=True)
        run_confirm = CONSOLE.input('run it? type "run" to execute or anything else to exit # ')
        if run_confirm == "run":
            subprocess.call(outfile, shell=True)

    if x == "14":
        outfile = os.path.join(OP, "vsc.exe")
        cmd = 'curl -C - -L -o "%s" "https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-user"' % outfile
        subprocess.call(cmd, shell=True)
        run_confirm = CONSOLE.input('run it? type "run" to execute or anything else to exit # ')
        if run_confirm == "run":
            subprocess.call(outfile, shell=True)

    if x == "15":
        #https://www.libreoffice.org/download/download-libreoffice/?type=win-x86_64&version=7.6.5&lang=en-US
        outfile = os.path.join(OP, "libre765.msi")
        cmd = 'curl -C - -L -o "%s" "https://ftp.fau.de/tdf/libreoffice/stable/7.6.5/win/x86_64/LibreOffice_7.6.5_Win_x86-64.msi"' % outfile
        subprocess.call(cmd, shell=True)
        run_confirm = CONSOLE.input('run it? type "run" to execute or anything else to exit # ')
        if run_confirm == "run":
            subprocess.call("%s /passive /qr" % outfile, shell=True)

    if x == "sshd1":
        #https://learn.microsoft.com/en-us/windows-server/administration/openssh/openssh_install_firstuse?tabs=powershell
        # powershell -Command "Get-WindowsCapability -Online | Where-Object Name -like 'OpenSSH*'"
        # powershell -Command "Get-WindowsCapability -Online -verb runas | Where-Object Name -like 'OpenSSH*'"
        # powershell -Command "Start-Process -FilePath powershell -ArgumentList '-Command Get-WindowsCapability -Online | Where-Object Name -like OpenSSH*'" -verb RunAs
        
        # win11.sshd.install.1
        # powershell -Command "Start-Process -FilePath powershell -ArgumentList '-Command Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0'" -verb RunAs
        
        cmd="""powershell -Command Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0"""
        subprocess.call(cmd, shell=True)
        cmd="""powershell -Command Start-Service sshd"""
        subprocess.call(cmd, shell=True)
        cmd="""powershell -Command Stop-Service sshd"""
        subprocess.call(cmd, shell=True)

    if x == "sshd2":
        #https://learn.microsoft.com/en-us/windows-server/administration/openssh/openssh_install_firstuse?tabs=powershell

        # win11.sshd.install.2
        # powershell -Command "Start-Process -FilePath notepad -ArgumentList 'C:/ProgramData/ssh/administrators_authorized_keys'" -verb RunAs

        cmd="""notepad C:\\ProgramData\\ssh\\administrators_authorized_keys"""
        subprocess.call(cmd, shell=True)

    if x == "sshd3":
        #https://learn.microsoft.com/en-us/windows-server/administration/openssh/openssh_install_firstuse?tabs=powershell
        cmd="""move C:\\ProgramData\\ssh\\administrators_authorized_keys.txt C:\\ProgramData\\ssh\\administrators_authorized_keys"""
        subprocess.call(cmd, shell=True)

    if x == "sshd4":
        #https://learn.microsoft.com/en-us/windows-server/administration/openssh/openssh_install_firstuse?tabs=powershell

        # win11.sshd.install.4
        # powershell -Command "Start-Process -FilePath icacls.exe -ArgumentList 'C:/ProgramData/ssh/administrators_authorized_keys /inheritance:r /grant Administrators:F /grant SYSTEM:F'" -verb RunAs

        
        cmd="""icacls.exe "C:\\ProgramData\\ssh\\administrators_authorized_keys" /inheritance:r /grant "Administrators:F" /grant "SYSTEM:F" """
        subprocess.call(cmd, shell=True)

    if x == "sshd5":

        # win11.sshd.install.3
        # powershell -Command "Start-Process -FilePath powershell -ArgumentList 'Start-Service sshd'" -verb RunAs

        #https://learn.microsoft.com/en-us/windows-server/administration/openssh/openssh_install_firstuse?tabs=powershell
        cmd="""powershell -Command Start-Service sshd"""
        subprocess.call(cmd, shell=True)

    if x == "sshd6":

        # win11.sshd.install.4
        # powershell -Command "Start-Process -FilePath powershell -ArgumentList 'Set-Service -Name sshd -StartupType Automatic'" -verb RunAs

        #https://learn.microsoft.com/en-us/windows-server/administration/openssh/openssh_install_firstuse?tabs=powershell
        cmd="""powershell -Command Set-Service -Name sshd -StartupType 'Automatic'"""
        subprocess.call(cmd, shell=True)

    if x == "q":
        break
