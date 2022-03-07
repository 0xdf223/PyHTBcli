NMCLI_CONNECTION_SHOW_ACTIVE = """NAME                UUID                                  TYPE      DEVICE  
htbcli              34bde648-0a9a-4dc0-abb4-e72b0c527cfd  vpn       enp0s3  
Wired connection 1  4eca0c31-1d22-338c-98ad-cf3d84a7f354  ethernet  enp0s3  
tun0                99a6ebcc-426e-40a5-8488-e6d2057caf9a  tun       tun0    
docker0             dda032a5-af9f-43a3-bc1c-f79a12fdb3d1  bridge    docker0
"""

NMCLI_CONNECTION_SHOW_ACTIVE_DISCONNECTED = """NAME                UUID                                  TYPE      DEVICE  
Wired connection 1  4eca0c31-1d22-338c-98ad-cf3d84a7f354  ethernet  enp0s3  
docker0             dda032a5-af9f-43a3-bc1c-f79a12fdb3d1  bridge    docker0 
"""

NMCLI_CONNECTION_EXPORT_HTBCLI = """client
remote 'edge-us-vip-8.hackthebox.eu' 1337
ca '/home/oxdf/.cert/nm-openvpn/htbcli-ca.pem'
cert '/home/oxdf/.cert/nm-openvpn/htbcli-cert.pem'
key '/home/oxdf/.cert/nm-openvpn/htbcli-key.pem'
cipher AES-128-CBC
comp-lzo adaptive
dev tun
proto udp
remote-cert-tls server
tls-auth '/home/oxdf/.cert/nm-openvpn/htbcli-tls-auth.pem' 1
nobind
auth-nocache
script-security 2
persist-key
persist-tun
user nm-openvpn
group nm-openvpn
"""

NMCLI_CONNECTION_SHOW = """NAME                    UUID                                  TYPE      DEVICE  
htbcli                  e49bb3ad-b42d-4afb-9a6c-653fbc1e7700  vpn       enp0s3  
Wired connection 1      4eca0c31-1d22-338c-98ad-cf3d84a7f354  ethernet  enp0s3  
tun0                    23e0ec26-2dc4-45fb-a4d0-c6d225434225  tun       tun0    
docker0                 dda032a5-af9f-43a3-bc1c-f79a12fdb3d1  bridge    docker0  
htbcli-ra               ae814cff-fb14-4e2c-8c12-5598fe97ba74  vpn       --
"""

NMCLI_CONNECTION_SHOW_WO_HTBCLI = """NAME                    UUID                                  TYPE      DEVICE  
Wired connection 1      4eca0c31-1d22-338c-98ad-cf3d84a7f354  ethernet  enp0s3  
tun0                    23e0ec26-2dc4-45fb-a4d0-c6d225434225  tun       tun0    
docker0                 dda032a5-af9f-43a3-bc1c-f79a12fdb3d1  bridge    docker0 
"""
