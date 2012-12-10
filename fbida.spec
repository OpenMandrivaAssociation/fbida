Summary:	Collection of applications for viewing and editing images
Name:		fbida
Version:	2.09
Release:	2
License:	GPLv2+
Group:		Graphics
URL:		http://linux.bytesex.org/fbida/
Source0:	http://dl.bytesex.org/releases/fbida/%{name}-%{version}.tar.gz
# replace old copied jpeg headers from old libjpeg with new one from libjpeg8
# (c.f. the similar fix in mdv bug#57950)
Patch0:		fbida-2.07-replace-old-libjpeg-headers.patch
Patch1:		fbida-2.09-fmtstr.diff
Patch2:		fbida-2.09-no_strip.diff
Provides:	fbi
BuildRequires:	curl-devel
BuildRequires:	freetype2-devel
BuildRequires:	jpeg-devel
BuildRequires:	libexif-devel
BuildRequires:	libpcd-devel
BuildRequires:	lirc-devel
BuildRequires:	png-devel
BuildRequires:	sane-devel
BuildRequires:	tiff-devel
BuildRequires:	ungif-devel
BuildRequires:	lesstif-devel
BuildRequires:	xpm-devel
BuildRequires:	libxext-devel
BuildRequires:	x11-server-common
BuildRequires:	fontconfig-devel
# fwang: the app needs /etc/X11/app-defaults
BuildRequires:	xsysinfo
# fbi uses convert to show indirectly supported image format
Requires:	imagemagick
# fbgs requires gs
Requires:	ghostscript
Requires:	exiftran = %{version}

%description
The fbida project contains a few applications for viewing and editing
images, with the main focus being photos. The applications are:

fbi	- Image viewer for Linux framebuffer console
fbgs	- Wrapper script using fbi, for viewing ps/pdf files on framebuffer
ida	- X11 application (Motif based) for viewing images with
	basic editing functions
exiftran- command line tool to do lossless transformations of JPEG
	images, similar to jpegtran but includes EXIF data
thumbnail.cgi - CGI script to extract EXIF thumbnails from jpeg images
	 and send them to web browser

This project used to be 2 seperate projects (fbi and ida), but later
merged by author.

%package -n	exiftran
Summary:	Transform Digital Camera JPEG Images
Group:		Graphics
Conflicts:	fbida < 2.09

%description -n	exiftran
exiftran is a command-line utility to transform digital image JPEG
images. It can do lossless rotations like jpegtran, but unlike
jpegtran, it cares about the EXIF data.  It can rotate images
automatically by checking the EXIF orientation tag, updating the EXIF
information if needed (image dimension, orientation), and also rotating
the EXIF thumbnail. It can process multiple images at once.

%prep

%setup -q
%patch0 -p1 -b .oldjpeg
%patch1 -p0 -b .fmtstr
%patch2 -p0 -b .no_strip
rm -f jpeg/*/jpeg*

%build
# Must use CFLAGS as env variable, because makefile adds flags to it.
# Directly specifying CFLAGS as make variable would fail
export CFLAGS="%optflags"
%make verbose=yes

%install

%makeinstall_std prefix=%{_prefix}

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop <<EOF
[Desktop Entry]
Name=IDA Image Viewer
Comment=Basic image viewer and editor
Exec=%{_bindir}/ida
Icon=graphics_section
Terminal=false
Type=Application
StartupNotify=true
Categories=Motif;Graphics;2DGraphics;RasterGraphics;Viewer;
EOF

%files
%doc Changes COPYING README
%config(noreplace) %{_sysconfdir}/X11/app-defaults/*
%{_bindir}/fbi
%{_bindir}/fbgs
%{_bindir}/ida
%{_datadir}/applications/mandriva-%{name}.desktop
%{_mandir}/man1/fbi.1*
%{_mandir}/man1/fbgs.1*
%{_mandir}/man1/ida.1*

%files -n exiftran
%{_bindir}/exiftran
%{_mandir}/man1/exiftran.1*


%changelog
* Thu Aug 30 2012 Dmitry Mikhirev <dmikhirev@mandriva.org> 2.09-2
+ Revision: 816054
- fix reqs

* Fri Jul 13 2012 Oden Eriksson <oeriksson@mandriva.com> 2.09-1
+ Revision: 809106
- 2.09
- split out exiftran
- various fixes

* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 2.07-5mdv2011.0
+ Revision: 610420
- rebuild

* Mon Mar 29 2010 Ahmad Samir <ahmadsamir@mandriva.org> 2.07-4mdv2010.1
+ Revision: 528921
- replace old copied jpeg headers from old libjpeg with new one from libjpeg8
  (c.f. the similar fix in mdv bug#57950), (fixes mdv bug#58212)

  + Sandro Cazzaniga <kharec@mandriva.org>
    - fix warnings and licence

* Wed Oct 07 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 2.07-3mdv2010.0
+ Revision: 455800
- rebuild for new curl SSL backend

* Thu Sep 10 2009 Funda Wang <fwang@mandriva.org> 2.07-2mdv2010.0
+ Revision: 436263
- fix compatibility with libjpeg v7

* Sat Aug 22 2009 Funda Wang <fwang@mandriva.org> 2.07-1mdv2010.0
+ Revision: 419486
- fix linkage

* Tue Feb 17 2009 Jérôme Soyer <saispo@mandriva.org> 2.07-1mdv2009.1
+ Revision: 341622
- Fix Requiers

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - kill re-definition of %%buildroot on Pixel's request
    - do not harcode icon extension
    - kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Wed Jul 18 2007 Adam Williamson <awilliamson@mandriva.org> 2.06-2mdv2008.0
+ Revision: 53338
- rebuild with new lesstif
- add menu entry for ida

* Sat May 26 2007 Funda Wang <fwang@mandriva.org> 2.06-1mdv2008.0
+ Revision: 31494
- BuildRequires fontconfig
- BuildRequires /etc/x11/app-defaults
- BuildRequires X11-devel
- Patch0 not needed
- New version 2.06
- bunzip2 the patches
- Import fbida



* Fri Jan 28 2005 Abel Cheung <deaddog@mandrake.org> 2.03-1mdk
- New version, obsoletes fbi
- Redo P0 (partially fixed upstream), only change it to use mktemp
- P1: Add -r switch for fbgs to support any user specified resolution

* Wed Nov 17 2004 Abel Cheung <deaddog@mandrake.org> 1.31-4mdk
- Add missing BuildRequires
- Patch0: Fix fbgs and make it use mktemp

* Fri Jul 02 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 1.31-3mdk
- Rebuild 

* Wed May 19 2004 Michael Scherer <misc@mandrake.org> 1.31-2mdk 
- update Url, thanks to Eskild Hustvedt

* Tue May 18 2004 Michael Scherer <misc@mandrake.org> 1.31-1mdk
- New release 1.31
- rpmbuildupdate aware

* Wed Dec 03 2003 Abel Cheung <deaddog@deaddog.org> 1.28-2mdk
- Rebuild against libpcd for PhotoCD support
- Remove bogus post/preun scriptlets (sorry)

* Mon Dec 01 2003 Abel Cheung <deaddog@deaddog.org> 1.28-1mdk
- First Mandrake package, based on spec from source
