%if %{defined fedora}
# actual firmware builds support cross-compiling.  edk2-tools
# in theory should build everywhere without much trouble, but
# in practice the edk2 build system barfs on archs it doesn't know
# (such as ppc), so lets limit things to the known-good ones.
ExclusiveArch: %{ix86} x86_64 %{arm} aarch64
%else
ExclusiveArch: x86_64 aarch64
%endif

%define GITDATE        20210527
%define GITCOMMIT      e1999b264f1f
%define TOOLCHAIN      GCC5
%define OPENSSL_VER    1.1.1k

%define qosb_testing 0
%ifarch x86_64
%define qosb_testing 1
%endif

%if %{defined rhel}
%define qemu_package qemu-kvm-core >= 2.12.0-89
%define qemu_binary /usr/libexec/qemu-kvm

%define build_ovmf 0
%define build_aarch64 0
%ifarch x86_64
  %define build_ovmf 1
%endif
%ifarch aarch64
  %define build_aarch64 1
%endif
%else
%define qemu_package qemu-system-x86-core
%define qemu_binary /usr/bin/qemu-system-x86_64
%define build_ovmf 1
%define build_aarch64 1
%endif

%global softfloat_version 20180726-gitb64af41
%define cross %{defined fedora}
%define disable_werror %{defined fedora}


Name:       edk2
Version:    %{GITDATE}git%{GITCOMMIT}
Release:    2%{?dist}
Summary:    UEFI firmware for 64-bit virtual machines
License:    BSD-2-Clause-Patent and OpenSSL and MIT
URL:        http://www.tianocore.org

# The source tarball is created using following commands:
# COMMIT=e1999b264f1f
# git archive --format=tar --prefix=edk2-$COMMIT/ $COMMIT \
# | xz -9ev >/tmp/edk2-$COMMIT.tar.xz
Source0: edk2-%{GITCOMMIT}.tar.xz
Source1: ovmf-whitepaper-c770f8c.txt
Source2: openssl-rhel-bdd048e929dcfcf2f046d74e812e0e3d5fc58504.tar.xz
Source3: ovmf-vars-generator
Source4: LICENSE.qosb
Source5: RedHatSecureBootPkKek1.pem

Source10: edk2-aarch64-verbose.json
Source11: edk2-aarch64.json
Source12: edk2-ovmf-sb.json
Source13: edk2-ovmf.json
Source14: edk2-ovmf-cc.json

# Fedora specific sources
Source50: softfloat-%{softfloat_version}.tar.xz
Source55: 40-edk2-ovmf-ia32-sb-enrolled.json
Source56: 50-edk2-ovmf-ia32-sb.json
Source57: 60-edk2-ovmf-ia32.json
Source58: edk2-ovmf-nosb.json
Source59: 70-edk2-arm-verbose.json

Patch0008: 0008-BaseTools-do-not-build-BrotliCompress-RH-only.patch
Patch0009: 0009-MdeModulePkg-remove-package-private-Brotli-include-p.patch
Patch0010: 0010-advertise-OpenSSL-on-TianoCore-splash-screen-boot-lo.patch
Patch0011: 0011-OvmfPkg-increase-max-debug-message-length-to-512-RHE.patch
Patch0012: 0012-MdeModulePkg-TerminalDxe-add-other-text-resolutions-.patch
Patch0013: 0013-MdeModulePkg-TerminalDxe-set-xterm-resolution-on-mod.patch
Patch0014: 0014-OvmfPkg-take-PcdResizeXterm-from-the-QEMU-command-li.patch
Patch0015: 0015-ArmVirtPkg-take-PcdResizeXterm-from-the-QEMU-command.patch
Patch0016: 0016-OvmfPkg-allow-exclusion-of-the-shell-from-the-firmwa.patch
Patch0017: 0017-ArmPlatformPkg-introduce-fixed-PCD-for-early-hello-m.patch
Patch0018: 0018-ArmPlatformPkg-PrePeiCore-write-early-hello-message-.patch
Patch0019: 0019-ArmVirtPkg-set-early-hello-message-RH-only.patch
Patch0020: 0020-OvmfPkg-enable-DEBUG_VERBOSE-RHEL-only.patch
Patch0021: 0021-OvmfPkg-silence-DEBUG_VERBOSE-0x00400000-in-QemuVide.patch
Patch0022: 0022-ArmVirtPkg-silence-DEBUG_VERBOSE-0x00400000-in-QemuR.patch
Patch0023: 0023-OvmfPkg-QemuRamfbDxe-Do-not-report-DXE-failure-on-Aa.patch
Patch0024: 0024-OvmfPkg-silence-EFI_D_VERBOSE-0x00400000-in-NvmExpre.patch
Patch0025: 0025-CryptoPkg-OpensslLib-list-RHEL8-specific-OpenSSL-fil.patch
Patch0026: 0026-OvmfPkg-QemuKernelLoaderFsDxe-suppress-error-on-no-k.patch
Patch0027: 0027-SecurityPkg-Tcg2Dxe-suppress-error-on-no-swtpm-in-si.patch

# Fedora specific
Patch1000: fedora-Tweak-the-tools_def-to-support-cross-compiling.patch


# python3-devel and libuuid-devel are required for building tools.
# python3-devel is also needed for varstore template generation and
# verification with "ovmf-vars-generator".
BuildRequires:  python3-devel
BuildRequires:  libuuid-devel
BuildRequires:  /usr/bin/iasl
BuildRequires:  binutils gcc git gcc-c++ make

%if %{build_ovmf}
# Only OVMF includes 80x86 assembly files (*.nasm*).
BuildRequires:  nasm

# Only OVMF includes the Secure Boot feature, for which we need to separate out
# the UEFI shell.
BuildRequires:  dosfstools
BuildRequires:  mtools
BuildRequires:  xorriso

# For generating the variable store template with the default certificates
# enrolled, we need the qemu-kvm executable.
BuildRequires:  %{qemu_package}

%if %{qosb_testing}
# For verifying SB enablement in the above variable store template, we need a
# guest kernel that prints "Secure boot enabled".
BuildRequires: kernel-core >= 4.18.0-161
BuildRequires: rpmdevtools
%endif

# endif build_ovmf
%endif

%if %{cross}
BuildRequires:  gcc-aarch64-linux-gnu
BuildRequires:  gcc-arm-linux-gnu
BuildRequires:  gcc-x86_64-linux-gnu
%endif



%package ovmf
Summary:    UEFI firmware for x86_64 virtual machines
BuildArch:  noarch
Provides:   OVMF = %{version}-%{release}
Obsoletes:  OVMF < 20180508-100.gitee3198e672e2.el7

# OVMF includes the Secure Boot and IPv6 features; it has a builtin OpenSSL
# library.
Provides:   bundled(openssl) = %{OPENSSL_VER}
License:    BSD-2-Clause-Patent and OpenSSL

# URL taken from the Maintainers.txt file.
URL:        http://www.tianocore.org/ovmf/

%description ovmf
OVMF (Open Virtual Machine Firmware) is a project to enable UEFI support for
Virtual Machines. This package contains a sample 64-bit UEFI firmware for QEMU
and KVM.


%package aarch64
Summary:    UEFI firmware for aarch64 virtual machines
BuildArch:  noarch
Provides:   AAVMF = %{version}-%{release}
Obsoletes:  AAVMF < 20180508-100.gitee3198e672e2.el7

# No Secure Boot for AAVMF yet, but we include OpenSSL for the IPv6 stack.
Provides:   bundled(openssl) = %{OPENSSL_VER}
License:    BSD-2-Clause-Patent and OpenSSL

# URL taken from the Maintainers.txt file.
URL:        https://github.com/tianocore/tianocore.github.io/wiki/ArmVirtPkg

%description aarch64
AAVMF (ARM Architecture Virtual Machine Firmware) is an EFI Development Kit II
platform that enables UEFI support for QEMU/KVM ARM Virtual Machines. This
package contains a 64-bit build.


%package tools
Summary:        EFI Development Kit II Tools
License:        BSD-2-Clause-Patent
URL:            https://github.com/tianocore/tianocore.github.io/wiki/BaseTools
%description tools
This package provides tools that are needed to
build EFI executables and ROMs using the GNU tools.

%package tools-doc
Summary:        Documentation for EFI Development Kit II Tools
BuildArch:      noarch
License:        BSD-2-Clause-Patent
URL:            https://github.com/tianocore/tianocore.github.io/wiki/BaseTools
%description tools-doc
This package documents the tools that are needed to
build EFI executables and ROMs using the GNU tools.

%description
EDK II is a modern, feature-rich, cross-platform firmware development
environment for the UEFI and PI specifications. This package contains sample
64-bit UEFI firmware builds for QEMU and KVM.


%if %{defined fedora}
%package ovmf-ia32
Summary:        Open Virtual Machine Firmware
License:        BSD-2-Clause-Patent and OpenSSL
Provides:       bundled(openssl)
BuildArch:      noarch
%description ovmf-ia32
EFI Development Kit II
Open Virtual Machine Firmware (ia32)

%package arm
Summary:        ARM Virtual Machine Firmware
BuildArch:      noarch
License:        BSD-2-Clause-Patent and OpenSSL
%description arm
EFI Development Kit II
ARMv7 UEFI Firmware

%package qosb
Summary:        Tool to enroll secureboot
Requires:       python3
Buildarch:      noarch
%description qosb
This package contains QOSB (QEMU OVMF Secure Boot), which can enroll OVMF
variable files to enforce Secure Boot.

%package tools-python
Summary:        EFI Development Kit II Tools
Requires:       python3
BuildArch:      noarch

%description tools-python
This package provides tools that are needed to build EFI executables
and ROMs using the GNU tools.  You do not need to install this package;
you probably want to install edk2-tools only.
# endif fedora
%endif



%prep
# We needs some special git config options that %%autosetup won't give us.
# We init the git dir ourselves, then tell %%autosetup not to blow it away.
%setup -q -n edk2-%{GITCOMMIT}
git init -q
git config core.whitespace cr-at-eol
git config am.keepcr true
# -T is passed to %%setup to not re-extract the archive
# -D is passed to %%setup to not delete the existing archive dir
%autosetup -T -D -n edk2-%{GITCOMMIT} -S git_am

cp -a -- %{SOURCE1} %{SOURCE3} .
cp -a -- %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE13} %{SOURCE14} .
tar -C CryptoPkg/Library/OpensslLib -a -f %{SOURCE2} -x

# Format the Red Hat-issued certificate that is to be enrolled as both Platform
# Key and first Key Exchange Key, as an SMBIOS OEM String. This means stripping
# the PEM header and footer, and prepending the textual representation of the
# GUID that identifies this particular OEM String to "EnrollDefaultKeys.efi",
# plus the separator ":". For details, see
# <https://bugzilla.tianocore.org/show_bug.cgi?id=1747> comments 2, 7, 14.
sed \
  -e 's/^-----BEGIN CERTIFICATE-----$/4e32566d-8e9e-4f52-81d3-5bb9715f9727:/' \
  -e '/^-----END CERTIFICATE-----$/d' \
  %{SOURCE5} \
  > PkKek1.oemstr

# Done by %setup, but we do not use it for the auxiliary tarballs
chmod -Rf a+rX,u+w,g-w,o-w .

# Fedora specific
cp -a -- %{SOURCE4} .
# extract softfloat into place
tar -xf %{SOURCE50} --strip-components=1 --directory ArmPkg/Library/ArmSoftFloatLib/berkeley-softfloat-3/


%build
export PYTHON_COMMAND=%{__python3}
source ./edksetup.sh
%make_build -C "$EDK_TOOLS_PATH" \
  EXTRA_OPTFLAGS="%{optflags}" \
  EXTRA_LDFLAGS="%{__global_ldflags}"

SMP_MFLAGS="%{?_smp_mflags}"
if [[ x"$SMP_MFLAGS" = x-j* ]]; then
        CC_FLAGS="$CC_FLAGS -n ${SMP_MFLAGS#-j}"
elif [ -n "%{?jobs}" ]; then
        CC_FLAGS="$CC_FLAGS -n %{?jobs}"
fi

CC_FLAGS="$CC_FLAGS --cmd-len=65536 -t %{TOOLCHAIN} -b DEBUG --hash"
CC_FLAGS="$CC_FLAGS -D NETWORK_IP6_ENABLE"
CC_FLAGS="$CC_FLAGS -D NETWORK_HTTP_BOOT_ENABLE -D NETWORK_TLS_ENABLE"
CC_FLAGS="$CC_FLAGS -D TPM_ENABLE"

OVMF_FLAGS="${CC_FLAGS}"
%if %{defined rhel}
OVMF_FLAGS="${OVMF_FLAGS} -D FD_SIZE_4MB"
OVMF_FLAGS="${OVMF_FLAGS} -D PVSCSI_ENABLE=FALSE -D MPT_SCSI_ENABLE=FALSE"
%else
OVMF_FLAGS="${OVMF_FLAGS} -D FD_SIZE_2MB"
%endif

OVMF_SB_FLAGS="${OVMF_FLAGS}"
OVMF_SB_FLAGS="${OVMF_SB_FLAGS} -D SECURE_BOOT_ENABLE"
OVMF_SB_FLAGS="${OVMF_SB_FLAGS} -D SMM_REQUIRE"
OVMF_SB_FLAGS="${OVMF_SB_FLAGS} -D EXCLUDE_SHELL_FROM_FD"

%if %{disable_werror}
sed -i -e 's/-Werror//' Conf/tools_def.txt
%endif


%if %{cross}
export GCC5_IA32_PREFIX="x86_64-linux-gnu-"
export GCC5_X64_PREFIX="x86_64-linux-gnu-"
export GCC5_AARCH64_PREFIX="aarch64-linux-gnu-"
export GCC5_ARM_PREFIX="arm-linux-gnu-"
%endif

build_iso() {
  dir="$1"
  UEFI_SHELL_BINARY=${dir}/Shell.efi
  ENROLLER_BINARY=${dir}/EnrollDefaultKeys.efi
  UEFI_SHELL_IMAGE=uefi_shell.img
  ISO_IMAGE=${dir}/UefiShell.iso

  UEFI_SHELL_BINARY_BNAME=$(basename -- "$UEFI_SHELL_BINARY")
  UEFI_SHELL_SIZE=$(stat --format=%s -- "$UEFI_SHELL_BINARY")
  ENROLLER_SIZE=$(stat --format=%s -- "$ENROLLER_BINARY")

  # add 1MB then 10% for metadata
  UEFI_SHELL_IMAGE_KB=$((
    (UEFI_SHELL_SIZE + ENROLLER_SIZE + 1 * 1024 * 1024) * 11 / 10 / 1024
  ))

  # create non-partitioned FAT image
  rm -f -- "$UEFI_SHELL_IMAGE"
  mkdosfs -C "$UEFI_SHELL_IMAGE" -n UEFI_SHELL -- "$UEFI_SHELL_IMAGE_KB"

  # copy the shell binary into the FAT image
  export MTOOLS_SKIP_CHECK=1
  mmd   -i "$UEFI_SHELL_IMAGE"                       ::efi
  mmd   -i "$UEFI_SHELL_IMAGE"                       ::efi/boot
  mcopy -i "$UEFI_SHELL_IMAGE"  "$UEFI_SHELL_BINARY" ::efi/boot/bootx64.efi
  mcopy -i "$UEFI_SHELL_IMAGE"  "$ENROLLER_BINARY"   ::
  mdir  -i "$UEFI_SHELL_IMAGE"  -/                   ::

  # build ISO with FAT image file as El Torito EFI boot image
  mkisofs -input-charset ASCII -J -rational-rock \
    -e "$UEFI_SHELL_IMAGE" -no-emul-boot \
    -o "$ISO_IMAGE" "$UEFI_SHELL_IMAGE"
}


%if %{build_ovmf}
# Build with neither SB nor SMM; include UEFI shell.
build ${OVMF_FLAGS} -a X64 \
  -p OvmfPkg/OvmfPkgX64.dsc

# Build with SB and SMM; exclude UEFI shell.
build ${OVMF_SB_FLAGS} -a IA32 -a X64 \
  -p OvmfPkg/OvmfPkgIa32X64.dsc

# Sanity check: the varstore templates must be identical.
cmp Build/OvmfX64/DEBUG_%{TOOLCHAIN}/FV/OVMF_VARS.fd \
  Build/Ovmf3264/DEBUG_%{TOOLCHAIN}/FV/OVMF_VARS.fd

# Prepare an ISO image that boots the UEFI shell.
build_iso Build/Ovmf3264/DEBUG_%{TOOLCHAIN}/X64

# Enroll the default certificates in a separate variable store template.
%{__python3} ovmf-vars-generator --verbose --verbose \
  --qemu-binary        %{qemu_binary} \
  --ovmf-binary        Build/Ovmf3264/DEBUG_%{TOOLCHAIN}/FV/OVMF_CODE.fd \
  --ovmf-template-vars Build/Ovmf3264/DEBUG_%{TOOLCHAIN}/FV/OVMF_VARS.fd \
  --uefi-shell-iso     Build/Ovmf3264/DEBUG_%{TOOLCHAIN}/X64/UefiShell.iso \
  --oem-string         "$(< PkKek1.oemstr)" \
  --skip-testing \
  Build/Ovmf3264/DEBUG_%{TOOLCHAIN}/FV/OVMF_VARS.secboot.fd

# endif build_ovmf
%endif

%if %{build_aarch64}
# Build with a verbose debug mask first, and stash the binary.
build ${CC_FLAGS} -a AARCH64 \
  -p ArmVirtPkg/ArmVirtQemu.dsc \
  -D DEBUG_PRINT_ERROR_LEVEL=0x8040004F
cp -a Build/ArmVirtQemu-AARCH64/DEBUG_%{TOOLCHAIN}/FV/QEMU_EFI.fd \
  Build/ArmVirtQemu-AARCH64/DEBUG_%{TOOLCHAIN}/FV/QEMU_EFI.verbose.fd

# Rebuild with a silent (errors only) debug mask.
build ${CC_FLAGS} -a AARCH64 \
  -p ArmVirtPkg/ArmVirtQemu.dsc \
  -D DEBUG_PRINT_ERROR_LEVEL=0x80000000
# endif build_aarch64
%endif


%if %{defined fedora}
# build ovmf-ia32
mkdir -p ovmf-ia32
build ${OVMF_FLAGS} -a IA32 -p OvmfPkg/OvmfPkgIa32.dsc
cp Build/OvmfIa32/*/FV/OVMF_CODE*.fd ovmf-ia32/
# cp VARS files from from ovmf/, which are all we need
cp -a Build/Ovmf3264/DEBUG_%{TOOLCHAIN}/FV/OVMF_VARS*.fd ovmf-ia32
rm -rf Build/OvmfIa32

# build ovmf-ia32 with secure boot
build ${OVMF_SB_FLAGS} -a IA32 -p OvmfPkg/OvmfPkgIa32.dsc
cp Build/OvmfIa32/*/FV/OVMF_CODE.fd ovmf-ia32/OVMF_CODE.secboot.fd

# build ovmf-ia32 shell iso with EnrollDefaultKeys
build_iso Build/OvmfIa32/DEBUG_%{TOOLCHAIN}/IA32
mv Build/OvmfIa32/DEBUG_%{TOOLCHAIN}/IA32/UefiShell.iso ovmf-ia32
cp -a Build/OvmfIa32/DEBUG_%{TOOLCHAIN}/IA32/Shell.efi ovmf-ia32
cp -a Build/OvmfIa32/DEBUG_%{TOOLCHAIN}/IA32/EnrollDefaultKeys.efi ovmf-ia32


# build ARMv7 firmware
mkdir -p arm
build ${CC_FLAGS} -a ARM -p ArmVirtPkg/ArmVirtQemu.dsc
cp Build/ArmVirtQemu-ARM/DEBUG_*/FV/*.fd arm
dd of="arm/QEMU_EFI-pflash.raw" if="/dev/zero" bs=1M count=64
dd of="arm/QEMU_EFI-pflash.raw" if="arm/QEMU_EFI.fd" conv=notrunc
dd of="arm/vars-template-pflash.raw" if="/dev/zero" bs=1M count=64

# endif defined fedora
%endif



%install

cp -a OvmfPkg/License.txt License.OvmfPkg.txt
cp -a CryptoPkg/Library/OpensslLib/openssl/LICENSE LICENSE.openssl
mkdir -p %{buildroot}%{_datadir}/qemu/firmware

# install the tools
mkdir -p %{buildroot}%{_bindir} \
         %{buildroot}%{_datadir}/%{name}/Conf \
         %{buildroot}%{_datadir}/%{name}/Scripts
install BaseTools/Source/C/bin/* \
        %{buildroot}%{_bindir}
install BaseTools/BinWrappers/PosixLike/LzmaF86Compress \
        %{buildroot}%{_bindir}
install BaseTools/BuildEnv \
        %{buildroot}%{_datadir}/%{name}
install BaseTools/Conf/*.template \
        %{buildroot}%{_datadir}/%{name}/Conf
install BaseTools/Scripts/GccBase.lds \
        %{buildroot}%{_datadir}/%{name}/Scripts


%if %{build_ovmf}
mkdir -p \
  %{buildroot}%{_datadir}/OVMF \
  %{buildroot}%{_datadir}/%{name}/ovmf

install -m 0644 Build/OvmfX64/DEBUG_%{TOOLCHAIN}/FV/OVMF_CODE.fd \
  %{buildroot}%{_datadir}/%{name}/ovmf/OVMF_CODE.fd
install -m 0644 Build/OvmfX64/DEBUG_%{TOOLCHAIN}/FV/OVMF_CODE.fd \
  %{buildroot}%{_datadir}/%{name}/ovmf/OVMF_CODE.cc.fd
install -m 0644 Build/Ovmf3264/DEBUG_%{TOOLCHAIN}/FV/OVMF_CODE.fd \
  %{buildroot}%{_datadir}/%{name}/ovmf/OVMF_CODE.secboot.fd

install -m 0644 Build/OvmfX64/DEBUG_%{TOOLCHAIN}/FV/OVMF_VARS.fd \
  %{buildroot}%{_datadir}/%{name}/ovmf/OVMF_VARS.fd
install -m 0644 Build/Ovmf3264/DEBUG_%{TOOLCHAIN}/FV/OVMF_VARS.secboot.fd \
  %{buildroot}%{_datadir}/%{name}/ovmf/OVMF_VARS.secboot.fd
install -m 0644 Build/Ovmf3264/DEBUG_%{TOOLCHAIN}/X64/UefiShell.iso \
  %{buildroot}%{_datadir}/%{name}/ovmf/UefiShell.iso

ln -s ../%{name}/ovmf/OVMF_CODE.fd         %{buildroot}%{_datadir}/OVMF
ln -s ../%{name}/ovmf/OVMF_CODE.secboot.fd %{buildroot}%{_datadir}/OVMF/
ln -s ../%{name}/ovmf/OVMF_VARS.fd         %{buildroot}%{_datadir}/OVMF/
ln -s ../%{name}/ovmf/OVMF_VARS.secboot.fd %{buildroot}%{_datadir}/OVMF/
ln -s ../%{name}/ovmf/UefiShell.iso        %{buildroot}%{_datadir}/OVMF/

install -m 0644 Build/Ovmf3264/DEBUG_%{TOOLCHAIN}/X64/Shell.efi \
  %{buildroot}%{_datadir}/%{name}/ovmf/Shell.efi
install -m 0644 Build/Ovmf3264/DEBUG_%{TOOLCHAIN}/X64/EnrollDefaultKeys.efi \
  %{buildroot}%{_datadir}/%{name}/ovmf/EnrollDefaultKeys.efi

install -m 0644 edk2-ovmf-sb.json \
  %{buildroot}%{_datadir}/qemu/firmware/40-edk2-ovmf-sb.json
install -m 0644 edk2-ovmf.json \
  %{buildroot}%{_datadir}/qemu/firmware/50-edk2-ovmf.json
install -m 0644 edk2-ovmf-cc.json \
  %{buildroot}%{_datadir}/qemu/firmware/50-edk2-ovmf-cc.json
# endif build_ovmf
%endif

%if %{build_aarch64}
mkdir -p \
  %{buildroot}%{_datadir}/AAVMF \
  %{buildroot}%{_datadir}/%{name}/aarch64

# Pad and install the verbose binary.
cat Build/ArmVirtQemu-AARCH64/DEBUG_%{TOOLCHAIN}/FV/QEMU_EFI.verbose.fd \
  /dev/zero \
| head -c 64m \
  > %{buildroot}%{_datadir}/%{name}/aarch64/QEMU_EFI-pflash.raw

# Pad and install the silent (default) binary.
cat Build/ArmVirtQemu-AARCH64/DEBUG_%{TOOLCHAIN}/FV/QEMU_EFI.fd \
  /dev/zero \
| head -c 64m \
  > %{buildroot}%{_datadir}/%{name}/aarch64/QEMU_EFI-silent-pflash.raw

# Create varstore template.
cat Build/ArmVirtQemu-AARCH64/DEBUG_%{TOOLCHAIN}/FV/QEMU_VARS.fd \
  /dev/zero \
| head -c 64m \
  > %{buildroot}%{_datadir}/%{name}/aarch64/vars-template-pflash.raw

ln -s ../%{name}/aarch64/QEMU_EFI-pflash.raw \
  %{buildroot}%{_datadir}/AAVMF/AAVMF_CODE.verbose.fd
ln -s ../%{name}/aarch64/QEMU_EFI-silent-pflash.raw \
  %{buildroot}%{_datadir}/AAVMF/AAVMF_CODE.fd
ln -s ../%{name}/aarch64/vars-template-pflash.raw \
  %{buildroot}%{_datadir}/AAVMF/AAVMF_VARS.fd

chmod 0644 -- %{buildroot}%{_datadir}/AAVMF/AAVMF_*.fd

install -m 0644 Build/ArmVirtQemu-AARCH64/DEBUG_%{TOOLCHAIN}/FV/QEMU_EFI.verbose.fd \
  %{buildroot}%{_datadir}/%{name}/aarch64/QEMU_EFI.fd
install -m 0644 Build/ArmVirtQemu-AARCH64/DEBUG_%{TOOLCHAIN}/FV/QEMU_EFI.fd \
  %{buildroot}%{_datadir}/%{name}/aarch64/QEMU_EFI.silent.fd
install -m 0644 Build/ArmVirtQemu-AARCH64/DEBUG_%{TOOLCHAIN}/FV/QEMU_VARS.fd \
  %{buildroot}%{_datadir}/%{name}/aarch64/QEMU_VARS.fd

install -m 0644 edk2-aarch64.json \
  %{buildroot}%{_datadir}/qemu/firmware/60-edk2-aarch64.json
install -m 0644 edk2-aarch64-verbose.json \
  %{buildroot}%{_datadir}/qemu/firmware/70-edk2-aarch64-verbose.json
# endif build_aarch64
%endif


%if %{defined fedora}
# Install extra x86_64 json files
install -p -m 0644 %{_sourcedir}/edk2-ovmf-nosb.json \
  %{buildroot}%{_datadir}/qemu/firmware/60-edk2-ovmf-nosb.json


# install ia32
cp -a ovmf-ia32 %{buildroot}%{_datadir}/%{name}

for f in %{_sourcedir}/*edk2-ovmf-ia32*.json; do
    install -pm 644 $f %{buildroot}/%{_datadir}/qemu/firmware
done


# install arm32
cp -a arm %{buildroot}%{_datadir}/%{name}
ln -sf ../%{name}/arm/QEMU_EFI-pflash.raw          %{buildroot}%{_datadir}/AAVMF/AAVMF32_CODE.fd

for f in %{_sourcedir}/*edk2-arm-*.json; do
    install -pm 644 $f %{buildroot}/%{_datadir}/qemu/firmware
done


# edk2-tools-python install
cp -R BaseTools/Source/Python %{buildroot}%{_datadir}/%{name}/Python
for i in build BPDG Ecc GenDepex GenFds GenPatchPcdTable PatchPcdValue TargetTool Trim UPT; do
echo '#!/bin/sh
export PYTHONPATH=%{_datadir}/%{name}/Python
exec python3 '%{_datadir}/%{name}/Python/$i/$i.py' "$@"' > %{buildroot}%{_bindir}/$i
  chmod +x %{buildroot}%{_bindir}/$i
done

%if 0%{?py_byte_compile:1}
# https://docs.fedoraproject.org/en-US/packaging-guidelines/Python_Appendix/#manual-bytecompilation
%py_byte_compile %{python3} %{buildroot}%{_datadir}/edk2/Python
%endif

# edk2-qosb install
install -p ovmf-vars-generator %{buildroot}%{_bindir}

# endif defined fedora
%endif



%check

%if %{qosb_testing}
# Of the installed host kernels, boot the one with the highest Version-Release
# under OVMF, and check if it prints "Secure boot enabled".
KERNEL_PKG=$(rpm -q kernel-core | rpmdev-sort | tail -n 1)
KERNEL_IMG=$(rpm -q -l $KERNEL_PKG | egrep '^/lib/modules/[^/]+/vmlinuz$')

%{__python3} ovmf-vars-generator --verbose --verbose \
  --qemu-binary        %{qemu_binary} \
  --ovmf-binary        Build/Ovmf3264/DEBUG_%{TOOLCHAIN}/FV/OVMF_CODE.fd \
  --ovmf-template-vars Build/Ovmf3264/DEBUG_%{TOOLCHAIN}/FV/OVMF_VARS.fd \
  --uefi-shell-iso     Build/Ovmf3264/DEBUG_%{TOOLCHAIN}/X64/UefiShell.iso \
  --kernel-path        $KERNEL_IMG \
  --skip-enrollment \
  --no-download \
  Build/Ovmf3264/DEBUG_%{TOOLCHAIN}/FV/OVMF_VARS.secboot.fd

# endif qosb_testing
%endif


%global common_files \
  %%license License.txt License.OvmfPkg.txt License-History.txt LICENSE.openssl \
  %%dir %%{_datadir}/%%{name}/ \
  %%dir %%{_datadir}/qemu \
  %%dir %%{_datadir}/qemu/firmware

%if %{build_ovmf}
%files ovmf
%common_files
%doc OvmfPkg/README
%doc ovmf-whitepaper-c770f8c.txt
%dir %{_datadir}/OVMF/
%dir %{_datadir}/%{name}/ovmf/
%{_datadir}/%{name}/ovmf/OVMF_CODE.fd
%{_datadir}/%{name}/ovmf/OVMF_CODE.cc.fd
%{_datadir}/%{name}/ovmf/OVMF_CODE.secboot.fd
%{_datadir}/%{name}/ovmf/OVMF_VARS.fd
%{_datadir}/%{name}/ovmf/OVMF_VARS.secboot.fd
%{_datadir}/%{name}/ovmf/UefiShell.iso
%{_datadir}/OVMF/OVMF_CODE.fd
%{_datadir}/OVMF/OVMF_CODE.secboot.fd
%{_datadir}/OVMF/OVMF_VARS.fd
%{_datadir}/OVMF/OVMF_VARS.secboot.fd
%{_datadir}/OVMF/UefiShell.iso
%{_datadir}/%{name}/ovmf/Shell.efi
%{_datadir}/%{name}/ovmf/EnrollDefaultKeys.efi
%{_datadir}/qemu/firmware/40-edk2-ovmf-sb.json
%{_datadir}/qemu/firmware/50-edk2-ovmf-cc.json
%{_datadir}/qemu/firmware/50-edk2-ovmf.json
%if %{defined fedora}
%{_datadir}/qemu/firmware/60-edk2-ovmf-nosb.json
%endif
# endif build_ovmf
%endif

%if %{build_aarch64}
%files aarch64
%common_files
%dir %{_datadir}/AAVMF/
%dir %{_datadir}/%{name}/aarch64/
%{_datadir}/%{name}/aarch64/QEMU_EFI-pflash.raw
%{_datadir}/%{name}/aarch64/QEMU_EFI-silent-pflash.raw
%{_datadir}/%{name}/aarch64/vars-template-pflash.raw
%{_datadir}/AAVMF/AAVMF_CODE.verbose.fd
%{_datadir}/AAVMF/AAVMF_CODE.fd
%{_datadir}/AAVMF/AAVMF_VARS.fd
%{_datadir}/%{name}/aarch64/QEMU_EFI.fd
%{_datadir}/%{name}/aarch64/QEMU_EFI.silent.fd
%{_datadir}/%{name}/aarch64/QEMU_VARS.fd
%{_datadir}/qemu/firmware/60-edk2-aarch64.json
%{_datadir}/qemu/firmware/70-edk2-aarch64-verbose.json
# endif build_aarch64
%endif

%files tools
%license License.txt
%license License-History.txt
%{_bindir}/DevicePath
%{_bindir}/EfiRom
%{_bindir}/GenCrc32
%{_bindir}/GenFfs
%{_bindir}/GenFv
%{_bindir}/GenFw
%{_bindir}/GenSec
%{_bindir}/LzmaCompress
%{_bindir}/LzmaF86Compress
%{_bindir}/TianoCompress
%{_bindir}/VfrCompile
%{_bindir}/VolInfo
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/BuildEnv
%{_datadir}/%{name}/Conf
%{_datadir}/%{name}/Scripts

%files tools-doc
%doc BaseTools/UserManuals/*.rtf


%if %{defined fedora}
%files ovmf-ia32
%common_files
%dir %{_datadir}/%{name}/ovmf-ia32
%{_datadir}/%{name}/ovmf-ia32
%{_datadir}/%{name}/ovmf-ia32/EnrollDefaultKeys.efi
%{_datadir}/%{name}/ovmf-ia32/OVMF_CODE.fd
%{_datadir}/%{name}/ovmf-ia32/OVMF_CODE.secboot.fd
%{_datadir}/%{name}/ovmf-ia32/OVMF_VARS.fd
%{_datadir}/%{name}/ovmf-ia32/OVMF_VARS.secboot.fd
%{_datadir}/%{name}/ovmf-ia32/Shell.efi
%{_datadir}/%{name}/ovmf-ia32/UefiShell.iso
%{_datadir}/qemu/firmware/40-edk2-ovmf-ia32-sb-enrolled.json
%{_datadir}/qemu/firmware/50-edk2-ovmf-ia32-sb.json
%{_datadir}/qemu/firmware/60-edk2-ovmf-ia32.json


%files arm
%common_files
%dir %{_datadir}/%{name}/arm
%{_datadir}/AAVMF/AAVMF32_CODE.fd
%{_datadir}/%{name}/arm
%{_datadir}/%{name}/arm/QEMU_EFI-pflash.raw
%{_datadir}/%{name}/arm/QEMU_EFI.fd
%{_datadir}/%{name}/arm/QEMU_VARS.fd
%{_datadir}/%{name}/arm/vars-template-pflash.raw
%{_datadir}/qemu/firmware/70-edk2-arm-verbose.json


%files tools-python
%{_bindir}/build
%{_bindir}/BPDG
%{_bindir}/Ecc
%{_bindir}/GenDepex
%{_bindir}/GenFds
%{_bindir}/GenPatchPcdTable
%{_bindir}/PatchPcdValue
%{_bindir}/TargetTool
%{_bindir}/Trim
%{_bindir}/UPT
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/Python


%files qosb
%license LICENSE.qosb
%{_bindir}/ovmf-vars-generator

# endif fedora
%endif


%changelog
* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20210527gite1999b264f1f-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jul 20 2021 Cole Robinson <crobinso@redhat.com> - 20210527gite1999b264f1f-1
- Update to git snapshot
- Sync with c9s packaging

* Mon Jun 14 2021 Jiri Kucera <jkucera@redhat.com> - 20200801stable-5
- Replace genisoimage with xorriso

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20200801stable-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Dec 03 2020 Cole Robinson <aintdiscole@gmail.com> - 20200801stable-3
- Really fix TPM breakage (bz 1897367)

* Tue Nov 24 2020 Cole Robinson <aintdiscole@gmail.com> - 20200801stable-2
- Fix openssl usage, unbreak TPM (bz 1897367)

* Wed Sep 16 2020 Cole Robinson <crobinso@redhat.com> - 20200801stable-1
- Update to edk2 stable 202008

* Sat Sep 12 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 20200201stable-6
- Tweaks for aarch64/ARMv7 builds
- Minor cleanups

* Tue Aug 04 2020 Cole Robinson <aintdiscole@gmail.com> - 20200201stable-5
- Fix build failures on rawhide

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20200201stable-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20200201stable-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 13 2020 Tom Stellard <tstellar@redhat.com> - 20200201stable-2
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Mon Apr 13 2020 Cole Robinson <aintdiscole@gmail.com> - 20200201stable-1
- Update to stable-202002

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20190501stable-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Sep 06 2019 Patrick Uiterwijk <puiterwijk@redhat.com> - 20190501stable-4
- Updated HTTP_BOOT option to new upstream value

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20190501stable-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 15 2019 Cole Robinson <aintdiscole@gmail.com> - 20190501stable-2
- License is now BSD-2-Clause-Patent
- Re-enable secureboot enrollment
- Use qemu-ovmf-secureboot from git

* Thu Jul 11 2019 Cole Robinson <crobinso@redhat.com> - 20190501stable-1
- Update to stable-201905
- Update to openssl-1.1.1b
- Ship VARS file for ovmf-ia32 (bug 1688596)
- Ship Fedora-variant JSON "firmware descriptor files"
- Resolves rhbz#1728652

* Mon Mar 18 2019 Cole Robinson <aintdiscole@gmail.com> - 20190308stable-1
- Use YYYYMMDD versioning to fix upgrade path

* Fri Mar 15 2019 Cole Robinson <aintdiscole@gmail.com> - 201903stable-1
- Update to stable-201903
- Update to openssl-1.1.0j
- Move to python3 deps

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20180815gitcb5f4f45ce-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Nov 14 2018 Patrick Uiterwijk <puiterwijk@redhat.com> - 20180815gitcb5f4f45ce-5
- Add -qosb dependency on python3

* Fri Nov 9 2018 Paolo Bonzini <pbonzini@redhat.com> - 20180815gitcb5f4f45ce-4
- Fix network boot via grub (bz 1648476)

* Wed Sep 12 2018 Paolo Bonzini <pbonzini@redhat.com> - 20180815gitcb5f4f45ce-3
- Explicitly compile the scripts using py_byte_compile

* Fri Aug 31 2018 Cole Robinson <crobinso@redhat.com> - 20180815gitcb5f4f45ce-2
- Fix passing through RPM build flags (bz 1540244)

* Tue Aug 21 2018 Cole Robinson <crobinso@redhat.com> - 20180815gitcb5f4f45ce-1
- Update to edk2 git cb5f4f45ce, edk2-stable201808
- Update to qemu-ovmf-secureboot-1.1.3
- Enable TPM2 support

* Mon Jul 23 2018 Paolo Bonzini <pbonzini@redhat.com> - 20180529gitee3198e672e2-5
- Fixes for AMD SEV on OVMF_CODE.fd
- Add Provides for bundled OpenSSL

* Wed Jul 18 2018 Paolo Bonzini <pbonzini@redhat.com> - 20180529gitee3198e672e2-4
- Enable IPv6

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20180529gitee3198e672e2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 20 2018 Paolo Bonzini <pbonzini@redhat.com> - 20180529gitee3198e672e2-2
- Backport two bug fixes from RHEL: connect again virtio-rng devices, and
  connect consoles unconditionally in OVMF (ARM firmware already did it)

* Tue May 29 2018 Paolo Bonzini <pbonzini@redhat.com> - 20180529gitee3198e672e2-1
- Rebase to ee3198e672e2

* Tue May 01 2018 Cole Robinson <crobinso@redhat.com> - 20171011git92d07e4-7
- Bump release for new build

* Fri Mar 30 2018 Patrick Uiterwijk <puiterwijk@redhat.com> - 20171011git92d07e4-6
- Add qemu-ovmf-secureboot (qosb)
- Generate pre-enrolled Secure Boot OVMF VARS files

* Wed Mar 07 2018 Paolo Bonzini <pbonzini@redhat.com> - 20171011git92d07e4-5
- Fix GCC 8 compilation
- Replace dosfstools and mtools with qemu-img vvfat

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20171011git92d07e4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 19 2018 Paolo Bonzini <pbonzini@redhat.com> - 20170209git296153c5-3
- Add OpenSSL patches from Fedora
- Enable TLS_MODE

* Fri Nov 17 2017 Paolo Bonzini <pbonzini@redhat.com> - 20170209git296153c5-2
- Backport patches 19-21 from RHEL
- Add patches 22-24 to fix SEV slowness
- Add fedora conditionals

* Tue Nov 14 2017 Paolo Bonzini <pbonzini@redhat.com> - 20171011git92d07e4-1
- Import source and patches from RHEL version
- Update OpenSSL to 1.1.0e
- Refresh 0099-Tweak-the-tools_def-to-support-cross-compiling.patch

* Mon Nov 13 2017 Paolo Bonzini <pbonzini@redhat.com> - 20170209git296153c5-6
- Allow non-cross builds
- Install /usr/share/OVMF and /usr/share/AAVMF

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20170209git296153c5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20170209git296153c5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Mar 15 2017 Cole Robinson <crobinso@redhat.com> - 20170209git296153c5-3
- Ship ovmf-ia32 package (bz 1424722)

* Thu Feb 16 2017 Cole Robinson <crobinso@redhat.com> - 20170209git296153c5-2
- Update EnrollDefaultKeys patch (bz #1398743)

* Mon Feb 13 2017 Paolo Bonzini <pbonzini@redhat.com> - 20170209git296153c5-1
- Rebase to git master
- New patch 0010 fixes failure to build from source.

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20161105git3b25ca8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Nov 06 2016 Cole Robinson <crobinso@redhat.com> - 20161105git3b25ca8-1
- Rebase to git master

* Fri Sep  9 2016 Tom Callaway <spot@fedoraproject.org> - 20160418gita8c39ba-5
- replace legally problematic openssl source with "hobbled" tarball

* Thu Jul 21 2016 Gerd Hoffmann <kraxel@redhat.com> - 20160418gita8c39ba-4
- Also build for armv7.

* Tue Jul 19 2016 Gerd Hoffmann <kraxel@redhat.com> 20160418gita8c39ba-3
- Update EnrollDefaultKeys patch.

* Fri Jul 8 2016 Paolo Bonzini <pbonzini@redhat.com> - 20160418gita8c39ba-2
- Distribute edk2-ovmf on aarch64

* Sat May 21 2016 Cole Robinson <crobinso@redhat.com> - 20160418gita8c39ba-1
- Distribute edk2-aarch64 on x86 (bz #1338027)

* Mon Apr 18 2016 Gerd Hoffmann <kraxel@redhat.com> 20160418gita8c39ba-0
- Update to latest git.
- Add firmware builds (FatPkg is free now).

* Mon Feb 15 2016 Cole Robinson <crobinso@redhat.com> 20151127svn18975-3
- Fix FTBFS gcc warning (bz 1307439)

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 20151127svn18975-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Nov 27 2015 Paolo Bonzini <pbonzini@redhat.com> - 20151127svn18975-1
- Rebase to 20151127svn18975-1
- Linker script renamed to GccBase.lds

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20150519svn17469-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 19 2015 Paolo Bonzini <pbonzini@redhat.com> - 20150519svn17469-1
- Rebase to 20150519svn17469-1
- edk2-remove-tree-check.patch now upstream

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 20140724svn2670-6
- Rebuilt for GCC 5 C++11 ABI change

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20140724svn2670-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 24 2014 Paolo Bonzini <pbonzini@redhat.com> - 20140724svn2670-1
- Rebase to 20140724svn2670-1

* Tue Jun 24 2014 Paolo Bonzini <pbonzini@redhat.com> - 20140624svn2649-1
- Use standalone .tar.xz from buildtools repo

* Tue Jun 24 2014 Paolo Bonzini <pbonzini@redhat.com> - 20140328svn15376-4
- Install BuildTools/BaseEnv

* Mon Jun 23 2014 Paolo Bonzini <pbonzini@redhat.com> - 20140328svn15376-3
- Rebase to get GCC48 configuration
- Package EDK_TOOLS_PATH as /usr/share/edk2
- Package "build" and LzmaF86Compress too, as well as the new
  tools Ecc and TianoCompress.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20131114svn14844-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Nov 14 2013 Paolo Bonzini <pbonzini@redhat.com> - 20131114svn14844-1
- Upgrade to r14844.
- Remove upstreamed parts of patch 1.

* Fri Nov 8 2013 Paolo Bonzini <pbonzini@redhat.com> - 20130515svn14365-7
- Make BaseTools compile on ARM.

* Fri Aug 30 2013 Paolo Bonzini <pbonzini@redhat.com> - 20130515svn14365-6
- Revert previous change; firmware packages should be noarch, and building
  BaseTools twice is simply wrong.

* Mon Aug 19 2013 Kay Sievers <kay@redhat.com> - 20130515svn14365-5
- Add sub-package with EFI shell

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20130515svn14365-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 23 2013 Dan Horák <dan[at]danny.cz> 20130515svn14365-3
- set ExclusiveArch

* Thu May 16 2013 Paolo Bonzini <pbonzini@redhat.com> 20130515svn14365-2
- Fix edk2-tools-python Requires

* Wed May 15 2013 Paolo Bonzini <pbonzini@redhat.com> 20130515svn14365-1
- Split edk2-tools-doc and edk2-tools-python
- Fix Python BuildRequires
- Remove FatBinPkg at package creation time.
- Use fully versioned dependency.
- Add comment on how to generate the sources.

* Thu May 2 2013 Paolo Bonzini <pbonzini@redhat.com> 20130502.g732d199-1
- Create.
