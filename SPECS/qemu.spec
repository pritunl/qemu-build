%global libfdt_version 1.6.0
%global libseccomp_version 2.4.0
%global libusbx_version 1.0.23
%global meson_version 0.63.3
%global usbredir_version 0.7.1

%global have_sdl 0
%global have_gtk 0
%global have_opengl 1
%global have_virgl 1
%global have_rutabaga 0

%global target_list x86_64-softmmu
%global firmwaredirs "%{_datadir}/qemu-firmware:%{_datadir}/ipxe/qemu:%{_datadir}/seavgabios:%{_datadir}/seabios"
%global qemudocdir %{_docdir}/qemu

%define evr %{epoch}:%{version}-%{release}
%define requires_block_blkio Requires: %{name}-block-blkio = %{evr}
%define requires_block_iscsi Requires: %{name}-block-iscsi = %{evr}
%define requires_audio_pa Requires: %{name}-audio-pa = %{evr}
%if %{have_sdl}
%define requires_audio_sdl Requires: %{name}-audio-sdl = %{evr}
%else
%define requires_audio_sdl %{nil}
%endif
%define requires_device_usb_host Requires: %{name}-device-usb-host = %{evr}
%define requires_device_usb_redirect Requires: %{name}-device-usb-redirect = %{evr}
%if %{have_gtk}
%define requires_ui_gtk Requires: %{name}-ui-gtk = %{evr}
%else
%define requires_ui_gtk %{nil}
%endif
%if %{have_sdl}
%define requires_ui_sdl Requires: %{name}-ui-sdl = %{evr}
%else
%define requires_ui_sdl %{nil}
%endif
%define requires_ui_egl_headless Requires: %{name}-ui-egl-headless = %{evr}
%define requires_ui_opengl Requires: %{name}-ui-opengl = %{evr}
%define requires_device_display_virtio_gpu Requires: %{name}-device-display-virtio-gpu = %{evr}
%define requires_device_display_virtio_gpu_pci Requires: %{name}-device-display-virtio-gpu-pci = %{evr}
%define requires_device_display_virtio_vga Requires: %{name}-device-display-virtio-vga = %{evr}
%define requires_device_display_virtio_vga_gl Requires: %{name}-device-display-virtio-vga-gl = %{evr}
%define requires_package_qemu_pr_helper Requires: qemu-pr-helper
%define requires_package_virtiofsd Requires: virtiofsd
%if %{have_virgl}
%define requires_device_display_vhost_user_gpu Requires: %{name}-device-display-vhost-user-gpu = %{evr}
%define requires_device_display_virtio_gpu_gl Requires: %{name}-device-display-virtio-gpu-gl = %{evr}
%define requires_device_display_virtio_gpu_pci_gl Requires: %{name}-device-display-virtio-gpu-pci-gl = %{evr}
%else
%define requires_device_display_vhost_user_gpu %{nil}
%define requires_device_display_virtio_gpu_gl %{nil}
%define requires_device_display_virtio_gpu_pci_gl %{nil}
%endif
%if %{have_rutabaga}
%define requires_device_display_virtio_gpu_rutabaga Requires: %{name}-device-display-virtio-gpu-rutabaga = %{evr}
%define requires_device_display_virtio_gpu_pci_rutabaga Requires: %{name}-device-display-virtio-gpu-pci-rutabaga = %{evr}
%define requires_device_display_virtio_vga_rutabaga Requires: %{name}-device-display-virtio-vga-rutabaga = %{evr}
%else
%define requires_device_display_virtio_gpu_rutabaga %{nil}
%define requires_device_display_virtio_gpu_pci_rutabaga %{nil}
%define requires_device_display_virtio_vga_rutabaga %{nil}
%endif
%define requires_audio_dbus Requires: %{name}-audio-dbus = %{evr}
%define requires_ui_dbus Requires: %{name}-ui-dbus = %{evr}

%global requires_all_modules \
%{requires_block_blkio} \
%{requires_block_iscsi} \
%{requires_audio_dbus} \
%{requires_audio_pa} \
%{requires_audio_sdl} \
%{requires_ui_gtk} \
%{requires_ui_sdl} \
%{requires_ui_egl_headless} \
%{requires_ui_opengl} \
%{requires_device_display_vhost_user_gpu} \
%{requires_device_display_virtio_gpu} \
%{requires_device_display_virtio_gpu_gl} \
%{requires_device_display_virtio_gpu_rutabaga} \
%{requires_device_display_virtio_gpu_pci} \
%{requires_device_display_virtio_gpu_pci_gl} \
%{requires_device_display_virtio_gpu_pci_rutabaga} \
%{requires_device_display_virtio_vga} \
%{requires_device_display_virtio_vga_gl} \
%{requires_device_display_virtio_vga_rutabaga} \
%{requires_device_usb_host} \
%{requires_device_usb_redirect} \
%{requires_package_qemu_pr_helper} \
%{requires_package_virtiofsd} \

# Release candidate version tracking
%if 0%{?rcver:1}
%global rcrel .%{rcver}
%global rcstr -%{rcver}
%endif


Summary: QEMU is a machine emulator and virtualizer
Name: qemu
Version: 9.1.0
Release: 12%{?rcrel}%{?dist}
Epoch: 18
License: GPLv2 and GPLv2+ and CC-BY
URL: http://www.qemu.org/
ExclusiveArch: x86_64

Source0: https://download.qemu.org/qemu-%{version}%{?rcstr}.tar.xz
Source1: https://download.qemu.org/qemu-%{version}%{?rcstr}.tar.xz.sig
Source2: gpgkey-CEACC9E15534EBABB82D3FA03353C9CEF108B584.gpg
Source3: vhost.conf
Source4: kvm-x86.conf

BuildRequires: gnupg2
BuildRequires: meson >= %{meson_version}
BuildRequires: bison
BuildRequires: flex
BuildRequires: zlib-devel
BuildRequires: glib2-devel
BuildRequires: gnutls-devel
BuildRequires: libselinux-devel
BuildRequires: cyrus-sasl-devel
BuildRequires: libaio-devel
BuildRequires: python3-devel
BuildRequires: libiscsi-devel
BuildRequires: libattr-devel
BuildRequires: libusbx-devel >= %{libusbx_version}
BuildRequires: usbredir-devel >= %{usbredir_version}
BuildRequires: python3-sphinx
BuildRequires: python3-sphinx_rtd_theme
BuildRequires: libseccomp-devel >= %{libseccomp_version}
# For VNC PNG support
BuildRequires: libpng-devel
# For virtiofs
BuildRequires: libcap-ng-devel
# Hard requirement for version >= 1.3
BuildRequires: pixman-devel
# For rdma
BuildRequires: rdma-core-devel
BuildRequires: libfdt-devel >= %{libfdt_version}
# For compressed guest memory dumps
BuildRequires: lzo-devel snappy-devel
BuildRequires: numactl-devel
# qemu-pr-helper multipath support (requires libudev too)
BuildRequires: device-mapper-multipath-devel
BuildRequires: systemd-devel
BuildRequires: libpmem-devel
# qemu-keymap
BuildRequires: pkgconfig(xkbcommon)
%if %{have_opengl}
BuildRequires: pkgconfig(epoxy)
BuildRequires: pkgconfig(libdrm)
BuildRequires: pkgconfig(gbm)
%endif
BuildRequires: perl-Test-Harness
BuildRequires: libslirp-devel
BuildRequires: libbpf-devel
BuildRequires: libblkio-devel
BuildRequires: clang
BuildRequires: compiler-rt
BuildRequires: make
# For autosetup git_am
BuildRequires: git
%if %{have_sdl}
# -display sdl support
BuildRequires: SDL2-devel
%endif
# pulseaudio audio output
BuildRequires: pulseaudio-libs-devel
# spice support
BuildRequires: spice-protocol
# VNC JPEG support
BuildRequires: libjpeg-devel
# Braille device support
BuildRequires: brlapi-devel
%if %{have_gtk}
# GTK frontend
BuildRequires: gtk3-devel
BuildRequires: vte291-devel
# GTK translations
BuildRequires: gettext
%endif
# reading bzip2 compressed dmg images
BuildRequires: bzip2-devel
# TLS test suite
BuildRequires: libtasn1-devel
%if %{have_virgl}
# virgl 3d support
BuildRequires: virglrenderer-devel
%endif
# preferred disassembler for TCG
BuildRequires: capstone-devel
# qemu-ga
BuildRequires: libudev-devel
# qauth infrastructure
BuildRequires: pam-devel
# liburing support. Library isn't built for arm
BuildRequires: liburing-devel
# zstd compression support
BuildRequires: libzstd-devel
# `hostname` used by test suite
BuildRequires: hostname
# nvdimm dax
BuildRequires: daxctl-devel
# Used by cryptodev-backend-lkcf
BuildRequires: keyutils-libs-devel
# Used by net AF_XDP
BuildRequires: libxdp-devel
# used by virtio-gpu-rutabaga
%if %{have_rutabaga}
BuildRequires: rutabaga-gfx-ffi-devel
%endif
BuildRequires: python-tomli

# Requires for the qemu metapackage
Requires: %{name}-system-x86 = %{epoch}:%{version}-%{release}
Requires: %{name}-img = %{epoch}:%{version}-%{release}
Requires: %{name}-tools = %{epoch}:%{version}-%{release}

%description
QEMU is an open source virtualizer that provides hardware
emulation for the KVM hypervisor. QEMU acts as a virtual
machine monitor together with the KVM kernel modules, and emulates the
hardware for a full system such as a PC and its associated peripherals.


%package common
Summary: QEMU common files needed by all QEMU targets
Requires(post): /usr/bin/getent
Requires(post): /usr/sbin/groupadd
Requires(post): /usr/sbin/useradd
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
Requires: ipxe-roms-qemu
%description common
QEMU is an open source virtualizer that provides hardware emulation for
the KVM hypervisor.

This package provides documentation and auxiliary programs used with QEMU.


%package docs
Summary: %{name} documentation
BuildArch: noarch
%description docs
%{name}-docs provides documentation files regarding %{name}.


%package img
Summary: QEMU command line tool for manipulating disk images
%description img
This package provides a command line tool for manipulating disk images.


%package tools
Summary: %{name} support tools
%description tools
%{name}-tools provides various tools related to %{name} usage.


%package pr-helper
Summary: %{name}-pr-helper utility for %{name}
%description pr-helper
This package provides the qemu-pr-helper utility that is required for certain
SCSI features.


%package tests
Summary: tests for the %{name} package
Requires: %{name} = %{epoch}:%{version}-%{release}

%define testsdir %{_libdir}/%{name}/tests-src

%description tests
The %{name}-tests rpm contains tests that can be used to verify
the functionality of the installed %{name} package

Install this package if you want access to the avocado_qemu
tests, or qemu-iotests.


%package block-blkio
Summary: QEMU blkio block driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description block-blkio
This package provides the additional blkio block driver for QEMU.

Install this package if you want to access disks over vhost-user-blk, vdpa-blk,
and other transports using the libblkio library.


%package block-iscsi
Summary: QEMU iSCSI block driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description block-iscsi
This package provides the additional iSCSI block driver for QEMU.

Install this package if you want to access iSCSI volumes.


%package audio-dbus
Summary: QEMU D-Bus audio driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description audio-dbus
This package provides the additional D-Bus audio driver for QEMU.


%package audio-pa
Summary: QEMU PulseAudio audio driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description audio-pa
This package provides the additional PulseAudio audio driver for QEMU.


%if %{have_sdl}
%package audio-sdl
Summary: QEMU SDL audio driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description audio-sdl
This package provides the additional SDL audio driver for QEMU.
%endif


%if %{have_opengl}
%package ui-opengl
Summary: QEMU opengl support
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
Requires: mesa-libGL
Requires: mesa-libEGL
Requires: mesa-dri-drivers
%description ui-opengl
This package provides opengl support.
%endif


%package ui-dbus
Summary: QEMU D-Bus UI driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description ui-dbus
This package provides the additional D-Bus UI for QEMU.


%if %{have_gtk}
%package ui-gtk
Summary: QEMU GTK UI driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
Requires: %{name}-ui-opengl%{?_isa} = %{epoch}:%{version}-%{release}
%description ui-gtk
This package provides the additional GTK UI for QEMU.
%endif


%if %{have_sdl}
%package ui-sdl
Summary: QEMU SDL UI driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
Requires: %{name}-ui-opengl%{?_isa} = %{epoch}:%{version}-%{release}
%description ui-sdl
This package provides the additional SDL UI for QEMU.
%endif


%package ui-egl-headless
Summary: QEMU EGL headless driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
Requires: %{name}-ui-opengl%{?_isa} = %{epoch}:%{version}-%{release}
%description ui-egl-headless
This package provides the additional egl-headless UI for QEMU.


%package device-display-virtio-gpu
Summary: QEMU virtio-gpu display device
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description device-display-virtio-gpu
This package provides the virtio-gpu display device for QEMU.


%if %{have_virgl}
%package device-display-virtio-gpu-gl
Summary: QEMU virtio-gpu-gl display device
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description device-display-virtio-gpu-gl
This package provides the virtio-gpu-gl display device for QEMU.
%endif


%if %{have_rutabaga}
%package device-display-virtio-gpu-rutabaga
Summary: QEMU virtio-gpu-rutabaga display device
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description device-display-virtio-gpu-rutabaga
This package provides the virtio-gpu-rutabaga display device for QEMU.
%endif


%package device-display-virtio-gpu-pci
Summary: QEMU virtio-gpu-pci display device
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description device-display-virtio-gpu-pci
This package provides the virtio-gpu-pci display device for QEMU.


%if %{have_virgl}
%package device-display-virtio-gpu-pci-gl
Summary: QEMU virtio-gpu-pci-gl display device
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description device-display-virtio-gpu-pci-gl
This package provides the virtio-gpu-pci-gl display device for QEMU.
%endif


%if %{have_rutabaga}
%package device-display-virtio-gpu-pci-rutabaga
Summary: QEMU virtio-gpu-pci-rutabaga display device
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description device-display-virtio-gpu-pci-rutabaga
This package provides the virtio-gpu-pci-rutabaga display device for QEMU.
%endif


%package device-display-virtio-vga
Summary: QEMU virtio-vga display device
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description device-display-virtio-vga
This package provides the virtio-vga display device for QEMU.


%package device-display-virtio-vga-gl
Summary: QEMU virtio-vga-gl display device
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description device-display-virtio-vga-gl
This package provides the virtio-vga-gl display device for QEMU.


%if %{have_rutabaga}
%package device-display-virtio-vga-rutabaga
Summary: QEMU virtio-vga-rutabaga display device
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description device-display-virtio-vga-rutabaga
This package provides the virtio-vga-rutabaga display device for QEMU.
%endif


%package device-usb-host
Summary: QEMU usb host device
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description device-usb-host
This package provides the USB pass through driver for QEMU.


%package device-usb-redirect
Summary: QEMU usbredir device
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description device-usb-redirect
This package provides the usbredir device for QEMU.


%if %{have_virgl}
%package device-display-vhost-user-gpu
Summary: QEMU QXL display device
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description device-display-vhost-user-gpu
This package provides the vhost-user-gpu display device for QEMU.
%endif


%package kvm
Summary: QEMU metapackage for KVM support
Requires: %{name}-system-x86 = %{epoch}:%{version}-%{release}
%description kvm
This is a meta-package that provides a qemu-system-<arch> package for native
architectures where kvm can be enabled. For example, in an x86 system, this
will install qemu-system-x86


%package kvm-core
Summary: QEMU metapackage for KVM support
Requires: %{name}-system-x86-core = %{epoch}:%{version}-%{release}
%description kvm-core
This is a meta-package that provides a qemu-system-<arch>-core package
for native architectures where kvm can be enabled. For example, in an
x86 system, this will install qemu-system-x86-core


%package system-x86
Summary: QEMU system emulator for x86
Requires: %{name}-system-x86-core = %{epoch}:%{version}-%{release}
%{requires_all_modules}
%description system-x86
This package provides the QEMU system emulator for x86. When being run in a x86
machine that supports it, this package also provides the KVM virtualization
platform.


%package system-x86-core
Summary: QEMU system emulator for x86
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Requires: seabios-bin
Requires: seavgabios-bin
Requires: edk2-ovmf
%description system-x86-core
This package provides the QEMU system emulator for x86. When being run in a x86
machine that supports it, this package also provides the KVM virtualization
platform.


%prep
gpgv2 --keyring %{SOURCE2} %{SOURCE1} %{SOURCE0}
%autosetup -n qemu-%{version}%{?rcstr} -S git_am

%global qemu_kvm_build qemu_kvm_build
mkdir -p %{qemu_kvm_build}


%build
%define disable_everything         \\\
  --audio-drv-list=                \\\
  --disable-af-xdp                 \\\
  --disable-alsa                   \\\
  --disable-attr                   \\\
  --disable-auth-pam               \\\
  --disable-avx2                   \\\
  --disable-avx512bw               \\\
  --disable-blkio                  \\\
  --disable-block-drv-whitelist-in-tools \\\
  --disable-bochs                  \\\
  --disable-bpf                    \\\
  --disable-brlapi                 \\\
  --disable-bsd-user               \\\
  --disable-bzip2                  \\\
  --disable-cap-ng                 \\\
  --disable-capstone               \\\
  --disable-cfi                    \\\
  --disable-cfi-debug              \\\
  --disable-cloop                  \\\
  --disable-cocoa                  \\\
  --disable-colo-proxy             \\\
  --disable-coreaudio              \\\
  --disable-coroutine-pool         \\\
  --disable-crypto-afalg           \\\
  --disable-curl                   \\\
  --disable-curses                 \\\
  --disable-dbus-display           \\\
  --disable-debug-graph-lock       \\\
  --disable-debug-info             \\\
  --disable-debug-mutex            \\\
  --disable-debug-remap            \\\
  --disable-debug-tcg              \\\
  --disable-dmg                    \\\
  --disable-docs                   \\\
  --disable-download               \\\
  --disable-dsound                 \\\
  --disable-fdt                    \\\
  --disable-fuse                   \\\
  --disable-fuse-lseek             \\\
  --disable-gcrypt                 \\\
  --disable-gettext                \\\
  --disable-gio                    \\\
  --disable-glusterfs              \\\
  --disable-gnutls                 \\\
  --disable-gtk                    \\\
  --disable-gtk-clipboard          \\\
  --disable-guest-agent            \\\
  --disable-guest-agent-msi        \\\
  --disable-hv-balloon             \\\
  --disable-hvf                    \\\
  --disable-iconv                  \\\
  --disable-jack                   \\\
  --disable-kvm                    \\\
  --disable-l2tpv3                 \\\
  --disable-libdaxctl              \\\
  --disable-libdw                  \\\
  --disable-libkeyutils            \\\
  --disable-libiscsi               \\\
  --disable-libnfs                 \\\
  --disable-libpmem                \\\
  --disable-libssh                 \\\
  --disable-libudev                \\\
  --disable-libusb                 \\\
  --disable-linux-aio              \\\
  --disable-linux-io-uring         \\\
  --disable-linux-user             \\\
  --disable-lto                    \\\
  --disable-lzfse                  \\\
  --disable-lzo                    \\\
  --disable-malloc-trim            \\\
  --disable-membarrier             \\\
  --disable-modules                \\\
  --disable-module-upgrades        \\\
  --disable-mpath                  \\\
  --disable-multiprocess           \\\
  --disable-netmap                 \\\
  --disable-nettle                 \\\
  --disable-numa                   \\\
  --disable-nvmm                   \\\
  --disable-opengl                 \\\
  --disable-oss                    \\\
  --disable-pa                     \\\
  --disable-parallels              \\\
  --disable-pie                    \\\
  --disable-pipewire               \\\
  --disable-pixman                 \\\
  --disable-plugins                \\\
  --disable-qcow1                  \\\
  --disable-qed                    \\\
  --disable-qom-cast-debug         \\\
  --disable-qpl                    \\\
  --disable-rbd                    \\\
  --disable-rdma                   \\\
  --disable-relocatable            \\\
  --disable-replication            \\\
  --disable-rutabaga-gfx           \\\
  --disable-rng-none               \\\
  --disable-safe-stack             \\\
  --disable-sanitizers             \\\
  --disable-sdl                    \\\
  --disable-sdl-image              \\\
  --disable-seccomp                \\\
  --disable-selinux                \\\
  --disable-slirp                  \\\
  --disable-slirp-smbd             \\\
  --disable-smartcard              \\\
  --disable-snappy                 \\\
  --disable-sndio                  \\\
  --disable-sparse                 \\\
  --disable-spice                  \\\
  --disable-spice-protocol         \\\
  --disable-strip                  \\\
  --disable-system                 \\\
  --disable-tcg                    \\\
  --disable-tools                  \\\
  --disable-tpm                    \\\
  --disable-tsan                   \\\
  --disable-uadk                   \\\
  --disable-u2f                    \\\
  --disable-usb-redir              \\\
  --disable-user                   \\\
  --disable-vpc                    \\\
  --disable-vde                    \\\
  --disable-vdi                    \\\
  --disable-vfio-user-server       \\\
  --disable-vhdx                   \\\
  --disable-vhost-crypto           \\\
  --disable-vhost-kernel           \\\
  --disable-vhost-net              \\\
  --disable-vhost-user             \\\
  --disable-vhost-user-blk-server  \\\
  --disable-vhost-vdpa             \\\
  --disable-virglrenderer          \\\
  --disable-virtfs                 \\\
  --disable-vnc                    \\\
  --disable-vnc-jpeg               \\\
  --disable-png                    \\\
  --disable-vnc-sasl               \\\
  --disable-vte                    \\\
  --disable-vvfat                  \\\
  --disable-werror                 \\\
  --disable-whpx                   \\\
  --disable-xen                    \\\
  --disable-xen-pci-passthrough    \\\
  --disable-xkbcommon              \\\
  --disable-zstd                   \\\
  --without-default-devices

run_configure() {
    ../configure  \
        --cc=%{__cc} \
        --cxx=/bin/false \
        --prefix="%{_prefix}" \
        --libdir="%{_libdir}" \
        --datadir="%{_datadir}" \
        --sysconfdir="%{_sysconfdir}" \
        --interp-prefix=%{_prefix}/qemu-%M \
        --localstatedir="%{_localstatedir}" \
        --docdir="%{_docdir}" \
        --libexecdir="%{_libexecdir}" \
        --extra-ldflags="%{build_ldflags}" \
        --extra-cflags="%{optflags}" \
        --with-pkgversion="%{name}-%{version}-%{release}" \
        --with-suffix="qemu" \
        --firmwarepath="%firmwaredirs" \
        --with-coroutine=ucontext \
        --tls-priority=@QEMU,SYSTEM \
        %{disable_everything} \
        "$@" \
    || ( cat config.log ; exit 1 )

    echo "config-host.mak contents:"
    echo "==="
    cat config-host.mak
    echo "==="
}

# TODO removed due to errors
#  --enable-safe-stack \
# TODO possible issue
#  --enable-lto \

pushd %{qemu_kvm_build}
run_configure \
%if %{defined target_list}
  --target-list="%{target_list}" \
%endif
%if %{defined block_drivers_rw_list}
  --block-drv-rw-whitelist=%{block_drivers_rw_list} \
%endif
%if %{defined block_drivers_ro_list}
  --block-drv-ro-whitelist=%{block_drivers_ro_list} \
%endif
  --enable-af-xdp \
  --enable-attr \
  --enable-avx2 \
  --enable-avx512bw \
  --enable-blkio \
  --enable-bpf \
  --enable-cap-ng \
  --enable-capstone \
  --enable-coroutine-pool \
  --enable-dbus-display \
  --enable-debug-info \
  --enable-docs \
  --enable-fdt=system \
  --enable-gio \
  --enable-gnutls \
  --enable-iconv \
  --enable-kvm \
  --enable-l2tpv3 \
  --enable-libiscsi \
  --enable-libpmem \
  --enable-libusb \
  --enable-libudev \
  --enable-linux-aio \
  --enable-linux-io-uring \
  --enable-lto \
  --enable-lzo \
  --enable-malloc-trim \
  --enable-modules \
  --enable-mpath \
  --enable-numa \
%if %{have_opengl}
  --enable-opengl \
%endif
  --enable-pa \
  --enable-pie \
  --enable-pixman \
  --enable-rdma \
  --enable-seccomp \
  --enable-selinux \
  --enable-slirp \
  --enable-slirp-smbd \
  --enable-snappy \
  --enable-system \
  --enable-tcg \
  --enable-tools \
  --enable-tpm \
  --enable-usb-redir \
  --enable-vdi \
  --enable-vhost-kernel \
  --enable-vhost-net \
  --enable-vhost-user \
  --enable-vhost-user-blk-server \
  --enable-vhost-vdpa \
  --enable-vnc \
  --enable-png \
  --enable-vnc-sasl \
  --enable-xkbcommon \
  --enable-zstd \
  \
  \
  --with-default-devices \
  --enable-bzip2 \
  --enable-libdaxctl \
  --enable-libkeyutils \
  --enable-multiprocess \
  --enable-replication \
%if %{have_rutabaga}
  --enable-rutabaga-gfx \
%endif
  --enable-spice-protocol \
  --enable-vhost-crypto \
%if %{have_virgl}
  --enable-virglrenderer \
%endif
  --enable-virtfs \
  --enable-virtfs-proxy-helper \
  --enable-vnc-jpeg


%make_build
popd


%install
# Install qemu-pr-helper service
mkdir -p %{buildroot}%{_unitdir}
install -m 0644 contrib/systemd/qemu-pr-helper.service %{buildroot}%{_unitdir}
install -m 0644 contrib/systemd/qemu-pr-helper.socket %{buildroot}%{_unitdir}

# Install qemu-vmsr-helper service
install -m 0644 contrib/systemd/qemu-vmsr-helper.service %{buildroot}%{_unitdir}
install -m 0644 contrib/systemd/qemu-vmsr-helper.socket %{buildroot}%{_unitdir}

install -D -p -m 0644 %{_sourcedir}/vhost.conf %{buildroot}%{_sysconfdir}/modprobe.d/vhost.conf
install -D -p -m 0644 %{_sourcedir}/kvm-x86.conf %{buildroot}%{_sysconfdir}/modprobe.d/kvm.conf

# Copy some static data into place
install -D -p -m 0644 -t %{buildroot}%{qemudocdir} README.rst COPYING COPYING.LIB LICENSE docs/interop/qmp-spec.rst
install -D -p -m 0644 qemu.sasl %{buildroot}%{_sysconfdir}/sasl2/qemu.conf

mkdir -p %{buildroot}%{_datadir}/qemu
install -m 0644 scripts/dump-guest-memory.py %{buildroot}%{_datadir}/qemu

# Ensure vhost-user directory is present even if built without virgl
mkdir -p %{buildroot}%{_datadir}/qemu/vhost-user

# Create new directories and put them all under tests-src
mkdir -p %{buildroot}%{testsdir}/python
mkdir -p %{buildroot}%{testsdir}/tests
mkdir -p %{buildroot}%{testsdir}/tests/avocado
mkdir -p %{buildroot}%{testsdir}/tests/qemu-iotests
mkdir -p %{buildroot}%{testsdir}/scripts/qmp

# Install avocado_qemu tests
cp -R %{qemu_kvm_build}/tests/avocado/* %{buildroot}%{testsdir}/tests/avocado/

# Install qemu.py and qmp/ scripts required to run avocado_qemu tests
cp -R %{qemu_kvm_build}/python/qemu %{buildroot}%{testsdir}/python
cp -R %{qemu_kvm_build}/scripts/qmp/* %{buildroot}%{testsdir}/scripts/qmp
install -p -m 0755 tests/Makefile.include %{buildroot}%{testsdir}/tests/

# Install qemu-iotests
cp -R tests/qemu-iotests/* %{buildroot}%{testsdir}/tests/qemu-iotests/
cp -ur %{qemu_kvm_build}/tests/qemu-iotests/* %{buildroot}%{testsdir}/tests/qemu-iotests/

# Do the actual qemu tree install
pushd %{qemu_kvm_build}
%make_install
popd

# We need to make the block device modules and other qemu SO files executable
# otherwise RPM won't pick up their dependencies.
chmod +x %{buildroot}%{_libdir}/qemu/*.so

# Remove docs we don't care about
find %{buildroot}%{qemudocdir} -name .buildinfo -delete
rm -rf %{buildroot}%{qemudocdir}/specs

# Provided by package openbios
rm -rf %{buildroot}%{_datadir}/qemu/openbios-ppc
rm -rf %{buildroot}%{_datadir}/qemu/openbios-sparc32
rm -rf %{buildroot}%{_datadir}/qemu/openbios-sparc64
# Provided by package SLOF
rm -rf %{buildroot}%{_datadir}/qemu/slof.bin
# Provided by package ipxe
rm -rf %{buildroot}%{_datadir}/qemu/pxe*rom
rm -rf %{buildroot}%{_datadir}/qemu/efi*rom
# Provided by package seavgabios
rm -rf %{buildroot}%{_datadir}/qemu/vgabios*bin
# Provided by package seabios
rm -rf %{buildroot}%{_datadir}/qemu/bios*.bin
# Provided by edk2
rm -rf %{buildroot}%{_datadir}/qemu/edk2*
rm -rf %{buildroot}%{_datadir}/qemu/firmware

# Remove sparc files
rm -f %{buildroot}%{_datadir}/qemu/QEMU,tcx.bin
rm -f %{buildroot}%{_datadir}/qemu/QEMU,cgthree.bin
# Remove ppc files
rm -f %{buildroot}%{_datadir}/qemu/bamboo.dtb
rm -f %{buildroot}%{_datadir}/qemu/canyonlands.dtb
rm -f %{buildroot}%{_datadir}/qemu/qemu_vga.ndrv
rm -f %{buildroot}%{_datadir}/qemu/skiboot.lid
rm -f %{buildroot}%{_datadir}/qemu/u-boot.e500
rm -f %{buildroot}%{_datadir}/qemu/u-boot-sam460-20100605.bin
rm -f %{buildroot}%{_datadir}/qemu/vof*.bin
# Remove hppa files
rm -f %{buildroot}%{_datadir}/qemu/hppa-firmware.img
rm -f %{buildroot}%{_datadir}/qemu/hppa-firmware64.img
# Remove arm files
rm -f %{buildroot}%{_datadir}/qemu/npcm7xx_bootrom.bin
# Remove riscv files
rm -f %{buildroot}%{_datadir}/qemu/opensbi-riscv*.bin
# Remove alpha files
rm -f %{buildroot}%{_datadir}/qemu/palcode-clipper
# Remove microblaze files
rm -f %{buildroot}%{_datadir}/qemu/petalogix*.dtb
# Remove s390x files
rm -f %{buildroot}%{_libdir}/qemu/hw-s390x-virtio-gpu-ccw.so
rm -f %{buildroot}%{_datadir}/qemu/s390-ccw.img
rm -f %{buildroot}%{_datadir}/qemu/s390-netboot.img

# Generate qemu-system-* man pages
chmod -x %{buildroot}%{_mandir}/man1/*
for emu in %{buildroot}%{_bindir}/qemu-system-*; do
    ln -sf qemu.1.gz %{buildroot}%{_mandir}/man1/$(basename $emu).1.gz
done

# Install kvm specific source bits, and qemu-kvm manpage
ln -sf qemu.1.gz %{buildroot}%{_mandir}/man1/qemu-kvm.1.gz
ln -sf qemu-system-x86_64 %{buildroot}%{_bindir}/qemu-kvm


%check
# Disable iotests. RHEL has done this forever, and these
# tests have been flakey in the past
export MTESTARGS="--no-suite block"

%if %{with check}
pushd %{qemu_kvm_build}
echo "Testing %{name}-build"
%make_build check
popd
# endif with check
%endif


%post common
getent group kvm >/dev/null || groupadd -g 36 -r kvm
getent group qemu >/dev/null || groupadd -g 107 -r qemu
getent passwd qemu >/dev/null || \
useradd -r -u 107 -g qemu -G kvm -d / -s /sbin/nologin \
  -c "qemu user" qemu


%files img
%{_bindir}/qemu-img
%{_bindir}/qemu-io
%{_bindir}/qemu-nbd
%{_bindir}/qemu-storage-daemon
%{_mandir}/man1/qemu-img.1*
%{_mandir}/man8/qemu-nbd.8*
%{_mandir}/man1/qemu-storage-daemon.1*
%{_mandir}/man7/qemu-storage-daemon-qmp-ref.7*


%files
# Deliberately empty


%files pr-helper
%{_bindir}/qemu-pr-helper
%{_unitdir}/qemu-pr-helper.service
%{_unitdir}/qemu-pr-helper.socket
%{_mandir}/man8/qemu-pr-helper.8*


%files tools
%{_bindir}/qemu-keymap
%{_bindir}/qemu-edid
%{_datadir}/qemu/dump-guest-memory.py*
%{_datadir}/qemu/trace-events-all


%files docs
%doc %{qemudocdir}


%files common
%license COPYING COPYING.LIB LICENSE
%dir %{_datadir}/qemu/
%dir %{_datadir}/qemu/vhost-user/
%{_datadir}/icons/*
%{_datadir}/qemu/keymaps/
%{_datadir}/qemu/linuxboot_dma.bin
%attr(4755, -, -) %{_libexecdir}/qemu-bridge-helper
%{_mandir}/man1/qemu.1*
%{_mandir}/man7/qemu-block-drivers.7*
%{_mandir}/man7/qemu-cpu-models.7*
%{_mandir}/man7/qemu-qmp-ref.7*
%config(noreplace) %{_sysconfdir}/modprobe.d/kvm.conf
%config(noreplace) %{_sysconfdir}/modprobe.d/vhost.conf
%config(noreplace) %{_sysconfdir}/sasl2/qemu.conf

%{_datadir}/applications/qemu.desktop
%exclude %{_datadir}/qemu/qemu-nsis.bmp
%{_libexecdir}/virtfs-proxy-helper
%{_mandir}/man1/virtfs-proxy-helper.1*


%files tests
%{testsdir}
%{_libdir}/qemu/accel-qtest-*.so


%files block-blkio
%{_libdir}/qemu/block-blkio.so


%files block-iscsi
%{_libdir}/qemu/block-iscsi.so


%if %{have_opengl}
%files ui-opengl
%{_libdir}/qemu/ui-opengl.so
%endif


%files audio-dbus
%{_libdir}/qemu/audio-dbus.so


%files audio-pa
%{_libdir}/qemu/audio-pa.so


%if %{have_sdl}
%files audio-sdl
%{_libdir}/qemu/audio-sdl.so
%endif


%files ui-dbus
%{_libdir}/qemu/ui-dbus.so


%files ui-egl-headless
%{_libdir}/qemu/ui-egl-headless.so


%files device-display-virtio-gpu
%{_libdir}/qemu/hw-display-virtio-gpu.so


%if %{have_virgl}
%files device-display-virtio-gpu-gl
%{_libdir}/qemu/hw-display-virtio-gpu-gl.so
%endif


%if %{have_rutabaga}
%files device-display-virtio-gpu-rutabaga
%{_libdir}/qemu/hw-display-virtio-gpu-rutabaga.so
%endif


%files device-display-virtio-gpu-pci
%{_libdir}/qemu/hw-display-virtio-gpu-pci.so


%if %{have_virgl}
%files device-display-virtio-gpu-pci-gl
%{_libdir}/qemu/hw-display-virtio-gpu-pci-gl.so
%endif


%if %{have_rutabaga}
%files device-display-virtio-gpu-pci-rutabaga
%{_libdir}/qemu/hw-display-virtio-gpu-pci-rutabaga.so
%endif


%files device-display-virtio-vga
%{_libdir}/qemu/hw-display-virtio-vga.so


%files device-display-virtio-vga-gl
%{_libdir}/qemu/hw-display-virtio-vga-gl.so


%if %{have_rutabaga}
%files device-display-virtio-vga-rutabaga
%{_libdir}/qemu/hw-display-virtio-vga-rutabaga.so
%endif


%files device-usb-host
%{_libdir}/qemu/hw-usb-host.so


%files device-usb-redirect
%{_libdir}/qemu/hw-usb-redirect.so


%if %{have_virgl}
%files device-display-vhost-user-gpu
%{_datadir}/qemu/vhost-user/50-qemu-gpu.json
%{_libexecdir}/vhost-user-gpu
%endif


%files kvm
# Deliberately empty

%files kvm-core
# Deliberately empty


%files system-x86
%files system-x86-core
%{_bindir}/qemu-system-x86_64
%{_libdir}/qemu/accel-tcg-x86_64.so
%{_mandir}/man1/qemu-system-x86_64.1*
%{_datadir}/qemu/kvmvapic.bin
%{_datadir}/qemu/linuxboot.bin
%{_datadir}/qemu/multiboot.bin
%{_datadir}/qemu/multiboot_dma.bin
%{_datadir}/qemu/pvh.bin
%{_datadir}/qemu/qboot.rom
%{_bindir}/qemu-kvm
%{_mandir}/man1/qemu-kvm.1*
%{_bindir}/qemu-vmsr-helper
%{_unitdir}/qemu-vmsr-helper.service
%{_unitdir}/qemu-vmsr-helper.socket


%changelog
* Wed Oct 9 2024 Zachary Huff <zach@pritunl.com> - 9.1.0-1
- Rebase to qemu 9.1.0
