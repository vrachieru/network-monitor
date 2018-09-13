# Network monitor

### Features:

* Speedtest


### Quick start:

Build the Docker image yourself:

```bash
$ docker build -t <yourname>/network-monitor .
```

Specify your desired configuration and run the container:

```bash
$ docker run -<d|i> --rm \
    -e SPEEDTEST_CRON='0 * * * *' \
    -e TZ='Europe/Bucharest' \
    -v /host/path/to/database.db:/app/database.db \
    -p <host_port>:80 \
    --name network-monitor \
    <yourname>/network-monitor
```

You can stop the container using:

```bash
$ docker stop network-monitor
```


### Configuration

You can configure the service via the following environment variables.

| Environment Variable | Default Value | Description                                                                                             |
| -------------------- | ------------- | ------------------------------------------------------------------------------------------------------- |
| SPEEDTEST_CRON       | 0 * * * *     | A cron style expression representing how often to run speedtests. I find that doing so hourly is plenty |
| TZ                   | UTC           | Timezone of the container                                                                               |


### To do

* Bandwith consumption
* Internet outages
* DNS queries


### License

MIT