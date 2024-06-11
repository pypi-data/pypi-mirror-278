import os
import platform
import re
import subprocess
import sys
from subprocess import CalledProcessError

from cpbox.tool import datatypes


def get_os_name():
    os_name = platform.system()
    map = {
            'Linux': 'linux',
            'Darwin': 'mac',
            'CYGWIN': 'cygwin',
            'MINGW': 'MinGw',
            }
    for name, sys_name in map.items():
        if os_name.startswith(name):
            return sys_name
    return 'unknown'

def available_cpu_count():
    """ Number of available virtual or physical CPUs on this system, i.e.
    user/real as output by time(1) when called with an optimally scaling
    userspace-only program"""

    # cpuset
    # cpuset may restrict the number of *available* processors
    try:
        m = re.search(r'(?m)^Cpus_allowed:\s*(.*)$',
                      open('/proc/self/status').read())
        if m:
            res = bin(int(m.group(1).replace(',', ''), 16)).count('1')
            if res > 0:
                return res
    except IOError:
        pass

    # Python 2.6+
    try:
        import multiprocessing
        return multiprocessing.cpu_count()
    except (ImportError, NotImplementedError):
        pass

    # https://github.com/giampaolo/psutil
    try:
        import psutil
        return psutil.cpu_count()   # psutil.NUM_CPUS on old versions
    except (ImportError, AttributeError):
        pass

    # POSIX

def memtotal_bytes():
    bytes = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
    return bytes

def memtotal_mb():
    return memtotal_bytes() / (1024 ** 2)

# adapt to `commands.getstatusoutput` for python 3+
# https://stackoverflow.com/questions/11344557/replacement-for-getstatusoutput-in-python-3
def run_cmd(cmd, stdout=None):
    ret = 0
    try:
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
    except CalledProcessError as e:
        ret = e.returncode
        output = e.output
    output = output.decode('utf-8')
    return ret, output.rstrip('\n')
# the difference between `subprocess.call()` and `subprocess.check_output()`
# https://stackoverflow.com/questions/25333537/performance-of-subprocess-check-output-vs-subprocess-call
def shell_run(cmd, keep_pipeline=True, exit_on_error=True, stdout=None, stderr=None):
    if datatypes.is_list_or_tuple(cmd):
        cmd = ';\n'.join(cmd)
    return_code = 0
    ret = subprocess.run(cmd, shell=True, stdout=stdout, stderr=stderr, check=False)
    return_code = ret.returncode
    if return_code != 0 and exit_on_error:
        sys.exit(return_code)
    return return_code
