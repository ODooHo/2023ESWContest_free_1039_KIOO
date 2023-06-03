import paramiko

def sftp_upload(hostname, username, private_key_path, local_file_path, remote_directory):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    private_key = paramiko.RSAKey.from_private_key_file(private_key_path)

    try:
        # SSH 서버에 연결
        client.connect(hostname=hostname, username=username, pkey=private_key)

        sftp = client.open_sftp()

        sftp.chdir(remote_directory)

        # 파일 전송
        sftp.put(local_file_path, local_file_path)

        print("파일 전송이 완료되었습니다.")

    except Exception as e:
        print("파일 전송 중 오류가 발생했습니다:", str(e))

    finally:
        # 연결 종료
        sftp.close()
        client.close()

# 사용 예시
hostname = "<EC2_IP_ADDRESS>"
username = "ubuntu"
private_key_path = "/Users/oduho/Desktop/WEB_server_key_KIOO/my-key.pem"
local_file_path = "/Users/oduho/Desktop/Graduation/event.mp4"
remote_directory = "/home/KIOO_Application/KIOO/src/main/resources/static/event"

sftp_upload(hostname, username, private_key_path, local_file_path, remote_directory)
