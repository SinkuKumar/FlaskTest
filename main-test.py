import requests
import threading

def send_request(endpoint):
    url = f"http://127.0.0.1:9000/{endpoint}"
    response = requests.get(url)
    print(f"Response from {endpoint}: {response.json()}")

endpoints = ["cpu-load", "memory-load", "db-load"]
endpoints = ["db-load",]

threads = []
for _ in range(10):  # 10 requests per endpoint
    for endpoint in endpoints:
        t = threading.Thread(target=send_request, args=(endpoint,))
        t.start()
        threads.append(t)

for t in threads:
    t.join()
