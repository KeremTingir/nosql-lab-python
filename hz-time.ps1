Measure-Command {
    1..100 | ForEach-Object -Parallel { curl -s "http://<IpV4>:8080/nosql-lab-hz/ogrenci_no=2025000001" | Out-Null } -ThrottleLimit 10
} | Out-File -FilePath hz-time.results