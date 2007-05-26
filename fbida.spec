%define version 2.06
%define release %mkrel 1

Summary:	Collection of applications for viewing and editing images
Name:		fbida
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
#BuildRequires:	XFree86-devel
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
BuildRequires:	X11-devel
# fbi uses convert to show indirectly supported image format
Requires:	ImageMagick
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

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc Changes COPYING README
%config(noreplace) %{_sysconfdir}/X11/app-defaults/*
%{_bindir}/*
%{_mandir}/man1/*
