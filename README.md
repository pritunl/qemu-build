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

sudo yum-config-manager --enable ol9_addons
sudo yum-config-manager --enable ol9_appstream
sudo yum-config-manager --enable ol9_codeready_builder
sudo yum-config-manager --enable ol9_distro_builder

sudo yum -y install oracle-epel-release-el9
sudo yum -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm
sudo yum-config-manager --enable ol9_developer_EPEL
sudo yum-config-manager --disable epel
sudo yum-config-manager --disable epel-cisco-openh264


sudo dnf install rust-anyhow+default-devel rust-cfg-if+default-devel rust-libc+default-devel rust-log+default-devel rust-nix+default-devel rust-nix0.26+default-devel rust-once_cell+default-devel rust-pkg-config+default-devel rust-thiserror+default-devel rust-zerocopy+default-devel

sudo yum-config-manager --disable ol9_developer_EPEL
sudo yum-config-manager --enable epel
sudo yum-config-manager --enable epel-cisco-openh264

sudo dnf install rust-zerocopy0.6-devel rust-zerocopy0.6+default-devel rust-zerocopy-derive0.6-devel rust-zerocopy-derive0.6+default-devel

sudo dnf install rust-rustversion-devel rust-rustversion+default-devel rust-syn-devel rust-syn+default-devel rust-syn+full-devel rust-syn+visit-mut-devel rust-trybuild-devel rust-trybuild+default-devel rust-trybuild+diff-devel

sudo yum-config-manager --enable ol9_developer_EPEL
sudo yum-config-manager --disable epel
sudo yum-config-manager --disable epel-cisco-openh264


sudo yum -y update
sudo yum -y remove cockpit cockpit-ws
sudo yum -y install rpm-build rpm-sign createrepo wget nano git
sudo yum -y install seabios seabios-bin seavgabios-bin
sudo yum -y groupinstall 'Development Tools'

sudo systemctl stop firewalld
sudo systemctl disable firewalld

mkdir rpmkeys
cd rpmkeys

wget https://download-ib01.fedoraproject.org/pub/fedora/linux/development/rawhide/Everything/x86_64/os/Packages/d/distribution-gpg-keys-1.100-1.fc40.noarch.rpm
rpm2cpio ./distribution-gpg-keys-1.100-1.fc40.noarch.rpm | cpio -idmv
sudo rpm --import ./usr/share/distribution-gpg-keys/fedora/RPM-GPG-KEY-fedora-rawhide-primary

cd ..
rm -rf rpmkeys


wget https://yum.oracle.com/repo/OracleLinux/OL9/appstream/x86_64/getPackageSource/libepoxy-1.5.5-4.el9.src.rpm
wget https://yum.oracle.com/repo/OracleLinux/OL9/appstream/x86_64/getPackageSource/liburing-0.7-7.el9.src.rpm
wget https://yum.oracle.com/repo/OracleLinux/OL9/appstream/x86_64/getPackageSource/capstone-4.0.2-10.el9.src.rpm
wget https://yum.oracle.com/repo/OracleLinux/OL9/developer/EPEL/x86_64/getPackageSource/libnfs-5.0.2-2.el9.src.rpm
wget https://yum.oracle.com/repo/OracleLinux/OL9/appstream/x86_64/getPackageSource/libslirp-4.4.0-7.el9.src.rpm
wget https://yum.oracle.com/repo/OracleLinux/OL9/appstream/x86_64/getPackageSource/ipxe-20200823-9.git4bd064de.el9.src.rpm
wget https://yum.oracle.com/repo/OracleLinux/OL9/appstream/x86_64/getPackageSource/dtc-1.6.0-7.el9.src.rpm
wget https://yum.oracle.com/repo/OracleLinux/OL9/appstream/x86_64/getPackageSource/seabios-1.16.1-1.el9.src.rpm
wget https://yum.oracle.com/repo/OracleLinux/OL9/kvm/utils/x86_64/getPackageSource/edk2-20230821-1.el9.src.rpm
wget https://yum.oracle.com/repo/OracleLinux/OL8/appstream/x86_64/getPackageSource/spice-0.14.3-4.el8.src.rpm
wget https://yum.oracle.com/repo/OracleLinux/OL9/developer/EPEL/x86_64/getPackageSource/libcacard-2.8.1-6.el9.src.rpm
wget https://yum.oracle.com/repo/OracleLinux/OL9/codeready/builder/x86_64/getPackageSource/meson-0.63.3-1.el9.src.rpm
wget https://yum.oracle.com/repo/OracleLinux/OL9/appstream/x86_64/getPackageSource/virtiofsd-1.7.2-1.el9.src.rpm

wget https://download-ib01.fedoraproject.org/pub/fedora/linux/releases/39/Everything/source/tree/Packages/c/celt051-0.5.1.3-26.fc39.src.rpm
wget https://download-ib01.fedoraproject.org/pub/fedora/linux/development/rawhide/Everything/source/tree/Packages/v/virglrenderer-1.0.1-1.fc40.src.rpm
wget https://download-ib01.fedoraproject.org/pub/fedora/linux/development/rawhide/Everything/source/tree/Packages/r/rutabaga-gfx-ffi-0.1.2-2.20230913gitc3ad0e43e.fc40.src.rpm
wget https://download-ib01.fedoraproject.org/pub/fedora/linux/development/rawhide/Everything/source/tree/Packages/q/qemu-sanity-check-1.1.6-11.fc40.src.rpm
wget https://download-ib01.fedoraproject.org/pub/fedora/linux/development/rawhide/Everything/source/tree/Packages/q/qemu-8.2.0-2.fc40.src.rpm


rpm -K libepoxy-1.5.5-4.el9.src.rpm
rpm -K liburing-0.7-7.el9.src.rpm
rpm -K capstone-4.0.2-10.el9.src.rpm
rpm -K libnfs-5.0.2-2.el9.src.rpm
rpm -K libslirp-4.4.0-7.el9.src.rpm
rpm -K ipxe-20200823-9.git4bd064de.el9.src.rpm
rpm -K dtc-1.6.0-7.el9.src.rpm
rpm -K seabios-1.16.1-1.el9.src.rpm
rpm -K edk2-20230821-1.el9.src.rpm
rpm -K spice-0.14.3-4.el8.src.rpm
rpm -K libcacard-2.8.1-6.el9.src.rpm
rpm -K meson-0.63.3-1.el9.src.rpm
rpm -K virtiofsd-1.7.2-1.el9.src.rpm
rpm -K celt051-0.5.1.3-26.fc39.src.rpm
rpm -K virglrenderer-1.0.1-1.fc40.src.rpm
rpm -K rutabaga-gfx-ffi-0.1.2-2.20230913gitc3ad0e43e.fc40.src.rpm
rpm -K qemu-sanity-check-1.1.6-11.fc40.src.rpm
rpm -K qemu-8.2.0-2.fc40.src.rpm

sudo rpm -i libepoxy-1.5.5-4.el9.src.rpm
sudo rpm -i liburing-0.7-7.el9.src.rpm
sudo rpm -i capstone-4.0.2-10.el9.src.rpm
sudo rpm -i libnfs-5.0.2-2.el9.src.rpm
sudo rpm -i libslirp-4.4.0-7.el9.src.rpm
sudo rpm -i ipxe-20200823-9.git4bd064de.el9.src.rpm
sudo rpm -i dtc-1.6.0-7.el9.src.rpm
sudo rpm -i seabios-1.16.1-1.el9.src.rpm
sudo rpm -i edk2-20230821-1.el9.src.rpm
sudo rpm -i spice-0.14.3-4.el8.src.rpm
sudo rpm -i libcacard-2.8.1-6.el9.src.rpm
sudo rpm -i meson-0.63.3-1.el9.src.rpm
sudo rpm -i virtiofsd-1.7.2-1.el9.src.rpm
sudo rpm -i celt051-0.5.1.3-26.fc39.src.rpm
sudo rpm -i virglrenderer-1.0.1-1.fc40.src.rpm
sudo rpm -i rutabaga-gfx-ffi-0.1.2-2.20230913gitc3ad0e43e.fc40.src.rpm
sudo rpm -i qemu-sanity-check-1.1.6-11.fc40.src.rpm
sudo rpm -i qemu-8.2.0-2.fc40.src.rpm

sudo mv /root/rpmbuild ~/rpmbuild
sudo chown -R opc:opc ~/rpmbuild


rsync --human-readable --archive --xattrs --progress --delete --exclude=.git \
    opc@123.123.123.123:/home/opc/*.rpm /home/cloud/git/qemu-build/SRPMS/
rsync --human-readable --archive --xattrs --progress --delete --exclude=.git \
    opc@123.123.123.123:/home/opc/rpmbuild/SOURCES/ /home/cloud/git/qemu-build/SOURCES/
rsync --human-readable --archive --xattrs --progress --delete --exclude=.git \
    opc@123.123.123.123:/home/opc/rpmbuild/SPECS/ /home/cloud/git/qemu-build/SPECS/

rsync --human-readable --archive --xattrs --progress --delete --exclude=.git \
    /home/cloud/git/qemu-build/SOURCES/ opc@123.123.123.123:/home/opc/rpmbuild/SOURCES/
rsync --human-readable --archive --xattrs --progress --delete --exclude=.git \
    /home/cloud/git/qemu-build/SPECS/ opc@123.123.123.123:/home/opc/rpmbuild/SPECS/

scp /home/cloud/git/qemu-build/SPECS/qemu.spec opc@123.123.123.123:/home/opc/rpmbuild/SPECS/qemu.spec
scp /home/cloud/git/qemu-build/SPECS/qemu-sanity-check.spec opc@123.123.123.123:/home/opc/rpmbuild/SPECS/qemu-sanity-check.spec


cd ~/rpmbuild/SPECS/

sudo dnf builddep -y ~/rpmbuild/SPECS/libepoxy.spec
rpmbuild -ba libepoxy.spec

sudo yum -y install ~/rpmbuild/RPMS/x86_64/libepoxy-*.el9.x86_64.rpm

sudo dnf builddep -y ~/rpmbuild/SPECS/libcacard.spec
rpmbuild -ba libcacard.spec

sudo yum -y install ~/rpmbuild/RPMS/x86_64/libcacard-*.el9.x86_64.rpm

sudo dnf builddep -y ~/rpmbuild/SPECS/celt051.spec
rpmbuild -ba celt051.spec

sudo yum -y install ~/rpmbuild/RPMS/x86_64/celt051-*.el9.x86_64.rpm

sudo dnf builddep -y ~/rpmbuild/SPECS/spice.spec
rpmbuild -ba spice.spec

sudo yum -y install ~/rpmbuild/RPMS/x86_64/spice-*.el9.x86_64.rpm

sudo dnf builddep -y ~/rpmbuild/SPECS/virglrenderer.spec
rpmbuild -ba virglrenderer.spec

sudo yum -y install ~/rpmbuild/RPMS/x86_64/virglrenderer-*.el9.x86_64.rpm

sudo dnf builddep -y ~/rpmbuild/SPECS/rust-remain.spec
rpmbuild -ba rust-remain.spec

sudo yum -y install ~/rpmbuild/RPMS/noarch/rust-remain*.el9.noarch.rpm

sudo dnf builddep -y ~/rpmbuild/SPECS/rutabaga-gfx-ffi.spec

rpmbuild -ba rutabaga-gfx-ffi.spec

sudo yum -y install ~/rpmbuild/RPMS/x86_64/rutabaga-gfx-ffi*.el9.x86_64.rpm

sudo dnf builddep -y ~/rpmbuild/SPECS/liburing.spec
rpmbuild -ba liburing.spec

sudo yum -y install ~/rpmbuild/RPMS/x86_64/liburing-*.el9.x86_64.rpm

sudo dnf builddep -y ~/rpmbuild/SPECS/qemu-sanity-check.spec
rpmbuild -ba qemu-sanity-check.spec

sudo yum -y install ~/rpmbuild/RPMS/x86_64/qemu-sanity-check-nodeps-*.el9.x86_64.rpm

sudo dnf builddep -y ~/rpmbuild/SPECS/capstone.spec
rpmbuild -ba capstone.spec

sudo yum -y install ~/rpmbuild/RPMS/x86_64/capstone-*.el9.x86_64.rpm

sudo dnf builddep -y ~/rpmbuild/SPECS/libslirp.spec
rpmbuild -ba libslirp.spec

sudo yum -y install ~/rpmbuild/RPMS/x86_64/libslirp-*.el9.x86_64.rpm

sudo dnf builddep -y ~/rpmbuild/SPECS/libnfs.spec
rpmbuild -ba libnfs.spec

sudo yum -y install ~/rpmbuild/RPMS/x86_64/libnfs-*.el9.x86_64.rpm

sudo dnf builddep -y ~/rpmbuild/SPECS/dtc.spec
rpmbuild -ba dtc.spec

sudo yum -y install ~/rpmbuild/RPMS/x86_64/dtc-*.el9.x86_64.rpm

sudo dnf builddep -y ~/rpmbuild/SPECS/edk2.spec
rpmbuild -ba edk2.spec

sudo yum -y install ~/rpmbuild/RPMS/noarch/edk2-*.el9.noarch.rpm ~/rpmbuild/RPMS/x86_64/edk2-*.el9.x86_64.rpm

sudo dnf builddep -y ~/rpmbuild/SPECS/ipxe.spec
rpmbuild -ba ipxe.spec

sudo yum -y install ~/rpmbuild/RPMS/noarch/ipxe-*.el9.noarch.rpm

sudo dnf builddep -y ~/rpmbuild/SPECS/seabios.spec
rpmbuild -ba seabios.spec

sudo dnf builddep -y ~/rpmbuild/SPECS/meson.spec
rpmbuild -ba meson.spec

sudo yum -y install ~/rpmbuild/RPMS/noarch/meson-*.el9.noarch.rpm

sudo dnf builddep -y ~/rpmbuild/SPECS/virtiofsd.spec
rpmbuild -ba virtiofsd.spec

sudo dnf builddep -y ~/rpmbuild/SPECS/qemu.spec
rpmbuild -ba qemu.spec
```

# repo

```bash
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
qemu 8.2.0

  Build environment
    Build directory                              : /home/opc/rpmbuild/BUILD/qemu-8.2.0/qemu_kvm_build
    Source path                                  : /home/opc/rpmbuild/BUILD/qemu-8.2.0
    Download dependencies                        : NO

  Directories
    Build directory                              : /home/opc/rpmbuild/BUILD/qemu-8.2.0/qemu_kvm_build
    Source path                                  : /home/opc/rpmbuild/BUILD/qemu-8.2.0
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
    python                                       : /home/opc/rpmbuild/BUILD/qemu-8.2.0/qemu_kvm_build/pyvenv/bin/python3 (version: 3.9)
    sphinx-build                                 : /home/opc/rpmbuild/BUILD/qemu-8.2.0/qemu_kvm_build/pyvenv/bin/sphinx-build
    gdb                                          : /usr/bin/gdb
    iasl                                         : /usr/bin/iasl
    genisoimage                                  : /usr/bin/genisoimage
    smbd                                         : /usr/sbin/smbd

  Configurable features
    Documentation                                : YES
    system-mode emulation                        : YES
    user-mode emulation                          : YES
    block layer                                  : YES
    Install blobs                                : YES
    module support                               : YES
    alternative module path                      : NO
    fuzzing support                              : NO
    Audio drivers                                : pa alsa oss
    Trace backends                               : log
    D-Bus display                                : NO
    QOM debugging                                : YES
    Relocatable install                          : YES
    vhost-kernel support                         : YES
    vhost-net support                            : YES
    vhost-user support                           : YES
    vhost-user-crypto support                    : YES
    vhost-user-blk server support                : YES
    vhost-vdpa support                           : YES
    build guest agent                            : YES

  Compilation
    host CPU                                     : x86_64
    host endianness                              : little
    C compiler                                   : gcc -m64 -mcx16
    Host C compiler                              : gcc -m64 -mcx16
    C++ compiler                                 : NO
    Objective-C compiler                         : NO
    CFLAGS                                       : -O2 -fexceptions -g -grecord-gcc-switches -pipe -Wall -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -Wp,-D_GLIBCXX_ASSERTIONS -specs=/usr/lib/rpm/redhat/redhat-hardened-cc1 -fstack-protector-strong -specs=/usr/lib/rpm/redhat/redhat-annobin-cc1 -m64 -march=x86-64-v2 -mtune=generic -fasynchronous-unwind-tables -fstack-clash-protection -fcf-protection -g -O2
    LDFLAGS                                      : -O2 -fexceptions -g -grecord-gcc-switches -pipe -Wall -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -Wp,-D_GLIBCXX_ASSERTIONS -specs=/usr/lib/rpm/redhat/redhat-hardened-cc1 -fstack-protector-strong -specs=/usr/lib/rpm/redhat/redhat-annobin-cc1 -m64 -march=x86-64-v2 -mtune=generic -fasynchronous-unwind-tables -fstack-clash-protection -fcf-protection -Wl,-z,relro -Wl,--as-needed -Wl,-z,now -specs=/usr/lib/rpm/redhat/redhat-hardened-ld -specs=/usr/lib/rpm/redhat/redhat-annobin-cc1
    QEMU_CFLAGS                                  : -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -fno-strict-aliasing -fno-common -fwrapv -fstack-protector-strong
    QEMU_LDFLAGS                                 : -fstack-protector-strong -Wl,-z,relro -Wl,-z,now -Wl,--warn-common
    link-time optimization (LTO)                 : NO
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
    avx512f optimization                         : YES
    gcov                                         : NO
    thread sanitizer                             : NO
    CFI support                                  : NO
    strip binaries                               : NO
    sparse                                       : NO
    mingw32 support                              : NO

  Cross compilers
    i386                                         : gcc
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
    target list                                  : aarch64-linux-user aarch64_be-linux-user alpha-linux-user arm-linux-user armeb-linux-user cris-linux-user hexagon-linux-user hppa-linux-user i386-linux-user loongarch64-linux-user m68k-linux-user microblaze-linux-user microblazeel-linux-user mips-linux-user mips64-linux-user mips64el-linux-user mipsel-linux-user mipsn32-linux-user mipsn32el-linux-user nios2-linux-user or1k-linux-user ppc-linux-user ppc64-linux-user ppc64le-linux-user riscv32-linux-user riscv64-linux-user s390x-linux-user sh4-linux-user sh4eb-linux-user sparc-linux-user sparc32plus-linux-user sparc64-linux-user x86_64-linux-user xtensa-linux-user xtensaeb-linux-user aarch64-softmmu alpha-softmmu arm-softmmu avr-softmmu cris-softmmu hppa-softmmu i386-softmmu loongarch64-softmmu m68k-softmmu microblaze-softmmu microblazeel-softmmu mips-softmmu mips64-softmmu mips64el-softmmu mipsel-softmmu nios2-softmmu or1k-softmmu ppc-softmmu ppc64-softmmu riscv32-softmmu riscv64-softmmu rx-softmmu s390x-softmmu sh4-softmmu sh4eb-softmmu sparc-softmmu sparc64-softmmu tricore-softmmu x86_64-softmmu xtensa-softmmu xtensaeb-softmmu
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
    Live block migration                         : YES
    replication support                          : YES
    bochs support                                : YES
    cloop support                                : YES
    dmg support                                  : YES
    qcow v1 support                              : YES
    vdi support                                  : YES
    vhdx support                                 : YES
    vmdk support                                 : YES
    vpc support                                  : YES
    vvfat support                                : YES
    qed support                                  : YES
    parallels support                            : YES
    FUSE exports                                 : YES 3.10.2
    VDUSE block exports                          : YES

  Crypto
    TLS priority                                 : @QEMU,SYSTEM
    GNUTLS support                               : YES 3.7.6
      GNUTLS crypto                              : YES
    libgcrypt                                    : NO
    nettle                                       : NO
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
      spice server support                       : YES 0.14.3
    curses support                               : YES
    brlapi support                               : YES

  Audio backends
    OSS support                                  : YES
    sndio support                                : NO
    ALSA support                                 : YES 1.2.9
    PulseAudio support                           : YES 15.0
    PipeWire support                             : NO
    JACK support                                 : NO

  Network backends
    AF_XDP support                               : YES 1.4.0
    slirp support                                : YES 4.4.0
    vde support                                  : NO
    netmap support                               : NO
    l2tpv3 support                               : YES

  Dependencies
    libtasn1                                     : YES 4.16.0
    PAM                                          : YES
    iconv support                                : YES
    virgl support                                : YES 1.0.1
    rutabaga support                             : YES 0.1.2
    blkio support                                : YES 1.3.0
    curl support                                 : YES 7.76.1
    Multipath support                            : YES
    Linux AIO support                            : YES
    Linux io_uring support                       : YES 2.3
    ATTR/XATTR support                           : YES
    RDMA support                                 : YES
    PVRDMA support                               : YES
    fdt support                                  : system
    libcap-ng support                            : YES
    bpf support                                  : YES 1.2.0
    rbd support                                  : YES
    smartcard support                            : YES 2.8.1
    U2F support                                  : NO
    libusb                                       : YES 1.0.26
    usb net redir                                : YES 0.13.0
    OpenGL support (epoxy)                       : YES 1.5.5
    GBM                                          : YES 23.1.4
    libiscsi support                             : YES 1.19.0
    libnfs support                               : YES 5.0.2
    seccomp support                              : YES 2.5.2
    GlusterFS support                            : YES 7.6.0
    hv-balloon support                           : YES
    TPM support                                  : YES
    libssh support                               : YES 0.10.4
    lzo support                                  : YES
    snappy support                               : YES
    bzip2 support                                : YES
    lzfse support                                : NO
    zstd support                                 : YES 1.5.1
    NUMA host support                            : YES
    capstone                                     : YES 4.0.2
    libpmem support                              : YES 1.12.1
    libdaxctl support                            : YES 73
    libudev                                      : YES 252
    FUSE lseek                                   : NO
    selinux                                      : YES 3.5
    libdw                                        : YES 0.189

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
    b_lto                                        : false
    af_xdp                                       : enabled
    alsa                                         : enabled
    attr                                         : enabled
    audio_drv_list                               : pa,alsa,oss
    auth_pam                                     : enabled
    avx2                                         : enabled
    avx512bw                                     : enabled
    avx512f                                      : enabled
    blkio                                        : enabled
    block_drv_whitelist_in_tools                 : false
    bochs                                        : enabled
    bpf                                          : enabled
    brlapi                                       : enabled
    bzip2                                        : enabled
    cap_ng                                       : enabled
    capstone                                     : enabled
    cfi_debug                                    : false
    cloop                                        : enabled
    cocoa                                        : disabled
    colo_proxy                                   : disabled
    coreaudio                                    : disabled
    coroutine_backend                            : ucontext
    coroutine_pool                               : true
    crypto_afalg                                 : disabled
    curl                                         : enabled
    curses                                       : enabled
    dbus_display                                 : disabled
    debug_graph_lock                             : false
    debug_mutex                                  : false
    debug_tcg                                    : false
    default_devices                              : true
    dmg                                          : enabled
    docdir                                       : /usr/share/doc
    docs                                         : enabled
    dsound                                       : disabled
    fdt                                          : system
    fuse                                         : enabled
    fuse_lseek                                   : disabled
    gcrypt                                       : disabled
    gettext                                      : disabled
    gio                                          : enabled
    glusterfs                                    : enabled
    gnutls                                       : enabled
    gtk                                          : disabled
    gtk_clipboard                                : disabled
    guest_agent                                  : enabled
    guest_agent_msi                              : disabled
    hv_balloon                                   : enabled
    hvf                                          : disabled
    iconv                                        : enabled
    interp_prefix                                : /usr/qemu-%M
    jack                                         : disabled
    kvm                                          : enabled
    l2tpv3                                       : enabled
    libdaxctl                                    : enabled
    libdw                                        : enabled
    libiscsi                                     : enabled
    libkeyutils                                  : enabled
    libnfs                                       : enabled
    libpmem                                      : enabled
    libssh                                       : enabled
    libudev                                      : enabled
    libusb                                       : enabled
    linux_aio                                    : enabled
    linux_io_uring                               : enabled
    live_block_migration                         : enabled
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
    oss                                          : enabled
    pa                                           : enabled
    parallels                                    : enabled
    pipewire                                     : disabled
    pixman                                       : enabled
    pkgversion                                   : pritunl-qemu-8.2.0-2.el9
    png                                          : enabled
    pvrdma                                       : enabled
    qcow1                                        : enabled
    qed                                          : enabled
    qemu_firmwarepath                            : ["""/usr/share/qemu-firmware""","""/usr/share/ipxe/qemu""","""/usr/share/seavgabios""","""/usr/share/seabios""",]
    qemu_suffix                                  : qemu
    qom_cast_debug                               : true
    rbd                                          : enabled
    rdma                                         : enabled
    relocatable                                  : true
    replication                                  : enabled
    rng_none                                     : false
    rutabaga_gfx                                 : enabled
    safe_stack                                   : false
    sanitizers                                   : false
    sdl                                          : disabled
    sdl_image                                    : disabled
    seccomp                                      : enabled
    selinux                                      : enabled
    slirp                                        : enabled
    slirp_smbd                                   : enabled
    smartcard                                    : enabled
    snappy                                       : enabled
    sndio                                        : disabled
    sparse                                       : disabled
    spice                                        : enabled
    spice_protocol                               : enabled
    tls_priority                                 : @QEMU,SYSTEM
    tools                                        : enabled
    tpm                                          : enabled
    tsan                                         : false
    u2f                                          : disabled
    usb_redir                                    : enabled
    vde                                          : disabled
    vdi                                          : enabled
    vfio_user_server                             : disabled
    vhdx                                         : enabled
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
    vpc                                          : enabled
    vte                                          : disabled
    vvfat                                        : enabled
    whpx                                         : disabled
    xen                                          : disabled
    xen_pci_passthrough                          : disabled
    xkbcommon                                    : enabled
    zstd                                         : enabled
```
