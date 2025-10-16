# gen_dnschefv2.py
Useful for defining the exact recipe needed for DNS resolution under broken DNS scenarios, specifically LDAP querying conditions, when performing a Bloodhound collection.

How it works:
Ya feed it a list of domain:ip as csv, you get back a "cheffed.txt" that dnschef (https://github.com/iphelix/dnschef) can use to define cooked responses to the various queries emitting from Bloodhound collector (like for example https://github.com/dirkjanm/BloodHound.py/tree/bloodhound-ce)

Has also been tested with legacy bloodhound ingestors (like bloodhound-python https://github.com/dirkjanm/BloodHound.py/tree/master, netexec, etc)


Example usage:
```
$ gen_dnschefv2.py -d babydc.baby.vl:10.129.61.163
```

Creates a "cheffed.txt" like so:
```
[A]
babydc.baby.vl=10.129.61.163

[CNAME]
10.129.61.163=babydc.baby.vl

[PTR]
163.61.129.10.in-addr-arpa=babydc.baby.vl

[SRV]
_kerberos-master._udp.BABY.VL=1 100 88 babydc.baby.vl
_kerberos-master._tcp.BABY.VL=1 100 88 babydc.baby.vl
_kerberos.BABY.VL=1 100 88 babydc.baby.vl
_kerberos._tcp.dc._msdcs.BABY.VL=1 100 88 babydc.baby.vl
_kerberos._tcp.dc._msdcs=1 100 88 babydc.baby.vl
_ldap._tcp.BABY.VL=1 100 389 babydc.baby.vl
_ldap._tcp.dc._msdcs.BABY.VL=1 100 389 babydc.baby.vl
_ldap._tcp.pdc._msdcs.BABY.VL=1 100 389 babydc.baby.vl
_ldap._tcp.pdc._msdcs=1 100 389 babydc.baby.vl
_ldap._tcp.gc._msdcs.BABY.VL=1 100 3268 babydc.baby.vl
_ldap._tcp.gc._msdcs=1 100 3268 babydc.baby.vl
_ldaps._tcp.BABY.VL=1 100 636 babydc.baby.vl
_ldaps._tcp.dc._msdcs.BABY.VL=1 100 636 babydc.baby.vl
_ldaps._tcp.pdc._msdcs.BABY.VL=1 100 636 babydc.baby.vl
_ldaps._tcp.pdc._msdcs=1 100 636 babydc.baby.vl
_ldaps._tcp.gc._msdcs.BABY.VL=1 100 3269 babydc.baby.vl
_ldaps._tcp.gc._msdcs=1 100 3269 babydc.baby.vl
```
And you can use dnschef to run a local DNS server, responding to all the things the DC should have been in the first place (gimme that bloodhound.zip anyways!)

Don't forget to add 127.0.0.1 as the first nameserver in /etc/resolv.conf

After that, perform your bloodhound collection
```
$ bloodhound-ce-python -u someuser -p 'somepassword123!' -c All -op bloody --zip --dns-timeout 10 -ns 127.0.0.1 --dns-tcp -dc BabyDc.baby.vl -d baby.vl
INFO: BloodHound.py for BloodHound Community Edition
INFO: Found AD domain: baby.vl
INFO: Getting TGT for user
INFO: Connecting to LDAP server: BabyDc.baby.vl
INFO: Found 1 domains
INFO: Found 1 domains in the forest
INFO: Found 1 computers
INFO: Connecting to LDAP server: BabyDc.baby.vl
INFO: Found 14 users
INFO: Found 54 groups
INFO: Found 2 gpos
INFO: Found 3 ous
INFO: Found 19 containers
INFO: Found 0 trusts
INFO: Starting computer enumeration with 10 workers
INFO: Querying computer: BabyDC.baby.vl
INFO: Done in 00M 34S
INFO: Compressing output into 20251015225950_bloodhound.zip
```

As you can see from dnschef output, every query got a cooked response
```
$ dnschef -i 127.0.0.1 --nameservers babydc.baby.vl --file cheffed.txt -t
          _                _          __  
         | | version 0.4  | |        / _| 
       __| |_ __  ___  ___| |__   ___| |_ 
      / _` | '_ \/ __|/ __| '_ \ / _ \  _|
     | (_| | | | \__ \ (__| | | |  __/ |  
      \__,_|_| |_|___/\___|_| |_|\___|_|  
                   iphelix@thesprawl.org  

(22:57:13) [*] DNSChef started on interface: 127.0.0.1
(22:57:13) [*] Using the following nameservers: babydc.baby.vl
(22:57:13) [*] Cooking A replies for domain babydc.baby.vl with '10.129.61.163'
(22:57:13) [*] Cooking CNAME replies for domain 10.129.61.163 with 'babydc.baby.vl'
(22:57:13) [*] Cooking PTR replies for domain 163.61.129.10.in-addr-arpa with 'babydc.baby.vl'
(22:57:13) [*] Cooking SRV replies for domain _kerberos-master._udp.baby.vl with '1 100 88 babydc.baby.vl'
(22:57:13) [*] Cooking SRV replies for domain _kerberos-master._tcp.baby.vl with '1 100 88 babydc.baby.vl'
(22:57:13) [*] Cooking SRV replies for domain _kerberos.baby.vl with '1 100 88 babydc.baby.vl'
(22:57:13) [*] Cooking SRV replies for domain _kerberos._tcp.dc._msdcs.baby.vl with '1 100 88 babydc.baby.vl'
(22:57:13) [*] Cooking SRV replies for domain _kerberos._tcp.dc._msdcs with '1 100 88 babydc.baby.vl'
(22:57:13) [*] Cooking SRV replies for domain _ldap._tcp.baby.vl with '1 100 389 babydc.baby.vl'
(22:57:13) [*] Cooking SRV replies for domain _ldap._tcp.dc._msdcs.baby.vl with '1 100 389 babydc.baby.vl'
(22:57:13) [*] Cooking SRV replies for domain _ldap._tcp.pdc._msdcs.baby.vl with '1 100 389 babydc.baby.vl'
(22:57:13) [*] Cooking SRV replies for domain _ldap._tcp.pdc._msdcs with '1 100 389 babydc.baby.vl'
(22:57:13) [*] Cooking SRV replies for domain _ldap._tcp.gc._msdcs.baby.vl with '1 100 3268 babydc.baby.vl'
(22:57:13) [*] Cooking SRV replies for domain _ldap._tcp.gc._msdcs with '1 100 3268 babydc.baby.vl'
(22:57:13) [*] Cooking SRV replies for domain _ldaps._tcp.baby.vl with '1 100 636 babydc.baby.vl'
(22:57:13) [*] Cooking SRV replies for domain _ldaps._tcp.dc._msdcs.baby.vl with '1 100 636 babydc.baby.vl'
(22:57:13) [*] Cooking SRV replies for domain _ldaps._tcp.pdc._msdcs.baby.vl with '1 100 636 babydc.baby.vl'
(22:57:13) [*] Cooking SRV replies for domain _ldaps._tcp.pdc._msdcs with '1 100 636 babydc.baby.vl'
(22:57:13) [*] Cooking SRV replies for domain _ldaps._tcp.gc._msdcs.baby.vl with '1 100 3269 babydc.baby.vl'
(22:57:13) [*] Cooking SRV replies for domain _ldaps._tcp.gc._msdcs with '1 100 3269 babydc.baby.vl'
(22:57:13) [*] DNSChef is running in TCP mode
(22:57:23) [*] 127.0.0.1: cooking the response of type 'SRV' for _ldap._tcp.pdc._msdcs to 1 100 389 babydc.baby.vl
(22:57:23) [*] 127.0.0.1: cooking the response of type 'SRV' for _ldap._tcp.gc._msdcs to 1 100 3268 babydc.baby.vl
(22:57:23) [*] 127.0.0.1: cooking the response of type 'SRV' for _kerberos._tcp.dc._msdcs to 1 100 88 babydc.baby.vl
(22:57:23) [*] 127.0.0.1: cooking the response of type 'SRV' for _kerberos._tcp.dc._msdcs to 1 100 88 babydc.baby.vl
(22:57:23) [*] 127.0.0.1: cooking the response of type 'A' for babydc.baby.vl to 10.129.61.163
(22:58:49) [*] 127.0.0.1: cooking the response of type 'SRV' for _ldap._tcp.pdc._msdcs to 1 100 389 babydc.baby.vl
(22:58:49) [*] 127.0.0.1: cooking the response of type 'SRV' for _ldap._tcp.gc._msdcs to 1 100 3268 babydc.baby.vl
(22:58:49) [*] 127.0.0.1: cooking the response of type 'SRV' for _kerberos._tcp.dc._msdcs to 1 100 88 babydc.baby.vl
(22:58:49) [*] 127.0.0.1: cooking the response of type 'SRV' for _kerberos._tcp.dc._msdcs to 1 100 88 babydc.baby.vl
(22:58:49) [*] 127.0.0.1: cooking the response of type 'A' for BabyDc.baby.vl to 10.129.61.163
(22:59:49) [*] 127.0.0.1: cooking the response of type 'SRV' for _ldap._tcp.pdc._msdcs.baby.vl to 1 100 389 babydc.baby.vl
(22:59:49) [*] 127.0.0.1: cooking the response of type 'SRV' for _ldap._tcp.gc._msdcs.baby.vl to 1 100 3268 babydc.baby.vl
(22:59:49) [*] 127.0.0.1: cooking the response of type 'SRV' for _kerberos._tcp.dc._msdcs.baby.vl to 1 100 88 babydc.baby.vl
(22:59:50) [*] 127.0.0.1: cooking the response of type 'A' for BabyDc.baby.vl to 10.129.61.163
(22:59:59) [*] 127.0.0.1: cooking the response of type 'A' for BabyDc.baby.vl to 10.129.61.163
(23:00:15) [*] 127.0.0.1: cooking the response of type 'A' for BabyDC.baby.vl to 10.129.61.163
```