            #GIT_CMT=63d08c648e2a0cf096573f3113c37b850a884fd5
%global debug_package %{nil}
%global python_ver python3

#
# Example ARCHIVE Generation:
# export COMMIT=b6e48ec6
# export VERSION=20191205
# export RELEASE=1.el9
# rpmdev-setuptree
# git-archive-all --prefix edk2-${VERSION}/ ~/rpmbuild/SOURCES/edk2-${RELEASE}.tar.gz
#
# Copy over patches/files:
# cp buildrpm/ol9/* ~/rpmbuild/SOURCES
#
# Build the RPMs:
# rpmbuild -ba buildrpm/ol9/edk2.spec
#
Name:		edk2
Version:	20220628
Release:    1.el9
Epoch:		30
Summary:	UEFI Firmware for 64-bit virtual machines

Group:		Applications/Emulators
License:	BSD and OpenSSL
URL:		http://www.tianocore.org
Source0: edk2-20220628.tar.bz2
Source3:	OpenSSL-1.1.1n-d82e959e621a3d597f1e0d50ff8c2d8b96915fd7.tgz
Source4:	BaseTools-BrotliCompress-f4153a09f87cbb9c826d8fc12c74642bb2d879ea.tgz
Source5:	MdeModulePkg-BrotliCustomDecompressLib-f4153a09f87cbb9c826d8fc12c74642bb2d879ea.tgz
Source6:	nasm

Patch4:		0001-MdeModulePkg-TerminalDxe-add-other-text-resolutions.patch
Patch5:		0002-EXCLUDE_SHELL_FROM_FD.patch

#Patch10:	0001-OvmfPkg-SmbiosPlatformDxe-install-legacy-QEMU-tables.patch
#Patch11:	0002-OvmfPkg-SmbiosPlatformDxe-install-patch-default-lega.patch
#Patch12:	0003-OvmfPkg-SmbiosPlatformDxe-install-patch-default-lega.patch
Patch13:	0004-OvmfPkg-SmbiosPlatformDxe-install-legacy-QEMU-tables.patch

Patch30:	0001-tools_def.template-take-GCC4-_-IA32-X64-prefixes-fro.patch

Patch40:	0001-MdeModulePkg-silence-image-start-error.patch
Patch50:	0002-OvmfPkgX64-DSC-Updates.patch
Patch51:	0001-ArmVirtPkg-DSC-Updates.patch
Patch60:	0002-Smbios-ovmf-version-update.patch
Patch70:	0001-Bug31156337-Connect-MassStorage-WAR.patch
#Patch80:	0001-Silence-BootOption-Load-Errors.patch
Patch85:	0001-BaseTools-GCC12-Compile-error1-fix1.patch
Patch105:	0001-ArmPlatformPkg-NorFlashDxe-Allow_Readonly.patch
Patch110:	0001-SecurityPkg-Disable-Secureboot-User-Config.patch
Patch111:	0001-Disable-Tcg2-MeasureCPUs-x86_64.patch
Patch112:	0001-Disable-Tcg2-MeasureCPUs-aarch64.patch
Patch120:	0001-SecureBoot-Logging1.patch
Patch121:	0001-Serial-Console-Output1.patch
Patch125:	0001-Serial-Console-Debug.patch
Patch126:	0001-Assert-On-Serial-Port.patch
Patch130:	0001-Bug33117114-SevResetLoop-WAR.patch

BuildRequires:	mtools
BuildRequires:	dosfstools
BuildRequires:	iasl
BuildRequires:	python3
BuildRequires:	libuuid-devel
BuildRequires:	git

%description
EFI Development Kit II

%package tools
Summary:	EFI Development Kit II Tools
%description tools
EFI Development Kit II Tools


%ifarch x86_64
%global subpkgname ovmf

%package ovmf 
Summary:	UEFI Firmware for 64-bit virtual machines
License:	BSD and OpenSSL
BuildArch:      noarch

%description ovmf
UEFI Firmware for 64-bit virtual machines
%endif


%ifarch aarch64
%global subpkgname aarch64

%package aarch64 
Summary:	UEFI Firmware for aarch64 virtual machines
License:	BSD
BuildArch:      noarch

%description aarch64 
UEFI Firmware for aarch64 virtual machines
%endif

%prep
%setup -q -n %{name}-%{version}

%patch4 -p1
%patch5 -p1
#%patch10 -p1
#%patch11 -p1
#%patch12 -p1
%patch13 -p1
%patch30 -p1
%patch40 -p1
%patch50 -p1
%patch51 -p1
%patch60 -p1
%patch70 -p1
#%patch80 -p1
%patch85 -p1
%patch105 -p1
%patch110 -p1
%ifarch x86_64
%patch111 -p1
%endif
%ifarch aarch64
%patch112 -p1
%endif
%patch120 -p1
%patch121 -p1
%patch125 -p1
%patch126 -p1
%patch130 -p1

cp -a -- %{SOURCE3} .
cp -a -- %{SOURCE4} .
cp -a -- %{SOURCE5} .
cp -a -- %{SOURCE6} .

tar xfz OpenSSL-1.1.1n-d82e959e621a3d597f1e0d50ff8c2d8b96915fd7.tgz -C CryptoPkg/Library/OpensslLib/
tar xfz BaseTools-BrotliCompress-f4153a09f87cbb9c826d8fc12c74642bb2d879ea.tgz -C BaseTools/Source/C/BrotliCompress
tar xfz MdeModulePkg-BrotliCustomDecompressLib-f4153a09f87cbb9c826d8fc12c74642bb2d879ea.tgz -C MdeModulePkg/Library/BrotliCustomDecompressLib

# Patch brotli to use the -Wno-error=vla-parameter to workaround build error with GCC 11+
sed -i '/^LIBS/a BUILD_CFLAGS += -Wno-error=vla-parameter' BaseTools/Source/C/BrotliCompress/GNUmakefile 
sed -i '/^CFLAGS/a BUILD_CFLAGS += -Wno-error=vla-parameter' MdeModulePkg/Library/BrotliCustomDecompressLib/brotli/Makefile

%build

# Build Oracle/OvmfVarsMgr utilities first (as it is used for OVMF/AAVMF build)
cd Oracle/OvmfVarsMgr/
%ifarch x86_64
make ARCH=x86_64
%endif
%ifarch aarch64
make ARCH=arm64
%endif
cd ../..

# specify the proper python for use by the edk build system
PYTHON_COMMAND=%{python_ver}
export PYTHON_COMMAND
source ./edksetup.sh

# figure tools switch
GCCVER=$(gcc --version | awk '{ print $3; exit}')
case "$GCCVER" in
4.4*)	CC_FLAGS="-t GCC44";;
4.5*)	CC_FLAGS="-t GCC45";;
4.6*)	CC_FLAGS="-t GCC46";;
4.7*)	CC_FLAGS="-t GCC47";;
4.8*)	CC_FLAGS="-t GCC48";;
4.9*)	CC_FLAGS="-t GCC49";;
5.*)	CC_FLAGS="-t GCC5";;
6.*)	CC_FLAGS="-t GCC5";;
7.*)	CC_FLAGS="-t GCC5";;
8.*)	CC_FLAGS="-t GCC5";;
9.*)	CC_FLAGS="-t GCC5";;
1?.*)	CC_FLAGS="-t GCC5";;
esac

# parallel builds
SMP_MFLAGS="%{?_smp_mflags}"
if [[ x"$SMP_MFLAGS" = x-j* ]]; then
	CC_FLAGS="$CC_FLAGS -n ${SMP_MFLAGS#-j}"
elif [ -n "%{?jobs}" ]; then
	CC_FLAGS="$CC_FLAGS -n %{?jobs}"
fi

# prepare
make -C BaseTools

# EDK2 has many uninitialized stack variables which cause build errors on older versions of GCC. Ignore those errors.
sed -i '/^DEFINE GCC_ALL_CC_FLAGS/s/=/& -Wno-error=maybe-uninitialized/' Conf/tools_def.txt

# Use our own nasm. EDK2 build requires a very recent nasm version.
sed -i '/NASM_PATH/s/ENV.*/$(WORKSPACE)\/nasm/' Conf/tools_def.txt

%ifarch x86_64
# build OVMF
for cfg in pure-efi pure-efi-debug secboot secboot-debug; do
	OVMF_FLAGS="$CC_FLAGS -D HTTP_BOOT_ENABLE -D FD_SIZE_4MB"

	case "$cfg" in
	pure-efi)
		OVMF_FLAGS="$OVMF_FLAGS -D TPM2_ENABLE"
		# nothing
		;;
	pure-efi-debug)
		OVMF_FLAGS="$OVMF_FLAGS -D DEBUG_LOG_ENABLE"
		OVMF_FLAGS="$OVMF_FLAGS -D TPM2_ENABLE"
		;;
	secboot)
		OVMF_FLAGS="$OVMF_FLAGS -D SECURE_BOOT_ENABLE"
		OVMF_FLAGS="$OVMF_FLAGS -D SMM_REQUIRE"
		OVMF_FLAGS="$OVMF_FLAGS -D TPM2_ENABLE"
		OVMF_FLAGS="$OVMF_FLAGS -D EXCLUDE_SHELL_FROM_FD"
		;;
	secboot-debug)
		OVMF_FLAGS="$OVMF_FLAGS -D DEBUG_LOG_ENABLE"
		OVMF_FLAGS="$OVMF_FLAGS -D SECURE_BOOT_ENABLE"
		OVMF_FLAGS="$OVMF_FLAGS -D SMM_REQUIRE"
		OVMF_FLAGS="$OVMF_FLAGS -D TPM2_ENABLE"
		OVMF_FLAGS="$OVMF_FLAGS -D EXCLUDE_SHELL_FROM_FD"
		;;
	esac

	build $OVMF_FLAGS -a IA32 -a X64 -p OvmfPkg/OvmfPkgIa32X64.dsc
	mkdir -p "OVMF"
	cp Build/Ovmf3264/DEBUG_*/FV/OVMF_CODE.fd OVMF/OVMF_CODE.${cfg}.fd
	cp Build/Ovmf3264/DEBUG_*/FV/OVMF_VARS.fd OVMF/OVMF_VARS.${cfg}.fd
	if [ "$cfg" = secboot ] || [ "$cfg" = secboot-debug ]; then
		# Enroll the Secureboot vars into the variable store template
		Oracle/OvmfVarsMgr/ovmf-vars-mgr --var PK --write --vars-file OVMF/OVMF_VARS.${cfg}.fd < Oracle/SB/x86_64/PK.bin
		Oracle/OvmfVarsMgr/ovmf-vars-mgr --var KEK --write --vars-file OVMF/OVMF_VARS.${cfg}.fd < Oracle/SB/x86_64/KEK.bin
		Oracle/OvmfVarsMgr/ovmf-vars-mgr --var db --write --vars-file OVMF/OVMF_VARS.${cfg}.fd < Oracle/SB/x86_64/db.bin
		Oracle/OvmfVarsMgr/ovmf-vars-mgr --var dbx --write --vars-file OVMF/OVMF_VARS.${cfg}.fd < Oracle/SB/x86_64/dbxupdate_x64-04-2021.bin
	fi
	rm -rf Build/Ovmf3264
done

%endif

%ifarch aarch64
# build AAVMF
for cfg in pure-efi pure-efi-debug secboot secboot-debug; do
	AAVMF_FLAGS="$CC_FLAGS -D HTTP_BOOT_ENABLE "

	case "$cfg" in
	pure-efi)
		AAVMF_FLAGS="$AAVMF_FLAGS -D DEBUG_PRINT_ERROR_LEVEL=0x80000000"
		AAVMF_FLAGS="$AAVMF_FLAGS -D TPM2_ENABLE"
		;;
	pure-efi-debug)
		AAVMF_FLAGS="$AAVMF_FLAGS -D DEBUG_PRINT_ERROR_LEVEL=0x8040004F"
		AAVMF_FLAGS="$AAVMF_FLAGS -D TPM2_ENABLE"
		;;
	secboot)
		AAVMF_FLAGS="$AAVMF_FLAGS -D DEBUG_PRINT_ERROR_LEVEL=0x80000000"
		AAVMF_FLAGS="$AAVMF_FLAGS -D SECURE_BOOT_ENABLE"
		AAVMF_FLAGS="$AAVMF_FLAGS -D TPM2_ENABLE"
		AAVMF_FLAGS="$AAVMF_FLAGS -D EXCLUDE_SHELL_FROM_FD"
		;;
	secboot-debug)
		AAVMF_FLAGS="$AAVMF_FLAGS -D DEBUG_PRINT_ERROR_LEVEL=0x8040004F"
		AAVMF_FLAGS="$AAVMF_FLAGS -D SECURE_BOOT_ENABLE"
		AAVMF_FLAGS="$AAVMF_FLAGS -D TPM2_ENABLE"
		AAVMF_FLAGS="$AAVMF_FLAGS -D EXCLUDE_SHELL_FROM_FD"
		;;
	esac

	build $AAVMF_FLAGS -a AARCH64 -p ArmVirtPkg/ArmVirtQemu.dsc
	mkdir -p "AAVMF"
	cp Build/ArmVirtQemu-AARCH64/DEBUG_*/FV/QEMU_EFI.fd AAVMF
	cp Build/ArmVirtQemu-AARCH64/DEBUG_*/FV/QEMU_VARS.fd AAVMF
	# Pad the binaries and name them similar to the standard AAVMF package
	cat AAVMF/QEMU_EFI.fd /dev/zero | head -c 64m > AAVMF/AAVMF_CODE.${cfg}.fd
	cat AAVMF/QEMU_VARS.fd /dev/zero | head -c 64m > AAVMF/AAVMF_VARS.${cfg}.fd
	rm AAVMF/QEMU_EFI.fd
	rm AAVMF/QEMU_VARS.fd
	if [ "$cfg" = secboot ] || [ "$cfg" = secboot-debug ] ; then
		# Enroll the Secureboot vars into the variable store template
		Oracle/OvmfVarsMgr/aavmf-vars-mgr --var PK --write --vars-file AAVMF/AAVMF_VARS.${cfg}.fd < Oracle/SB/aarch64/PK.bin
		Oracle/OvmfVarsMgr/aavmf-vars-mgr --var KEK --write --vars-file AAVMF/AAVMF_VARS.${cfg}.fd < Oracle/SB/aarch64/KEK.bin
		Oracle/OvmfVarsMgr/aavmf-vars-mgr --var db --write --vars-file AAVMF/AAVMF_VARS.${cfg}.fd < Oracle/SB/aarch64/db.bin
		Oracle/OvmfVarsMgr/aavmf-vars-mgr --var dbx --write --vars-file AAVMF/AAVMF_VARS.${cfg}.fd < Oracle/SB/aarch64/dbxupdate_arm64-04-2021.bin
	fi
        # Create smaller versions
        cat AAVMF/AAVMF_CODE.${cfg}.fd | head -c 2m > AAVMF/AAVMF_CODE_2M.${cfg}.fd
        cat AAVMF/AAVMF_VARS.${cfg}.fd | head -c 1m > AAVMF/AAVMF_VARS_1M.${cfg}.fd

	rm -rf Build/ArmVirtQemu-AARCH64

done

%endif

%install

mkdir -p %{buildroot}%{_bindir}
install	--strip \
	BaseTools/Source/C/bin/EfiRom \
	BaseTools/Source/C/bin/VolInfo \
	%{buildroot}%{_bindir}

%ifarch x86_64
cp -a Oracle/OvmfVarsMgr/ovmf-vars-mgr %{buildroot}%{_bindir}
cp -a Oracle/OvmfVarsMgr/ovmf-serial-debug %{buildroot}%{_bindir}
%endif
%ifarch aarch64
cp -a Oracle/OvmfVarsMgr/aavmf-vars-mgr %{buildroot}%{_bindir}
cp -a Oracle/OvmfVarsMgr/aavmf-serial-debug %{buildroot}%{_bindir}
%endif
cp -a Oracle/OvmfVarsMgr/efi-siglist-gen %{buildroot}%{_bindir}

# Install License files
%ifarch x86_64
mkdir -p %{buildroot}/%{_docdir}/OVMF/Licenses
cp -a OvmfPkg/License.txt %{buildroot}/%{_docdir}/OVMF/Licenses/OvmfPkg-License.txt
cp -a License.txt %{buildroot}/%{_docdir}/OVMF/Licenses/edk2-License.txt
cp -a CryptoPkg/Library/OpensslLib/openssl/LICENSE %{buildroot}/%{_docdir}/OVMF/Licenses/OpensslLib-License.txt
%endif
%ifarch aarch64
mkdir -p %{buildroot}/%{_docdir}/AAVMF/Licenses
cp -a OvmfPkg/License.txt %{buildroot}/%{_docdir}/AAVMF/Licenses/OvmfPkg-License.txt
cp -a License.txt %{buildroot}/%{_docdir}/AAVMF/Licenses/FatPkg-License.txt
cp -a License.txt %{buildroot}/%{_docdir}/AAVMF/Licenses/IntelFrameworkModulePkg-License.txt
cp -a License.txt %{buildroot}/%{_docdir}/AAVMF/Licenses/MdeModulePkg-License.txt
cp -a License.txt %{buildroot}/%{_docdir}/AAVMF/Licenses/MdePkg-License.txt
cp -a License.txt %{buildroot}/%{_docdir}/AAVMF/Licenses/OptionRomPkg-License.txt
cp -a License.txt %{buildroot}/%{_docdir}/AAVMF/Licenses/ShellPkg-License.txt
cp -a License.txt %{buildroot}/%{_docdir}/AAVMF/Licenses/ArmPkg-License.txt
cp -a License.txt %{buildroot}/%{_docdir}/AAVMF/Licenses/ArmPlatformPkg-License.txt
cp -a License.txt %{buildroot}/%{_docdir}/AAVMF/Licenses/EmbeddedPkg-License.txt
%endif

%ifarch x86_64
mkdir -p %{buildroot}/usr/share/OVMF
cp -a OVMF/* %{buildroot}/usr/share/OVMF
cp -a OvmfPkg/README %{buildroot}/%{_docdir}/OVMF
cp -a OVMF-ol9-changelog.txt %{buildroot}/%{_docdir}/OVMF
# JSON files
mkdir -p %{buildroot}/usr/share/qemu/firmware
cp -a json_files/*ovmf* %{buildroot}/usr/share/qemu/firmware
# Include dup base files for compat with older libvirt
cp OVMF/OVMF_CODE.pure-efi.fd  %{buildroot}/usr/share/OVMF/OVMF_CODE.fd
cp OVMF/OVMF_VARS.pure-efi.fd  %{buildroot}/usr/share/OVMF/OVMF_VARS.fd
%endif
%ifarch aarch64
mkdir -p %{buildroot}/usr/share/AAVMF
cp -a AAVMF/* %{buildroot}/usr/share/AAVMF
cp -a AAVMF-ol9-changelog.txt %{buildroot}/%{_docdir}/AAVMF
# JSON files
mkdir -p %{buildroot}/usr/share/qemu/firmware
cp -a json_files/*aarch64* %{buildroot}/usr/share/qemu/firmware
# Include dup base files for compat with older libvirt
cp AAVMF/AAVMF_CODE.pure-efi.fd  %{buildroot}/usr/share/AAVMF/AAVMF_CODE.fd
cp AAVMF/AAVMF_VARS.pure-efi.fd  %{buildroot}/usr/share/AAVMF/AAVMF_VARS.fd
%endif

%files tools
%doc BaseTools/UserManuals/EfiRom_Utility_Man_Page.rtf
%doc BaseTools/UserManuals/VolInfo_Utility_Man_Page.rtf
%ifarch x86_64
%doc Oracle/OvmfVarsMgr/ovmf-vars-mgr.md
%endif
%ifarch aarch64
%doc Oracle/OvmfVarsMgr/aavmf-vars-mgr.md
%endif
%doc Oracle/OvmfVarsMgr/efi-siglist-gen.md
%{_bindir}/*

%defattr(-,root,root,-)

%ifarch x86_64
%files ovmf 
%dir /usr/share/OVMF
/usr/share/OVMF
%endif

%ifarch aarch64
%files aarch64
%dir /usr/share/AAVMF
/usr/share/AAVMF
%endif

%dir /usr/share/qemu/firmware
/usr/share/qemu/firmware

%ifarch x86_64
%dir %{_docdir}/OVMF/Licenses
%doc %{_docdir}/OVMF/Licenses/OvmfPkg-License.txt
%doc %{_docdir}/OVMF/Licenses/OpensslLib-License.txt
%doc %{_docdir}/OVMF/Licenses/edk2-License.txt
%doc %{_docdir}/OVMF/README
%doc %{_docdir}/OVMF/OVMF-ol9-changelog.txt
%endif

%ifarch aarch64
%dir %{_docdir}/AAVMF/Licenses
%doc %{_docdir}/AAVMF/Licenses/OvmfPkg-License.txt
%doc %{_docdir}/AAVMF/Licenses/FatPkg-License.txt
%doc %{_docdir}/AAVMF/Licenses/IntelFrameworkModulePkg-License.txt
%doc %{_docdir}/AAVMF/Licenses/MdeModulePkg-License.txt
%doc %{_docdir}/AAVMF/Licenses/MdePkg-License.txt
%doc %{_docdir}/AAVMF/Licenses/OptionRomPkg-License.txt
%doc %{_docdir}/AAVMF/Licenses/ArmPkg-License.txt
%doc %{_docdir}/AAVMF/Licenses/ArmPlatformPkg-License.txt
%doc %{_docdir}/AAVMF/Licenses/EmbeddedPkg-License.txt
%doc %{_docdir}/AAVMF/Licenses/ShellPkg-License.txt
%doc %{_docdir}/AAVMF/AAVMF-ol9-changelog.txt
%endif


%changelog
* Tue Jun 28 2022 Aaron Young <aaron.young@oracle.com>
- Create new 20220628 release for OL9
* Wed Jun 01 2022 Aaron Young <aaron.young@oracle.com>
- Create new 20220601 release for OL9
* Wed May 11 2022 Aaron Young <aaron.young@oracle.com>
- Create new 20220511 release for OL9
* Wed Apr 06 2022 Aaron Young <aaron.young@oracle.com>
- Create new 20220406 release for OL9 which includes the following fixed CVEs:
  {CVE-2022-0778}
* Mon Feb 07 2022 Aaron Young <aaron.young@oracle.com>
- Create new 20220207 build for OL9
