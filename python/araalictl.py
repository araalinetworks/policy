#!/usr/bin/env python
"""
Wrappers for araalictl for python use
"""
import json
import os
import requests
import sys
from sys import platform
import yaml

from main import Usage, run_command

g_debug = False

def help():
    """get araalictl help"""
    print(run_command("./araalictl -h", result=True, debug=False)[1])

def fetch():
    """For downloading and upgrading araalictl"""
    linux_url = "https://s3-us-west-2.amazonaws.com/araalinetworks.cf/araalictl-api.linux-amd64"
    darwin_url = "https://s3-us-west-2.amazonaws.com/araalinetworks.cf/araalictl-api.darwin-amd64"

    if platform == "linux" or platform == "linux2":
        url = linux_url
    elif platform == "darwin":
        url = darwin_url
    else:
        raise Usage("only linux and mac are currently supported")
    if not os.path.exists("araalictl"):
        print("Fetching araalictl ...")
        r = requests.get(url, allow_redirects=True)
        open('araalictl', 'wb').write(r.content)
        os.chmod('araalictl', 0o777)
    else:
        pass
        #print("upgrading araalictl ...")
        #run_command("sudo ./araalictl upgrade")

def tenant_create(tenant_id, user_email, tenant_name=None, user_name=None):
    """Create a subtenant"""
    cmd = "./araalictl tenant -op=add -id=%s -name=\"%s\" -user-email=%s -user-name=\"%s\"" % (
        tenant_id, tenant_name, user_email, user_name)
    rc = run_command(cmd, result=True, strip=False)
    assert rc[0] == 0, rc[1]

def tenant_delete(tenant_id):
    """Delete a subtenant"""
    rc = run_command("./araalictl tenant -op=del -id=%s" % tenant_id, result=True, strip=False)
    assert rc[0] == 0, rc[1]

def fog_setupconfig(tenant_id, dns_name, vpc_id, subnet_id, key_name,
                    dns_hosted_zone_id, instance_type="m5.large"):
    """Setup config required to install a fog"""
    rc = run_command("./araalictl config -tenant=%s Fog=%s" % (tenant_id, dns_name),
                     result=True, strip=False)
    assert rc[0] == 0, rc[1]

    cfg_str = "VPCIDParameter=%s,SubnetIDParameter=%s,KeyNameParameter=%s,HostedZoneParameter=%s,InstanceTypeParameter=%s,ReadOnlyRoleParameter=" % (
        vpc_id, subnet_id, key_name, dns_hosted_zone_id, instance_type)
    rc = run_command("./araalictl config -tenant=%s InternalFogInstallParams=%s" % (tenant_id, cfg_str),
                     result=True, strip=False)
    assert rc[0] == 0, rc[1]

def fog_install(tenant_id, nodes=1):
    """Install AWS mode fog"""
    rc = run_command("./araalictl install-fog -tenant=%s -mode=aws -nodes=%d" %
                     (tenant_id, nodes), result=True, strip=False)
    assert rc[0] == 0, rc[1]

def fog_uninstall(tenant_id):
    """Uninstall AWS mode fog"""
    rc = run_command("./araalictl uninstall-fog -tenant=%s -mode=aws" % tenant_id,
                     result=True, strip=False)
    assert rc[0] == 0, rc[1]

def get_zones(full=False, tenant=None):
    """Get zones and apps for tenant"""
    tstr = " -tenant=%s " % (tenant) if tenant else ""
    rc = run_command("./araalictl api -fetch-zone-apps %s %s" % ("-full" if full else "", tstr),
            result=True, strip=False)
    assert rc[0] == 0, rc[1]
    return yaml.load(rc[1], yaml.SafeLoader)

def update_links(zone, app, data, tenant=None):
    """Update actions on a link"""
    tstr = " -tenant=%s " % (tenant) if tenant else ""
    ret_val = {}
    for link in data:
        if link["new_state"] == "DEFINED_POLICY":
            ret_val["policies"] = ret_val.get("policies", 0) + 1
            if link["state"] == "BASELINE_ALERT":
                ret_val["alerts"] = ret_val.get("alerts", 0) + 1
    
        elif link["new_state"] == "SNOOZED_POLICY":
            if link["state"] == "BASELINE_ALERT":
                ret_val["alerts"] = ret_val.get("alerts", 0) + 1
            ret_val["policies"] = ret_val.get("policies", 0) + 1

    if not ret_val:
        ret_val['empty'] = {"success": "Empty policy request"}
    else:
        if g_debug: print(yaml.dump(data))
        rc = run_command("./araalictl api -zone %s -app %s -update-links %s" % (zone, app, tstr),
                         in_text=yaml.dump(data), result=True, strip=False)
        assert rc[0] == 0, rc[1]
        ret_val = json.loads(rc[1])

    return ret_val

def get_links(zone, app, tenant=None):
    """Get links for a zone and app"""
    tstr = " -tenant=%s " % (tenant) if tenant else ""
    rc = run_command("./araalictl api -zone %s -app %s -fetch-links %s" % (
        zone, app, tstr), result=True, strip=False)
    assert rc[0] == 0, rc[1]
    return yaml.load(rc[1], yaml.SafeLoader)


def enforce(data, service=False, tenant=None):
    """Enforce zone app or service."""
    tstr = " -tenant=%s " % (tenant) if tenant else ""
    ostr = " -enforce-service " if service else " -enforce-zone-app "

    ret_val = {}
    if not data:
        ret_val['empty'] = {"success": "Empty enforcement request"}
    else:
        if g_debug:
            print(yaml.dump(data))
        rc = run_command("./araalictl api %s %s" % (
            ostr, tstr), result=True, strip=False)
        assert rc[0] == 0, rc[1]
        ret_val = json.loads(rc[1])

    return ret_val


if __name__ == '__main__':
    sys.exit(fetch())
