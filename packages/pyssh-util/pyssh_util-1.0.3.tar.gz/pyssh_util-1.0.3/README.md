<h1 align="center">pyssh_util</h1>

- ssh_util.py

ssh到服务器的各种封装方法，使用示例：

```python
host = ''
password = ''

ssh = SSHClient(host, password)

# 执行单行命令
result_single = ssh.execute_command('ls -l')

# 执行多行命令
commands = ['pwd', 'whoami']
result_multiple = ssh.execute_commands(commands)

# 上传并执行脚本
local_script_path = 'C:\\Users\\buyfakett\\Desktop\\1.sh'
remote_script_path = '/root/1.sh'
result_script = ssh.upload_and_execute_script(local_script_path, remote_script_path)

ssh.close()
```
