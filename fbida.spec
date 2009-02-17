%define Werror_cflags %nil

%define name	fbida
%define version 2.07
%define release %mkrel 1

Summary:	Collection of applications for viewing and editing images
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Graphics
URL:		http://linux.bytesex.org/fbida/
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Source:		http://dl.bytesex.org/releases/fbida/%{name}-%{version}.tar.bz2
Patch1:		fbida-2.03-fbgs-arbitrary-resolution.patch
Obsoletes:	fbi
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
BuildRequires: 	fontconfig-devel
# fwang: the app needs /etc/X11/app-defaults
BuildRequires:	xsysinfo
# fbi uses convert to show indirectly supported image format
Requires:	imagemagick
# fbgs requires gs
Requires:	ghostscript

%description
The fbida project contains a few applications for viewing and editing
images, with the main focus being photos. The applications are:

fbi      - Image viewer for Linux framebuffer console
fbgs     - Wrapper script using fbi, for viewing ps/pdf files on framebuffer
ida      - X11 application (Motif based) for viewing images with
           basic editing functions
exiftran - command line tool to do lossless transformations of JPEG
           images, similar to jpegtran but includes EXIF data
thumbnail.cgi - CGI script to extract EXIF thumbnails from jpeg images
                and send them to web browser

This project used to be 2 seperate projects (fbi and ida), but later
merged by author.

%prep
%setup -q
%patch1 -p1 -b .resolution

%build
# Must use CFLAGS as env variable, because makefile adds flags to it.
# Directly specifying CFLAGS as make variable would fail
export CFLAGS="%optflags"
%make verbose=yes

%install
rm -rf %{buildroot}
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

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc Changes COPYING README
%config(noreplace) %{_sysconfdir}/X11/app-defaults/*
%{_bindir}/*
%{_datadir}/applications/mandriva-%{name}.desktop
%{_mandir}/man1/*
