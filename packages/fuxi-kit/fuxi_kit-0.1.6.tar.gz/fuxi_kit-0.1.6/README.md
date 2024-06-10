# FUXI-KIT

## Howto

1. Create fuxi-kit config file.

```sh
$ pip3 install fuxi-kit
$ cat <<EOF | tee /etc/openvpn/config.yaml
fuxi_web:
  endpoint: ""    # Example: https://example.com
  auth_api_key: ""
  auth_api: "/api/v1/tunnel/auth"
log:
  level: info
EOF
```

2. Config with openvpn server.

```sh
# /etc/openvpn/openvpn_server.conf
# CONFIG EXAMPLE:
script-security 3
auth-user-pass-verify python3 -m fuxi_kit via-env
```
