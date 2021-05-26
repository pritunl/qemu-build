%ifarch %{ix86}
%global kvm_package   system-x86
# need_qemu_kvm should only ever be used by x86
%global need_qemu_kvm 1
%endif
%ifarch x86_64
%global kvm_package   system-x86
# need_qemu_kvm should only ever be used by x86
%global need_qemu_kvm 1
%endif
%ifarch %{power64}
%global kvm_package   system-ppc
%endif
%ifarch s390x
%global kvm_package   system-s390x
%endif
%ifarch armv7hl
%global kvm_package   system-arm
%endif
%ifarch aarch64
%global kvm_package   system-aarch64
%endif
%ifarch %{mips}
%global kvm_package   system-mips
%endif
%ifarch riscv64
%global kvm_package   system-riscv
%endif

%global user_static 1

%global have_kvm 0
%if 0%{?kvm_package:1}
%global have_kvm 1
%endif

# Matches numactl ExcludeArch
%global have_numactl 1
%ifarch %{arm}
%global have_numactl 0
%endif

# Matches spice ExclusiveArch
%global have_spice 1

# Matches xen ExclusiveArch
%global have_xen 0

%global have_liburing 1

%global have_virgl 1

%global have_pmem 0
%ifarch x86_64 %{power64}
%global have_pmem 1
%endif

%global have_jack 0


# Matches edk2.spec ExclusiveArch
%global have_edk2 0
%ifarch %{ix86} x86_64 %{arm} aarch64
%global have_edk2 1
%endif

# If we can run qemu-sanity-check, hostqemu gets defined.
%ifarch %{arm}
%global hostqemu arm-softmmu/qemu-system-arm
%endif
%ifarch aarch64
%global hostqemu aarch64-softmmu/qemu-system-aarch64
%endif
%ifarch %{ix86}
%global hostqemu i386-softmmu/qemu-system-i386
%endif
%ifarch x86_64
%global hostqemu x86_64-softmmu/qemu-system-x86_64
%endif

%global qemu_sanity_check 0
%ifarch x %{?kernel_arches}
%if 0%{?hostqemu:1}
%global qemu_sanity_check 1
%endif
%endif

# QEMU sanity check doesn't know how to pick machine type
# which is needed on ARM as there is no defualt
# https://bugzilla.redhat.com/show_bug.cgi?id=1875763
%ifarch %{arm} aarch64
%global qemu_sanity_check 0
%endif

# All modules should be listed here.
%ifarch %{ix86} %{arm}
%define with_block_rbd 0
%else
%define with_block_rbd 1
%endif
%global with_block_gluster 1

%define with_block_nfs 1

%ifarch %{arm}
%define with_rdma 0
%else
%define with_rdma 1
%endif

%define evr %{epoch}:%{version}-%{release}

%define requires_block_curl Requires: %{name}-block-curl = %{evr}
%define requires_block_dmg Requires: %{name}-block-dmg = %{evr}
%if %{with_block_gluster}
%define requires_block_gluster Requires: %{name}-block-gluster = %{evr}
%define obsoletes_block_gluster %{nil}
%else
%define requires_block_gluster %{nil}
%define obsoletes_block_gluster Obsoletes: %{name}-block-gluster < %{evr}
%endif
%define requires_block_iscsi Requires: %{name}-block-iscsi = %{evr}
%if %{with_block_nfs}
%define requires_block_nfs Requires: %{name}-block-nfs = %{evr}
%define obsoletes_block_nfs %{nil}
%else
%define requires_block_nfs %{nil}
%define obsoletes_block_nfs Obsoletes: %{name}-block-nfs < %{evr}
%endif
%if %{with_block_rbd}
%define requires_block_rbd Requires: %{name}-block-rbd = %{evr}
%define obsoletes_block_rbd %{nil}
%else
%define requires_block_rbd %{nil}
%define obsoletes_block_rbd Obsoletes: %{name}-block-rbd < %{evr}
%endif
%define requires_block_ssh Requires: %{name}-block-ssh = %{evr}
%define requires_audio_alsa Requires: %{name}-audio-alsa = %{evr}
%define requires_audio_oss Requires: %{name}-audio-oss = %{evr}
%define requires_audio_pa Requires: %{name}-audio-pa = %{evr}
%define requires_char_baum Requires: %{name}-char-baum = %{evr}
%define requires_device_usb_redirect Requires: %{name}-device-usb-redirect = %{evr}
%define requires_device_usb_smartcard Requires: %{name}-device-usb-smartcard = %{evr}
%define requires_ui_curses Requires: %{name}-ui-curses = %{evr}
%define requires_ui_egl_headless Requires: %{name}-ui-egl-headless = %{evr}
%define requires_ui_opengl Requires: %{name}-ui-opengl = %{evr}
%define requires_device_display_virtio_gpu Requires: %{name}-device-display-virtio-gpu = %{evr}
%define requires_device_display_virtio_gpu_pci Requires: %{name}-device-display-virtio-gpu-pci = %{evr}
%define requires_device_display_virtio_gpu_ccw Requires: %{name}-device-display-virtio-gpu-ccw = %{evr}
%define requires_device_display_virtio_vga Requires: %{name}-device-display-virtio-vga = %{evr}

%if %{have_jack}
%define requires_audio_jack Requires: %{name}-audio-jack = %{evr}
%else
%define requires_audio_jack %{nil}
%endif

%if %{have_spice}
%define requires_ui_spice_app Requires: %{name}-ui-spice-app = %{evr}
%define requires_ui_spice_core Requires: %{name}-ui-spice-core = %{evr}
%define requires_device_display_qxl Requires: %{name}-device-display-qxl = %{evr}
%define requires_audio_spice Requires: %{name}-audio-spice = %{evr}
%define requires_char_spice Requires: %{name}-char-spice = %{evr}
%else
%define requires_ui_spice_app %{nil}
%define requires_ui_spice_core %{nil}
%define requires_device_display_qxl %{nil}
%define requires_audio_spice %{nil}
%define requires_char_spice %{nil}
%endif

%global requires_all_modules \
%{requires_block_curl} \
%{requires_block_dmg} \
%{requires_block_gluster} \
%{requires_block_iscsi} \
%{requires_block_nfs} \
%{requires_block_rbd} \
%{requires_block_ssh} \
%{requires_audio_alsa} \
%{requires_audio_oss} \
%{requires_audio_pa} \
%{requires_audio_jack} \
%{requires_audio_spice} \
%{requires_ui_curses} \
%{requires_ui_egl_headless} \
%{requires_ui_opengl} \
%{requires_ui_spice_app} \
%{requires_ui_spice_core} \
%{requires_char_baum} \
%{requires_char_spice} \
%{requires_device_display_qxl} \
%{requires_device_display_virtio_gpu} \
%{requires_device_display_virtio_gpu_pci} \
%{requires_device_display_virtio_vga} \
%{requires_device_usb_redirect} \
%{requires_device_usb_smartcard} \

# Modules which can be conditionally built
%global obsoletes_some_modules \
%{obsoletes_block_gluster} \
%{obsoletes_block_rbd} \
%{obsoletes_block_rbd}

# Release candidate version tracking
# global rcver rc4
%if 0%{?rcver:1}
%global rcrel .%{rcver}
%global rcstr -%{rcver}
%endif


Summary: QEMU is a FAST! processor emulator
Name: pritunl-qemu
Version: 6.0.0
Release: 1%{?rcrel}%{?dist}
Epoch: 2
License: GPLv2 and BSD and MIT and CC-BY
URL: http://www.qemu.org/

Source0: http://wiki.qemu-project.org/download/qemu-%{version}%{?rcstr}.tar.xz

# guest agent service
Source10: qemu-guest-agent.service
Source17: qemu-ga.sysconfig
# guest agent udev rules
Source11: 99-qemu-guest-agent.rules
# /etc/qemu/bridge.conf
Source12: bridge.conf
# /etc/modprobe.d/kvm.conf, for x86
Source20: kvm-x86.modprobe.conf
# /etc/security/limits.d/95-kvm-ppc64-memlock.conf
Source21: 95-kvm-ppc64-memlock.conf


BuildRequires: make
BuildRequires: meson
BuildRequires: gcc
# documentation deps
BuildRequires: texinfo
%if %{qemu_sanity_check}
BuildRequires: qemu-sanity-check-nodeps
BuildRequires: kernel
%endif
# chrpath calls in specfile
BuildRequires: chrpath

# used in various places for compression
BuildRequires: zlib-devel
# used in various places for crypto
BuildRequires: gnutls-devel
# VNC sasl auth support
BuildRequires: cyrus-sasl-devel
# aio implementation for block drivers
BuildRequires: libaio-devel
# pulseaudio audio output
BuildRequires: pulseaudio-libs-devel
# alsa audio output
BuildRequires: alsa-lib-devel
# qemu-pr-helper multipath support (requires libudev too)
BuildRequires: device-mapper-multipath-devel
BuildRequires: systemd-devel
# iscsi drive support
BuildRequires: libiscsi-devel
# NFS drive support
BuildRequires: libnfs-devel
# snappy compression for memory dump
BuildRequires: snappy-devel
# lzo compression for memory dump
BuildRequires: lzo-devel
# curses display backend
BuildRequires: ncurses-devel
# 9pfs filesystem
BuildRequires: libattr-devel
# qemu-bridge-helper, qemu-pr-helper and more
BuildRequires: libcap-ng-devel
# spice usb redirection support
BuildRequires: usbredir-devel
%if %{have_spice}
# spice graphics support
BuildRequires: spice-protocol
BuildRequires: spice-server-devel
%endif
# seccomp containment support
BuildRequires: libseccomp-devel
# network block driver
BuildRequires: libcurl-devel
%if %{with_block_rbd}
# RBD block driver
BuildRequires: librbd-devel
%endif
# We need both because the 'stap' binary is probed for by configure
BuildRequires: systemtap
BuildRequires: systemtap-sdt-devel
# VNC JPEG support
BuildRequires: libjpeg-devel
# VNC PNG support
BuildRequires: libpng-devel
# Braille device support
BuildRequires: brlapi-devel
# FDT device tree support
BuildRequires: libfdt-devel
# QEMU display pixel manipulation
BuildRequires: pixman-devel
%if %{with_block_gluster}
# gluster block driver
BuildRequires: glusterfs-api-devel
%endif
# USB passthrough
BuildRequires: libusbx-devel
# SSH block driver
BuildRequires: libssh-devel
# GTK translations
BuildRequires: gettext
# RDMA migration
%if %{with_rdma}
BuildRequires: rdma-core-devel
%endif
%if %{have_xen}
# Xen support
BuildRequires: xen-devel
%endif
%if %{have_numactl}
# memdev hostmem backend
BuildRequires: numactl-devel
%endif
# reading bzip2 compressed dmg images
BuildRequires: bzip2-devel
# opengl bits
BuildRequires: libepoxy-devel
# TLS test suite
BuildRequires: libtasn1-devel
# smartcard device
BuildRequires: libcacard-devel
%if %{have_virgl}
# virgl 3d support
BuildRequires: virglrenderer-devel
%endif
# gtk GL support, vhost-user-gpu
BuildRequires: mesa-libgbm-devel
# preferred disassembler for TCG
BuildRequires: capstone-devel
# parallels disk images require libxml2
BuildRequires: libxml2-devel
%if %{have_pmem}
# nvdimm
BuildRequires: libpmem-devel
%endif
# qemu-ga
BuildRequires: libudev-devel
# qauth infrastructure
BuildRequires: pam-devel
# user-mode networking
BuildRequires: libslirp-devel
# Documentation build
BuildRequires: python3-sphinx
# Test suite ./scripts/tap-driver.pl
BuildRequires: perl-Test-Harness
# For making python shebangs versioned
BuildRequires: /usr/bin/pathfix.py
BuildRequires: python3-devel
%if %{have_liburing}
# liburing support. Library isn't built for arm
BuildRequires: liburing-devel
%endif
# zstd compression support
BuildRequires: libzstd-devel
# `hostname` used by test suite
BuildRequires: hostname
# nvdimm dax
BuildRequires: daxctl-devel
# used by some linux user impls
BuildRequires: libdrm-devel
# fuse block device
BuildRequires: fuse-devel
%if %{have_jack}
# jack audio driver
BuildRequires: jack-audio-connection-kit-devel
%endif

%if %{user_static}
BuildRequires: glibc-static pcre-static glib2-static zlib-static
%endif


Requires: %{name}-user = %{epoch}:%{version}-%{release}
Requires: %{name}-system-aarch64 = %{epoch}:%{version}-%{release}
Requires: %{name}-system-alpha = %{epoch}:%{version}-%{release}
Requires: %{name}-system-arm = %{epoch}:%{version}-%{release}
Requires: %{name}-system-avr = %{epoch}:%{version}-%{release}
Requires: %{name}-system-cris = %{epoch}:%{version}-%{release}
Requires: %{name}-system-m68k = %{epoch}:%{version}-%{release}
Requires: %{name}-system-microblaze = %{epoch}:%{version}-%{release}
Requires: %{name}-system-mips = %{epoch}:%{version}-%{release}
Requires: %{name}-system-nios2 = %{epoch}:%{version}-%{release}
Requires: %{name}-system-or1k = %{epoch}:%{version}-%{release}
Requires: %{name}-system-ppc = %{epoch}:%{version}-%{release}
Requires: %{name}-system-riscv = %{epoch}:%{version}-%{release}
Requires: %{name}-system-rx = %{epoch}:%{version}-%{release}
Requires: %{name}-system-s390x = %{epoch}:%{version}-%{release}
Requires: %{name}-system-sh4 = %{epoch}:%{version}-%{release}
Requires: %{name}-system-sparc = %{epoch}:%{version}-%{release}
Requires: %{name}-system-tricore = %{epoch}:%{version}-%{release}
Requires: %{name}-system-x86 = %{epoch}:%{version}-%{release}
Requires: %{name}-system-xtensa = %{epoch}:%{version}-%{release}
Requires: %{name}-img = %{epoch}:%{version}-%{release}


%description
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation. QEMU has two operating modes:

 * Full system emulation. In this mode, QEMU emulates a full system (for
   example a PC), including a processor and various peripherials. It can be
   used to launch different Operating Systems without rebooting the PC or
   to debug system code.
 * User mode emulation. In this mode, QEMU can launch Linux processes compiled
   for one CPU on another CPU.

As QEMU requires no host kernel patches to run, it is safe and easy to use.


%package  common
Summary: QEMU common files needed by all QEMU targets
Requires: ipxe-roms-qemu
Requires(post): /usr/bin/getent
Requires(post): /usr/sbin/groupadd
Requires(post): /usr/sbin/useradd
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
Obsoletes: %{name}-system-lm32 <= %{epoch}:%{version}-%{release}
Obsoletes: %{name}-system-lm32-core <= %{epoch}:%{version}-%{release}
Obsoletes: %{name}-system-moxie <= %{epoch}:%{version}-%{release}
Obsoletes: %{name}-system-moxie-core <= %{epoch}:%{version}-%{release}
Obsoletes: %{name}-system-unicore32 <= %{epoch}:%{version}-%{release}
Obsoletes: %{name}-system-unicore32-core <= %{epoch}:%{version}-%{release}
%{obsoletes_some_modules}
%description common
This package provides the common files needed by all QEMU targets


%package guest-agent
Summary: QEMU guest agent
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
%description guest-agent
This package provides an agent to run inside guests, which communicates
with the host over a virtio-serial channel named "org.qemu.guest_agent.0"

This package does not need to be installed on the host OS.


%package  img
Summary: QEMU command line tool for manipulating disk images
%description img
This package provides a command line tool for manipulating disk images


%package  block-curl
Summary: QEMU CURL block driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description block-curl
This package provides the additional CURL block driver for QEMU.

Install this package if you want to access remote disks over
http, https, ftp and other transports provided by the CURL library.


%package  block-dmg
Summary: QEMU block driver for DMG disk images
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description block-dmg
This package provides the additional DMG block driver for QEMU.

Install this package if you want to open '.dmg' files.


%if %{with_block_gluster}
%package  block-gluster
Summary: QEMU Gluster block driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description block-gluster
This package provides the additional Gluster block driver for QEMU.

Install this package if you want to access remote Gluster storage.
%endif


%package  block-iscsi
Summary: QEMU iSCSI block driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description block-iscsi
This package provides the additional iSCSI block driver for QEMU.

Install this package if you want to access iSCSI volumes.


%if %{with_block_nfs}
%package  block-nfs
Summary: QEMU NFS block driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}

%description block-nfs
This package provides the additional NFS block driver for QEMU.

Install this package if you want to access remote NFS storage.
%endif


%if %{with_block_rbd}
%package  block-rbd
Summary: QEMU Ceph/RBD block driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description block-rbd
This package provides the additional Ceph/RBD block driver for QEMU.

Install this package if you want to access remote Ceph volumes
using the rbd protocol.
%endif

%package  block-ssh
Summary: QEMU SSH block driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description block-ssh
This package provides the additional SSH block driver for QEMU.

Install this package if you want to access remote disks using
the Secure Shell (SSH) protocol.


%package  audio-alsa
Summary: QEMU ALSA audio driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description audio-alsa
This package provides the additional ALSA audio driver for QEMU.

%package  audio-oss
Summary: QEMU OSS audio driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description audio-oss
This package provides the additional OSS audio driver for QEMU.

%package  audio-pa
Summary: QEMU PulseAudio audio driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description audio-pa
This package provides the additional PulseAudi audio driver for QEMU.

%if %{have_jack}
%package  audio-jack
Summary: QEMU Jack audio driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description audio-jack
This package provides the additional Jack audio driver for QEMU.
%endif


%package  ui-curses
Summary: QEMU curses UI driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description ui-curses
This package provides the additional curses UI for QEMU.

%package  ui-egl-headless
Summary: QEMU EGL headless driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
Requires: %{name}-ui-opengl%{?_isa} = %{epoch}:%{version}-%{release}
%description ui-egl-headless
This package provides the additional egl-headless UI for QEMU.

%package  ui-opengl
Summary: QEMU OpenGL driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description ui-opengl
This package provides the additional opengl UI for QEMU.


%package  char-baum
Summary: QEMU Baum chardev driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description char-baum
This package provides the Baum chardev driver for QEMU.


%package device-display-virtio-gpu
Summary: QEMU virtio-gpu display device
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description device-display-virtio-gpu
This package provides the virtio-gpu display device for QEMU.
%package device-display-virtio-gpu-pci
Summary: QEMU virtio-gpu-pci display device
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description device-display-virtio-gpu-pci
This package provides the virtio-gpu-pci display device for QEMU.
%package device-display-virtio-gpu-ccw
Summary: QEMU virtio-gpu-ccw display device
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description device-display-virtio-gpu-ccw
This package provides the virtio-gpu-ccw display device for QEMU.
%package device-display-virtio-vga
Summary: QEMU virtio-vga display device
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description device-display-virtio-vga
This package provides the virtio-vga display device for QEMU.

%package device-usb-redirect
Summary: QEMU usbredir device
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description device-usb-redirect
This package provides the usbredir device for QEMU.

%package device-usb-smartcard
Summary: QEMU USB smartcard device
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description device-usb-smartcard
This package provides the USB smartcard device for QEMU.


%if %{have_spice}
%package  ui-spice-core
Summary: QEMU spice-core UI driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
Requires: %{name}-ui-opengl%{?_isa} = %{epoch}:%{version}-%{release}
%description ui-spice-core
This package provides the additional spice-core UI for QEMU.

%package  ui-spice-app
Summary: QEMU spice-app UI driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
Requires: %{name}-ui-spice-core%{?_isa} = %{epoch}:%{version}-%{release}
Requires: %{name}-char-spice%{?_isa} = %{epoch}:%{version}-%{release}
%description ui-spice-app
This package provides the additional spice-app UI for QEMU.

%package device-display-qxl
Summary: QEMU QXL display device
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
Requires: %{name}-ui-spice-core%{?_isa} = %{epoch}:%{version}-%{release}
%description device-display-qxl
This package provides the QXL display device for QEMU.

%package  char-spice
Summary: QEMU spice chardev driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
Requires: %{name}-ui-spice-core%{?_isa} = %{epoch}:%{version}-%{release}
%description char-spice
This package provides the spice chardev driver for QEMU.

%package  audio-spice
Summary: QEMU spice audio driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
Requires: %{name}-ui-spice-core%{?_isa} = %{epoch}:%{version}-%{release}
%description audio-spice
This package provides the spice audio driver for QEMU.
%endif


%if %{have_kvm}
%package kvm
Summary: QEMU metapackage for KVM support
Requires: %{name}-%{kvm_package} = %{epoch}:%{version}-%{release}
%description kvm
This is a meta-package that provides a qemu-system-<arch> package for native
architectures where kvm can be enabled. For example, in an x86 system, this
will install qemu-system-x86


%package kvm-core
Summary: QEMU metapackage for KVM support
Requires: %{name}-%{kvm_package}-core = %{epoch}:%{version}-%{release}
%description kvm-core
This is a meta-package that provides a qemu-system-<arch>-core package
for native architectures where kvm can be enabled. For example, in an
x86 system, this will install qemu-system-x86-core
%endif


%package user
Summary: QEMU user mode emulation of qemu targets
Requires: %{name}-common = %{epoch}:%{version}-%{release}
# On upgrade, make qemu-user get replaced with qemu-user + qemu-user-binfmt
Obsoletes: %{name}-user < 2:2.6.0-5%{?dist}
%description user
This package provides the user mode emulation of qemu targets


%package user-binfmt
Summary: QEMU user mode emulation of qemu targets
Requires: %{name}-user = %{epoch}:%{version}-%{release}
Requires(post): systemd-units
Requires(postun): systemd-units
# qemu-user-binfmt + qemu-user-static both provide binfmt rules
Conflicts: %{name}-user-static
# On upgrade, make qemu-user get replaced with qemu-user + qemu-user-binfmt
Obsoletes: %{name}-user < 2:2.6.0-5%{?dist}
%description user-binfmt
This package provides the user mode emulation of qemu targets

%if %{user_static}
%package user-static
Summary: QEMU user mode emulation of qemu targets static build
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Requires(post): systemd-units
Requires(postun): systemd-units
# qemu-user-binfmt + qemu-user-static both provide binfmt rules
Conflicts: %{name}-user-binfmt
Provides: %{name}-user-binfmt
%description user-static
This package provides the user mode emulation of qemu targets built as
static binaries
%endif


%package system-aarch64
Summary: QEMU system emulator for AArch64
Requires: %{name}-system-aarch64-core = %{epoch}:%{version}-%{release}
%{requires_all_modules}
%description system-aarch64
This package provides the QEMU system emulator for AArch64.

%package system-aarch64-core
Summary: QEMU system emulator for AArch64
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%if %{have_edk2}
Requires: edk2-aarch64
%endif
%description system-aarch64-core
This package provides the QEMU system emulator for AArch64.


%package system-alpha
Summary: QEMU system emulator for Alpha
Requires: %{name}-system-alpha-core = %{epoch}:%{version}-%{release}
%{requires_all_modules}
%description system-alpha
This package provides the QEMU system emulator for Alpha systems.

%package system-alpha-core
Summary: QEMU system emulator for Alpha
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-alpha-core
This package provides the QEMU system emulator for Alpha systems.


%package system-arm
Summary: QEMU system emulator for ARM
Requires: %{name}-system-arm-core = %{epoch}:%{version}-%{release}
%{requires_all_modules}
%description system-arm
This package provides the QEMU system emulator for ARM systems.

%package system-arm-core
Summary: QEMU system emulator for ARM
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-arm-core
This package provides the QEMU system emulator for ARM boards.


%package system-avr
Summary: QEMU system emulator for AVR
Requires: %{name}-system-avr-core = %{epoch}:%{version}-%{release}
%{requires_all_modules}
%description system-avr
This package provides the QEMU system emulator for AVR systems.

%package system-avr-core
Summary: QEMU system emulator for AVR
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-avr-core
This package provides the QEMU system emulator for AVR systems.


%package system-cris
Summary: QEMU system emulator for CRIS
Requires: %{name}-system-cris-core = %{epoch}:%{version}-%{release}
%{requires_all_modules}
%description system-cris
This package provides the system emulator for CRIS systems.

%package system-cris-core
Summary: QEMU system emulator for CRIS
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-cris-core
This package provides the system emulator for CRIS boards.


%package system-hppa
Summary: QEMU system emulator for HPPA
Requires: %{name}-system-hppa-core = %{epoch}:%{version}-%{release}
%{requires_all_modules}
%description system-hppa
This package provides the QEMU system emulator for HPPA.

%package system-hppa-core
Summary: QEMU system emulator for hppa
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-hppa-core
This package provides the QEMU system emulator for HPPA.


%package system-m68k
Summary: QEMU system emulator for ColdFire (m68k)
Requires: %{name}-system-m68k-core = %{epoch}:%{version}-%{release}
%{requires_all_modules}
%description system-m68k
This package provides the QEMU system emulator for ColdFire boards.

%package system-m68k-core
Summary: QEMU system emulator for ColdFire (m68k)
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-m68k-core
This package provides the QEMU system emulator for ColdFire boards.


%package system-microblaze
Summary: QEMU system emulator for Microblaze
Requires: %{name}-system-microblaze-core = %{epoch}:%{version}-%{release}
%{requires_all_modules}
%description system-microblaze
This package provides the QEMU system emulator for Microblaze boards.

%package system-microblaze-core
Summary: QEMU system emulator for Microblaze
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-microblaze-core
This package provides the QEMU system emulator for Microblaze boards.


%package system-mips
Summary: QEMU system emulator for MIPS
Requires: %{name}-system-mips-core = %{epoch}:%{version}-%{release}
%{requires_all_modules}
%description system-mips
This package provides the QEMU system emulator for MIPS systems.

%package system-mips-core
Summary: QEMU system emulator for MIPS
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-mips-core
This package provides the QEMU system emulator for MIPS systems.


%package system-nios2
Summary: QEMU system emulator for nios2
Requires: %{name}-system-nios2-core = %{epoch}:%{version}-%{release}
%{requires_all_modules}
%description system-nios2
This package provides the QEMU system emulator for NIOS2.

%package system-nios2-core
Summary: QEMU system emulator for nios2
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-nios2-core
This package provides the QEMU system emulator for NIOS2.


%package system-or1k
Summary: QEMU system emulator for OpenRisc32
Requires: %{name}-system-or1k-core = %{epoch}:%{version}-%{release}
Obsoletes: %{name}-system-or32 < 2:2.9.0
%{requires_all_modules}
%description system-or1k
This package provides the QEMU system emulator for OpenRisc32 boards.

%package system-or1k-core
Summary: QEMU system emulator for OpenRisc32
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Obsoletes: %{name}-system-or32-core < 2:2.9.0
%description system-or1k-core
This package provides the QEMU system emulator for OpenRisc32 boards.


%package system-ppc
Summary: QEMU system emulator for PPC
Requires: %{name}-system-ppc-core = %{epoch}:%{version}-%{release}
%{requires_all_modules}
%description system-ppc
This package provides the QEMU system emulator for PPC and PPC64 systems.

%package system-ppc-core
Summary: QEMU system emulator for PPC
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Requires: openbios
Requires: SLOF
Requires: seavgabios-bin
%description system-ppc-core
This package provides the QEMU system emulator for PPC and PPC64 systems.


%package system-riscv
Summary: QEMU system emulator for RISC-V
Requires: %{name}-system-riscv-core = %{epoch}:%{version}-%{release}
%{requires_all_modules}
%description system-riscv
This package provides the QEMU system emulator for RISC-V systems.

%package system-riscv-core
Summary: QEMU system emulator for RISC-V
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-riscv-core
This package provides the QEMU system emulator for RISC-V systems.


%package system-rx
Summary: QEMU system emulator for RX
Requires: %{name}-system-rx-core = %{epoch}:%{version}-%{release}
%{requires_all_modules}
%description system-rx
This package provides the QEMU system emulator for RX systems.

%package system-rx-core
Summary: QEMU system emulator for RX
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-rx-core
This package provides the QEMU system emulator for RX systems.


%package system-s390x
Summary: QEMU system emulator for S390
Requires: %{name}-system-s390x-core = %{epoch}:%{version}-%{release}
%{requires_all_modules}
%description system-s390x
This package provides the QEMU system emulator for S390 systems.

%package system-s390x-core
Summary: QEMU system emulator for S390
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-s390x-core
This package provides the QEMU system emulator for S390 systems.


%package system-sh4
Summary: QEMU system emulator for SH4
Requires: %{name}-system-sh4-core = %{epoch}:%{version}-%{release}
%{requires_all_modules}
%description system-sh4
This package provides the QEMU system emulator for SH4 boards.

%package system-sh4-core
Summary: QEMU system emulator for SH4
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-sh4-core
This package provides the QEMU system emulator for SH4 boards.


%package system-sparc
Summary: QEMU system emulator for SPARC
Requires: %{name}-system-sparc-core = %{epoch}:%{version}-%{release}
%{requires_all_modules}
%description system-sparc
This package provides the QEMU system emulator for SPARC and SPARC64 systems.

%package system-sparc-core
Summary: QEMU system emulator for SPARC
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Requires: openbios
%description system-sparc-core
This package provides the QEMU system emulator for SPARC and SPARC64 systems.


%package system-tricore
Summary: QEMU system emulator for tricore
Requires: %{name}-system-tricore-core = %{epoch}:%{version}-%{release}
%{requires_all_modules}
%description system-tricore
This package provides the QEMU system emulator for Tricore.

%package system-tricore-core
Summary: QEMU system emulator for tricore
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-tricore-core
This package provides the QEMU system emulator for Tricore.


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
Requires: sgabios-bin
Requires: seavgabios-bin
%if %{have_edk2}
Requires: edk2-ovmf
%endif
%description system-x86-core
This package provides the QEMU system emulator for x86. When being run in a x86
machine that supports it, this package also provides the KVM virtualization
platform.


%package system-xtensa
Summary: QEMU system emulator for Xtensa
Requires: %{name}-system-xtensa-core = %{epoch}:%{version}-%{release}
%{requires_all_modules}
%description system-xtensa
This package provides the QEMU system emulator for Xtensa boards.

%package system-xtensa-core
Summary: QEMU system emulator for Xtensa
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-xtensa-core
This package provides the QEMU system emulator for Xtensa boards.




%prep
%setup -q -n qemu-%{version}%{?rcstr}
%autopatch -p1

# https://fedoraproject.org/wiki/Changes/Make_ambiguous_python_shebangs_error
# Fix all Python shebangs recursively in .
# -p preserves timestamps
# -n prevents creating ~backup files
# -i specifies the interpreter for the shebang
# Need to list files that do not match ^[a-zA-Z0-9_]+\.py$ explicitly!
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" scripts/qemu-trace-stap




%build
# Disable LTO since it caused lots of strange assert failures.
%define _lto_cflags %{nil}

# OOM killer breaks builds with parallel make on s390(x)
%ifarch s390x
%global _smp_mflags %{nil}
%endif

# --build-id option is used for giving info to the debug packages.
extraldflags="-Wl,--build-id";
buildldflags="VL_LDFLAGS=-Wl,--build-id"

# As of qemu 2.1, --enable-trace-backends supports multiple backends,
# but there's a performance impact for non-dtrace so we don't use them
tracebackends="dtrace"

%if %{have_spice}
    %global spiceflag --enable-spice
%else
    %global spiceflag --disable-spice
%endif


run_configure() {
    # Base configure call with standard shared options
    CC=%{__cc} CXX=%{__cxx} ../configure \
        --prefix=%{_prefix} \
        --libdir=%{_libdir} \
        --sysconfdir=%{_sysconfdir} \
        --localstatedir=%{_localstatedir} \
        --libexecdir=%{_libexecdir} \
        --interp-prefix=%{_prefix}/qemu-%%M \
        --with-pkgversion=%{name}-%{version}-%{release} \
        --extra-ldflags="$extraldflags -Wl,-z,relro -Wl,-z,now" \
        --extra-cflags="%{optflags}" \
        --disable-strip \
        --disable-werror \
        --tls-priority=@QEMU,SYSTEM \
        --enable-trace-backend=$tracebackends \
        "$@" || cat config.log
}

run_configure_disable_everything() {
    # Disable every qemu feature. Callers can --enable-X the bits they need
    run_configure \
        --audio-drv-list= \
        --without-default-features \
        --without-default-devices \
        --disable-system \
        --disable-tcg \
        --disable-user \
        --disable-blobs \
        --disable-capstone \
        --disable-fdt \
        --disable-vnc \
        --disable-vnc-jpeg \
        --disable-vnc-png \
        --disable-vhost-kernel \
        --disable-vhost-vdpa \
        "$@"
}



# Build for qemu-user-static
%if %{user_static}
mkdir build-static
pushd build-static

run_configure_disable_everything \
    --disable-pie \
    --enable-attr \
    --enable-linux-user \
    --enable-tcg \
    --static

make V=1 %{?_smp_mflags} $buildldflags

popd
%endif



# Build for non-static qemu-*
mkdir build-dynamic
pushd build-dynamic

run_configure \
    --audio-drv-list=pa,alsa,oss \
    --enable-kvm \
    --enable-system \
    --target-list-exclude=moxie-softmmu \
    --enable-tcg \
    --enable-linux-user \
    --enable-pie \
    --enable-modules \
    --enable-mpath \
    %{spiceflag} \
    --enable-slirp=system \
    --disable-sdl \
    --disable-gtk \
    --disable-vte \

echo "config-host.mak contents:"
echo "==="
cat config-host.mak
echo "==="

make V=1 %{?_smp_mflags} $buildldflags

popd




%install

%global _udevdir /lib/udev/rules.d
%global qemudocdir %{_docdir}/qemu


# Install rules to use the bridge helper with libvirt's virbr0
install -D -m 0644 %{_sourcedir}/bridge.conf %{buildroot}%{_sysconfdir}/qemu/bridge.conf


# Install qemu-guest-agent service and udev rules
install -D -p -m 0644 %{_sourcedir}/qemu-guest-agent.service %{buildroot}%{_unitdir}/qemu-guest-agent.service
install -D -p -m 0644 %{_sourcedir}/qemu-ga.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/qemu-ga
install -D -m 0644 %{_sourcedir}/99-qemu-guest-agent.rules %{buildroot}%{_udevdir}/99-qemu-guest-agent.rules


# Install qemu-ga fsfreeze bits
mkdir -p %{buildroot}%{_sysconfdir}/qemu-ga/fsfreeze-hook.d
install -p -m 0755 scripts/qemu-guest-agent/fsfreeze-hook %{buildroot}%{_sysconfdir}/qemu-ga
install -p -m 0644 scripts/qemu-guest-agent/fsfreeze-hook.d/*.sample %{buildroot}%{_sysconfdir}/qemu-ga/fsfreeze-hook.d/
mkdir -p %{buildroot}%{_localstatedir}/log
touch %{buildroot}%{_localstatedir}/log/qga-fsfreeze-hook.log


# Install qemu-pr-helper service
install -m 0644 ./contrib/systemd/qemu-pr-helper.service %{buildroot}%{_unitdir}
install -m 0644 ./contrib/systemd/qemu-pr-helper.socket %{buildroot}%{_unitdir}


# Install ppc64 memlock
%ifarch %{power64}
install -d %{buildroot}%{_sysconfdir}/security/limits.d
install -m 0644 %{_sourcedir}/95-kvm-ppc64-memlock.conf %{buildroot}%{_sysconfdir}/security/limits.d
%endif


# Install qemu-user-static tree
mkdir -p %{buildroot}%{_bindir}
%if %{user_static}
pushd build-static
make DESTDIR=%{buildroot} install

# Rename all QEMU user emulators to have a -static suffix
for src in %{buildroot}%{_bindir}/qemu-*
do
  mv $src $src-static
done

# Rename trace files to match -static suffix
for src in %{buildroot}%{_datadir}/systemtap/tapset/qemu-*.stp
do
  dst=`echo $src | sed -e 's/.stp/-static.stp/'`
  mv $src $dst
  perl -i -p -e 's/(qemu-\w+)/$1-static/g; s/(qemu\.user\.\w+)/$1.static/g' $dst
done

popd
%endif


# Install main qemu-system-* tree
pushd build-dynamic
make DESTDIR=%{buildroot} install
popd


# Copy some static data into place
install -D -p -m 0644 -t %{buildroot}%{qemudocdir} README.rst COPYING COPYING.LIB LICENSE
install -D -p -m 0644 qemu.sasl %{buildroot}%{_sysconfdir}/sasl2/qemu.conf


# Generate qemu-system-* man pages
chmod -x %{buildroot}%{_mandir}/man1/*
for emu in %{buildroot}%{_bindir}/qemu-system-*; do
    ln -sf qemu.1.gz %{buildroot}%{_mandir}/man1/$(basename $emu).1.gz
done


# Install kvm specific source bits, and qemu-kvm manpage
%if 0%{?need_qemu_kvm}
ln -sf qemu.1.gz %{buildroot}%{_mandir}/man1/qemu-kvm.1.gz
ln -sf qemu-system-x86_64 %{buildroot}%{_bindir}/qemu-kvm
install -D -p -m 0644 %{_sourcedir}/kvm-x86.modprobe.conf %{buildroot}%{_sysconfdir}/modprobe.d/kvm.conf
%endif


# Install binfmt
%global binfmt_dir %{buildroot}%{_exec_prefix}/lib/binfmt.d
mkdir -p %{binfmt_dir}

./scripts/qemu-binfmt-conf.sh --systemd ALL --exportdir %{binfmt_dir} --qemu-path %{_bindir}
for i in %{binfmt_dir}/*; do
    mv $i $(echo $i | sed 's/.conf/-dynamic.conf/')
done

%if %{user_static}
for regularfmt in %{binfmt_dir}/*; do
  staticfmt="$(echo $regularfmt | sed 's/-dynamic/-static/g')"
  cat $regularfmt | tr -d '\n' | sed "s/:$/-static:F/" > $staticfmt
done
%endif


# XXX With qemu 2.11 we can probably drop this symlinking with use of
# configure --firmwarepath, see qemu git 3d5eecab4

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
rm -rf %{buildroot}%{_datadir}/qemu/bios.bin
rm -rf %{buildroot}%{_datadir}/qemu/bios-256k.bin
# Provided by package sgabios
rm -rf %{buildroot}%{_datadir}/qemu/sgabios.bin
# Provided by package edk2
rm -rf %{buildroot}%{_datadir}/qemu/edk2*
rm -rf %{buildroot}%{_datadir}/qemu/firmware/*edk2*.json

pxe_link() {
  ln -s ../ipxe/$2.rom %{buildroot}%{_datadir}/qemu/pxe-$1.rom
  ln -s ../ipxe.efi/$2.rom %{buildroot}%{_datadir}/qemu/efi-$1.rom
}

pxe_link e1000 8086100e
pxe_link ne2k_pci 10ec8029
pxe_link pcnet 10222000
pxe_link rtl8139 10ec8139
pxe_link virtio 1af41000
pxe_link eepro100 80861209
pxe_link e1000e 808610d3
pxe_link vmxnet3 15ad07b0

rom_link() {
    ln -s $1 %{buildroot}%{_datadir}/qemu/$2
}

rom_link ../seavgabios/vgabios-isavga.bin vgabios.bin
rom_link ../seavgabios/vgabios-cirrus.bin vgabios-cirrus.bin
rom_link ../seavgabios/vgabios-qxl.bin vgabios-qxl.bin
rom_link ../seavgabios/vgabios-stdvga.bin vgabios-stdvga.bin
rom_link ../seavgabios/vgabios-vmware.bin vgabios-vmware.bin
rom_link ../seavgabios/vgabios-virtio.bin vgabios-virtio.bin
rom_link ../seavgabios/vgabios-ramfb.bin vgabios-ramfb.bin
rom_link ../seavgabios/vgabios-bochs-display.bin vgabios-bochs-display.bin
rom_link ../seavgabios/vgabios-ati.bin vgabios-ati.bin
rom_link ../seabios/bios.bin bios.bin
rom_link ../seabios/bios-256k.bin bios-256k.bin
rom_link ../sgabios/sgabios.bin sgabios.bin


# When building using 'rpmbuild' or 'fedpkg local', RPATHs can be left in
# the binaries and libraries (although this doesn't occur when
# building in Koji, for some unknown reason). Some discussion here:
#
# https://lists.fedoraproject.org/pipermail/devel/2013-November/192553.html
#
# In any case it should always be safe to remove RPATHs from
# the final binaries:
for f in %{buildroot}%{_bindir}/* %{buildroot}%{_libdir}/* \
         %{buildroot}%{_libexecdir}/*; do
  if file $f | grep -q ELF | grep -q -i shared; then chrpath --delete $f; fi
done


# We need to make the modules executable else
# RPM won't pick up their dependencies.
chmod +x %{buildroot}%{_libdir}/qemu/*.so



%check
# 2020-08-31: tests passing, but s390x fails due to
# spurious warning breaking an iotest case
# https://lists.gnu.org/archive/html/qemu-devel/2020-08/msg03279.html
%ifarch s390x
perl -i -p -e 's/^(127|267)/# $1/' tests/qemu-iotests/group
%endif

pushd build-dynamic
make check V=1

# Check the binary runs (see eg RHBZ#998722).
b="./x86_64-softmmu/qemu-system-x86_64"
if [ -x "$b" ]; then "$b" -help; fi

%if %{qemu_sanity_check}
# Sanity-check current kernel can boot on this qemu.
KERNEL=`find /lib/modules -name vmlinuz | head -1`
echo "Trying to boot kernel $KERNEL with %{?hostqemu}"
qemu-sanity-check --qemu=%{?hostqemu} --kernel=$KERNEL
%endif

popd


%post common
getent group kvm >/dev/null || groupadd -g 36 -r kvm
getent group qemu >/dev/null || groupadd -g 107 -r qemu
getent passwd qemu >/dev/null || \
  useradd -r -u 107 -g qemu -G kvm -d / -s /sbin/nologin \
    -c "qemu user" qemu


%post user-binfmt
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :
%postun user-binfmt
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :

%if %{user_static}
%post user-static
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :
%postun user-static
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :
%endif

%post guest-agent
%systemd_post qemu-guest-agent.service
%preun guest-agent
%systemd_preun qemu-guest-agent.service
%postun guest-agent
%systemd_postun_with_restart qemu-guest-agent.service



%files
# Deliberately empty


%files common
%license %{qemudocdir}/COPYING
%license %{qemudocdir}/COPYING.LIB
%license %{qemudocdir}/LICENSE
%doc %{qemudocdir}
%dir %{_datadir}/qemu/
%{_datadir}/applications/qemu.desktop
%{_datadir}/icons/hicolor/*/apps/*
%exclude %{_datadir}/qemu/qemu-nsis.bmp
%{_datadir}/qemu/keymaps/
%{_datadir}/qemu/trace-events-all
%{_datadir}/qemu/vgabios.bin
%{_datadir}/qemu/vgabios-cirrus.bin
%{_datadir}/qemu/vgabios-qxl.bin
%{_datadir}/qemu/vgabios-stdvga.bin
%{_datadir}/qemu/vgabios-vmware.bin
%{_datadir}/qemu/vgabios-virtio.bin
%{_datadir}/qemu/vgabios-ramfb.bin
%{_datadir}/qemu/vgabios-bochs-display.bin
%{_datadir}/qemu/vgabios-ati.bin
%{_datadir}/qemu/pxe-e1000.rom
%{_datadir}/qemu/efi-e1000.rom
%{_datadir}/qemu/pxe-e1000e.rom
%{_datadir}/qemu/efi-e1000e.rom
%{_datadir}/qemu/pxe-eepro100.rom
%{_datadir}/qemu/efi-eepro100.rom
%{_datadir}/qemu/pxe-ne2k_pci.rom
%{_datadir}/qemu/efi-ne2k_pci.rom
%{_datadir}/qemu/pxe-pcnet.rom
%{_datadir}/qemu/efi-pcnet.rom
%{_datadir}/qemu/pxe-rtl8139.rom
%{_datadir}/qemu/efi-rtl8139.rom
%{_datadir}/qemu/pxe-virtio.rom
%{_datadir}/qemu/efi-virtio.rom
%{_datadir}/qemu/pxe-vmxnet3.rom
%{_datadir}/qemu/efi-vmxnet3.rom
%{_datadir}/qemu/vhost-user/50-qemu-virtiofsd.json
%{_mandir}/man1/qemu.1*
%{_mandir}/man1/qemu-storage-daemon.1*
%{_mandir}/man1/qemu-trace-stap.1*
%{_mandir}/man1/virtfs-proxy-helper.1*
%{_mandir}/man1/virtiofsd.1*
%{_mandir}/man7/qemu-block-drivers.7*
%{_mandir}/man7/qemu-cpu-models.7*
%{_mandir}/man7/qemu-qmp-ref.7*
%{_mandir}/man7/qemu-ga-ref.7*
%{_mandir}/man7/qemu-storage-daemon-qmp-ref.7*
%{_mandir}/man8/qemu-pr-helper.8*
%{_bindir}/elf2dmp
%{_bindir}/qemu-edid
%{_bindir}/qemu-keymap
%{_bindir}/qemu-pr-helper
%{_bindir}/qemu-storage-daemon
%{_bindir}/qemu-trace-stap
%{_unitdir}/qemu-pr-helper.service
%{_unitdir}/qemu-pr-helper.socket
%attr(4755, root, root) %{_libexecdir}/qemu-bridge-helper
%{_libexecdir}/virtfs-proxy-helper
%{_libexecdir}/virtiofsd
%config(noreplace) %{_sysconfdir}/sasl2/qemu.conf
%dir %{_sysconfdir}/qemu
%config(noreplace) %{_sysconfdir}/qemu/bridge.conf
%dir %{_libdir}/qemu
%if %{have_virgl}
%{_datadir}/qemu/vhost-user/50-qemu-gpu.json
%{_libexecdir}/vhost-user-gpu
%endif


%files guest-agent
%{_bindir}/qemu-ga
%{_mandir}/man8/qemu-ga.8*
%{_unitdir}/qemu-guest-agent.service
%{_udevdir}/99-qemu-guest-agent.rules
%config(noreplace) %{_sysconfdir}/sysconfig/qemu-ga
%{_sysconfdir}/qemu-ga
%ghost %{_localstatedir}/log/qga-fsfreeze-hook.log


%files img
%{_bindir}/qemu-img
%{_bindir}/qemu-io
%{_bindir}/qemu-nbd
%{_mandir}/man1/qemu-img.1*
%{_mandir}/man8/qemu-nbd.8*


%files block-curl
%{_libdir}/qemu/block-curl.so
%files block-dmg
%{_libdir}/qemu/block-dmg-bz2.so
%if %{with_block_gluster}
%files block-gluster
%{_libdir}/qemu/block-gluster.so
%endif
%files block-iscsi
%{_libdir}/qemu/block-iscsi.so
%if %{with_block_rbd}
%files block-rbd
%{_libdir}/qemu/block-rbd.so
%endif
%files block-ssh
%{_libdir}/qemu/block-ssh.so
%if %{with_block_nfs}
%files block-nfs
%{_libdir}/qemu/block-nfs.so
%endif


%files audio-alsa
%{_libdir}/qemu/audio-alsa.so
%files audio-oss
%{_libdir}/qemu/audio-oss.so
%files audio-pa
%{_libdir}/qemu/audio-pa.so
%if %{have_jack}
%files audio-jack
%{_libdir}/qemu/audio-jack.so
%endif


%files ui-curses
%{_libdir}/qemu/ui-curses.so
%files ui-egl-headless
%{_libdir}/qemu/ui-egl-headless.so
%files ui-opengl
%{_libdir}/qemu/ui-opengl.so

%files char-baum
%{_libdir}/qemu/chardev-baum.so


%files device-display-virtio-gpu
%{_libdir}/qemu/hw-display-virtio-gpu.so
%files device-display-virtio-gpu-pci
%{_libdir}/qemu/hw-display-virtio-gpu-pci.so
%files device-display-virtio-gpu-ccw
%{_libdir}/qemu/hw-s390x-virtio-gpu-ccw.so
%files device-display-virtio-vga
%{_libdir}/qemu/hw-display-virtio-vga.so
%files device-usb-redirect
%{_libdir}/qemu/hw-usb-redirect.so
%files device-usb-smartcard
%{_libdir}/qemu/hw-usb-smartcard.so


%if %{have_spice}
%files audio-spice
%{_libdir}/qemu/audio-spice.so
%files char-spice
%{_libdir}/qemu/chardev-spice.so
%files device-display-qxl
%{_libdir}/qemu/hw-display-qxl.so
%files ui-spice-core
%{_libdir}/qemu/ui-spice-core.so
%files ui-spice-app
%{_libdir}/qemu/ui-spice-app.so
%endif


%if %{have_kvm}
%files kvm
# Deliberately empty

%files kvm-core
# Deliberately empty
%endif


%files user
%{_bindir}/qemu-i386
%{_bindir}/qemu-x86_64
%{_bindir}/qemu-aarch64
%{_bindir}/qemu-aarch64_be
%{_bindir}/qemu-alpha
%{_bindir}/qemu-arm
%{_bindir}/qemu-armeb
%{_bindir}/qemu-cris
%{_bindir}/qemu-hppa
%{_bindir}/qemu-hexagon
%{_bindir}/qemu-m68k
%{_bindir}/qemu-microblaze
%{_bindir}/qemu-microblazeel
%{_bindir}/qemu-mips
%{_bindir}/qemu-mipsel
%{_bindir}/qemu-mips64
%{_bindir}/qemu-mips64el
%{_bindir}/qemu-mipsn32
%{_bindir}/qemu-mipsn32el
%{_bindir}/qemu-nios2
%{_bindir}/qemu-or1k
%{_bindir}/qemu-ppc
%{_bindir}/qemu-ppc64
%{_bindir}/qemu-ppc64le
%{_bindir}/qemu-riscv32
%{_bindir}/qemu-riscv64
%{_bindir}/qemu-s390x
%{_bindir}/qemu-sh4
%{_bindir}/qemu-sh4eb
%{_bindir}/qemu-sparc
%{_bindir}/qemu-sparc32plus
%{_bindir}/qemu-sparc64
%{_bindir}/qemu-xtensa
%{_bindir}/qemu-xtensaeb

%{_datadir}/systemtap/tapset/qemu-i386*.stp
%{_datadir}/systemtap/tapset/qemu-x86_64*.stp
%{_datadir}/systemtap/tapset/qemu-aarch64*.stp
%{_datadir}/systemtap/tapset/qemu-alpha*.stp
%{_datadir}/systemtap/tapset/qemu-arm*.stp
%{_datadir}/systemtap/tapset/qemu-cris*.stp
%{_datadir}/systemtap/tapset/qemu-hppa*.stp
%{_datadir}/systemtap/tapset/qemu-hexagon*.stp
%{_datadir}/systemtap/tapset/qemu-m68k*.stp
%{_datadir}/systemtap/tapset/qemu-microblaze*.stp
%{_datadir}/systemtap/tapset/qemu-mips*.stp
%{_datadir}/systemtap/tapset/qemu-nios2*.stp
%{_datadir}/systemtap/tapset/qemu-or1k*.stp
%{_datadir}/systemtap/tapset/qemu-ppc*.stp
%{_datadir}/systemtap/tapset/qemu-riscv*.stp
%{_datadir}/systemtap/tapset/qemu-s390x*.stp
%{_datadir}/systemtap/tapset/qemu-sh4*.stp
%{_datadir}/systemtap/tapset/qemu-sparc*.stp
%{_datadir}/systemtap/tapset/qemu-xtensa*.stp


%files user-binfmt
%{_exec_prefix}/lib/binfmt.d/qemu-*-dynamic.conf

%if %{user_static}
%files user-static
# Just use wildcard matches here: we will catch any new/missing files
# in the qemu-user filelists
%{_exec_prefix}/lib/binfmt.d/qemu-*-static.conf
%{_bindir}/qemu-*-static
%{_datadir}/systemtap/tapset/qemu-*-static.stp
%endif


%files system-aarch64
%files system-aarch64-core
%{_bindir}/qemu-system-aarch64
%{_datadir}/systemtap/tapset/qemu-system-aarch64*.stp
%{_mandir}/man1/qemu-system-aarch64.1*


%files system-alpha
%files system-alpha-core
%{_bindir}/qemu-system-alpha
%{_datadir}/systemtap/tapset/qemu-system-alpha*.stp
%{_mandir}/man1/qemu-system-alpha.1*
%{_datadir}/qemu/palcode-clipper


%files system-arm
%files system-arm-core
%{_bindir}/qemu-system-arm
%{_datadir}/qemu/npcm7xx_bootrom.bin
%{_datadir}/systemtap/tapset/qemu-system-arm*.stp
%{_mandir}/man1/qemu-system-arm.1*


%files system-avr
%files system-avr-core
%{_bindir}/qemu-system-avr
%{_datadir}/systemtap/tapset/qemu-system-avr*.stp
%{_mandir}/man1/qemu-system-avr.1*


%files system-cris
%files system-cris-core
%{_bindir}/qemu-system-cris
%{_datadir}/systemtap/tapset/qemu-system-cris*.stp
%{_mandir}/man1/qemu-system-cris.1*


%files system-hppa
%files system-hppa-core
%{_bindir}/qemu-system-hppa
%{_datadir}/systemtap/tapset/qemu-system-hppa*.stp
%{_mandir}/man1/qemu-system-hppa.1*
%{_datadir}/qemu/hppa-firmware.img


%files system-m68k
%files system-m68k-core
%{_bindir}/qemu-system-m68k
%{_datadir}/systemtap/tapset/qemu-system-m68k*.stp
%{_mandir}/man1/qemu-system-m68k.1*


%files system-microblaze
%files system-microblaze-core
%{_bindir}/qemu-system-microblaze
%{_bindir}/qemu-system-microblazeel
%{_datadir}/systemtap/tapset/qemu-system-microblaze*.stp
%{_mandir}/man1/qemu-system-microblaze.1*
%{_mandir}/man1/qemu-system-microblazeel.1*
%{_datadir}/qemu/petalogix*.dtb


%files system-mips
%files system-mips-core
%{_bindir}/qemu-system-mips
%{_bindir}/qemu-system-mipsel
%{_bindir}/qemu-system-mips64
%{_bindir}/qemu-system-mips64el
%{_datadir}/systemtap/tapset/qemu-system-mips*.stp
%{_mandir}/man1/qemu-system-mips.1*
%{_mandir}/man1/qemu-system-mipsel.1*
%{_mandir}/man1/qemu-system-mips64el.1*
%{_mandir}/man1/qemu-system-mips64.1*


%files system-nios2
%files system-nios2-core
%{_bindir}/qemu-system-nios2
%{_datadir}/systemtap/tapset/qemu-system-nios2*.stp
%{_mandir}/man1/qemu-system-nios2.1*


%files system-or1k
%files system-or1k-core
%{_bindir}/qemu-system-or1k
%{_datadir}/systemtap/tapset/qemu-system-or1k*.stp
%{_mandir}/man1/qemu-system-or1k.1*


%files system-ppc
%files system-ppc-core
%{_bindir}/qemu-system-ppc
%{_bindir}/qemu-system-ppc64
%{_datadir}/systemtap/tapset/qemu-system-ppc*.stp
%{_mandir}/man1/qemu-system-ppc.1*
%{_mandir}/man1/qemu-system-ppc64.1*
%{_datadir}/qemu/bamboo.dtb
%{_datadir}/qemu/canyonlands.dtb
%{_datadir}/qemu/qemu_vga.ndrv
%{_datadir}/qemu/skiboot.lid
%{_datadir}/qemu/u-boot.e500
%{_datadir}/qemu/u-boot-sam460-20100605.bin
%ifarch %{power64}
%{_sysconfdir}/security/limits.d/95-kvm-ppc64-memlock.conf
%endif


%files system-riscv
%files system-riscv-core
%{_bindir}/qemu-system-riscv32
%{_bindir}/qemu-system-riscv64
%{_datadir}/qemu/opensbi-riscv*.bin
%{_datadir}/qemu/opensbi-riscv*.elf
%{_datadir}/systemtap/tapset/qemu-system-riscv*.stp
%{_mandir}/man1/qemu-system-riscv*.1*


%files system-rx
%files system-rx-core
%{_bindir}/qemu-system-rx
%{_datadir}/systemtap/tapset/qemu-system-rx*.stp
%{_mandir}/man1/qemu-system-rx.1*


%files system-s390x
%files system-s390x-core
%{_bindir}/qemu-system-s390x
%{_datadir}/systemtap/tapset/qemu-system-s390x*.stp
%{_mandir}/man1/qemu-system-s390x.1*
%{_datadir}/qemu/s390-ccw.img
%{_datadir}/qemu/s390-netboot.img


%files system-sh4
%files system-sh4-core
%{_bindir}/qemu-system-sh4
%{_bindir}/qemu-system-sh4eb
%{_datadir}/systemtap/tapset/qemu-system-sh4*.stp
%{_mandir}/man1/qemu-system-sh4.1*
%{_mandir}/man1/qemu-system-sh4eb.1*


%files system-sparc
%files system-sparc-core
%{_bindir}/qemu-system-sparc
%{_bindir}/qemu-system-sparc64
%{_datadir}/systemtap/tapset/qemu-system-sparc*.stp
%{_mandir}/man1/qemu-system-sparc.1*
%{_mandir}/man1/qemu-system-sparc64.1*
%{_datadir}/qemu/QEMU,tcx.bin
%{_datadir}/qemu/QEMU,cgthree.bin


%files system-tricore
%files system-tricore-core
%{_bindir}/qemu-system-tricore
%{_datadir}/systemtap/tapset/qemu-system-tricore*.stp
%{_mandir}/man1/qemu-system-tricore.1*


%files system-x86
%files system-x86-core
%{_bindir}/qemu-system-i386
%{_bindir}/qemu-system-x86_64
%{_datadir}/systemtap/tapset/qemu-system-i386*.stp
%{_datadir}/systemtap/tapset/qemu-system-x86_64*.stp
%{_mandir}/man1/qemu-system-i386.1*
%{_mandir}/man1/qemu-system-x86_64.1*
%{_datadir}/qemu/bios.bin
%{_datadir}/qemu/bios-256k.bin
%{_datadir}/qemu/bios-microvm.bin
%{_datadir}/qemu/kvmvapic.bin
%{_datadir}/qemu/linuxboot.bin
%{_datadir}/qemu/linuxboot_dma.bin
%{_datadir}/qemu/multiboot.bin
%{_datadir}/qemu/pvh.bin
%{_datadir}/qemu/qboot.rom
%{_datadir}/qemu/sgabios.bin
%if 0%{?need_qemu_kvm}
%{_bindir}/qemu-kvm
%{_mandir}/man1/qemu-kvm.1*
%config(noreplace) %{_sysconfdir}/modprobe.d/kvm.conf
%endif


%files system-xtensa
%files system-xtensa-core
%{_bindir}/qemu-system-xtensa
%{_bindir}/qemu-system-xtensaeb
%{_datadir}/systemtap/tapset/qemu-system-xtensa*.stp
%{_mandir}/man1/qemu-system-xtensa.1*
%{_mandir}/man1/qemu-system-xtensaeb.1*


%changelog
* Wed May 12 2021 Cole Robinson <crobinso@redhat.com> - 2:6.0.0-1
- Rebase to qemu 6.0.0 GA

* Wed Apr 21 2021 Cole Robinson <crobinso@redhat.com> - 2:6.0.0-0.3.rc4
- Rebase to qemu 6.0.0-rc4

* Wed Apr 14 2021 Richard W.M. Jones <rjones@redhat.com> - 2:6.0.0-0.2.rc2
- Rebuild for updated liburing.

* Tue Apr 06 2021 Cole Robinson <aintdiscole@gmail.com> - 6.0.0-0.1.rc2
- Rebase to qemu 6.0.0-rc2

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2:5.2.0-6.1
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Mon Mar 01 2021 Cole Robinson <aintdiscole@gmail.com> - 5.2.0-6
- Fix building on centos stream in copr

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2:5.2.0-5.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 11 2021 Paolo Bonzini <pbonzini@redhat.com> - 2:5.2.0-5
- Use symlink for qemu-kvm.
- Fix make check on bash 5.1.

* Fri Dec 11 2020 Richard W.M. Jones <rjones@redhat.com> - 2:5.2.0-4
- qemu-char-spice not qemu-chardev-spice.

* Thu Dec 10 2020 Mohan Boddu <mboddu@bhujji.com> - 5.2.0-2
- Fixing the ISA Dependencies

* Wed Dec 09 2020 Cole Robinson <aintdiscole@gmail.com> - 5.2.0-1
- Rebase to qemu-5.2.0 GA
- Fix spice and GL UI module deps (bz 1904603)

* Thu Dec 03 2020 Richard W.M. Jones <rjones@redhat.com> - 5.2.0-0.9.rc4
- Enable qemu-kvm-core package on riscv64.

* Thu Dec 03 2020 Cole Robinson <aintdiscole@gmail.com> - 5.2.0-0.8.rc4
- Rebase to qemu-5.2.0-rc4

* Tue Nov 24 2020 Cole Robinson <aintdiscole@gmail.com> - 5.2.0-0.7.rc2
- Fix running 9p tests in copr

* Thu Nov 19 2020 Paolo Bonzini <pbonzini@redhat.com> - 5.2.0-0.6.rc2
- Remove --python=... to force use of system meson

* Thu Nov 19 2020 Daniel P. Berrangé <berrange@redhat.com> - 5.2.0-0.5.rc2
- Re-enable systemtap tracing

* Wed Nov 18 2020 Cole Robinson <aintdiscole@gmail.com> - 5.2.0-0.4.rc2
- Rebase to qemu-5.2.0-rc2

* Fri Nov 13 2020 Daniel P. Berrangé <berrange@redhat.com> - 5.2.0-0.3.rc1
- Disable user mode static builds in ELN

* Wed Nov 11 2020 Cole Robinson <aintdiscole@gmail.com> - 5.2.0-0.2.rc1
- Rebase to qemu-5.2.0-rc1

* Sun Nov 08 2020 Cole Robinson <aintdiscole@gmail.com> - 5.2.0-0.1.rc0
- Rebase to qemu-5.2.0-rc0

* Thu Nov  5 2020 Daniel P. Berrangé <berrange@redhat.com> - 5.1.0-7
- Disable LTO again. Tests were not passing, we were ignoring failures.

* Mon Oct 26 2020 Daniel P. Berrangé <berrange@redhat.com> - 5.1.0-6
- Re-enable LTO since tests now pass without asserts

* Fri Sep  4 2020 Daniel P. Berrangé <berrange@redhat.com> - 5.1.0-5
- Drop conditions for ppc, ppc64, mips64 and s390 arches
- Fix host qemu binary path for aarch64
- Re-enable kernel BR for QEMU sanity check
- Fix conditionals for enabling QEMU sanity check
- Check whether emulator works before doing sanity check
- Provide explicit kernel path for QEMU sanity check
- Make QEMU sanity check a build blocker

* Thu Sep  3 2020 Daniel P. Berrangé <berrange@redhat.com> - 5.1.0-4
- Add btrfs ioctls to linux-user (rhbz #1872918)

* Tue Aug 18 2020 Tom Stellard <tstellar@redhat.com> - 5.1.0-3
- Add BuildRequires: gcc
- https://fedoraproject.org/wiki/Packaging:C_and_C%2B%2B#BuildRequires_and_Requires

* Mon Aug 17 2020 Cole Robinson <aintdiscole@gmail.com> - 5.1.0-2
- Disable dtrace generation to fix use of modules (bz 1869339)

* Tue Aug 11 2020 Cole Robinson <crobinso@redhat.com> - 5.1.0-1
- Update to version 5.1.0

* Fri Aug 07 2020 Cole Robinson <crobinso@redhat.com> - 5.1.0-0.3.rc3
- Update to version 5.1.0-rc3

* Thu Aug 06 2020 Merlin Mathesius <mmathesi@redhat.com> - 5.1.0-0.2.rc2
- Use new %%{kernel_arches} macro to determine when a full kernel is available

* Wed Aug 05 2020 Cole Robinson <aintdiscole@gmail.com> - 5.1.0-0.2.rc2
- Pull in new modules by default, like we do for others

* Tue Aug 04 2020 Cole Robinson <aintdiscole@gmail.com> - 5.1.0-0.1.rc2
- Update to qemu 5.1.0 rc2

* Fri Jul 31 2020 Daniel P. Berrangé <berrange@redhat.com> - 5.0.0-6
- Remove obsolete Fedora conditionals (PR#9)

* Thu Jul 30 2020 Richard W.M. Jones <rjones@redhat.com> - 5.0.0-5
- Disable LTO as it caused many strange assert failures.

* Wed Jul 29 2020 Richard W.M. Jones <rjones@redhat.com> - 5.0.0-4
- Backport Dan's upstream patch to fix insecure cert in test suite.

* Mon Jul 27 2020 Kevin Fenzi <kevin@scrye.com> - 5.0.0-3
- Rebuild for new xen

* Wed May 13 2020 Cole Robinson <crobinso@redhat.com> - 5.0.0-2
- Fix iouring hang (bz #1823751)

* Wed May 06 2020 Cole Robinson <crobinso@redhat.com> - 5.0.0-1
- Update to version 5.0.0

* Thu Apr 16 2020 Cole Robinson <aintdiscole@gmail.com> - 5.0.0-0.3.rc3
- Update to qemu 5.0.0 rc3

* Thu Apr 09 2020 Cole Robinson <aintdiscole@gmail.com> - 5.0.0-0.3.rc2
- Update to qemu 5.0.0 rc2

* Wed Apr 08 2020 Adam Williamson <awilliam@redhat.com> - 2:5.0.0-0.2.rc0
- Rebuild for new brltty

* Wed Mar 25 2020 Cole Robinson <crobinso@redhat.com> - 2:5.0.0-0.1.rc0
- Update to qemu-5.0.0-rc0

* Tue Mar 17 2020 Fabiano Fidêncio <fidencio@redhat.com> - 2:4.2.0-7
- Fix segfault with SR-IOV hot-{plug,unplug} (bz #1814017)

* Tue Feb 25 2020 Cole Robinson <crobinso@redhat.com> - 2:4.2.0-6
- Rebuild for libiscsi soname bump

* Sat Feb 15 2020 Cole Robinson <crobinso@redhat.com> - 2:4.2.0-5
- Fix ppc shutdown issue (bz #1784961)

* Tue Jan 28 2020 Cole Robinson <crobinso@redhat.com> - 2:4.2.0-4
- virtio-fs support

* Sat Jan 25 2020 Richard W.M. Jones <rjones@redhat.com> - 4.2.0-3
- Add miscellaneous fixes for RISC-V (RHBZ#1794902).
