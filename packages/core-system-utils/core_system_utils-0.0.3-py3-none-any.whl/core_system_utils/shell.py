import subprocess

def shell(string):
    return subprocess.run(string, capture_output=True, shell=True)
    
def shell_extract(string, _return=True):
    ret = shell(string)
    
    if _return:
        return ret.stdout.decode().strip()
        
if __name__ == "__main__":
    base_command = 'ls -l /etc/shadow | cut -d " " -f'
    command = f'{base_command} 1 | cut -c5-6'
    group_name_command = f'{base_command} 4'

    result, group = shell_extract(command), shell_extract(group_name_command)

    if 'r' in result:
        print(f'The {group} group has readable access to the shadow file!')
    if 'w' in result:
        print(f'The {group} group has writable access to the shadow file!')
        
    print(f'All others has the following access: {shell_extract(command[:-3] + "8-9")}')
