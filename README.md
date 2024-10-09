# qemu-build

Build source for Pritunl KVM repository, provides updated QEMU for RHEL9.

```bash
# stable repository
sudo tee /etc/yum.repos.d/pritunl-kvm.repo << EOF
[pritunl-kvm]
name=Pritunl KVM Repository
baseurl=https://repo.pritunl.com/kvm-stable/oraclelinux/9/
gpgcheck=1
enabled=1
gpgkey=https://raw.githubusercontent.com/pritunl/pgp/master/pritunl_kvm_repo_pub.asc
EOF

# unstable repository
sudo tee /etc/yum.repos.d/pritunl-kvm.repo << EOF
[pritunl-kvm]
name=Pritunl KVM Repository
baseurl=https://repo.pritunl.com/kvm-unstable/oraclelinux/9/
gpgcheck=1
enabled=1
gpgkey=https://raw.githubusercontent.com/pritunl/pgp/master/pritunl_kvm_repo_pub.asc
EOF
```

# build

```bash
sudo /usr/libexec/oci-growfs

sudo dnf -y update
sudo dnf -y remove cockpit cockpit-ws
sudo dnf -y install rpm-build rpm-sign createrepo wget nano git
sudo dnf -y install seabios seabios-bin seavgabios-bin
sudo dnf -y groupinstall 'Development Tools'
sudo dnf config-manager --enable ol9_codeready_builder

sudo systemctl stop firewalld
sudo systemctl disable firewalld

wget https://download-ib01.fedoraproject.org/pub/fedora/linux/development/rawhide/Everything/source/tree/Packages/v/virglrenderer-1.1.0-1.fc42.src.rpm
wget https://download-ib01.fedoraproject.org/pub/fedora/linux/releases/40/Everything/source/tree/Packages/q/qemu-sanity-check-1.1.6-14.fc40.src.rpm

sudo rpm -i virglrenderer-1.1.0-1.fc42.src.rpm
sudo rpm -i qemu-sanity-check-1.1.6-14.fc40.src.rpm

sudo mv /root/rpmbuild ~/rpmbuild
sudo chown -R 1000:1000 ~/rpmbuild

rsync --human-readable --archive --xattrs --progress --delete --exclude=.git \
    cloud@123.123.123.123:/home/cloud/*.rpm /home/cloud/git/qemu-build/SRPMS/
rsync --human-readable --archive --xattrs --progress --delete --exclude=.git \
    cloud@123.123.123.123:/home/cloud/rpmbuild/SOURCES/ /home/cloud/git/qemu-build/SOURCES/
rsync --human-readable --archive --xattrs --progress --exclude=.git \
    cloud@123.123.123.123:/home/cloud/rpmbuild/SPECS/ /home/cloud/git/qemu-build/SPECS/

rsync --human-readable --archive --xattrs --progress --delete --exclude=.git \
    /home/cloud/git/qemu-build/SOURCES/ cloud@123.123.123.123:/home/cloud/rpmbuild/SOURCES/
rsync --human-readable --archive --xattrs --progress --delete --exclude=.git \
    /home/cloud/git/qemu-build/SPECS/ cloud@123.123.123.123:/home/cloud/rpmbuild/SPECS/

scp /home/cloud/git/qemu-build/SPECS/qemu.spec cloud@123.123.123.123:/home/cloud/rpmbuild/SPECS/qemu.spec
scp /home/cloud/git/qemu-build/SPECS/qemu-sanity-check.spec cloud@123.123.123.123:/home/cloud/rpmbuild/SPECS/qemu-sanity-check.spec

scp /home/cloud/git/qemu-build/SOURCES/gpgkey-CEACC9E15534EBABB82D3FA03353C9CEF108B584.gpg cloud@123.123.123.123:/home/cloud/rpmbuild/SOURCES/
scp /home/cloud/git/qemu-build/SOURCES/vhost.conf cloud@123.123.123.123:/home/cloud/rpmbuild/SOURCES/
scp /home/cloud/git/qemu-build/SOURCES/kvm-x86.conf cloud@123.123.123.123:/home/cloud/rpmbuild/SOURCES/
scp /home/cloud/git/qemu-build/SPECS/qemu.spec cloud@123.123.123.123:/home/cloud/rpmbuild/SPECS/qemu.spec

cd ~/rpmbuild/SOURCES/
wget https://download.qemu.org/qemu-9.1.0.tar.xz
wget https://download.qemu.org/qemu-9.1.0.tar.xz.sig

cd ~/rpmbuild/SPECS/

sudo dnf builddep ~/rpmbuild/SPECS/qemu-sanity-check.spec
rpmbuild -ba qemu-sanity-check.spec
sudo dnf install ~/rpmbuild/RPMS/x86_64/qemu-sanity-check-nodeps-*.el9.x86_64.rpm

sudo dnf builddep ~/rpmbuild/SPECS/virglrenderer.spec
rpmbuild -ba virglrenderer.spec
sudo dnf install ~/rpmbuild/RPMS/x86_64/virglrenderer-*.el9.x86_64.rpm

sudo dnf builddep ~/rpmbuild/SPECS/qemu.spec
rpmbuild -ba qemu.spec
```

# repo

```bash
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

gpg --keyserver hkp://keyserver.ubuntu.com --recv-keys 12C74390F9AAC728
gpg --edit-key 12C74390F9AAC728
trust
5
quit

rm mc*
wget https://dl.min.io/client/mc/release/linux-amd64/mc
wget https://dl.min.io/client/mc/release/linux-amd64/mc.asc
gpg --verify mc.asc mc

sudo rm -f /usr/bin/mc
sudo cp mc /usr/bin/mc
sudo chmod +x /usr/bin/mc

mc ls repo-east
mc ls repo-west

rm -rf ~/repo
mkdir ~/repo
cp rpmbuild/RPMS/noarch/* ~/repo
cp rpmbuild/RPMS/x86_64/* ~/repo
rm ~/repo/*debuginfo*
rm ~/repo/*debugsource*

rpm --resign ~/repo/*.rpm
createrepo ~/repo

mc mirror --remove --overwrite --md5 ~/repo repo-east/kvm-unstable/oraclelinux/9
mc mirror --remove --overwrite --md5 ~/repo repo-west/kvm-unstable/oraclelinux/9

mc mirror --remove --overwrite --md5 ~/repo repo-east/kvm-stable/oraclelinux/9
mc mirror --remove --overwrite --md5 ~/repo repo-west/kvm-stable/oraclelinux/9
```

# qemu features

```
qemu 9.1.0

  Build environment
    Build directory                              : /home/cloud/rpmbuild/BUILD/qemu-9.1.0/qemu_kvm_build
    Source path                                  : /home/cloud/rpmbuild/BUILD/qemu-9.1.0
    Download dependencies                        : NO

  Directories
    Build directory                              : /home/cloud/rpmbuild/BUILD/qemu-9.1.0/qemu_kvm_build
    Source path                                  : /home/cloud/rpmbuild/BUILD/qemu-9.1.0
    Download dependencies                        : NO
    Install prefix                               : /usr
    BIOS directory                               : share/qemu
    firmware path                                : /usr/share/qemu-firmware:/usr/share/ipxe/qemu:/usr/share/seavgabios:/usr/share/seabios
    binary directory                             : /usr/bin
    library directory                            : /usr/lib64
    module directory                             : lib64/qemu
    libexec directory                            : /usr/libexec
    include directory                            : /usr/include
    config directory                             : /etc
    local state directory                        : /var
    Manual directory                             : /usr/share/man
    Doc directory                                : /usr/share/doc

  Host binaries
    python                                       : /home/cloud/rpmbuild/BUILD/qemu-9.1.0/qemu_kvm_build/pyvenv/bin/python3 (version: 3.9)
    sphinx-build                                 : /home/cloud/rpmbuild/BUILD/qemu-9.1.0/qemu_kvm_build/pyvenv/bin/sphinx-build
    gdb                                          : /usr/bin/gdb
    iasl                                         : NO
    genisoimage                                  :
    smbd                                         : /usr/sbin/smbd

  Configurable features
    Documentation                                : YES
    system-mode emulation                        : YES
    user-mode emulation                          : NO
    block layer                                  : YES
    Install blobs                                : YES
    module support                               : YES
    alternative module path                      : NO
    fuzzing support                              : NO
    Audio drivers                                :
    Trace backends                               : log
    D-Bus display                                : YES
    QOM debugging                                : NO
    Relocatable install                          : NO
    vhost-kernel support                         : YES
    vhost-net support                            : YES
    vhost-user support                           : YES
    vhost-user-crypto support                    : YES
    vhost-user-blk server support                : YES
    vhost-vdpa support                           : YES
    build guest agent                            : NO

  Compilation
    host CPU                                     : x86_64
    host endianness                              : little
    C compiler                                   : gcc -m64
    Host C compiler                              : gcc -m64
    C++ compiler                                 : NO
    Objective-C compiler                         : NO
    CFLAGS                                       : -O2 -flto=auto -ffat-lto-objects -fexceptions -g -grecord-gcc-switches -pipe -Wall -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -Wp,-D_GLIBCXX_ASSERTIONS -specs=/usr/lib/rpm/redhat/redhat-hardened-cc1 -fstack-protector-strong -specs=/usr/lib/rpm/redhat/redhat-annobin-cc1 -m64 -march=x86-64-v2 -mtune=generic -fasynchronous-unwind-tables -fstack-clash-protection -fcf-protection -g -O2
    LDFLAGS                                      : -O2 -flto=auto -ffat-lto-objects -fexceptions -g -grecord-gcc-switches -pipe -Wall -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -Wp,-D_GLIBCXX_ASSERTIONS -specs=/usr/lib/rpm/redhat/redhat-hardened-cc1 -fstack-protector-strong -specs=/usr/lib/rpm/redhat/redhat-annobin-cc1 -m64 -march=x86-64-v2 -mtune=generic -fasynchronous-unwind-tables -fstack-clash-protection -fcf-protection -Wl,-z,relro -Wl,--as-needed -Wl,-z,now -specs=/usr/lib/rpm/redhat/redhat-hardened-ld -specs=/usr/lib/rpm/redhat/redhat-annobin-cc1
    QEMU_CFLAGS                                  : -msse2 -mcx16 -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -fno-strict-aliasing -fno-common -fwrapv -ftrivial-auto-var-init=zero -fzero-call-used-regs=used-gpr -fstack-protector-strong
    QEMU_LDFLAGS                                 : -fstack-protector-strong -Wl,-z,relro -Wl,-z,now
    link-time optimization (LTO)                 : YES
    PIE                                          : YES
    static build                                 : NO
    malloc trim support                          : YES
    membarrier                                   : NO
    debug graph lock                             : NO
    debug stack usage                            : NO
    mutex debugging                              : NO
    memory allocator                             : system
    avx2 optimization                            : YES
    avx512bw optimization                        : YES
    gcov                                         : NO
    thread sanitizer                             : NO
    CFI support                                  : NO
    strip binaries                               : NO
    sparse                                       : NO
    mingw32 support                              : NO

  Cross compilers
    x86_64                                       : gcc

  Targets and accelerators
    KVM support                                  : YES
    HVF support                                  : NO
    WHPX support                                 : NO
    NVMM support                                 : NO
    Xen support                                  : NO
    Xen emulation                                : YES
    TCG support                                  : YES
    TCG backend                                  : native (x86_64)
    TCG plugins                                  : NO
    TCG debug enabled                            : NO
    target list                                  : x86_64-softmmu
    default devices                              : YES
    out of process emulation                     : YES
    vfio-user server                             : NO

  Block layer support
    coroutine backend                            : ucontext
    coroutine pool                               : YES
    Block whitelist (rw)                         :
    Block whitelist (ro)                         :
    Use block whitelist in tools                 : NO
    VirtFS (9P) support                          : YES
    VirtFS (9P) Proxy Helper support (deprecated): YES
    replication support                          : YES
    bochs support                                : NO
    cloop support                                : NO
    dmg support                                  : NO
    qcow v1 support                              : NO
    vdi support                                  : YES
    vhdx support                                 : NO
    vmdk support                                 : YES
    vpc support                                  : NO
    vvfat support                                : NO
    qed support                                  : NO
    parallels support                            : NO
    FUSE exports                                 : NO
    VDUSE block exports                          : YES

  Crypto
    TLS priority                                 : @QEMU,SYSTEM
    GNUTLS support                               : YES 3.8.3
      GNUTLS crypto                              : YES
    libgcrypt                                    : NO
    nettle                                       : NO
    SM4 ALG support                              : NO
    AF_ALG support                               : NO
    rng-none                                     : NO
    Linux keyring                                : YES
    Linux keyutils                               : YES 1.6.3

  User interface
    SDL support                                  : NO
    SDL image support                            : NO
    GTK support                                  : NO
    pixman                                       : YES 0.40.0
    VTE support                                  : NO
    PNG support                                  : YES 1.6.37
    VNC support                                  : YES
    VNC SASL support                             : YES
    VNC JPEG support                             : YES 2.0.90
    spice protocol support                       : YES 0.14.3
      spice server support                       : NO
    curses support                               : NO
    brlapi support                               : NO

  Graphics backends
    VirGL support                                : YES 1.1.0
    Rutabaga support                             : NO

  Audio backends
    OSS support                                  : NO
    sndio support                                : NO
    ALSA support                                 : NO
    PulseAudio support                           : YES 15.0
    PipeWire support                             : NO
    JACK support                                 : NO

  Network backends
    AF_XDP support                               : YES 1.4.2
    slirp support                                : YES 4.4.0
    vde support                                  : NO
    netmap support                               : NO
    l2tpv3 support                               : YES

  Dependencies
    libtasn1                                     : YES 4.16.0
    PAM                                          : NO
    iconv support                                : NO
    blkio support                                : YES 1.5.0
    curl support                                 : NO
    Multipath support                            : YES
    Linux AIO support                            : YES
    Linux io_uring support                       : YES 2.5
    ATTR/XATTR support                           : YES
    RDMA support                                 : YES
    fdt support                                  : YES
    libcap-ng support                            : YES
    bpf support                                  : YES 1.3.0
    rbd support                                  : NO
    smartcard support                            : NO
    U2F support                                  : NO
    libusb                                       : YES 1.0.26
    usb net redir                                : YES 0.13.0
    OpenGL support (epoxy)                       : YES 1.5.5
    GBM                                          : YES 23.3.3
    libiscsi support                             : YES 1.19.0
    libnfs support                               : NO
    seccomp support                              : YES 2.5.2
    GlusterFS support                            : NO
    hv-balloon support                           : NO
    TPM support                                  : YES
    libssh support                               : NO
    lzo support                                  : YES
    snappy support                               : YES
    bzip2 support                                : YES
    lzfse support                                : NO
    zstd support                                 : YES 1.5.1
    Query Processing Library support             : NO
    UADK Library support                         : NO
    NUMA host support                            : YES
    capstone                                     : YES 4.0.2
    libpmem support                              : YES 1.12.1
    libdaxctl support                            : YES 73
    libudev                                      : YES 252
    FUSE lseek                                   : NO
    selinux                                      : YES 3.6
    libdw                                        : NO

  Subprojects
    berkeley-softfloat-3                         : YES
    berkeley-testfloat-3                         : YES
    keycodemapdb                                 : YES
    libvduse                                     : YES
    libvhost-user                                : YES

  User defined options
    Native files                                 : config-meson.cross
    datadir                                      : /usr/share
    debug                                        : true
    libdir                                       : /usr/lib64
    libexecdir                                   : /usr/libexec
    localstatedir                                : /var
    prefix                                       : /usr
    strip                                        : false
    sysconfdir                                   : /etc
    werror                                       : false
    wrap_mode                                    : nodownload
    b_lto                                        : true
    af_xdp                                       : enabled
    alsa                                         : disabled
    attr                                         : enabled
    audio_drv_list                               :
    auth_pam                                     : disabled
    avx2                                         : enabled
    avx512bw                                     : enabled
    blkio                                        : enabled
    block_drv_whitelist_in_tools                 : false
    bochs                                        : disabled
    bpf                                          : enabled
    brlapi                                       : disabled
    bzip2                                        : enabled
    cap_ng                                       : enabled
    capstone                                     : enabled
    cfi_debug                                    : false
    cloop                                        : disabled
    cocoa                                        : disabled
    colo_proxy                                   : disabled
    coreaudio                                    : disabled
    coroutine_backend                            : ucontext
    coroutine_pool                               : true
    crypto_afalg                                 : disabled
    curl                                         : disabled
    curses                                       : disabled
    dbus_display                                 : enabled
    debug_graph_lock                             : false
    debug_mutex                                  : false
    debug_remap                                  : false
    debug_tcg                                    : false
    default_devices                              : true
    dmg                                          : disabled
    docdir                                       : /usr/share/doc
    docs                                         : enabled
    dsound                                       : disabled
    fdt                                          : system
    fuse                                         : disabled
    fuse_lseek                                   : disabled
    gcrypt                                       : disabled
    gettext                                      : disabled
    gio                                          : enabled
    glusterfs                                    : disabled
    gnutls                                       : enabled
    gtk                                          : disabled
    gtk_clipboard                                : disabled
    guest_agent                                  : disabled
    guest_agent_msi                              : disabled
    hv_balloon                                   : disabled
    hvf                                          : disabled
    iconv                                        : enabled
    interp_prefix                                : /usr/qemu-%M
    jack                                         : disabled
    kvm                                          : enabled
    l2tpv3                                       : enabled
    libdaxctl                                    : enabled
    libdw                                        : disabled
    libiscsi                                     : enabled
    libkeyutils                                  : enabled
    libnfs                                       : disabled
    libpmem                                      : enabled
    libssh                                       : disabled
    libudev                                      : enabled
    libusb                                       : enabled
    linux_aio                                    : enabled
    linux_io_uring                               : enabled
    lzfse                                        : disabled
    lzo                                          : enabled
    malloc_trim                                  : enabled
    membarrier                                   : disabled
    module_upgrades                              : false
    modules                                      : enabled
    mpath                                        : enabled
    multiprocess                                 : enabled
    netmap                                       : disabled
    nettle                                       : disabled
    numa                                         : enabled
    nvmm                                         : disabled
    opengl                                       : enabled
    oss                                          : disabled
    pa                                           : enabled
    parallels                                    : disabled
    pipewire                                     : disabled
    pixman                                       : enabled
    pkgversion                                   : qemu-9.1.0-12.el9
    png                                          : enabled
    qcow1                                        : disabled
    qed                                          : disabled
    qemu_firmwarepath                            : ["""/usr/share/qemu-firmware""","""/usr/share/ipxe/qemu""","""/usr/share/seavgabios""","""/usr/share/seabios""",]
    qemu_suffix                                  : qemu
    qom_cast_debug                               : false
    qpl                                          : disabled
    rbd                                          : disabled
    rdma                                         : enabled
    relocatable                                  : false
    replication                                  : enabled
    rng_none                                     : false
    rutabaga_gfx                                 : disabled
    safe_stack                                   : false
    sanitizers                                   : false
    sdl                                          : disabled
    sdl_image                                    : disabled
    seccomp                                      : enabled
    selinux                                      : enabled
    slirp                                        : enabled
    slirp_smbd                                   : enabled
    smartcard                                    : disabled
    snappy                                       : enabled
    sndio                                        : disabled
    sparse                                       : disabled
    spice                                        : disabled
    spice_protocol                               : enabled
    tls_priority                                 : @QEMU,SYSTEM
    tools                                        : enabled
    tpm                                          : enabled
    tsan                                         : false
    u2f                                          : disabled
    uadk                                         : disabled
    usb_redir                                    : enabled
    vde                                          : disabled
    vdi                                          : enabled
    vfio_user_server                             : disabled
    vhdx                                         : disabled
    vhost_crypto                                 : enabled
    vhost_kernel                                 : enabled
    vhost_net                                    : enabled
    vhost_user                                   : enabled
    vhost_user_blk_server                        : enabled
    vhost_vdpa                                   : enabled
    virglrenderer                                : enabled
    virtfs                                       : enabled
    virtfs_proxy_helper                          : enabled
    vnc                                          : enabled
    vnc_jpeg                                     : enabled
    vnc_sasl                                     : enabled
    vpc                                          : disabled
    vte                                          : disabled
    vvfat                                        : disabled
    whpx                                         : disabled
    xen                                          : disabled
    xen_pci_passthrough                          : disabled
    xkbcommon                                    : enabled
    zstd                                         : enabled
```
