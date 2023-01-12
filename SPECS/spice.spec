Name:           spice
Version:        0.14.3
Release:        4%{?dist}
Summary:        Implements the SPICE protocol
Group:          User Interface/Desktops
License:        LGPLv2+
URL:            https://www.spice-space.org/
Source0:        https://www.spice-space.org/download/releases/%{name}-%{version}.tar.bz2
Source1:        https://www.spice-space.org/download/releases/%{name}-%{version}.tar.bz2.sig
Source2:        victortoso-E37A484F.keyring
Patch1:         0001-quic-Check-we-have-some-data-to-start-decoding-quic-.patch
Patch2:         0002-quic-Check-image-size-in-quic_decode_begin.patch
Patch3:         0003-quic-Check-RLE-lengths.patch
Patch4:         0004-quic-Avoid-possible-buffer-overflow-in-find_bucket.patch

Patch5:         0005-websocket-Fix-possible-integer-overflow.patch
Patch6:         0006-test-websocket-check-setsockopt-return-value.patch
Patch7:         0007-OpenSSL-1.0.2-disable-client-side-renegotiation.patch
Patch8:         0008-OpenSSL-1.1-disable-client-side-renegotiation.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=613529
%if 0%{?rhel} && 0%{?rhel} <= 7
ExclusiveArch:  x86_64
%else
ExclusiveArch:  %{ix86} x86_64 %{arm} aarch64
%endif

BuildRequires:  pkgconfig
BuildRequires:  glib2-devel >= 2.38
BuildRequires:  spice-protocol >= 0.14.0
BuildRequires:  celt051-devel
BuildRequires:  opus-devel
BuildRequires:  pixman-devel openssl-devel libjpeg-devel
BuildRequires:  libcacard-devel cyrus-sasl-devel
BuildRequires:  lz4-devel
BuildRequires:  gstreamer1-devel gstreamer1-plugins-base-devel
BuildRequires:  orc-devel
BuildRequires:  gnupg2
BuildRequires:  git-core
BuildRequires:  python3-devel
BuildRequires:  python3-pyparsing python3-six

%description
The Simple Protocol for Independent Computing Environments (SPICE) is
a remote display system built for virtual environments which allows
you to view a computing 'desktop' environment not only on the machine
where it is running, but from anywhere on the Internet and from a wide
variety of machine architectures.


%package server
Summary:        Implements the server side of the SPICE protocol
Group:          System Environment/Libraries

%description server
The Simple Protocol for Independent Computing Environments (SPICE) is
a remote display system built for virtual environments which allows
you to view a computing 'desktop' environment not only on the machine
where it is running, but from anywhere on the Internet and from a wide
variety of machine architectures.

This package contains the run-time libraries for any application that wishes
to be a SPICE server.


%package server-devel
Summary:        Header files, libraries and development documentation for spice-server
Group:          Development/Libraries
Requires:       %{name}-server%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description server-devel
This package contains the header files, static libraries and development
documentation for spice-server. If you like to develop programs
using spice-server, you will need to install spice-server-devel.


%prep
gpgv2 --quiet --keyring %{SOURCE2} %{SOURCE1} %{SOURCE0}
%autosetup -S git_am


%build
%define configure_client --disable-client
%configure \
    --enable-smartcard \
    --disable-client \
    --enable-lz4 \
    --enable-celt051 \
    --enable-gstreamer=1.0
make %{?_smp_mflags} WARN_CFLAGS='' V=1


%install
make DESTDIR=%{buildroot} install
rm -f %{buildroot}%{_libdir}/libspice-server.a
rm -f %{buildroot}%{_libdir}/libspice-server.la
mkdir -p %{buildroot}%{_libexecdir}


%ldconfig_scriptlets server


%files server
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc README CHANGELOG.md
%{_libdir}/libspice-server.so.1*

%files server-devel
%{_includedir}/spice-server
%{_libdir}/libspice-server.so
%{_libdir}/pkgconfig/spice-server.pc


%changelog
* Tue Jan 19 2021 Julien Ropé <jrope@redhat.com> - 0.14.3-4
- Disable client-side renegotiation to prevent potential DoS
  Resolves: rhbz#1904459

* Wed Jun 17 2020 Uri Lublin <uril@redhat.com> - 0.14.3-3
- Fix some static analyzer issues
- Removed Obsoletes line for spice-client
  Related: rhbz#1840240

* Mon Jun  1 2020 Frediano Ziglio <fziglio@redhat.com> - 0.14.3-2
- Fix multiple buffer overflows in QUIC decoding code
  Resolves: rhbz#1829946

* Thu May 28 2020 Frediano Ziglio <fziglio@redhat.com> - 0.14.3-1
- Update to 0.14.3
  Revolves: rhbz#1840240

* Fri May 17 2019 Victor Toso <victortoso@redhat.com> - 0.14.2-1
- Update to 0.14.2
  Resolves: rhbz#1562123

* Fri May 10 2019 Victor Toso <victortoso@redhat.com> - 0.14.0-8
- Fix builds on 8.1.0 branch
- Fix gating test (add bug)
  Resolves: rhbz#1686518

* Tue Dec 18 2018 Christophe Fergeau <cfergeau@redhat.com> - 0.14.0-7
- Fix off-by-one error during guest-to-host memory address conversion
  Resolves: CVE-2019-3813

* Fri Aug 17 2018 Frediano Ziglio <fziglio@redhat.com> - 0.14.0-6
- Fix flexible array buffer overflow
  Resolves: rhbz#1618555

* Mon Aug 13 2018 Victor Toso <victortoso@redhat.com>  - 0.14.0-5
- Include python3-devel to not fail on rhel-8.0 builds
- Resolves: rhbz#1615570

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.14.0-3
- Switch to %%ldconfig_scriptlets

* Wed Nov 08 2017 Merlin Mathesius <mmathesi@redhat.com> - 0.14.0-2
- Cleanup spec file conditionals

* Wed Oct 11 2017 Christophe Fergeau <cfergeau@redhat.com> - 0.14.0-1
- Update to new stable release

* Tue Sep 26 2017 Christophe Fergeau <christophe@redhat.com> - 0.13.91-1
- Update to latest upstream release

* Thu Aug 24 2017 Christophe Fergeau <cfergeau@redhat.com> - 0.13.90-3
- Add missing (new) BuildRequires, remove obsolete one

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Christophe Fergeau <cfergeau@redhat.com> 0.13.90-1
- Update to latest upstream release (0.13.90)

* Mon Feb 06 2017 Christophe Fergeau <cfergeau@redhat.com> 0.13.3-2
- Add upstream patches fixing CVE-2016-9577 and CVE-2016-9578

* Mon Nov 21 2016 Christophe Fergeau <cfergeau@redhat.com> 0.13.3-1
- Update to spice 0.13.3

* Fri Aug 05 2016 Christophe Fergeau <cfergeau@redhat.com> - 0.13.2-1
- Update to spice 0.13.2

* Tue Jun 14 2016 Peter Robinson <pbrobinson@fedoraproject.org> 0.13.1-2
- Use %%license
- Build on aarch64

* Wed Apr 13 2016 Christophe Fergeau <cfergeau@redhat.com> 0.13.1-1
- Update to 0.13.1 release. This is a development release, but by the
  time Fedora 25 gets released, a stable 0.14.0 should be released.

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Oct 06 2015 Christophe Fergeau <cfergeau@redhat.com> 0.12.6-1
- Update to new 0.12.6 upstream release

* Wed Jul 29 2015 Christophe Fergeau <cfergeau@redhat.com> 0.12.5-9
- Drop patch added in previous build which is no longer needed with
  spice-protocol 0.12.9 (and actually is actually breaking QEMU compilation
  without an additional patch)

* Fri Jul 03 2015 Christophe Fergeau <cfergeau@redhat.com> 0.12.5-8
- Add upstream patch avoiding a regression in spice-protocol 0.12.8 which
  breaks SPICE support in QEMU

* Thu Jul 02 2015 Christophe Fergeau <cfergeau@redhat.com> 0.12.5-7
- Fix migration race condition which causes a crash when triggered
  Resolves: rhbz#1238212

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 25 2014 Christophe Fergeau <cfergeau@redhat.com> 0.12.5-5
- Fix advertised sound playback/recording rates in public headers
  Resolves: rhbz#1129961 (QEMU would need a rebuild though)

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 19 2014 Christophe Fergeau <cfergeau@redhat.com> 0.12.5-2
- Add missing BuildRequires in order to enable Opus support

* Mon May 19 2014 Christophe Fergeau <cfergeau@redhat.com> 0.12.5-1
- Update to new 0.12.5 release

* Wed Oct 30 2013 Christophe Fergeau <cfergeau@redhat.com> 0.12.4-3
- Add patch fixing CVE-2013-4282

* Fri Sep 13 2013 Christophe Fergeau <cfergeau@redhat.com> 0.12.4-2
- Add upstream patch fixing rhbz#995041

* Fri Aug  2 2013 Hans de Goede <hdegoede@redhat.com> - 0.12.4-1
- New upstream bug-fix release 0.12.4
- Add patches from upstream git to fix sound-channel-free crash (rhbz#986407)
- Add Obsoletes for dropped spice-client sub-package

* Thu May 23 2013 Christophe Fergeau <cfergeau@redhat.com> 0.12.3-2
- Stop building spicec, it's obsolete and superseded by remote-viewer
  (part of virt-viewer)

* Tue May 21 2013 Christophe Fergeau <cfergeau@redhat.com> 0.12.3-1
- New upstream release 0.12.3
- Drop all patches (they were all upstreamed)

* Mon Apr 15 2013 Hans de Goede <hdegoede@redhat.com> - 0.12.2-4
- Add fix from upstream for a crash when the guest uses RGBA (rhbz#952242)

* Thu Mar 07 2013 Adam Jackson <ajax@redhat.com> 0.12.2-4
- Rebuild for new libsasl2 soname in F19

* Mon Jan 21 2013 Hans de Goede <hdegoede@redhat.com> - 0.12.2-3
- Add a number of misc. bug-fixes from upstream

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 0.12.2-2
- rebuild against new libjpeg

* Thu Dec 20 2012 Hans de Goede <hdegoede@redhat.com> - 0.12.2-1
- New upstream release 0.12.2

* Fri Sep 28 2012 Hans de Goede <hdegoede@redhat.com> - 0.12.0-1
- New upstream release 0.12.0
- Some minor spec file cleanups
- Enable building on arm

* Thu Sep 6 2012 Soren Sandmann <ssp@redhat.com> - 0.11.3-1
- BuildRequire pyparsing

* Thu Sep 6 2012 Soren Sandmann <ssp@redhat.com> - 0.11.3-1
- Add capability patches
- Add capability patches to the included copy of spice-protocol

    Please see the comment above Patch6 and Patch7
    regarding this situation.

* Thu Sep 6 2012 Soren Sandmann <ssp@redhat.com> - 0.11.3-1
- Update to 0.11.3 and drop upstreamed patches
- BuildRequire spice-protocol 0.12.1

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 14 2012 Alon Levy <alevy@redhat.com>
- Fix mjpeg memory leak and bad behavior.
- Add usbredir to list of channels for security purposes. (#819484)

* Sun May 13 2012 Alon Levy <alevy@redhat.com>
- Add double free fix. (#808936)

* Tue Apr 24 2012 Alon Levy <alevy@redhat.com>
- Add 32 bit fixes from git master. (#815717)

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.1-2
- Rebuilt for c++ ABI breakage

* Mon Jan 23 2012 Hans de Goede <hdegoede@redhat.com> - 0.10.1-1
- New upstream release 0.10.1

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 10 2011 Alon Levy <alevy@redhat.com> - 0.10.0-1
- New upstream release 0.10.0
- support spice-server.i686

* Wed Sep 28 2011 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.9.1-2
- Provides spice-xpi-client alternative in spice-client

* Thu Aug 25 2011 Hans de Goede <hdegoede@redhat.com> - 0.9.1-1
- New upstream release 0.9.1

* Mon Jul 25 2011 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.9.0-1
- New upstream release 0.9.0

* Wed Apr 20 2011 Hans de Goede <hdegoede@redhat.com> - 0.8.1-1
- New upstream release 0.8.1

* Fri Mar 11 2011 Hans de Goede <hdegoede@redhat.com> - 0.8.0-2
- Fix being unable to send ctrl+alt+key when release mouse is bound to
  ctrl+alt (which can happen when used from RHEV-M)

* Tue Mar  1 2011 Hans de Goede <hdegoede@redhat.com> - 0.8.0-1
- New upstream release 0.8.0

* Fri Feb 11 2011 Hans de Goede <hdegoede@redhat.com> - 0.7.3-1
- New upstream release 0.7.3

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 19 2011 Hans de Goede <hdegoede@redhat.com> - 0.7.2-1
- New upstream release 0.7.2

* Fri Dec 17 2010 Hans de Goede <hdegoede@redhat.com> - 0.7.1-1
- New upstream release 0.7.1
- Drop all patches (all upstreamed)
- Enable smartcard (CAC) support

* Wed Nov 17 2010 Hans de Goede <hdegoede@redhat.com> - 0.6.3-4
- Fix the info layer not showing when used through the XPI
- Do not let the connection gui flash by when a hostname has been specified
  on the cmdline
- Fix spice client locking up when dealing with XIM input (#654265)
- Fix modifier keys getting stuck (#655048)
- Fix spice client crashing when dealing with XIM ibus input (#655836)
- Fix spice client only showing a white screen in full screen mode

* Sat Nov  6 2010 Hans de Goede <hdegoede@redhat.com> - 0.6.3-3
- Log to ~/.spicec/cegui.log rather then to CEGUI.log in the cwd, this
  fixes spicec from aborting when run in a non writable dir (#650253)

* Fri Nov  5 2010 Hans de Goede <hdegoede@redhat.com> - 0.6.3-2
- Various bugfixes from upstream git:
  - Make spicec work together with the Firefox XPI for RHEV-M
  - Make sure the spicec window gets properly raised when first shown

* Mon Oct 18 2010 Hans de Goede <hdegoede@redhat.com> - 0.6.3-1
- Update to 0.6.3
- Enable GUI

* Thu Sep 30 2010 Gerd Hoffmann <kraxel@redhat.com> - 0.6.1-1
- Update to 0.6.1.

* Tue Aug 31 2010 Alexander Larsson <alexl@redhat.com> - 0.6.0-1
- Update to 0.6.0 (stable release)

* Tue Jul 20 2010 Alexander Larsson <alexl@redhat.com> - 0.5.3-1
- Update to 0.5.3

* Tue Jul 13 2010 Gerd Hoffmann <kraxel@redhat.com> - 0.5.2-4
- Quote %% in changelog to avoid macro expansion.

* Mon Jul 12 2010 Gerd Hoffmann <kraxel@redhat.com> - 0.5.2-3
- %%configure handles CFLAGS automatically, no need to fiddle
  with %%{optflags} manually.

* Mon Jul 12 2010 Gerd Hoffmann <kraxel@redhat.com> - 0.5.2-2
- Fix license: LGPL.
- Cleanup specfile, drop bits not needed any more with
  recent rpm versions (F13+).
- Use optflags as-is.
-

* Fri Jul 9 2010 Gerd Hoffmann <kraxel@redhat.com> - 0.5.2-1
- initial package.

