#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	aeson-pretty
Summary:	JSON pretty-printing library and command-line tool
Name:		ghc-%{pkgname}
Version:	0.8.8
Release:	1
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/aeson-pretty
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	2c323511f2ce49171a6312b579f73ef2
URL:		http://hackage.haskell.org/package/aeson-pretty
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-aeson
BuildRequires:	ghc-scientific
BuildRequires:	ghc-vector
%if %{with prof}
BuildRequires:	ghc-prof
BuildRequires:	ghc-aeson-prof
BuildRequires:	ghc-scientific-prof
BuildRequires:	ghc-vector-prof
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires(post,postun):	/usr/bin/ghc-pkg
Requires:	ghc-aeson
BuildRequires:	ghc-scientific
BuildRequires:	ghc-vector
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
A JSON pretty-printing library compatible with aeson as well as a
command-line tool to improve readabilty of streams of JSON data.

The library provides the function "encodePretty". It is a drop-in
replacement for aeson's "encode" function, producing JSON-ByteStrings
for human readers.

The command-line tool reads JSON from stdin and writes prettified JSON
to stdout. It also offers a complementary "compact"-mode, essentially
the opposite of pretty-printing. If you specify -flib-only like this

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-aeson-prof
BuildRequires:	ghc-scientific-prof
BuildRequires:	ghc-vector-prof

%description prof
Profiling %{pkgname} library for GHC.  Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc README.markdown %{name}-%{version}-doc/*
%attr(755,root,root) %{_bindir}/aeson-pretty
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a

%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Aeson
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Aeson/Encode
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Aeson/Encode/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Aeson/Encode/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Aeson/Encode/*.p_hi
%endif
