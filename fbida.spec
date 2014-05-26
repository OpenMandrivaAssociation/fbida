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
BuildRequires:	pkgconfig(freetype2)
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

