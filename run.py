import subprocess
from multiprocessing import Process

def run_uvicorn():
    subprocess.run(['uvicorn', 'main:app', '--host', '0.0.0.0', '--port', '8036', '--reload'])

def run_http_server():
    subprocess.run(['python', '-m', 'http.server', '--bind', 'localhost', '8048', '-d', 'frontend'])

if __name__ == '__main__':
    uvicorn_process = Process(target=run_uvicorn)
    http_server_process = Process(target=run_http_server)

    uvicorn_process.start()
    http_server_process.start()

    uvicorn_process.join()
    http_server_process.join()


# uvicorn main:app --host 0.0.0.0 --port 8037
# python -m http.server --bind localhost 8048 