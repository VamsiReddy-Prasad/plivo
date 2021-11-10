###########################################################################
# Name          : PrintCallDetailsSIPP.py
# Decription    :
# Version       : 1.0
###########################################################################


import paramiko,time, threading,re





class PrintCallDetailsSIPP:
    def __init__(self):
        pass

    def loginSession(self,hostName,userName,password,port,prompt,promptCount):
        """
        Description  : Login to a SSH session
        Parameters:
            hostName : Hostname of SSH session
            userName : Username of SSH session
            password : Password of SSH session
            port     : Port number of SSH session
            prompt   : Name of the Prompt
        Return Value:
            ssh : Handle name of the session in the case of successful login
            False: Returns False in the case of any failures in logging.
        """
        tries = 2
        flag=True
        count=0
        for i in range(tries+1):
            try:
                try:
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(hostName, port, userName, password,banner_timeout=200)
                except paramiko.ssh_exception.AuthenticationException:
                    key = paramiko.RSAKey.from_private_key_file("cloud_ats.key")
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    print("connecting")
                    ssh.connect(hostname=hostName, username=userName, pkey=key, port=port,banner_timeout=200)
                    print("connected")

                shell = ssh.invoke_shell()
                resp = shell.recv(9999)
                while(count<int(promptCount)):
                    m = re.search(prompt,str(resp))
                    if m:
                        break
                    else:
                        time.sleep(1)
                        count=count+1
                        flag=False

                print ("SSH session opened for "+hostName)
                return ssh
            except(Exception) as e:
                print(e)
                return False



    def executeCLIShell(self,sshHandle,commands,logFile):
        """
        Description:   Execute any command on SSH session.
        Parameters:
            sshHandle : sshHandle which is opened to execute a command
        Return Value:
            commandResponse : The output of the command response for any command.
            False: Returns False in the case of any failures in executing a command.
        """
        print('inside execute',commands)
        try:
            out =[]
            for command in commands:
                stdin,stdout,stderr =  sshHandle.exec_command(command +' > /tmp/'+logFile+' 2>&1 & echo $!;')
                procid = stdout.read().decode().strip()
                print("Waiting for process", procid)
                while True:
                    print(f"Waiting for process {procid} to complete")
                    stdin,stdout,stderr = sshHandle.exec_command('ps -p'+procid)
                    if len(stdout.readlines()) < 2:
                        print(f"Command execution for process {procid} Completed.")
                        break
                    time.sleep(10)
                    print("sleep for 10s")

                stdin,stdout,stderr = sshHandle.exec_command('cat /tmp/'+logFile)

                out.append(stdout.read().decode("utf-8").split('\n'))
            out = [val for sublist in out for val in sublist]
            sshHandle.exec_command('rm -rf /tmp/' + logFile)
            return out

        except(Exception) as e:
            print ("Unable to execute command",e)
            return False


    def closeSession(self,sshHandle):
        """
        Description:   Closes a SSH session
        Parameters:
            sshHandle : sshHandle which is opened.
        Return Value:
            True : Returns True if session is closed successfully.
            False: Returns False if session is not closed successfully.
        """
        try:
            sshHandle.close()
            print ("SSH session is closed")
            return True
        except(Exception) as e:
            print("Unable to close session, Error: ",e)
            return False


if __name__ == '__main__':
    PrintCallDetailsSIPPObj=PrintCallDetailsSIPP()
    start = time.time()
    print("Start Time =", start)
    ssh_handle_client = PrintCallDetailsSIPPObj.loginSession('10.54.81.66', 'vkonreddi', 'Jun_2019', 22, '', 2)
    ssh_handle_server = PrintCallDetailsSIPPObj.loginSession('10.54.81.66', 'vkonreddi', 'Jun_2019', 22, '', 2)
    ssh_handle=PrintCallDetailsSIPPObj.loginSession('10.54.81.66', 'vkonreddi', 'Jun_2019', 22, '', 2)
    commandToRunShellScript=['cd tc && bash vamsi.sh uac_messages.log uas_messages.log uas_screen_file /home/vkonreddi/tc/']
    if ssh_handle_client and ssh_handle_server:
        commandListClient = ['cd tc && /ats/bin/sipp -sf /home/vkonreddi/tc/uac.xml -i 10.54.81.66 -p 15070  -inf /home/vkonreddi/tc/call.csv 10.54.81.66:15088 -m 1  -trace_msg -message_file /home/vkonreddi/tc/uac_messages.log']
        commandListServer=['cd tc && /ats/bin/sipp -sf /home/vkonreddi/tc/uas.xml -i 10.54.81.66 -p 15088  -inf /home/vkonreddi/tc/call.csv 10.54.81.66:15070 -m 1  -screen_file /home/vkonreddi/tc/uas_screen_file -trace_screen -trace_msg -message_file /home/vkonreddi/tc/uas_messages.log']
        t1=threading.Thread(target=PrintCallDetailsSIPPObj.executeCLIShell, args=(ssh_handle_server,commandListServer, "server.log"))        
        t2=threading.Thread(target=PrintCallDetailsSIPPObj.executeCLIShell, args=(ssh_handle_client,commandListClient, "client.log"))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        PrintCallDetailsSIPPObj.closeSession(ssh_handle_server)
        PrintCallDetailsSIPPObj.closeSession(ssh_handle_client)

    output=PrintCallDetailsSIPPObj.executeCLIShell(ssh_handle, commandToRunShellScript,'finaloutput')

    print("call details:",output)
    PrintCallDetailsSIPPObj.closeSession(ssh_handle)


