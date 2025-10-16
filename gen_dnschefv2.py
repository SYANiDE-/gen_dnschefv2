#!/usr/bin/env python3
import os, sys, argparse
from IPython import embed

def getargs():
    AP = argparse.ArgumentParser(description="Make dnschef config for spoofing/resolve")
    AP.add_argument("-d","--dcmap",required=True,type=str,default=None,help="[domain controller FQDN]:[domain controller IP], comma-separated.")
    AR, trash = AP.parse_known_args()
    return vars(AR)

def process_dcmap(obj):
    processed_items = []
    dcs = obj['dcmap'].split(",")
    for item in dcs:
        dc, ip = item.split(":")
        reverse = '.'.join(ip.split(".")[::-1])
        domain_upper = '.'.join(dc.upper().split(".")[1:])
        processed_items.append({
            'domain':domain_upper,
            'ip':ip,
            'pi':reverse,
            'dc':dc
        })
    return processed_items

def fmt(indent,lst):
    return ('\n'+(' '*indent)).join(lst)

def main():
    args = getargs()
    processed_items = process_dcmap(args)
    indent=8
    ('\n'+(' '*indent)).join

    a_recs = fmt(indent,[f"{x['dc']}={x['ip']}" for x in processed_items])
    cname_recs = fmt(indent,[f"{x['ip']}={x['dc']}" for x in processed_items])
    ptr_recs = fmt(indent,[f"{x['pi']}.in-addr-arpa={x['dc']}" for x in processed_items])

    kmasterudp = fmt(indent,[f"_kerberos-master._udp.{x['domain']}=1 100 88 {x['dc']}" for x in processed_items])
    kmastertcp = fmt(indent,[f"_kerberos-master._tcp.{x['domain']}=1 100 88 {x['dc']}" for x in processed_items])
    kerberos = fmt(indent,[f"_kerberos.{x['domain']}=1 100 88 {x['dc']}" for x in processed_items])
    ktcpdcmsdcs = fmt(indent,[f"_kerberos._tcp.dc._msdcs.{x['domain']}=1 100 88 {x['dc']}" for x in processed_items])
    ktcpdcmsdcs2 = fmt(indent,[f"_kerberos._tcp.dc._msdcs=1 100 88 {x['dc']}" for x in processed_items])

    ldaptcp = fmt(indent,[f"_ldap._tcp.{x['domain']}=1 100 389 {x['dc']}" for x in processed_items])
    ldaptcpdcmsdcs = fmt(indent,[f"_ldap._tcp.dc._msdcs.{x['domain']}=1 100 389 {x['dc']}" for x in processed_items])
    ldaptcppdcmsdcs = fmt(indent,[f"_ldap._tcp.pdc._msdcs.{x['domain']}=1 100 389 {x['dc']}" for x in processed_items])
    ldaptcppdcmsdcs2 = fmt(indent,[f"_ldap._tcp.pdc._msdcs=1 100 389 {x['dc']}" for x in processed_items])
    ldaptcpgcmsdcs = fmt(indent,[f"_ldap._tcp.gc._msdcs.{x['domain']}=1 100 3268 {x['dc']}" for x in processed_items])
    ldaptcpgcmsdcs2 = fmt(indent,[f"_ldap._tcp.gc._msdcs=1 100 3268 {x['dc']}" for x in processed_items])

    ldapstcp = fmt(indent,[f"_ldaps._tcp.{x['domain']}=1 100 636 {x['dc']}" for x in processed_items])
    ldapstcpdcmsdcs = fmt(indent,[f"_ldaps._tcp.dc._msdcs.{x['domain']}=1 100 636 {x['dc']}" for x in processed_items])
    ldapstcppdcmsdcs = fmt(indent,[f"_ldaps._tcp.pdc._msdcs.{x['domain']}=1 100 636 {x['dc']}" for x in processed_items])
    ldapstcppdcmsdcs2 = fmt(indent,[f"_ldaps._tcp.pdc._msdcs=1 100 636 {x['dc']}" for x in processed_items])
    ldapstcpgcmsdcs = fmt(indent,[f"_ldaps._tcp.gc._msdcs.{x['domain']}=1 100 3269 {x['dc']}" for x in processed_items])
    ldapstcpgcmsdcs2 = fmt(indent,[f"_ldaps._tcp.gc._msdcs=1 100 3269 {x['dc']}" for x in processed_items])

    bloodhounds = fmt(indent,[f"netexec ldap {x['dc']} -k --use-kcache --bloodhound -c all --dns-server 127.0.0.1 [,--dns-tcp]" for x in processed_items])
    bloodhoundCEs = fmt(indent,[f"bloodhound-ce-python -u 'Administrator@{x['domain'].lower()}' -p 'sumptin123!' -d {x['domain'].lower()} -dc {x['dc']} -ns 127.0.0.1 [,--dns-tcp]" for x in processed_items])
    
    output = '\n'.join([x[indent:] for x in f""" 
        [A]
        {a_recs}

        [CNAME]
        {cname_recs}

        [PTR]
        {ptr_recs}

        [SRV]
        {kmasterudp}
        {kmastertcp}
        {kerberos}
        {ktcpdcmsdcs}
        {ktcpdcmsdcs2}
        {ldaptcp}
        {ldaptcpdcmsdcs}
        {ldaptcppdcmsdcs}
        {ldaptcppdcmsdcs2}
        {ldaptcpgcmsdcs}
        {ldaptcpgcmsdcs2}
        {ldapstcp}
        {ldapstcpdcmsdcs}
        {ldapstcppdcmsdcs}
        {ldapstcppdcmsdcs2}
        {ldapstcpgcmsdcs}
        {ldapstcpgcmsdcs2}
    """.split("\n")])

    output2 = '\n'.join([x[indent:] for x in f""" 
        ### Use one of the following, depending on DC hosts DNS on UDP53 or TCP53
        dnschef -i 127.0.0.1 --nameservers {','.join([x['dc'] for x in processed_items])} --file cheffed.txt" [,-t]

        Don't forget to update /etc/resolv.conf, add as FIRST nameserver:
            nameserver 127.0.0.1

        ### For bloodhound collection using netexec (crackmapexec-ng), Use one of the following, depending on DC hosts DNS on UDP53 or TCP53
        {bloodhounds}

        ### For bloodhound collection using bloodhound-ce-python, use oneof the following, depending on DC hosts DNS on UDP53 or TCP53
        {bloodhoundCEs}

    """.split("\n")])
    print(output)
    print(output2)
    with open('cheffed.txt','w') as F:
        F.write(output)
        F.close()
    print(f"[+] dnschef config written to ./cheffed.txt")




    



if __name__=="__main__":
    main()
