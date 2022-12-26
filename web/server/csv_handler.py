import paramiko

from os import environ

server_ip = environ['SERVER_IP']
user = environ['USERNAME']
key_directory = environ['KEY_DIR']

preferences_directory = environ['PREF_DIR']


def add_user(user_email, subreddit_prefs):
    # Uploads user information
    ssh = paramiko.SSHClient()

    ssh.load_system_host_keys()

    ssh.connect(server_ip, username=user, key_filename=key_directory)

    ssh.exec_command(f'echo "{ user_email + ";" + subreddit_prefs }" >> { preferences_directory }')

    ssh.close()


def unsubscribe_user(user_email):
    # Removes email from user_preferences file
    ssh = paramiko.SSHClient()

    ssh.load_system_host_keys()

    ssh.connect(server_ip, username=user, key_filename=key_directory)

    ssh.exec_command(f'sed -i "/{ user_email }/d" { preferences_directory }')

    ssh.close()
