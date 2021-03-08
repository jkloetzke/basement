from bob.errors import ParseError
import fnmatch
import platform

SUPPORTED_OS = ("linux-gnu", "msys", "win32")

# TODO: support more architectures; support musl/dietlibc

# get host architecture
def hostArch(args, **options):
    m = platform.uname().machine
    if m == "x86_64":
        return m
    elif m == "AMD64":
        return "x86_64"
    elif m.startswith("i"):
        return "i386"
    elif m.startswith("aarch64"):
        return "arm64"
    elif m.startswith("arm"):
        return "arm"
    else:
        raise ParseError("Unsupported host machine: " + m)

def hostMachine():
    m = platform.uname().machine
    if m == "x86_64":
        return m
    elif m == "AMD64":
        return "x86_64"
    elif m.startswith("i"):
        return "i386"
    elif m.startswith("aarch64"):
        return m
    elif m.startswith("arm"):
        return m
    else:
        raise ParseError("Unsupported host machine: " + m)

# get host autoconf triple
def hostAutoconf(args, **options):
    machine = hostMachine()
    system = platform.uname().system
    if system == 'Linux':
        return machine + "-linux-gnu"
    elif system.startswith("MSYS_NT"):
        return machine + "-pc-msys"
    elif system == "Windows":
        return machine + "-pc-win32"
    else:
        raise ParseError("Unsupported system: " + system)

# set or replace vendor field in autoconf triplet
def autoconfSetVendor(args, **options):
    if len(args) != 2:
        raise ParseError("$(autoconf-set-vendor,triplet,vendor) expects two arguments")

    # split off machine
    machine, _, rest = args[0].partition("-")

    # Determine OS. This is ambigous with the vendor field. Hence the list.
    for vendor in SUPPORTED_OS:
        if rest.endswith(vendor):
            system = vendor
            break
    else:
        raise ParseError("autoconf-set-vendor: unsupported triplet: " + args[0])

    return machine + '-' + args[1] + '-' + system

manifest = {
    'apiVersion' : "0.15",
    'stringFunctions' : {
        "autoconf-set-vendor" : autoconfSetVendor,
        "host-arch" : hostArch,
        "host-autoconf" : hostAutoconf,
    }
}
