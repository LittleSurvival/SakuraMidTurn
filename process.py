import subprocess

if __name__ == '__main__':
    processes = []
    for i in range(2, 5):
        host_ip = f'127.0.0.{i}'
        p = subprocess.Popen(['python', 'main.py', host_ip])
        processes.append(p)
        print(f'Started server on {host_ip}:8000')

    try:
        for p in processes:
            p.wait()
    except KeyboardInterrupt:
        print("Shutting down servers...")
        for p in processes:
            p.terminate()
        for p in processes:
            p.wait()
