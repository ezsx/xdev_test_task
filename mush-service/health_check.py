import http.client

conn = http.client.HTTPConnection("localhost", 8000)
conn.request("GET", "/health")
res = conn.getresponse()
exit(1) if res.status != 200 else exit(0)
