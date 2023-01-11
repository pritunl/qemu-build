#!/usr/bin/python3
import os
import sys
import glob
import shutil
import optparse
import subprocess
import configparser

rebase_prefix    = ""
version_override = None

def check_rebase():
    """ detect 'git rebase -x edk2-build.py master' testbuilds """
    global rebase_prefix
    global version_override

    if not os.path.exists('.git/rebase-merge/msgnum'):
        return ""
    with open('.git/rebase-merge/msgnum', 'r') as f:
        msgnum = int(f.read())
    with open('.git/rebase-merge/end', 'r') as f:
        end = int(f.read())
    with open('.git/rebase-merge/head-name', 'r') as f:
        head = f.read().strip().split('/')

    rebase_prefix = f'[ {int(msgnum/2)} / {int(end/2)} - {head[-1]} ] '
    if msgnum != end:
        # fixed version speeds up builds
        version_override = "test-build-patch-series"

def get_coredir(cfg):
    if cfg.has_option('global', 'core'):
        return os.path.abspath(cfg['global']['core'])
    else:
        return os.getcwd()

def get_version(cfg):
    coredir = get_coredir(cfg)
    if version_override:
        version = version_override
        print('')
        print(f'### version [override]: {version}')
        return version
    if os.environ.get('RPM_PACKAGE_NAME'):
        version = os.environ.get('RPM_PACKAGE_NAME');
        version += '-' + os.environ.get('RPM_PACKAGE_VERSION');
        version += '-' + os.environ.get('RPM_PACKAGE_RELEASE');
        print('')
        print(f'### version [rpmbuild]: {version}')
        return version
    if os.path.exists(coredir + '/.git'):
        cmdline = [ 'git', 'describe', '--tags', '--abbrev=8', '--match=edk2-stable*' ]
        result = subprocess.run(cmdline, capture_output = True, cwd = coredir)
        version = result.stdout.decode().strip()
        #cmdline = [ 'git', 'branch', '--show-current']
        #result = subprocess.run(cmdline, capture_output = True, cwd = coredir)
        #branch = result.stdout.decode().strip()
        #if branch != "master":
        #    version += f' ({branch})'
        print('')
        print(f'### version [git]: {version}')
        return version
    return None

def pcd_string(name, value):
    return f'{name}=L{value}\\0'

def pcd_version(cfg):
    version = get_version(cfg)
    if version is None:
        return []
    return [ '--pcd', pcd_string('PcdFirmwareVersionString', version) ]

def build_message(line):
    if os.environ.get('TERM') in [ 'xterm', 'xterm-256color' ]:
        # setxterm  title
        start  = '\x1b]2;'
        end    = '\x07'
        print(f'{start}{rebase_prefix}{line}{end}', end = '')

    print('')
    print('###')
    print(f'### {rebase_prefix}{line}')
    print('###')

def build_run(cmdline, name):
    print(cmdline)
    result = subprocess.run(cmdline)
    if result.returncode:
        print(f'ERROR: {cmdline[0]} exited with {result.returncode} while building {name}')
        sys.exit(result.returncode)

def build_copy(plat, tgt, dstdir, copy):
    srcdir = f'Build/{plat}/{tgt}_GCC5'
    names = copy.split()
    srcfile = names[0]
    if len(names) > 1:
        dstfile = names[1]
    else:
        dstfile = os.path.basename(srcfile)
    print(f'# copy: {srcdir} / {srcfile}  =>  {dstdir} / {dstfile}')

    os.makedirs(dstdir, exist_ok = True)
    shutil.copy(srcdir + '/' + srcfile,
                dstdir + '/' + dstfile)

def pad_file(dstdir, pad):
    args = pad.split()
    if len(args) < 2:
        raise RuntimeError(f'missing arg for pad ({args})')
    name = args[0]
    size = args[1]
    cmdline = [
        'truncate',
        '--size', size,
        dstdir + '/' + name,
    ]
    print(f'# padding: {dstdir} / {name}  =>  {size}')
    subprocess.run(cmdline)

def build_one(cfg, build, jobs = None):
    cmdline  = [ 'build' ]
    cmdline += [ '-t', 'GCC5' ]
    cmdline += [ '-p', cfg[build]['conf'] ]

    if (cfg[build]['conf'].startswith('OvmfPkg/') or
        cfg[build]['conf'].startswith('ArmVirtPkg/')):
        cmdline += pcd_version(cfg)

    if jobs:
        cmdline += [ '-n', jobs ]
    for arch in cfg[build]['arch'].split():
        cmdline += [ '-a', arch ]
    if 'opts' in cfg[build]:
        for name in cfg[build]['opts'].split():
            section = 'opts.' + name
            for opt in cfg[section]:
                cmdline += [ '-D', opt.upper() + '=' + cfg[section][opt] ]
    if 'tgts' in cfg[build]:
        tgts = cfg[build]['tgts'].split()
    else:
        tgts = [ 'DEBUG' ]
    for tgt in tgts:
        build_message(f'building: {cfg[build]["conf"]} ({cfg[build]["arch"]}, {tgt})')
        build_run(cmdline + [ '-b', tgt ],
                  cfg[build]['conf'])

        if 'plat' in cfg[build]:
            # copy files
            for cpy in cfg[build]:
                if not cpy.startswith('cpy'):
                    continue
                build_copy(cfg[build]['plat'],
                           tgt,
                           cfg[build]['dest'],
                           cfg[build][cpy])
            # pad builds
            for pad in cfg[build]:
                if not pad.startswith('pad'):
                    continue
                pad_file(cfg[build]['dest'],
                         cfg[build][pad])

def build_basetools():
    build_message(f'building: BaseTools')
    basedir = os.environ['EDK_TOOLS_PATH']
    cmdline = [ 'make', '-C', basedir ]
    build_run(cmdline, 'BaseTools')

def binary_exists(name):
    for dir in os.environ['PATH'].split(':'):
        if os.path.exists(dir + '/' + name):
            return True
    return False

def prepare_env(cfg):
    """ mimic Conf/BuildEnv.sh """
    workspace = os.getcwd()
    packages = [ workspace, ]
    path = os.environ['PATH'].split(':')
    dirs = [
        'BaseTools/Bin/Linux-x86_64',
        'BaseTools/BinWrappers/PosixLike'
    ]

    coredir = get_coredir(cfg)
    if coredir != workspace:
        packages.append(coredir)
    if cfg.has_option('global', 'pkgs'):
        for pkgdir in cfg['global']['pkgs'].split():
            packages.append(os.path.abspath(pkgdir))

    # add basetools to path
    for dir in dirs:
        p = coredir + '/' + dir
        if not os.path.exists(p):
            continue
        if p in path:
            continue
        path.insert(0, p)

    # run edksetup if needed
    toolsdef = coredir + '/Conf/tools_def.txt';
    if not os.path.exists(toolsdef):
        build_message('running edksetup')
        cmdline = [ 'sh', 'edksetup.sh' ]
        subprocess.run(cmdline, cwd = coredir)

    # set variables
    os.environ['PATH'] = ':'.join(path)
    os.environ['PACKAGES_PATH'] = ':'.join(packages)
    os.environ['WORKSPACE'] = workspace
    os.environ['EDK_TOOLS_PATH'] = coredir + '/BaseTools'
    os.environ['CONF_PATH'] = coredir + '/Conf'
    os.environ['PYTHON_COMMAND'] = '/usr/bin/python3'

    # for cross builds
    if binary_exists('arm-linux-gnu-gcc'):
        os.environ['GCC5_ARM_PREFIX'] = 'arm-linux-gnu-'
    if binary_exists('aarch64-linux-gnu-gcc'):
        os.environ['GCC5_AARCH64_PREFIX'] = 'aarch64-linux-gnu-'
    if binary_exists('x86_64-linux-gnu-gcc'):
        os.environ['GCC5_IA32_PREFIX'] = 'x86_64-linux-gnu-'
        os.environ['GCC5_X64_PREFIX'] = 'x86_64-linux-gnu-'

def build_list(cfg):
    for build in cfg.sections():
        if not build.startswith('build.'):
            continue
        name = build.lstrip('build.')
        desc = 'no description'
        if 'desc' in cfg[build]:
            desc = cfg[build]['desc']
        print(f'# {name:20s} - {desc}')
    
def main():
    parser = optparse.OptionParser()
    parser.add_option('-c', '--config', dest = 'configfile',
                      type = 'string', default = '.edk2.builds')
    parser.add_option('-j', '--jobs', dest = 'jobs', type = 'string')
    parser.add_option('-m', '--match', dest = 'match', type = 'string')
    parser.add_option('-l', '--list', dest = 'list', action = 'store_true')
    parser.add_option('--core', dest = 'core', type = 'string')
    parser.add_option('--version-override', dest = 'version_override', type = 'string')
    (options, args) = parser.parse_args()

    cfg = configparser.ConfigParser()
    cfg.read(options.configfile)

    if options.list:
        build_list(cfg)
        return

    if not cfg.has_section('global'):
        cfg.add_section('global')
    if options.core:
        cfg.set('global', 'core', options.core)

    check_rebase()
    if options.version_override:
        version_override = options.version_override

    prepare_env(cfg)
    build_basetools()
    for build in cfg.sections():
        if not build.startswith('build.'):
            continue
        if options.match and options.match not in build:
            print(f'# skipping "{build}" (not matching "{options.match}")')
            continue
        build_one(cfg, build, options.jobs)

if __name__ == '__main__':
    sys.exit(main())
