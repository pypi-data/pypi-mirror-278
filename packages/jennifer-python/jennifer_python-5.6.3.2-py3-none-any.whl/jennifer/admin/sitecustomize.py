
import os
import tempfile
import time
from datetime import datetime
import platform
import sys
import subprocess
import traceback


enable_diagnostics = os.getenv('JENNIFER_DBG') == '1'
root_dir = os.path.dirname(os.path.dirname(__file__))


def format_time(time_value):
    return time_value.strftime("%Y%m%d-%H%M%S")


def _log(level, *args):
    current_time = format_time(datetime.now())
    print(os.getpid(), current_time, '[jennifer]', level, args)


def _diag_log(*args):
    if enable_diagnostics is False:
        return

    current_time = format_time(datetime.now())
    print(os.getpid(), current_time, '[jennifer-diag-log]', args)


def run_master(bin_path, config_path, log_dir, sock_file):

    if sock_file is None:
        return

    arch = {
        'x86_64': 'amd64',
        'x86': '386',
        'arm64': 'arm64',
    }[platform.machine()]

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    if not os.path.exists(log_dir):
        _log('exception', 'ErrNotExist', log_dir)
        return

    platform_id = sys.platform
    if platform_id == "linux2":
        platform_id = "linux"

    _diag_log('[child]', sys.platform, arch)
    time.time()
    date_postfix = time.strftime("%Y%m%d")
    log_path = os.path.join(log_dir, 'agent_' + date_postfix + '.log')

    path = os.path.join(bin_path, platform_id, arch, 'jennifer_agent')
    log_stream = open(log_path, 'w+')  # log_path == '/tmp/agent_20220811.log'

    _diag_log('[child.open.before]', path)
    result = subprocess.Popen(
        [
            path,  # '/mnt/d/.../jennifer/bin/linux/amd64/jennifer_agent'
            config_path,  # '/mnt/d/.../myapp/jennifer.ini'
            sock_file,  # '/tmp/jennifer-1629185873.sock'
        ],
        stdout=log_stream,
        stderr=log_stream,
    )
    _diag_log('[child.open.after]', result)


def run_master_process():
    time_prefix = time.time()
    py_dbg_mode = int(os.getenv('JENNIFER_PY_DBG') or '0')
    if (py_dbg_mode & 0x02) == 0x02:
        time_prefix = 0

    config_path = os.environ.get('JENNIFER_CONFIG_FILE') or ''
    if config_path == '' or not os.path.exists(config_path):
        raise FileNotFoundError('[JENNIFER_CONFIG_FILE] ' + config_path + " not exists")

    log_dir = os.environ.get('JENNIFER_LOG_DIR') or '/tmp'
    os.environ['JENNIFER_LOG_DIR'] = log_dir

    master_path = os.path.join(root_dir, 'bin')
    sock_path = os.path.join(tempfile.gettempdir(), 'jennifer-%d.sock' % time_prefix)
    os.environ['JENNIFER_MASTER_ADDRESS'] = sock_path

    if os.path.exists(master_path):
        run_master(master_path, config_path, log_dir, sock_path)


def load_jennifer():
    try:
        jennifer = __import__('jennifer')
    except ImportError as e:
        jennifer_path = os.path.abspath(os.path.join(root_dir, '..'))
        sys.path.append(jennifer_path)
        jennifer = __import__('jennifer')

    if os.environ.get('JENNIFER_MASTER_ADDRESS') is not None:
        try:
            jennifer.startup.init()
        except Exception as e:
            _log('exception', 'site_customize', e)
            if enable_diagnostics:
                traceback.print_exc()


if __name__ == 'sitecustomize':
    run_master_process()

    os.environ['JENNIFER_PYTHON_PATH'] = sys.executable
    load_jennifer()
