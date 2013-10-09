#---------------------------------------------------------------
# Project         : pxemngr
# File            : views.py
# Copyright       : 2009-2010 Splitted-Desktop Systems
# Author          : Frederic Lepied
# Created On      : Sun Feb  1 13:54:41 2009
# Purpose         : http logic
#---------------------------------------------------------------

from django.http import HttpResponse, Http404
import os

import pxemngr.settings as settings
from pxe.common import get_mac, simplify_mac, mac2filename, create_symlink, set_next_boot
from pxe.models import Log, System
import pxeparse

def get_system(request, mac):
    try:
        return System.objects.filter(macaddress__mac=simplify_mac(mac))[0]
    except IndexError:
        pass

    addr = request.META['REMOTE_ADDR']
    l = map(lambda x: '%02x' % int(x), addr.split('.'))
    for i in range(len(l), 1, -1):
        try:
            return System.objects.filter(macaddress__mac=''.join(l[0:i]))[0]
        except IndexError:
            pass
    print 'No system defined for %s (%s)' % (mac, addr)
    raise Http404

def localboot1(request):
    return localboot(request, get_mac(request))
    
def localboot(request, mac):
    return nextboot(request, mac, settings.PXE_LOCAL)

def nextboot1(request, boot_name):
    print 'nextboot1', boot_name
    return nextboot(request, get_mac(request), boot_name)
    
def nextboot(request, mac, boot_name):
    print 'nextboot', mac, boot_name
    systems = System.objects.filter(macaddress__mac=simplify_mac(mac))
    if len(systems) > 1:
        set_next_boot(systems[0], boot_name)
    else:
        fn = '%s/%s' % (settings.PXE_ROOT, mac2filename(simplify_mac(mac)))
        create_symlink('%s/%s%s' % (settings.PXE_PROFILES, boot_name,
                                    settings.PXE_SUFFIX),
                       fn)
    return HttpResponse("Next boot set to %s" % boot_name,
                        mimetype="text/plain")

def profile1(request):
    return profile(request, get_mac(request))
    
def profile(request, mac):
    system = get_system(request, mac)
    log = Log.objects.filter(system=system).order_by('-date')[0]
    return HttpResponse(log.boot_name.name, mimetype="text/plain")

def ipxe1(request):
    return ipxe(request, get_mac(request))

def ipxe(request, mac):
    filename = os.path.join(settings.PXE_ROOT, mac2filename(simplify_mac(mac)))
    if not os.path.exists(filename):
        filename = os.path.join(settings.PXE_ROOT, 'default')
    pxe_entry = open(filename).read(-1)
    parsed = pxeparse.parse(pxe_entry)
    parsed['path'] = settings.IPXE_HTTP_ROOT
    label = parsed['default']
    if 'localboot' in parsed[label]:
        return HttpResponse('''#!ipxe

sanboot --no-describe --drive 0x%x
''' % (0x80 + int(parsed[label]['localboot'],)),
                            mimetype="text/plain")
    else:
        parsed['kernel'] = parsed[label]['kernel']
        parsed['initrd'], parsed['args'] = parsed[label]['append'].split('=', 1)[1].split(' ', 1)
        return HttpResponse('''#!ipxe

kernel %(path)s/%(kernel)s %(args)s
initrd %(path)s/%(initrd)s
boot
''' % parsed,
                        mimetype="text/plain")
