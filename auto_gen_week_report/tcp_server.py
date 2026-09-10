# server.py
import socket
import subprocess
import json

HOST = "0.0.0.0"   # 监听本机所有网卡，允许windows连进来
PORT = 9988        # 随便选一个未占用端口，防火墙放行

def run_shell_command(cmd):
    """在ubuntu本地bash执行命令"""
    try:
        proc = subprocess.Popen(
            cmd,
            shell=True,
            executable="/bin/bash",   # 使用ubuntu bash执行
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = proc.communicate()
        return {
            "stdout": stdout,
            "stderr": stderr,
            "retcode": proc.returncode
        }
    except Exception as e:
        return {
            "stdout": "",
            "stderr": str(e),
            "retcode": -1
        }

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"Server start, listen port {PORT}")

    while True:
        conn, addr = s.accept()
        print(f"client connect: {addr}")
        with conn:
            data = conn.recv(4096)
            if not data:
                continue
            cmd = data.decode("utf-8")
            print(f"receive cmd: {cmd}")
            res = run_shell_command(cmd)
            # json打包结果回传
            reply = json.dumps(res)
            conn.sendall(reply.encode("utf-8"))

if __name__ == "__main__":
    main()
