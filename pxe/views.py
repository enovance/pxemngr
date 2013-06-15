#---------------------------------------------------------------
# Project         : pxemngr
# File            : views.py
# Copyright       : 2009-2010 Splitted-Desktop Systems
# Author          : Frederic Lepied
# Created On      : Sun Feb  1 13:54:41 2009
# Purpose         : http logic
#---------------------------------------------------------------

from django.http import HttpResponse, Http404

import pxemngr.settings as settings
from pxe.common import get_mac, simplify_mac, mac2filename, create_symlink, set_next_boot
from pxe.models import Log, System
import pxeparse

def get_system(request, mac):
    try:
        return System.objects.get(macaddress__mac=simplify_mac(mac))
    except System.DoesNotExist:
        pass

    addr = request.META['REMOTE_ADDR']
    l = map(lambda x: '%02x' % int(x), addr.split('.'))
    for i in range(len(l), 1, -1):
        try:
            return System.objects.get(macaddress__mac=''.join(l[0:i]))
        except System.DoesNotExist:
            pass
    raise Http404

def localboot1(request):
    return localboot(request, get_mac(request))
    
def localboot(request, mac):
    try:
        system = System.objects.get(macaddress__mac=simplify_mac(mac))
        set_next_boot(system, settings.PXE_LOCAL)
    except System.DoesNotExist:
        fn = '%s/%s' % (settings.PXE_ROOT, mac2filename(simplify_mac(mac)))
        create_symlink('%s/%s%s' % (settings.PXE_PROFILES, settings.PXE_LOCAL, settings.PXE_SUFFIX), fn)
    
    return HttpResponse("Next boot set to local", mimetype="text/plain")

def profile1(request):
    return profile(request, get_mac(request))
    
def profile(request, mac):
    system = get_system(request, mac)
    log = Log.objects.filter(system=system).order_by('-date')[0]
    return HttpResponse(log.boot_name.name, mimetype="text/plain")

def ipxe1(request):
    return ipxe(request, get_mac(request))

def ipxe(request, mac):
    system = get_system(request, mac)
    log = Log.objects.filter(system=system).order_by('-date')[0]
    pxe_entry = open('%s/%s/%s%s' % (settings.PXE_ROOT,
                                     settings.PXE_PROFILES,
                                     log.boot_name.name,
                                     settings.PXE_SUFFIX)).read(-1)
    parsed = pxeparse.parse(pxe_entry)
    parsed['path'] = settings.IPXE_HTTP_ROOT
    label = parsed['DEFAULT']
    parsed['kernel'] = parsed[label]['KERNEL']
    parsed['initrd'] = parsed[label]['APPEND'].split('=', 1)[1]
    return HttpResponse('''#!ipxe

kernel %(path)s/%(kernel)s
initrd %(path)s/%(initrd)s
boot
''' % parsed,
                        mimetype="text/plain")
