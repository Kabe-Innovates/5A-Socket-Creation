import socket

def send_request(host, port, request):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(request.encode())
        response = s.recv(4096).decode()
    return response

def upload_file(host, port, filename):
    with open(filename, 'rb') as file:
        file_data = file.read()
        content_length = len(file_data)
        request = f"POST /upload HTTP/1.1\r\nHost: {host}\r\nContent-Length: {content_length}\r\n\r\n"
        request += file_data.decode()
        response = send_request(host, port, request)
    return response

def download_file(host, port, filename):
    request = f"GET /{filename} HTTP/1.1\r\nHost: {host}\r\n\r\n"
    response = send_request(host, port, request)
    # Assuming the response contains the file content after the headers
    file_content = response.split('\r\n\r\n', 1)[1]
    with open(filename, 'wb') as file:
        file.write(file_content.encode())

if __name__ == "__main__":
    host = '93.184.216.34'
    port = 80

    # Upload file
    upload_response = upload_file(host, port, 'example.txt')
    print("Upload response:", upload_response)

    # Download file
    download_file(host, port, 'example.txt')
    print("File downloaded successfully.")
