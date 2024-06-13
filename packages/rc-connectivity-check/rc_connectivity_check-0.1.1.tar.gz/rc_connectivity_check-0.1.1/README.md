# RC Connectivity Check tools

This PIP package measures the latencies to various hosts and provides statistics such as failure rates and latencies.

## Installation

```bash
pip install rc_connectivity_check
```

## Usage
Just run `rc-connectivity-check`

Example output:
```
$ rc-connectivity-check
Finding client Public IP...
Client Public IP: 1.2.3.4

Resolving hostnames...
* www.revenuecat.com: Resolved ok
  - 18.154.22.26
  - 18.154.22.30
  - 18.154.22.73
  - 18.154.22.107
* app.revenuecat.com: Resolved ok
  - 108.157.109.6
  - 108.157.109.103
  - 108.157.109.77
  - 108.157.109.82
* api.revenuecat.com: Resolved ok
  - 3.214.67.56
  - 54.163.59.173
  - 3.223.26.133
  - 3.208.129.96
  - 52.22.245.243
  - 34.196.186.56

Connectivity check...

Results for app.revenuecat.com:
  - 108.157.109.6: OK
    Latencies (min/max/avg): 35.2ms / 39.7ms / 35.2ms
  - 108.157.109.77: OK
    Latencies (min/max/avg): 35.2ms / 40.7ms / 35.2ms
  - 108.157.109.82: OK
    Latencies (min/max/avg): 35.3ms / 44.1ms / 35.3ms
  - 108.157.109.103: OK
    Latencies (min/max/avg): 36.0ms / 44.2ms / 36.0ms

Results for www.revenuecat.com:
  - 18.154.22.30: OK
    Latencies (min/max/avg): 48.4ms / 169.4ms / 48.4ms
  - 18.154.22.107: OK
    Latencies (min/max/avg): 50.0ms / 168.4ms / 50.0ms
  - 18.154.22.73: OK
    Latencies (min/max/avg): 50.9ms / 171.2ms / 50.9ms
  - 18.154.22.26: OK
    Latencies (min/max/avg): 51.1ms / 172.9ms / 51.1ms

Results for api.revenuecat.com:
  - 3.223.26.133: OK
    Latencies (min/max/avg): 52.0ms / 55.0ms / 52.0ms
  - 52.22.245.243: OK
    Latencies (min/max/avg): 52.4ms / 55.4ms / 52.4ms
  - 34.196.186.56: OK
    Latencies (min/max/avg): 52.6ms / 55.9ms / 52.6ms
  - 3.208.129.96: OK
    Latencies (min/max/avg): 52.7ms / 55.8ms / 52.7ms
  - 3.214.67.56: OK
    Latencies (min/max/avg): 53.5ms / 56.0ms / 53.5ms
  - 54.163.59.173: OK
    Latencies (min/max/avg): 53.9ms / 56.1ms / 53.9ms
```
