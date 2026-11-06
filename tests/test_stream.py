
import requests
import time

url = "http://127.0.0.1:8000/ask/stream"

payload = {
    "question": "Explain the three Vs of Big Data. Also explain the architecture of HDFS, including the roles of NameNode and DataNodes."
}

print("Sending request...\n")

start_time = time.time()

response = requests.post(
    url,
    json=payload,
    stream=True
)

print("Status Code:", response.status_code)
print("\nStreaming response:\n")

for line in response.iter_lines(decode_unicode=True):

    if line:
        elapsed = time.time() - start_time

        print(f"[{elapsed:.2f}s] {line}", flush=True)

print("\nStreaming completed!")
