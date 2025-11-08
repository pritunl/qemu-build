# qemu-build

Build source for Pritunl KVM repository, provides updated QEMU for RHEL10.

```bash
# stable repository
sudo tee /etc/yum.repos.d/pritunl-kvm.repo << EOF
[pritunl-kvm]
name=Pritunl KVM Repository
baseurl=https://repo.pritunl.com/kvm-stable/yum/oraclelinux/10/
gpgcheck=1
enabled=1
gpgkey=https://raw.githubusercontent.com/pritunl/pgp/master/pritunl_kvm_repo_pub.asc
EOF

# unstable repository
sudo tee /etc/yum.repos.d/pritunl-kvm.repo << EOF
[pritunl-kvm]
name=Pritunl KVM Repository
baseurl=https://repo.pritunl.com/kvm-unstable/yum/oraclelinux/10/
gpgcheck=1
enabled=1
gpgkey=https://raw.githubusercontent.com/pritunl/pgp/master/pritunl_kvm_repo_pub.asc
EOF

# stable gui repository
sudo tee /etc/yum.repos.d/pritunl-kvm.repo << EOF
[pritunl-kvm]
name=Pritunl KVM GUI Repository
baseurl=https://repo.pritunl.com/kvm-gui-stable/yum/oraclelinux/10/
gpgcheck=1
enabled=1
gpgkey=https://raw.githubusercontent.com/pritunl/pgp/master/pritunl_kvm_repo_pub.asc
EOF

# unstable gui repository
sudo tee /etc/yum.repos.d/pritunl-kvm.repo << EOF
[pritunl-kvm]
name=Pritunl KVM GUI Repository
baseurl=https://repo.pritunl.com/kvm-gui-unstable/yum/oraclelinux/10/
gpgcheck=1
enabled=1
gpgkey=https://raw.githubusercontent.com/pritunl/pgp/master/pritunl_kvm_repo_pub.asc
EOF
```

## prepare build

```bash
sudo dnf -y update
sudo dnf -y remove cockpit cockpit-ws
sudo dnf -y install rpm-build rpm-sign createrepo wget nano git podman
sudo dnf -y install seabios seabios-bin seavgabios-bin
sudo dnf -y groupinstall 'Development Tools'
sudo dnf config-manager --enable ol10_codeready_builder
```

## upgrade spec

```bash
wget https://download-ib01.fedoraproject.org/pub/fedora/linux/releases/43/Everything/source/tree/Packages/v/virglrenderer-1.2.0-2.fc43.src.rpm
wget https://download-ib01.fedoraproject.org/pub/fedora/linux/releases/43/Everything/source/tree/Packages/q/qemu-sanity-check-1.1.6-20.fc43.src.rpm

sudo rpm -i virglrenderer-1.2.0-2.fc43.src.rpm
sudo rpm -i qemu-sanity-check-1.1.6-20.fc43.src.rpm

sudo mv /root/rpmbuild ~/rpmbuild
sudo chown -R 1000:1000 ~/rpmbuild

scp /home/cloud/git/qemu-build/SOURCES/gpgkey-CEACC9E15534EBABB82D3FA03353C9CEF108B584.gpg cloud@$BUILD_SERVER:/home/cloud/rpmbuild/SOURCES/
scp /home/cloud/git/qemu-build/SOURCES/vhost.conf cloud@$BUILD_SERVER:/home/cloud/rpmbuild/SOURCES/
scp /home/cloud/git/qemu-build/SOURCES/kvm-x86.conf cloud@$BUILD_SERVER:/home/cloud/rpmbuild/SOURCES/
scp /home/cloud/git/qemu-build/SPECS/qemu.spec cloud@$BUILD_SERVER:/home/cloud/rpmbuild/SPECS/qemu.spec

rm -f /home/cloud/git/qemu-build/SRPMS/*
rsync --human-readable --archive --xattrs --progress --delete --exclude=.git \
    cloud@$BUILD_SERVER:/home/cloud/*.rpm /home/cloud/git/qemu-build/SRPMS/
rsync --human-readable --archive --xattrs --progress --delete --exclude=.git \
    cloud@$BUILD_SERVER:/home/cloud/rpmbuild/SOURCES/ /home/cloud/git/qemu-build/SOURCES/
rsync --human-readable --archive --xattrs --progress --exclude=.git \
    cloud@$BUILD_SERVER:/home/cloud/rpmbuild/SPECS/ /home/cloud/git/qemu-build/SPECS/
```

## build spec

```bash
rsync --human-readable --archive --xattrs --progress --delete --exclude=.git \
    /home/cloud/git/qemu-build/ cloud@$BUILD_SERVER:/home/cloud/rpmbuild/

cd ~/rpmbuild/SOURCES/
wget https://download.qemu.org/qemu-10.1.2.tar.xz
wget https://download.qemu.org/qemu-10.1.2.tar.xz.sig

cd ~/rpmbuild/SPECS/

sudo dnf builddep ~/rpmbuild/SPECS/qemu-sanity-check.spec
rpmbuild -ba qemu-sanity-check.spec
sudo dnf install ~/rpmbuild/RPMS/x86_64/qemu-sanity-check-nodeps-*.el10.x86_64.rpm

sudo dnf builddep ~/rpmbuild/SPECS/virglrenderer.spec
rpmbuild -ba virglrenderer.spec
sudo dnf install ~/rpmbuild/RPMS/x86_64/virglrenderer-1*.el10.x86_64.rpm ~/rpmbuild/RPMS/x86_64/virglrenderer-devel-*.el10.x86_64.rpm

sed -i 's/%global have_gtk 0/%global have_gtk 1/' ./qemu.spec
sudo dnf builddep ~/rpmbuild/SPECS/qemu.spec
rpmbuild -ba qemu.spec
```

## create repo

```bash
cd ~/rpmbuild/TOOLS
sudo podman build --rm -t tools .
cd
gpg --batch --allow-secret-key-import --import kvm_sign.key
rm kvm_sign.key

tee ~/gpg.conf << EOF
%no-protection
Key-Type: 1
Key-Length: 4096
Subkey-Type: 1
Subkey-Length: 4096
Name-Real: Pritunl Qemu
Name-Email: qemu@pritunl.com
Expire-Date: 0
%commit
EOF

tee ~/.rpmmacros << EOF
%_signature gpg
%_gpg_name kvm@pritunl.com
EOF

# kvm mirror
mkdir -p ~/mirror/yum/oraclelinux/10
rpm --resign rpmbuild/RPMS/noarch/*.rpm
rpm --resign rpmbuild/RPMS/x86_64/*.rpm
cp rpmbuild/RPMS/noarch/* ~/mirror/yum/oraclelinux/10
cp rpmbuild/RPMS/x86_64/* ~/mirror/yum/oraclelinux/10
rm ~/mirror/yum/oraclelinux/10/*debuginfo*
rm ~/mirror/yum/oraclelinux/10/*debugsource*
createrepo ~/mirror/yum/oraclelinux/10

# kvm gui mirror
mkdir -p ~/mirror-gui/yum/oraclelinux/10
rpm --resign rpmbuild/RPMS/noarch/*.rpm
rpm --resign rpmbuild/RPMS/x86_64/*.rpm
cp rpmbuild/RPMS/noarch/* ~/mirror-gui/yum/oraclelinux/10
cp rpmbuild/RPMS/x86_64/* ~/mirror-gui/yum/oraclelinux/10
rm ~/mirror-gui/yum/oraclelinux/10/*debuginfo*
rm ~/mirror-gui/yum/oraclelinux/10/*debugsource*
createrepo ~/mirror-gui/yum/oraclelinux/10

## kvm upload

```bash
python3 ~/rpmbuild/TOOLS/autoindex.py mirror kvm-unstable
sudo podman run --rm -v /home/cloud/.mc:/root/.mc:Z localhost/tools rm -r --force vultr-east/repo.pritunl.com/kvm-unstable
sudo podman run --rm -v /home/cloud/.mc:/root/.mc:Z localhost/tools rm -r --force r2/pritunl-repo-east/kvm-unstable
sudo podman run --rm -v /home/cloud/.mc:/root/.mc:Z localhost/tools rm -r --force r2/pritunl-repo-west/kvm-unstable
sudo podman run --rm -v /home/cloud/.mc:/root/.mc:Z -v /home/cloud/mirror:/mirror:Z localhost/tools mirror --summary --remove --overwrite --md5 --retry --checksum=MD5 --disable-multipart /mirror vultr-east/repo.pritunl.com/kvm-unstable
sudo podman run --rm -v /home/cloud/.mc:/root/.mc:Z -v /home/cloud/mirror:/mirror:Z localhost/tools mirror --summary --remove --overwrite --md5 --retry --checksum=MD5 --disable-multipart /mirror r2/pritunl-repo-east/kvm-unstable
sudo podman run --rm -v /home/cloud/.mc:/root/.mc:Z -v /home/cloud/mirror:/mirror:Z localhost/tools mirror --summary --remove --overwrite --md5 --retry --checksum=MD5 --disable-multipart /mirror r2/pritunl-repo-west/kvm-unstable

python3 ~/rpmbuild/TOOLS/autoindex.py mirror kvm-stable
sudo podman run --rm -v /home/cloud/.mc:/root/.mc:Z localhost/tools rm -r --force vultr-east/repo.pritunl.com/kvm-stable
sudo podman run --rm -v /home/cloud/.mc:/root/.mc:Z localhost/tools rm -r --force r2/pritunl-repo-east/kvm-stable
sudo podman run --rm -v /home/cloud/.mc:/root/.mc:Z localhost/tools rm -r --force r2/pritunl-repo-west/kvm-stable
sudo podman run --rm -v /home/cloud/.mc:/root/.mc:Z -v /home/cloud/mirror:/mirror:Z localhost/tools mirror --summary --remove --overwrite --md5 --retry --checksum=MD5 --disable-multipart /mirror vultr-east/repo.pritunl.com/kvm-stable
sudo podman run --rm -v /home/cloud/.mc:/root/.mc:Z -v /home/cloud/mirror:/mirror:Z localhost/tools mirror --summary --remove --overwrite --md5 --retry --checksum=MD5 --disable-multipart /mirror r2/pritunl-repo-east/kvm-stable
sudo podman run --rm -v /home/cloud/.mc:/root/.mc:Z -v /home/cloud/mirror:/mirror:Z localhost/tools mirror --summary --remove --overwrite --md5 --retry --checksum=MD5 --disable-multipart /mirror r2/pritunl-repo-west/kvm-stable
```

## kvm gui upload

```bash
python3 ~/rpmbuild/TOOLS/autoindex.py mirror-gui kvm-gui-unstable
sudo podman run --rm -v /home/cloud/.mc:/root/.mc:Z localhost/tools rm -r --force vultr-east/repo.pritunl.com/kvm-gui-unstable
sudo podman run --rm -v /home/cloud/.mc:/root/.mc:Z localhost/tools rm -r --force r2/pritunl-repo-east/kvm-gui-unstable
sudo podman run --rm -v /home/cloud/.mc:/root/.mc:Z localhost/tools rm -r --force r2/pritunl-repo-west/kvm-gui-unstable
sudo podman run --rm -v /home/cloud/.mc:/root/.mc:Z -v /home/cloud/mirror-gui:/mirror:Z localhost/tools mirror --summary --remove --overwrite --md5 --retry --checksum=MD5 --disable-multipart /mirror vultr-east/repo.pritunl.com/kvm-gui-unstable
sudo podman run --rm -v /home/cloud/.mc:/root/.mc:Z -v /home/cloud/mirror-gui:/mirror:Z localhost/tools mirror --summary --remove --overwrite --md5 --retry --checksum=MD5 --disable-multipart /mirror r2/pritunl-repo-east/kvm-gui-unstable
sudo podman run --rm -v /home/cloud/.mc:/root/.mc:Z -v /home/cloud/mirror-gui:/mirror:Z localhost/tools mirror --summary --remove --overwrite --md5 --retry --checksum=MD5 --disable-multipart /mirror r2/pritunl-repo-west/kvm-gui-unstable

python3 ~/rpmbuild/TOOLS/autoindex.py mirror-gui kvm-gui-stable
sudo podman run --rm -v /home/cloud/.mc:/root/.mc:Z localhost/tools rm -r --force vultr-east/repo.pritunl.com/kvm-gui-stable
sudo podman run --rm -v /home/cloud/.mc:/root/.mc:Z localhost/tools rm -r --force r2/pritunl-repo-east/kvm-gui-stable
sudo podman run --rm -v /home/cloud/.mc:/root/.mc:Z localhost/tools rm -r --force r2/pritunl-repo-west/kvm-gui-stable
sudo podman run --rm -v /home/cloud/.mc:/root/.mc:Z -v /home/cloud/mirror-gui:/mirror:Z localhost/tools mirror --summary --remove --overwrite --md5 --retry --checksum=MD5 --disable-multipart /mirror vultr-east/repo.pritunl.com/kvm-gui-stable
sudo podman run --rm -v /home/cloud/.mc:/root/.mc:Z -v /home/cloud/mirror-gui:/mirror:Z localhost/tools mirror --summary --remove --overwrite --md5 --retry --checksum=MD5 --disable-multipart /mirror r2/pritunl-repo-east/kvm-gui-stable
sudo podman run --rm -v /home/cloud/.mc:/root/.mc:Z -v /home/cloud/mirror-gui:/mirror:Z localhost/tools mirror --summary --remove --overwrite --md5 --retry --checksum=MD5 --disable-multipart /mirror r2/pritunl-repo-west/kvm-gui-stable
```

# qemu features

```
qemu 10.1.2

  Build environment
    Build directory                 : /home/cloud/rpmbuild/BUILD/qemu-10.1.2/qemu_kvm_build
    Source path                     : /home/cloud/rpmbuild/BUILD/qemu-10.1.2
    Download dependencies           : NO

  Directories
    Build directory                 : /home/cloud/rpmbuild/BUILD/qemu-10.1.2/qemu_kvm_build
    Source path                     : /home/cloud/rpmbuild/BUILD/qemu-10.1.2
    Download dependencies           : NO
    Install prefix                  : /usr
    BIOS directory                  : share/qemu
    firmware path                   : /usr/share/qemu-firmware:/usr/share/ipxe/qemu:/usr/share/seavgabios:/usr/share/seabios
    binary directory                : /usr/bin
    library directory               : /usr/lib64
    module directory                : lib64/qemu
    libexec directory               : /usr/libexec
    include directory               : /usr/include
    config directory                : /etc
    local state directory           : /var
    Manual directory                : /usr/share/man
    Doc directory                   : /usr/share/doc

  Host binaries
    python                          : /home/cloud/rpmbuild/BUILD/qemu-10.1.2/qemu_kvm_build/pyvenv/bin/python3 (version: 3.12)
    sphinx-build                    : /home/cloud/rpmbuild/BUILD/qemu-10.1.2/qemu_kvm_build/pyvenv/bin/sphinx-build
    gdb                             : /usr/bin/gdb
    iasl                            : NO
    genisoimage                     :
    smbd                            : /usr/sbin/smbd

  Configurable features
    Documentation                   : YES
    system-mode emulation           : YES
    user-mode emulation             : NO
    block layer                     : YES
    Install blobs                   : YES
    module support                  : YES
    alternative module path         : NO
    fuzzing support                 : NO
    Audio drivers                   :
    Trace backends                  : log
    QOM debugging                   : NO
    Relocatable install             : NO
    vhost-kernel support            : YES
    vhost-net support               : YES
    vhost-user support              : YES
    vhost-user-crypto support       : YES
    vhost-user-blk server support   : YES
    vhost-vdpa support              : YES
    build guest agent               : NO

  Compilation
    host CPU                        : x86_64
    host endianness                 : little
    C compiler                      : clang -m64
    Host C compiler                 : clang -m64
    C++ compiler                    : NO
    Objective-C compiler            : NO
    Rust support                    : NO
    CFLAGS                          : -O2 -flto=thin -fexceptions -g -grecord-gcc-switches -pipe -Wall -Werror=format-security -Wp,-U_FORTIFY_SOURCE,-D_FORTIFY_SOURCE=3 -Wp,-D_GLIBCXX_ASSERTIONS --config=/usr/lib/rpm/redhat/redhat-hardened-clang.cfg -fstack-protector-strong -m64 -march=x86-64-v3 -mtune=generic -fasynchronous-unwind-tables -fstack-clash-protection -fcf-protection -O2 -flto=thin -fexceptions -g -grecord-gcc-switches -pipe -Wall -Werror=format-security -Wp,-U_FORTIFY_SOURCE,-D_FORTIFY_SOURCE=3 -Wp,-D_GLIBCXX_ASSERTIONS --config=/usr/lib/rpm/redhat/redhat-hardened-clang.cfg -fstack-protector-strong -m64 -march=x86-64-v3 -mtune=generic -fasynchronous-unwind-tables -fstack-clash-protection -fcf-protection -g -O2
    LDFLAGS                         : -O2 -flto=thin -fexceptions -g -grecord-gcc-switches -pipe -Wall -Werror=format-security -Wp,-U_FORTIFY_SOURCE,-D_FORTIFY_SOURCE=3 -Wp,-D_GLIBCXX_ASSERTIONS --config=/usr/lib/rpm/redhat/redhat-hardened-clang.cfg -fstack-protector-strong -m64 -march=x86-64-v3 -mtune=generic -fasynchronous-unwind-tables -fstack-clash-protection -fcf-protection -Wl,-z,relro -Wl,--as-needed -Wl,-z,pack-relative-relocs -Wl,-z,now --config=/usr/lib/rpm/redhat/redhat-hardened-clang-ld.cfg -flto=thin -Wl,--build-id=sha1 -O2 -flto=thin -fexceptions -g -grecord-gcc-switches -pipe -Wall -Werror=format-security -Wp,-U_FORTIFY_SOURCE,-D_FORTIFY_SOURCE=3 -Wp,-D_GLIBCXX_ASSERTIONS --config=/usr/lib/rpm/redhat/redhat-hardened-clang.cfg -fstack-protector-strong -m64 -march=x86-64-v3 -mtune=generic -fasynchronous-unwind-tables -fstack-clash-protection -fcf-protection -Wl,-z,relro -Wl,--as-needed -Wl,-z,pack-relative-relocs -Wl,-z,now --config=/usr/lib/rpm/redhat/redhat-hardened-clang-ld.cfg -flto=thin -Wl,--build-id=sha1
    QEMU_CFLAGS                     : -mcx16 -msse2 -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -fno-strict-aliasing -fno-common -fwrapv -ftrivial-auto-var-init=zero -fzero-call-used-regs=used-gpr -fstack-protector-strong -fsanitize=safe-stack
    QEMU_LDFLAGS                    : -fstack-protector-strong -fsanitize=safe-stack -Wl,-z,relro -Wl,-z,now
    link-time optimization (LTO)    : YES
    PIE                             : YES
    static build                    : NO
    malloc trim support             : YES
    membarrier                      : NO
    debug graph lock                : NO
    debug stack usage               : NO
    mutex debugging                 : NO
    memory allocator                : system
    avx2 optimization               : YES
    avx512bw optimization           : YES
    gcov                            : NO
    thread sanitizer                : NO
    CFI support                     : NO
    strip binaries                  : NO
    sparse                          : NO
    mingw32 support                 : NO

  Cross compilers
    x86_64                          : /home/cloud/rpmbuild/BUILD/qemu-10.1.2/qemu_kvm_build/pyvenv/bin/python3 -B /home/cloud/rpmbuild/BUILD/qemu-10.1.2/tests/docker/docker.py --engine podman cc --cc x86_64-linux-gnu-gcc -i qemu/debian-amd64-cross -s /home/cloud/rpmbuild/BUILD/qemu-10.1.2 --

  Targets and accelerators
    KVM support                     : YES
    HVF support                     : NO
    WHPX support                    : NO
    NVMM support                    : NO
    Xen support                     : NO
    Xen emulation                   : YES
    TCG support                     : YES
    TCG backend                     : native (x86_64)
    TCG plugins                     : NO
    TCG debug enabled               : NO
    target list                     : x86_64-softmmu
    default devices                 : YES
    out of process emulation        : YES
    vfio-user server                : NO

  Block layer support
    coroutine backend               : ucontext
    coroutine pool                  : YES
    Block whitelist (rw)            :
    Block whitelist (ro)            :
    Use block whitelist in tools    : NO
    VirtFS (9P) support             : YES
    replication support             : YES
    bochs support                   : NO
    cloop support                   : NO
    dmg support                     : NO
    qcow v1 support                 : NO
    vdi support                     : YES
    vhdx support                    : NO
    vmdk support                    : YES
    vpc support                     : NO
    vvfat support                   : NO
    qed support                     : NO
    parallels support               : NO
    FUSE exports                    : NO
    VDUSE block exports             : YES

  Crypto
    TLS priority                    : @QEMU,SYSTEM
    GNUTLS support                  : YES 3.8.9
      GNUTLS crypto                 : YES
      GNUTLS bug 1717 workaround    : NO
    libgcrypt                       : NO
    nettle                          : NO
    SM4 ALG support                 : NO
    SM3 ALG support                 : NO
    AF_ALG support                  : NO
    rng-none                        : NO
    Linux keyring                   : YES
    Linux keyutils                  : YES 1.6.3

  User interface
    D-Bus display                   : YES
    SDL support                     : NO
    SDL image support               : NO
    GTK support                     : NO
    pixman                          : YES 0.43.4
    VTE support                     : NO
    PNG support                     : YES 1.6.40
    VNC support                     : YES
    VNC SASL support                : YES
    VNC JPEG support                : YES 3.0.2
    spice protocol support          : YES 0.14.4
      spice server support          : NO
    curses support                  : NO
    brlapi support                  : NO

  Graphics backends
    VirGL support                   : YES 1.2.0
    Rutabaga support                : NO

  Audio backends
    OSS support                     : NO
    sndio support                   : NO
    ALSA support                    : NO
    PulseAudio support              : YES 17.0
    PipeWire support                : NO
    JACK support                    : NO

  Network backends
    AF_XDP support                  : YES 1.5.5
    passt support                   : NO
    slirp support                   : YES 4.7.0
    vde support                     : NO
    netmap support                  : NO
    l2tpv3 support                  : YES

  Dependencies
    libtasn1                        : YES 4.20.0
    PAM                             : NO
    iconv support                   : NO
    blkio support                   : YES 1.5.0
    curl support                    : NO
    Multipath support               : YES
    Linux AIO support               : YES
    Linux io_uring support          : YES 2.5
    ATTR/XATTR support              : YES
    RDMA support                    : YES
    fdt support                     : YES
    libcap-ng support               : YES
    bpf support                     : YES 1.5.0
    rbd support                     : NO
    smartcard support               : NO
    U2F support                     : NO
    libusb                          : YES 1.0.27
    usb net redir                   : YES 0.13.0
    OpenGL support (epoxy)          : YES 1.5.10
    GBM                             : YES 24.2.8
    libiscsi support                : NO
    libnfs support                  : NO
    seccomp support                 : YES 2.5.3
    GlusterFS support               : NO
    hv-balloon support              : NO
    TPM support                     : YES
    IGVM support                    : NO
    libssh support                  : NO
    lzo support                     : YES
    snappy support                  : YES
    bzip2 support                   : YES
    lzfse support                   : NO
    zstd support                    : YES 1.5.5
    Query Processing Library support: NO
    UADK Library support            : NO
    qatzip support                  : NO
    NUMA host support               : YES
    capstone                        : YES 5.0.1
    libpmem support                 : NO
    libdaxctl support               : YES 80
    libcbor support                 : NO
    libudev                         : YES 257
    FUSE lseek                      : NO
    selinux                         : YES 3.8
    libdw                           : NO
    valgrind                        : NO

  Subprojects
    berkeley-softfloat-3            : YES
    berkeley-testfloat-3            : YES
    keycodemapdb                    : YES
    libvduse                        : YES
    libvhost-user                   : YES

  User defined options
    Native files                    : config-meson.cross
    af_xdp                          : enabled
    alsa                            : disabled
    asan                            : false
    attr                            : enabled
    audio_drv_list                  :
    auth_pam                        : disabled
    b_lto                           : true
    blkio                           : enabled
    block_drv_whitelist_in_tools    : false
    bochs                           : disabled
    bpf                             : enabled
    brlapi                          : disabled
    bzip2                           : enabled
    cap_ng                          : enabled
    capstone                        : enabled
    cfi_debug                       : false
    cloop                           : disabled
    cocoa                           : disabled
    colo_proxy                      : disabled
    coreaudio                       : disabled
    coroutine_backend               : ucontext
    coroutine_pool                  : true
    crypto_afalg                    : disabled
    curl                            : disabled
    curses                          : disabled
    datadir                         : /usr/share
    dbus_display                    : enabled
    debug                           : true
    debug_graph_lock                : false
    debug_mutex                     : false
    debug_remap                     : false
    debug_tcg                       : false
    default_devices                 : true
    dmg                             : disabled
    docdir                          : /usr/share/doc
    docs                            : enabled
    dsound                          : disabled
    fdt                             : system
    fuse                            : disabled
    fuse_lseek                      : disabled
    gcrypt                          : disabled
    gettext                         : disabled
    gio                             : enabled
    glusterfs                       : disabled
    gnutls                          : enabled
    gtk                             : disabled
    gtk_clipboard                   : disabled
    guest_agent                     : disabled
    guest_agent_msi                 : disabled
    hv_balloon                      : disabled
    hvf                             : disabled
    iconv                           : enabled
    igvm                            : disabled
    interp_prefix                   : /usr/qemu-%M
    jack                            : disabled
    kvm                             : enabled
    l2tpv3                          : enabled
    libcbor                         : disabled
    libdaxctl                       : enabled
    libdir                          : /usr/lib64
    libdw                           : disabled
    libexecdir                      : /usr/libexec
    libiscsi                        : disabled
    libkeyutils                     : enabled
    libnfs                          : disabled
    libpmem                         : disabled
    libssh                          : disabled
    libudev                         : enabled
    libusb                          : enabled
    linux_aio                       : enabled
    linux_io_uring                  : enabled
    localstatedir                   : /var
    lzfse                           : disabled
    lzo                             : enabled
    malloc_trim                     : enabled
    membarrier                      : disabled
    module_upgrades                 : false
    modules                         : enabled
    mpath                           : enabled
    multiprocess                    : enabled
    netmap                          : disabled
    nettle                          : disabled
    numa                            : enabled
    nvmm                            : disabled
    opengl                          : enabled
    oss                             : disabled
    pa                              : enabled
    parallels                       : disabled
    passt                           : disabled
    pipewire                        : disabled
    pixman                          : enabled
    pkgversion                      : qemu-10.1.2-12.el10
    png                             : enabled
    prefix                          : /usr
    pvg                             : disabled
    qcow1                           : disabled
    qed                             : disabled
    qemu_firmwarepath               : ["""/usr/share/qemu-firmware""","""/usr/share/ipxe/qemu""","""/usr/share/seavgabios""","""/usr/share/seabios""",]
    qemu_suffix                     : qemu
    qom_cast_debug                  : false
    qpl                             : disabled
    rbd                             : disabled
    rdma                            : enabled
    relocatable                     : false
    replication                     : enabled
    rng_none                        : false
    rutabaga_gfx                    : disabled
    safe_stack                      : true
    sdl                             : disabled
    sdl_image                       : disabled
    seccomp                         : enabled
    selinux                         : enabled
    slirp                           : enabled
    slirp_smbd                      : enabled
    smartcard                       : disabled
    snappy                          : enabled
    sndio                           : disabled
    sparse                          : disabled
    spice                           : disabled
    spice_protocol                  : enabled
    strict_rust_lints               : false
    strip                           : false
    sysconfdir                      : /etc
    tls_priority                    : @QEMU,SYSTEM
    tools                           : enabled
    tpm                             : enabled
    tsan                            : false
    u2f                             : disabled
    uadk                            : disabled
    ubsan                           : false
    usb_redir                       : enabled
    valgrind                        : disabled
    vde                             : disabled
    vdi                             : enabled
    vfio_user_server                : disabled
    vhdx                            : disabled
    vhost_crypto                    : enabled
    vhost_kernel                    : enabled
    vhost_net                       : enabled
    vhost_user                      : enabled
    vhost_user_blk_server           : enabled
    vhost_vdpa                      : enabled
    virglrenderer                   : enabled
    virtfs                          : enabled
    vnc                             : enabled
    vnc_jpeg                        : enabled
    vnc_sasl                        : enabled
    vpc                             : disabled
    vte                             : disabled
    vvfat                           : disabled
    werror                          : false
    whpx                            : disabled
    wrap_mode                       : nodownload
    xen                             : disabled
    xen_pci_passthrough             : disabled
    xkbcommon                       : enabled
    zstd                            : enabled
```

# qemu gui features

```
qemu 10.1.2

  Build environment
    Build directory                 : /home/cloud/rpmbuild/BUILD/qemu-10.1.2/qemu_kvm_build
    Source path                     : /home/cloud/rpmbuild/BUILD/qemu-10.1.2
    Download dependencies           : NO

  Directories
    Build directory                 : /home/cloud/rpmbuild/BUILD/qemu-10.1.2/qemu_kvm_build
    Source path                     : /home/cloud/rpmbuild/BUILD/qemu-10.1.2
    Download dependencies           : NO
    Install prefix                  : /usr
    BIOS directory                  : share/qemu
    firmware path                   : /usr/share/qemu-firmware:/usr/share/ipxe/qemu:/usr/share/seavgabios:/usr/share/seabios
    binary directory                : /usr/bin
    library directory               : /usr/lib64
    module directory                : lib64/qemu
    libexec directory               : /usr/libexec
    include directory               : /usr/include
    config directory                : /etc
    local state directory           : /var
    Manual directory                : /usr/share/man
    Doc directory                   : /usr/share/doc

  Host binaries
    python                          : /home/cloud/rpmbuild/BUILD/qemu-10.1.2/qemu_kvm_build/pyvenv/bin/python3 (version: 3.12)
    sphinx-build                    : /home/cloud/rpmbuild/BUILD/qemu-10.1.2/qemu_kvm_build/pyvenv/bin/sphinx-build
    gdb                             : /usr/bin/gdb
    iasl                            : NO
    genisoimage                     :
    smbd                            : /usr/sbin/smbd

  Configurable features
    Documentation                   : YES
    system-mode emulation           : YES
    user-mode emulation             : NO
    block layer                     : YES
    Install blobs                   : YES
    module support                  : YES
    alternative module path         : NO
    fuzzing support                 : NO
    Audio drivers                   :
    Trace backends                  : log
    QOM debugging                   : NO
    Relocatable install             : NO
    vhost-kernel support            : YES
    vhost-net support               : YES
    vhost-user support              : YES
    vhost-user-crypto support       : YES
    vhost-user-blk server support   : YES
    vhost-vdpa support              : YES
    build guest agent               : NO

  Compilation
    host CPU                        : x86_64
    host endianness                 : little
    C compiler                      : clang -m64
    Host C compiler                 : clang -m64
    C++ compiler                    : NO
    Objective-C compiler            : NO
    Rust support                    : NO
    CFLAGS                          : -O2 -flto=thin -fexceptions -g -grecord-gcc-switches -pipe -Wall -Werror=format-security -Wp,-U_FORTIFY_SOURCE,-D_FORTIFY_SOURCE=3 -Wp,-D_GLIBCXX_ASSERTIONS --config=/usr/lib/rpm/redhat/redhat-hardened-clang.cfg -fstack-protector-strong -m64 -march=x86-64-v3 -mtune=generic -fasynchronous-unwind-tables -fstack-clash-protection -fcf-protection -O2 -flto=thin -fexceptions -g -grecord-gcc-switches -pipe -Wall -Werror=format-security -Wp,-U_FORTIFY_SOURCE,-D_FORTIFY_SOURCE=3 -Wp,-D_GLIBCXX_ASSERTIONS --config=/usr/lib/rpm/redhat/redhat-hardened-clang.cfg -fstack-protector-strong -m64 -march=x86-64-v3 -mtune=generic -fasynchronous-unwind-tables -fstack-clash-protection -fcf-protection -g -O2
    LDFLAGS                         : -O2 -flto=thin -fexceptions -g -grecord-gcc-switches -pipe -Wall -Werror=format-security -Wp,-U_FORTIFY_SOURCE,-D_FORTIFY_SOURCE=3 -Wp,-D_GLIBCXX_ASSERTIONS --config=/usr/lib/rpm/redhat/redhat-hardened-clang.cfg -fstack-protector-strong -m64 -march=x86-64-v3 -mtune=generic -fasynchronous-unwind-tables -fstack-clash-protection -fcf-protection -Wl,-z,relro -Wl,--as-needed -Wl,-z,pack-relative-relocs -Wl,-z,now --config=/usr/lib/rpm/redhat/redhat-hardened-clang-ld.cfg -flto=thin -Wl,--build-id=sha1 -O2 -flto=thin -fexceptions -g -grecord-gcc-switches -pipe -Wall -Werror=format-security -Wp,-U_FORTIFY_SOURCE,-D_FORTIFY_SOURCE=3 -Wp,-D_GLIBCXX_ASSERTIONS --config=/usr/lib/rpm/redhat/redhat-hardened-clang.cfg -fstack-protector-strong -m64 -march=x86-64-v3 -mtune=generic -fasynchronous-unwind-tables -fstack-clash-protection -fcf-protection -Wl,-z,relro -Wl,--as-needed -Wl,-z,pack-relative-relocs -Wl,-z,now --config=/usr/lib/rpm/redhat/redhat-hardened-clang-ld.cfg -flto=thin -Wl,--build-id=sha1
    QEMU_CFLAGS                     : -mcx16 -msse2 -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -fno-strict-aliasing -fno-common -fwrapv -ftrivial-auto-var-init=zero -fzero-call-used-regs=used-gpr -fstack-protector-strong -fsanitize=safe-stack
    QEMU_LDFLAGS                    : -fstack-protector-strong -fsanitize=safe-stack -Wl,-z,relro -Wl,-z,now
    link-time optimization (LTO)    : YES
    PIE                             : YES
    static build                    : NO
    malloc trim support             : YES
    membarrier                      : NO
    debug graph lock                : NO
    debug stack usage               : NO
    mutex debugging                 : NO
    memory allocator                : system
    avx2 optimization               : YES
    avx512bw optimization           : YES
    gcov                            : NO
    thread sanitizer                : NO
    CFI support                     : NO
    strip binaries                  : NO
    sparse                          : NO
    mingw32 support                 : NO

  Cross compilers
    x86_64                          : /home/cloud/rpmbuild/BUILD/qemu-10.1.2/qemu_kvm_build/pyvenv/bin/python3 -B /home/cloud/rpmbuild/BUILD/qemu-10.1.2/tests/docker/docker.py --engine podman cc --cc x86_64-linux-gnu-gcc -i qemu/debian-amd64-cross -s /home/cloud/rpmbuild/BUILD/qemu-10.1.2 --

  Targets and accelerators
    KVM support                     : YES
    HVF support                     : NO
    WHPX support                    : NO
    NVMM support                    : NO
    Xen support                     : NO
    Xen emulation                   : YES
    TCG support                     : YES
    TCG backend                     : native (x86_64)
    TCG plugins                     : NO
    TCG debug enabled               : NO
    target list                     : x86_64-softmmu
    default devices                 : YES
    out of process emulation        : YES
    vfio-user server                : NO

  Block layer support
    coroutine backend               : ucontext
    coroutine pool                  : YES
    Block whitelist (rw)            :
    Block whitelist (ro)            :
    Use block whitelist in tools    : NO
    VirtFS (9P) support             : YES
    replication support             : YES
    bochs support                   : NO
    cloop support                   : NO
    dmg support                     : NO
    qcow v1 support                 : NO
    vdi support                     : YES
    vhdx support                    : NO
    vmdk support                    : YES
    vpc support                     : NO
    vvfat support                   : NO
    qed support                     : NO
    parallels support               : NO
    FUSE exports                    : NO
    VDUSE block exports             : YES

  Crypto
    TLS priority                    : @QEMU,SYSTEM
    GNUTLS support                  : YES 3.8.9
      GNUTLS crypto                 : YES
      GNUTLS bug 1717 workaround    : NO
    libgcrypt                       : NO
    nettle                          : NO
    SM4 ALG support                 : NO
    SM3 ALG support                 : NO
    AF_ALG support                  : NO
    rng-none                        : NO
    Linux keyring                   : YES
    Linux keyutils                  : YES 1.6.3

  User interface
    D-Bus display                   : YES
    SDL support                     : NO
    SDL image support               : NO
    GTK support                     : YES
    pixman                          : YES 0.43.4
    VTE support                     : NO
    PNG support                     : YES 1.6.40
    VNC support                     : YES
    VNC SASL support                : YES
    VNC JPEG support                : YES 3.0.2
    spice protocol support          : YES 0.14.4
      spice server support          : NO
    curses support                  : NO
    brlapi support                  : NO

  Graphics backends
    VirGL support                   : YES 1.2.0
    Rutabaga support                : NO

  Audio backends
    OSS support                     : NO
    sndio support                   : NO
    ALSA support                    : NO
    PulseAudio support              : YES 17.0
    PipeWire support                : NO
    JACK support                    : NO

  Network backends
    AF_XDP support                  : YES 1.5.5
    passt support                   : NO
    slirp support                   : YES 4.7.0
    vde support                     : NO
    netmap support                  : NO
    l2tpv3 support                  : YES

  Dependencies
    libtasn1                        : YES 4.20.0
    PAM                             : NO
    iconv support                   : NO
    blkio support                   : YES 1.5.0
    curl support                    : NO
    Multipath support               : YES
    Linux AIO support               : YES
    Linux io_uring support          : YES 2.5
    ATTR/XATTR support              : YES
    RDMA support                    : YES
    fdt support                     : YES
    libcap-ng support               : YES
    bpf support                     : YES 1.5.0
    rbd support                     : NO
    smartcard support               : NO
    U2F support                     : NO
    libusb                          : YES 1.0.27
    usb net redir                   : YES 0.13.0
    OpenGL support (epoxy)          : YES 1.5.10
    GBM                             : YES 24.2.8
    libiscsi support                : NO
    libnfs support                  : NO
    seccomp support                 : YES 2.5.3
    GlusterFS support               : NO
    hv-balloon support              : NO
    TPM support                     : YES
    IGVM support                    : NO
    libssh support                  : NO
    lzo support                     : YES
    snappy support                  : YES
    bzip2 support                   : YES
    lzfse support                   : NO
    zstd support                    : YES 1.5.5
    Query Processing Library support: NO
    UADK Library support            : NO
    qatzip support                  : NO
    NUMA host support               : YES
    capstone                        : YES 5.0.1
    libpmem support                 : NO
    libdaxctl support               : YES 80
    libcbor support                 : NO
    libudev                         : YES 257
    FUSE lseek                      : NO
    selinux                         : YES 3.8
    libdw                           : NO
    valgrind                        : NO

  Subprojects
    berkeley-softfloat-3            : YES
    berkeley-testfloat-3            : YES
    keycodemapdb                    : YES
    libvduse                        : YES
    libvhost-user                   : YES

  User defined options
    Native files                    : config-meson.cross
    af_xdp                          : enabled
    alsa                            : disabled
    asan                            : false
    attr                            : enabled
    audio_drv_list                  :
    auth_pam                        : disabled
    b_lto                           : true
    blkio                           : enabled
    block_drv_whitelist_in_tools    : false
    bochs                           : disabled
    bpf                             : enabled
    brlapi                          : disabled
    bzip2                           : enabled
    cap_ng                          : enabled
    capstone                        : enabled
    cfi_debug                       : false
    cloop                           : disabled
    cocoa                           : disabled
    colo_proxy                      : disabled
    coreaudio                       : disabled
    coroutine_backend               : ucontext
    coroutine_pool                  : true
    crypto_afalg                    : disabled
    curl                            : disabled
    curses                          : disabled
    datadir                         : /usr/share
    dbus_display                    : enabled
    debug                           : true
    debug_graph_lock                : false
    debug_mutex                     : false
    debug_remap                     : false
    debug_tcg                       : false
    default_devices                 : true
    dmg                             : disabled
    docdir                          : /usr/share/doc
    docs                            : enabled
    dsound                          : disabled
    fdt                             : system
    fuse                            : disabled
    fuse_lseek                      : disabled
    gcrypt                          : disabled
    gettext                         : disabled
    gio                             : enabled
    glusterfs                       : disabled
    gnutls                          : enabled
    gtk                             : enabled
    gtk_clipboard                   : disabled
    guest_agent                     : disabled
    guest_agent_msi                 : disabled
    hv_balloon                      : disabled
    hvf                             : disabled
    iconv                           : enabled
    igvm                            : disabled
    interp_prefix                   : /usr/qemu-%M
    jack                            : disabled
    kvm                             : enabled
    l2tpv3                          : enabled
    libcbor                         : disabled
    libdaxctl                       : enabled
    libdir                          : /usr/lib64
    libdw                           : disabled
    libexecdir                      : /usr/libexec
    libiscsi                        : disabled
    libkeyutils                     : enabled
    libnfs                          : disabled
    libpmem                         : disabled
    libssh                          : disabled
    libudev                         : enabled
    libusb                          : enabled
    linux_aio                       : enabled
    linux_io_uring                  : enabled
    localstatedir                   : /var
    lzfse                           : disabled
    lzo                             : enabled
    malloc_trim                     : enabled
    membarrier                      : disabled
    module_upgrades                 : false
    modules                         : enabled
    mpath                           : enabled
    multiprocess                    : enabled
    netmap                          : disabled
    nettle                          : disabled
    numa                            : enabled
    nvmm                            : disabled
    opengl                          : enabled
    oss                             : disabled
    pa                              : enabled
    parallels                       : disabled
    passt                           : disabled
    pipewire                        : disabled
    pixman                          : enabled
    pkgversion                      : qemu-10.1.2-12.el10
    png                             : enabled
    prefix                          : /usr
    pvg                             : disabled
    qcow1                           : disabled
    qed                             : disabled
    qemu_firmwarepath               : ["""/usr/share/qemu-firmware""","""/usr/share/ipxe/qemu""","""/usr/share/seavgabios""","""/usr/share/seabios""",]
    qemu_suffix                     : qemu
    qom_cast_debug                  : false
    qpl                             : disabled
    rbd                             : disabled
    rdma                            : enabled
    relocatable                     : false
    replication                     : enabled
    rng_none                        : false
    rutabaga_gfx                    : disabled
    safe_stack                      : true
    sdl                             : disabled
    sdl_image                       : disabled
    seccomp                         : enabled
    selinux                         : enabled
    slirp                           : enabled
    slirp_smbd                      : enabled
    smartcard                       : disabled
    snappy                          : enabled
    sndio                           : disabled
    sparse                          : disabled
    spice                           : disabled
    spice_protocol                  : enabled
    strict_rust_lints               : false
    strip                           : false
    sysconfdir                      : /etc
    tls_priority                    : @QEMU,SYSTEM
    tools                           : enabled
    tpm                             : enabled
    tsan                            : false
    u2f                             : disabled
    uadk                            : disabled
    ubsan                           : false
    usb_redir                       : enabled
    valgrind                        : disabled
    vde                             : disabled
    vdi                             : enabled
    vfio_user_server                : disabled
    vhdx                            : disabled
    vhost_crypto                    : enabled
    vhost_kernel                    : enabled
    vhost_net                       : enabled
    vhost_user                      : enabled
    vhost_user_blk_server           : enabled
    vhost_vdpa                      : enabled
    virglrenderer                   : enabled
    virtfs                          : enabled
    vnc                             : enabled
    vnc_jpeg                        : enabled
    vnc_sasl                        : enabled
    vpc                             : disabled
    vte                             : disabled
    vvfat                           : disabled
    werror                          : false
    whpx                            : disabled
    wrap_mode                       : nodownload
    xen                             : disabled
    xen_pci_passthrough             : disabled
    xkbcommon                       : enabled
    zstd                            : enabled
```
