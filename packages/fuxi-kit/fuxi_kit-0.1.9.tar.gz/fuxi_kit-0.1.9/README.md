# FUXI-KIT

## Howto

1. Create fuxi-kit config file.

```sh
$ pip3 install fuxi-kit

$ ipython
In [1]: import fuxi_kit
In [2]: fuxi_kit.__version__
Out[2]: '0.1.9'

$ cat <<EOF | tee /etc/openvpn/config.yaml
fuxi_web:
  endpoint: ""          # http://<FUXI-WEB.COM>
  auth_api_key: ""      # Identity Key
  auth_api: "/api/v1/tunnel/auth"
log:
  level: info
EOF
```

2. Config with openvpn server.

```sh
# CONFIG EXAMPLE:
# /etc/openvpn/openvpn_server.conf
script-security 3
auth-user-pass-verify "python3 -m fuxi_kit" via-env
```
