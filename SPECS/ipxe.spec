# ROMS we want for QEMU with format PCIID:QEMUNAME
%global qemuroms \\\
  8086100e:e1000 \\\
  10ec8139:rtl8139 \\\
  1af41000:virtio \\\
  808610d3:e1000e

%if 0%{?fedora}
# Fedora specific roms
%global qemuroms %{qemuroms} \\\
  10222000:pcnet \\\
  10ec8029:ne2k_pci \\\
  80861209:eepro100 \\\
  15ad07b0:vmxnet3
%endif

# We only build the ROMs if on an EFI build host. The resulting
# binary RPM will be noarch, so other archs will still be able
# to use the binary ROMs.
%global buildarches x86_64 aarch64

# debugging firmwares does not go the same way as a normal program.
# moreover, all architectures providing debuginfo for a single noarch
# package is currently clashing in koji, so don't bother.
%global debug_package %{nil}

# Upstream don't do "releases" :-( So we're going to use the date
# as the version, and a GIT hash as the release. Generate new GIT
# snapshots using the folowing commands:
#
# $ hash=`git log -1 --format='%h'`
# $ date=`git log -1 --format='%cd' --date=short | tr -d -`
# $ git archive --prefix ipxe-${date}-git${hash}/ ${hash} | xz -7e > ipxe-${date}-git${hash}.tar.xz
#
# And then change these two:

%global hash 4bd064de
%global date 20200823

Name:    ipxe
Version: %{date}
Release: 9.git%{hash}%{?dist}
Summary: A network boot loader

License: GPLv2 with additional permissions and BSD
URL:     http://ipxe.org/

Source0: %{name}-%{version}-git%{hash}.tar.xz
Source1: script.ipxe

# Enable IPv6 for qemu's config
# Sent upstream: http://lists.ipxe.org/pipermail/ipxe-devel/2015-November/004494.html
Patch0001: 0001-build-customize-configuration.patch
Patch0002: 0002-Use-spec-compliant-timeouts.patch
# For bz#1935932 - ipxe implements and/or uses the deprecated SHA-1 algorithm by default (
Patch3: ipxe-Disable-SHA-1.patch
# For bz#1985658 - carry forward rhel8 ipxe packaging changes
Patch4: ipxe-Add-ping-command-support.patch
# For bz#1985658 - carry forward rhel8 ipxe packaging changes
Patch5: ipxe-Add-VLAN-tagging-support.patch
# For bz#1985658 - carry forward rhel8 ipxe packaging changes
Patch6: ipxe-netdevice-Strip-802.Q-VLAN-0-priority-tags.patch

# Source-git patches

%ifarch %{buildarches}
BuildRequires: perl-interpreter
BuildRequires: perl-Getopt-Long
%if 0%{?fedora} >= 33 || 0%{?rhel} >= 9
BuildRequires: perl-FindBin
BuildRequires: perl-lib
%endif
%ifarch x86_64
BuildRequires: syslinux
%endif
BuildRequires: mtools
BuildRequires: xorriso
BuildRequires: edk2-tools
BuildRequires: xz-devel
BuildRequires: gcc

BuildRequires: binutils-devel
BuildRequires: make

Obsoletes: gpxe <= 1.0.1

%ifarch x86_64
%package rhcert
Summary: Redhat hwcert custom ipxe image
BuildArch: noarch

%description rhcert
Custom ipxe image for use in hardware certification and validation

%package bootimgs-x86
Summary: X86 Network boot loader images in bootable USB, CD, floppy and GRUB formats
BuildArch: noarch
Provides: %{name}-bootimgs = %{version}-%{release}
Obsoletes: %{name}-bootimgs < %{version}-%{release}
Obsoletes: gpxe-bootimgs <= 1.0.1

%description bootimgs-x86
iPXE is an open source network bootloader. It provides a direct
replacement for proprietary PXE ROMs, with many extra features such as
DNS, HTTP, iSCSI, etc.

This package contains the iPXE boot images in USB, CD, floppy, and PXE
UNDI formats.
%endif

%ifarch aarch64
%package bootimgs-aarch64
Summary: AArch64 Network boot loader images in bootable USB and GRUB formats
Group:   Development/Tools
BuildArch: noarch

%description bootimgs-aarch64
iPXE is an open source network bootloader. It provides a direct
replacement for proprietary PXE ROMs, with many extra features such as
DNS, HTTP, iSCSI, etc.

This package contains the iPXE ARM64 boot images in USB and GRUB formats.
%endif

%package roms
Summary: Network boot loader roms in .rom format
Requires: %{name}-roms-qemu = %{version}-%{release}
BuildArch: noarch
Obsoletes: gpxe-roms <= 1.0.1

%package roms-qemu
Summary: Network boot loader roms supported by QEMU, .rom format
BuildArch: noarch
Obsoletes: gpxe-roms-qemu <= 1.0.1

%description roms
iPXE is an open source network bootloader. It provides a direct
replacement for proprietary PXE ROMs, with many extra features such as
DNS, HTTP, iSCSI, etc.

This package contains the iPXE roms in .rom format.

%description roms-qemu
iPXE is an open source network bootloader. It provides a direct
replacement for proprietary PXE ROMs, with many extra features such as
DNS, HTTP, iSCSI, etc.

This package contains the iPXE ROMs for devices emulated by QEMU, in
.rom format.
%endif

%description
iPXE is an open source network bootloader. It provides a direct
replacement for proprietary PXE ROMs, with many extra features such as
DNS, HTTP, iSCSI, etc.

%prep
%setup -q -n %{name}-%{version}-git%{hash}
%autopatch -p1

pushd src
# ath9k drivers are too big for an Option ROM, and ipxe devs say it doesn't
# make sense anyways
# http://lists.ipxe.org/pipermail/ipxe-devel/2012-March/001290.html
rm -rf drivers/net/ath/ath9k

cp %{SOURCE1} .
popd


%build
cd src

make_ipxe() {
    make %{?_smp_mflags} \
        NO_WERROR=1 V=1 \
        GITVERSION=%{hash} \
        "$@"
}

%ifarch x86_64

make_ipxe bin-x86_64-efi/ipxe.efi EMBED=script.ipxe
mv bin-x86_64-efi/ipxe.efi bin-x86_64-efi/ipxe-rhcert.efi

make_ipxe bin-i386-efi/ipxe.efi bin-x86_64-efi/ipxe.efi \
    bin-x86_64-efi/snponly.efi

make_ipxe ISOLINUX_BIN=/usr/share/syslinux/isolinux.bin \
    bin/undionly.kpxe bin/ipxe.{dsk,iso,usb,lkrn} \
    allroms

# build roms with efi support for qemu
mkdir bin-combined
for romstr in %{qemuroms}; do
  rom=$(echo "$romstr" | cut -d ":" -f 1)

  make_ipxe CONFIG=qemu bin/${rom}.rom
  make_ipxe CONFIG=qemu bin-x86_64-efi/${rom}.efidrv
  vid="0x${rom%%????}"
  did="0x${rom#????}"
  EfiRom -f "$vid" -i "$did" --pci23 \
         -ec bin-x86_64-efi/${rom}.efidrv \
         -o  bin-combined/${rom}.eficrom
  util/catrom.pl \
      bin/${rom}.rom \
      bin-combined/${rom}.eficrom \
      > bin-combined/${rom}.rom
  EfiRom -d  bin-combined/${rom}.rom
  # truncate to at least 256KiB
  truncate -s \>256K bin-combined/${rom}.rom
  # verify rom fits in 256KiB
  test $(stat -c '%s' bin-combined/${rom}.rom) -le $((256 * 1024))
done

%endif

%ifarch aarch64
make_ipxe bin-arm64-efi/snponly.efi
%if 0%{?fedora}
make_ipxe bin-arm64-efi/ipxe.efi
%endif
%endif

%install
%ifarch x86_64
mkdir -p %{buildroot}/%{_datadir}/%{name}/
mkdir -p %{buildroot}/%{_datadir}/%{name}.efi/
pushd src/bin/

cp -a undionly.kpxe ipxe.{iso,usb,dsk,lkrn} %{buildroot}/%{_datadir}/%{name}/

for img in *.rom; do
  if [ -e $img ]; then
    cp -a $img %{buildroot}/%{_datadir}/%{name}/
    echo %{_datadir}/%{name}/$img >> ../../rom.list
  fi
done
popd

cp -a src/bin-i386-efi/ipxe.efi %{buildroot}/%{_datadir}/%{name}/ipxe-i386.efi
cp -a src/bin-x86_64-efi/ipxe.efi %{buildroot}/%{_datadir}/%{name}/ipxe-x86_64.efi
cp -a src/bin-x86_64-efi/snponly.efi %{buildroot}/%{_datadir}/%{name}/ipxe-snponly-x86_64.efi
cp -a src/bin-x86_64-efi/ipxe-rhcert.efi %{buildroot}/%{_datadir}/%{name}/ipxe-x86_64-rhcert.efi

mkdir -p %{buildroot}%{_datadir}/%{name}/qemu/

for romstr in %{qemuroms}; do
  # the roms supported by qemu will be packaged separatedly
  # remove from the main rom list and add them to qemu.list
  rom=$(echo "$romstr" | cut -d ":" -f 1)
  qemuname=$(echo "$romstr" | cut -d ":" -f 2)
  sed -i -e "/\/${rom}.rom/d" rom.list
  echo %{_datadir}/%{name}/${rom}.rom >> qemu.rom.list

  cp src/bin-combined/${rom}.rom %{buildroot}/%{_datadir}/%{name}.efi/
  echo %{_datadir}/%{name}.efi/${rom}.rom >> qemu.rom.list

  # Set up symlinks with expected qemu firmware names
  ln -s ../../ipxe/${rom}.rom %{buildroot}%{_datadir}/%{name}/qemu/pxe-${qemuname}.rom
  ln -s ../../ipxe.efi/${rom}.rom %{buildroot}%{_datadir}/%{name}/qemu/efi-${qemuname}.rom
done

# endif x86_64
%endif


%ifarch aarch64
mkdir -p %{buildroot}/%{_datadir}/%{name}/arm64-efi
cp -a src/bin-arm64-efi/snponly.efi %{buildroot}/%{_datadir}/%{name}/arm64-efi/snponly.efi
%if 0%{?fedora}
cp -a src/bin-arm64-efi/ipxe.efi %{buildroot}/%{_datadir}/%{name}/arm64-efi/ipxe.efi
%endif
%endif

%ifarch x86_64
%files bootimgs-x86
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/ipxe.iso
%{_datadir}/%{name}/ipxe.usb
%{_datadir}/%{name}/ipxe.dsk
%{_datadir}/%{name}/ipxe.lkrn
%{_datadir}/%{name}/ipxe-i386.efi
%{_datadir}/%{name}/ipxe-x86_64.efi
%{_datadir}/%{name}/undionly.kpxe
%{_datadir}/%{name}/ipxe-snponly-x86_64.efi
%doc COPYING COPYING.GPLv2 COPYING.UBDL

%files roms -f rom.list
%dir %{_datadir}/%{name}
%doc COPYING COPYING.GPLv2 COPYING.UBDL

%files roms-qemu -f qemu.rom.list
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}.efi
%{_datadir}/%{name}/qemu
%doc COPYING COPYING.GPLv2 COPYING.UBDL

%files rhcert
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/ipxe-x86_64-rhcert.efi
%endif

%ifarch aarch64
%files bootimgs-aarch64
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/arm64-efi
%if 0%{?fedora}
%{_datadir}/%{name}/arm64-efi/ipxe.efi
%endif
%{_datadir}/%{name}/arm64-efi/snponly.efi
%endif

%changelog
* Tue Apr 05 2022 Jarod Wilson <jarod@redhat.com> - 20200823-9.git4bd064de
- Fix Obsoletes: and changelog versioning

* Thu Mar 31 2022 Jarod Wilson <jarod@redhat.com> - 20200823-8.git4bd064de
- Add ARM 64 EFI artifacts [yselkowi] (bz 2059349)

* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com> - 20200823-7.git4bd064de
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Sat Aug 07 2021 Miroslav Rezanina <mrezanin@redhat.com> - 20200823-6.git4bd064de
- ipxe-Add-ping-command-support.patch [bz#1985658]
- ipxe-Add-VLAN-tagging-support.patch [bz#1985658]
- ipxe-netdevice-Strip-802.Q-VLAN-0-priority-tags.patch [bz#1985658]
- ipxe-Provide-snponly.efi-rom.patch [bz#1985658]
- ipxe-Build-hwcert-subpackage.patch [bz#1985658]
- Resolves: bz#1985658
  (carry forward rhel8 ipxe packaging changes)

* Mon Jul 26 2021 Miroslav Rezanina <mrezanin@redhat.com> - 20200823-5.git4bd064de
- ipxe-Disable-SHA-1.patch [bz#1935932]
- ipxe-Replace-genisoimage-with-xorriso.patch [bz#1971981]
- ipxe-spec-Drop-disabled-efi-ia32-build-infrastructure.patch [bz#1980138]
- ipxe-spec-Generate-qemu-compatible-rom-filenames.patch [bz#1980138]
- Resolves: bz#1935932
  (ipxe implements and/or uses the deprecated SHA-1 algorithm by default ()
- Resolves: bz#1971981
  (Please replace genisoimage with xorriso)
- Resolves: bz#1980138
  (install qemu rom symlinks so qemu doesn't have to)

* Tue Jun 08 2021 Miroslav Rezanina <mrezanin@redhat.com> - 20200823-4.git4bd064de
- ipxe-Skip-some-QEMU-ROMs-when-building-for-RHEL.patch [bz#1956931]
- ipxe-spec-combine-BIOS-and-EFI-roms-using-util-catrom.pl.patch [bz#1957246]
- Resolves: bz#1956931
  (ipxe-roms-qemu list: Clean out old ROMs)
- Resolves: bz#1957246
  (boot vm from pxe failed)

* Fri Apr 16 2021 Mohan Boddu <mboddu@redhat.com> - 20200823-3.git4bd064de
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20200823-2.git4bd064de
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Sep 15 2020 Cole Robinson <aintdiscole@gmail.com> - 20200823-1.git4bd064de.git
- Update to newer git snapshot, synced with qemu.git
- Re-enable HTTPS support, with edk2 fix included (bz 1820836)

* Fri Sep 04 2020 Merlin Mathesius <mmathesi@redhat.com> - 20190125-9.git36a4c85f
- Workaound fatal GCC 9 compilation/link errors
- Fix conditionals for perl BuildRequires

* Mon Aug 17 2020 Cole Robinson <aintdiscole@gmail.com> - 20190125-8.git36a4c85f
- Revert HTTPS support, causes boot hangs with UEFI (bz 1869102)

* Tue Aug 11 2020 Cole Robinson <aintdiscole@gmail.com> - 20190125-7.git36a4c85f
- Enable HTTPS support (bug 1820836)

* Wed Jul 29 2020 Richard W.M. Jones <rjones@redhat.com> - 20190125-6.git36a4c85f
- Explicitly BR perl-FindBin and perl-lib.

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20190125-5.git36a4c85f
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20190125-4.git36a4c85f
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20190125-3.git36a4c85f
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 16 2019 Paolo Bonzini <pbonxini@redhat.com> - 20190125-2.git36a4c85f
- Allow removing IA32 EFI images from combined oproms
- Check that the ROMs fit in 256K and pad them

* Tue Feb 12 2019 Daniel P. Berrangé <berrange@redhat.com> - 20190125-1.git36a4c85f
- Update to latest git snapshot

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20170710-6.git0600d3ae
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jul 23 2018 Daniel P. Berrangé <berrange@redhat.com> - 20170710-5.git0600d3ae
- mkisofs tool moved to genisoimage RPM

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20170710-4.git0600d3ae
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20170710-3.git0600d3ae
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Nov 21 2017 Paolo Bonzini <pbonzini@redhat.com> - ipxe-20170710-2.git0600d3ae
- Include bugfix and configuration patches from RHEL
- Disable cross compilation on RHEL

* Thu Aug 03 2017 Cole Robinson <crobinso@redhat.com> - ipxe-20170710-1.git0600d3ae
- Update to ipxe 0600d3ae for qemu-2.10.0

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20161108-4.gitb991c67
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20161108-3.gitb991c67
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20161108-2.gitb991c67
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Dec 04 2016 Cole Robinson <crobinso@redhat.com> - 20161108-1.gitb991c67
- Rebase to version shipped with qemu 2.8

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 20150821-3.git4e03af8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 26 2016 Cole Robinson <crobinso@redhat.com> 20150821-2.git4e03af8
- Build ipxe.efi (bug 1300865)
- Build eepro100 rom for qemu

* Tue Nov 17 2015 Cole Robinson <crobinso@redhat.com> - 20150821-1.git4e03af8
- Update to commit 4e03af8 for qemu 2.5
- Enable IPv6 (bug 1280318)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20150407-3.gitdc795b9f
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Apr 16 2015 Paolo Bonzini <pbonzini@redhat.com> - 20150407-2.gitdc795b9f
- Fix virtio bug with UEFI driver

* Thu Apr 16 2015 Paolo Bonzini <pbonzini@redhat.com> - 20150407-1.gitdc795b9f
- Update to latest upstream snapshot
- Switch source to .tar.xz
- Include patches from QEMU submodule
- Use config file for configuration
- Distribute additional permissions on top of GPLv2 ("UBDL")

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20140303-3.gitff1e7fc7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20140303-2.gitff1e7fc7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 03 2014 Cole Robinson <crobinso@redhat.com> - 20140303-1.gitff1e7fc7
- Allow access to ipxe prompt if VM is set to pxe boot (bz #842932)
- Enable PNG support (bz #1058176)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20130517-3.gitc4bce43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May 20 2013 Paolo Bonzini <pbonzini@redhat.com> - 20130103-3.git717279a
- Fix BuildRequires, use cross-compiler when building on 32-bit i686
- Build UEFI drivers for QEMU and include them (patch from Gerd Hoffmann.
  BZ#958875)

* Fri May 17 2013 Daniel P. Berrange <berrange@redhat.com> - 20130517-1.gitc4bce43
- Update to latest upstream snapshot

* Fri May 17 2013 Daniel P. Berrange <berrange@redhat.com> - 20130103-3.git717279a
- Fix build with GCC 4.8 (rhbz #914091)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20130103-2.git717279a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan  3 2013 Daniel P. Berrange <berrange@redhat.com> - 20130103-1.git717279a
- Updated to latest GIT snapshot

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20120328-2.gitaac9718
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Mar 28 2012 Daniel P. Berrange <berrange@redhat.com> - 20120328-1.gitaac9718
- Update to newer upstream

* Fri Mar 23 2012 Daniel P. Berrange <berrange@redhat.com> - 20120319-3.git0b2c788
- Remove more defattr statements

* Tue Mar 20 2012 Daniel P. Berrange <berrange@redhat.com> - 20120319-2.git0b2c788
- Remove BuildRoot & rm -rf of it in install/clean sections
- Remove defattr in file section
- Switch to use global, instead of define for macros
- Add note about Patch1 not going upstream
- Split BRs across lines for easier readability

* Mon Feb 27 2012 Daniel P. Berrange <berrange@redhat.com> - 20120319-1.git0b2c788
- Initial package based on gPXE

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 21 2011 Matt Domsch <mdomsch@fedoraproject.org> - 1.0.1-4
- don't use -Werror, it flags a failure that is not a failure for gPXE

* Mon Feb 21 2011 Matt Domsch <mdomsch@fedoraproject.org> - 1.0.1-3
- Fix virtio-net ethernet frame length (patch by cra), fixes BZ678789

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Aug  5 2010 Matt Domsch <mdomsch@fedoraproject.org> - 1.0.1-1
- New drivers: Intel e1000, e1000e, igb, EFI snpnet, JMicron jme,
  Neterion X3100, vxge, pcnet32.
- Bug fixes and improvements to drivers, wireless, DHCP, iSCSI,
  COMBOOT, and EFI.
* Tue Feb  2 2010 Matt Domsch <mdomsch@fedoraproject.org> - 1.0.0-1
- bugfix release, also adds wireless card support
- bnx2 builds again
- drop our one patch

* Tue Oct 27 2009 Matt Domsch <mdomsch@fedoraproject.org> - 0.9.9-1
- new upstream version 0.9.9
-- plus patches from git up to 20090818 which fix build errors and
   other release-critical bugs.
-- 0.9.9: added Attansic L1E and sis190/191 ethernet drivers.  Fixes
   and updates to e1000 and 3c90x drivers.
-- 0.9.8: new commands: time, sleep, md5sum, sha1sum. 802.11 wireless
   support with Realtek 8180/8185 and non-802.11n Atheros drivers.
   New Marvell Yukon-II gigabet Ethernet driver.  HTTP redirection
   support.  SYSLINUX floppy image type (.sdsk) with usable file
   system.  Rewrites, fixes, and updates to 3c90x, forcedeth, pcnet32,
   e1000, and hermon drivers.

* Mon Oct  5 2009 Matt Domsch <mdomsch@fedoraproject.org> - 0.9.7-6
- move rtl8029 from -roms to -roms-qemu for qemu ne2k_pci NIC (BZ 526776)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue May 19 2009 Matt Domsch <mdomsch@fedoraproject.org> - 0.9.7-4
- add undionly.kpxe to -bootimgs

* Tue May 12 2009 Matt Domsch <mdomsch@fedoraproject.org> - 0.9.7-3
- handle isolinux changing paths

* Sat May  9 2009 Matt Domsch <mdomsch@fedoraproject.org> - 0.9.7-2
- add dist tag

* Thu Mar 26 2009 Matt Domsch <mdomsch@fedoraproject.org> - 0.9.7-1
- Initial release based on etherboot spec
