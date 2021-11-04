Name:           SDL2
Version:        2.0.10
Release:        2%{?dist}
Summary:        Cross-platform multimedia library

%if 0%{?fedora}
%global enable_jack 1
%endif

License:        zlib and MIT
URL:            http://www.libsdl.org/
Source0:        http://www.libsdl.org/release/%{name}-%{version}.tar.gz
Source1:        SDL_config.h

Patch0:         multilib.patch
# ptrdiff_t is not the same as khronos defines on 32bit arches
Patch1:         SDL2-2.0.9-khrplatform.patch
Patch2:         CVE-2019-13616-validate_image_size_when_loading_BMP_files.patch

BuildRequires:	gcc
BuildRequires:  alsa-lib-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libGLU-devel
BuildRequires:  mesa-libEGL-devel
BuildRequires:  mesa-libGLES-devel
BuildRequires:  libXext-devel
BuildRequires:  libX11-devel
BuildRequires:  libXi-devel
BuildRequires:  libXrandr-devel
BuildRequires:  libXrender-devel
BuildRequires:  libXScrnSaver-devel
BuildRequires:  libusb-devel
BuildRequires:  libXinerama-devel
BuildRequires:  libXcursor-devel
BuildRequires:  systemd-devel
# PulseAudio
BuildRequires:  pkgconfig(libpulse-simple)
# Jack
%if 0%{?enable_jack}
BuildRequires:  pkgconfig(jack)
%endif
# D-Bus
BuildRequires:  pkgconfig(dbus-1)
# IBus
BuildRequires:  pkgconfig(ibus-1.0)
# Wayland
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(xkbcommon)
# Vulkan
%ifnarch s390 s390x aarch64 ppc64le
BuildRequires:  vulkan-devel
%endif
# KMS
BuildRequires:  mesa-libgbm-devel
BuildRequires:  libdrm-devel

%description
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library designed
to provide fast access to the graphics frame buffer and audio device.

%package devel
Summary:        Files needed to develop Simple DirectMedia Layer applications
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       mesa-libEGL-devel%{?_isa}
Requires:       mesa-libGLES-devel%{?_isa}
Requires:       libX11-devel%{?_isa}

%description devel
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library designed
to provide fast access to the graphics frame buffer and audio device. This
package provides the libraries, include files, and other resources needed for
developing SDL applications.

%package static
Summary:        Static libraries for SDL2

%description static
Static libraries for SDL2.

%prep
%autosetup -p1
# Compilation without ESD
sed -i -e 's/.*AM_PATH_ESD.*//' configure.ac
sed -i -e 's/\r//g' TODO.txt README.txt WhatsNew.txt BUGS.txt COPYING.txt CREDITS.txt README-SDL.txt

%build
%configure \
    --enable-sdl-dlopen \
    --enable-video-kmsdrm \
    --disable-arts \
    --disable-esd \
    --disable-nas \
    --enable-pulseaudio-shared \
%if 0%{?enable_jack}
    --enable-jack-shared \
%else
    --disable-jack \
%endif
    --enable-alsa \
    --enable-video-wayland \
%ifnarch s390 s390x aarch64 ppc64le
    --enable-video-vulkan \
%endif
    --enable-sse2=no \
    --enable-sse3=no \
    --disable-rpath \
%ifarch ppc64le
    --disable-altivec \
%endif

make %{?_smp_mflags}

%install
%make_install

# Rename SDL_config.h to SDL_config-<arch>.h to avoid file conflicts on
# multilib systems and install SDL_config.h wrapper
mv %{buildroot}%{_includedir}/SDL2/SDL_config.h %{buildroot}%{_includedir}/SDL2/SDL_config-%{_arch}.h
install -p -m 644 %{SOURCE1} %{buildroot}%{_includedir}/SDL2/SDL_config.h

# remove libtool .la file
rm -vf %{buildroot}%{_libdir}/*.la
# remove static .a file
# rm -f %{buildroot}%{_libdir}/*.a

%ldconfig_scriptlets

%files
%license COPYING.txt
%doc BUGS.txt CREDITS.txt README-SDL.txt
%{_libdir}/lib*.so.*

%files devel
%doc README.txt TODO.txt WhatsNew.txt
%{_bindir}/*-config
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/sdl2.pc
%{_libdir}/cmake/SDL2/
%{_includedir}/SDL2
%{_datadir}/aclocal/*

%files static
%license COPYING.txt
%{_libdir}/lib*.a

%changelog
* Fri Nov 22 2019 Wim Taymans <wtaymans@redhat.com> - 2.0.10-2
- Fix CVE-2019-13616 SDL: heap-based buffer overflow in SDL blit
  functions in video/SDL_blit*.c
- Resolves: rhbz#1756279

* Tue Nov 12 2019 Wim Taymans <wtaymans@redhat.com> - 2.0.10-1
- Update to 2.0.10
- Resolves: rhbz#1751780

* Fri Feb 15 2019 Tom Callaway <spot@fedoraproject.org> - 2.0.9-3
- use khrplatform defines, not ptrdiff_t

* Tue Aug 14 2018 Wim Taymans <wtaymans@redhat.com> - 2.0.8-7
- Disable jack

* Sat Aug 11 2018 Wim Taymans <wtaymans@redhat.com> - 2.0.8-6
- Disable vulkan on s390, s390x, aarch64 and ppc64le
- Resolves: rhbz#1610034

* Tue Jul 17 2018 Wim Taymans <wtaymans@redhat.com> - 2.0.8-5
- Disable obsolete audiofile-devel BR (#1588283)

* Wed Apr 11 2018 Tom Callaway <spot@fedoraproject.org> - 2.0.8-4
- enable video-kmsdrm

* Fri Mar 30 2018 David Abdurachmanov <david.abdurachmanov@gmail.com> - 2.0.8-3
- Add riscv64 to SDL_config.h

* Sun Mar 04 2018 Miro Hrončok <mhroncok@redhat.com> - 2.0.8-2
- Disable altivec on ppc64le (RHBZ #1551338)

* Sun Mar  4 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2.0.8-1
- Update to 2.0.8

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 31 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.0.7-3
- Switch to %%ldconfig_scriptlets

* Sun Nov 05 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.0.7-2
- Fix IBus

* Tue Oct 24 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.0.7-1
- Update to 2.0.7

* Thu Oct 19 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.0.6-4
- Fully fix last overflow

* Wed Oct 11 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.0.6-3
- Fix potential overflow in surface allocation

* Thu Oct 05 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.0.6-2
- Fix invalid dbus arguments

* Sat Sep 23 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.0.6-1
- Update to 2.0.6

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 27 2017 Igor Gnatenko <ignatenko@redhat.com> - 2.0.5-3
- Fix NULL dereference (RHBZ #1416945)

* Wed Oct 26 2016 Dan Horák <dan[at]danny.cz> - 2.0.5-2
- fix FTBFS on ppc64/ppc64le

* Thu Oct 20 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.5-1
- Update to 2.0.5 (RHBZ #1387238)

* Mon Sep 05 2016 Kalev Lember <klember@redhat.com> - 2.0.4-9
- Backport Wayland fixes from upstream

* Sun Aug 14 2016 Igor Gnatenko <ignatenko@redhat.com> - 2.0.4-8
- Fix whitespaces in CMake file (RHBZ #1366868)

* Sun Jul 10 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.4-7
- Remove useless Requirements from -devel subpkg

* Sun Jul 10 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.4-6
- Add ibus support

* Sun Jul 10 2016 Joseph Mullally <jwmullally@gmail.com> - 2.0.4-5
- fix Wayland dynamic symbol loading (bz1354155)

* Thu Feb 25 2016 Tom Callaway <spot@fedoraproject.org> - 2.0.4-4
- enable static subpackage (bz1253930)

* Fri Feb  5 2016 Tom Callaway <spot@fedoraproject.org> - 2.0.4-3
- fix compile against latest wayland

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 04 2016 Tom Callaway <spot@fedoraproject.org> - 2.0.4-1
- update to 2.0.4

* Fri Sep 04 2015 Michal Toman <mtoman@fedoraproject.org> - 2.0.3-7
- Add support for MIPS architecture to SDL_config.h

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun  2 2015 Tom Callaway <spot@fedoraproject.org> - 2.0.3-5
- remove code preventing builds with ancient gcc

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jun 11 2014 Karsten Hopp <karsten@redhat.com> 2.0.3-3
- fix filename of SDL_config.h for ppc64le

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 19 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.3-1
- 2.0.3 upstream release

* Sat Mar 08 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.2-1
- 2.0.2 upstream release
- Enable wayland backend

* Tue Dec 10 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.1-2
- Add libXinerama, libudev, libXcursor support (RHBZ #1039702)

* Thu Oct 24 2013 Tom Callaway <spot@fedoraproject.org> - 2.0.1-1
- update to 2.0.1

* Sat Aug 24 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.0-3
- Fix multilib issues

* Tue Aug 13 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.0-2
- SDL2 is released. Announce:
- http://lists.libsdl.org/pipermail/sdl-libsdl.org/2013-August/089854.html

* Sat Aug 10 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.0-1.rc4
- Update to latest SDL2 (08.08.2013)

* Tue Jul 30 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.0-1.rc3
- Fix Licenses
- some cleanups in spec

* Tue Jul 30 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.0-1.rc2
- Delete -static package
- Fix License tag
- Fix end-of-line in documents
- Remove all spike-nails EL-specify (if someone will want to do - 'patches are welcome')
- Change Release tag to .rcX%%{?dist} (maintainer has changed released tarballs)

* Mon Jul 29 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.0-1.rc1
- Some fixes in spec and cleanup

* Mon Jul 29 2013 Jon Ciesla <limburgher@gmail.com> - 2.0.0-1
- Ported from SDL 1.2.15-10
