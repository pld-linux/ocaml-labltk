#
# Conditional build:
%bcond_without	ocaml_opt	# build opt

%ifnarch %{ix86} %{x8664} arm aarch64 ppc sparc sparcv9 
%undefine	with_ocaml_opt
%endif

%define		module	labltk
Summary:	Runtime for LablTk library
Summary(pl.UTF-8):	Środowisko uruchomieniowe dla biblioteki LablTk
Name:		ocaml-labltk
Version:	8.06.10
Release:	2
Epoch:		1
License:	LGPL v2 with linking exception
Group:		Libraries
Source0:	https://github.com/garrigue/labltk/archive/%{version}/labltk-%{version}.tar.gz
# Source0-md5:	d6b4691bb03b114d45411158143883d7
Patch0:		%{name}-CFLAGS.patch
URL:		https://github.com/garrigue/labltk
BuildRequires:	ocaml >= 1:4.02
BuildRequires:	tk-devel >= 8.2
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		debug_package	%{nil}

%description
LablTk gives OCaml program access to Tcl/Tk GUI widgets. This package
contains files needed to run bytecode OCaml programs using LablTk.

%description -l pl.UTF-8
Biblioteka LablTk daje programom napisanym w OCamlu dostęp do widgetów
Tcl/Tk. Pakiet ten zawiera binaria potrzebne do uruchamiania programów
używających LablTk.

%package devel
Summary:	LablTk library for OCaml
Summary(pl.UTF-8):	Biblioteka LablTk dla OCamla
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
%requires_eq	ocaml
Conflicts:	ocaml-findlib < 1.5.5

%description devel
LablTk gives OCaml program access to Tcl/Tk GUI widgets. This package
contains files needed to develop OCaml programs using LablTk.

%description devel -l pl.UTF-8
Biblioteka LablTk daje programom napisanym w OCamlu dostęp do widgetów
Tcl/Tk. Pakiet ten zawiera pliki niezbędne do tworzenia programów
używających LablTk.

%package examples
Summary:	Example OCaml source code for LablTk
Summary(pl.UTF-8):	Przykładowe kody źródłowe w OCamlu dla LablTk
Group:		Development/Languages
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description examples
Example OCaml source code for LablTk.

%description examples -l pl.UTF-8
Przykładowe kody źródłowe w OCamlu dla LablTk.

%prep
%setup -q -n labltk-%{version}
%patch0 -p1

%build
./configure

%{__make} -j1 all %{?with_ocaml_opt:opt} \
	CCFLAGS="%{rpmcflags} -Wall"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/ocaml/stublibs,%{_examplesdir}/%{name}-%{version}}

%{__make} install \
	BINDIR=$RPM_BUILD_ROOT%{_bindir} \
	LIBDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml \
	STUBLIBDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs \
	MANDIR=$RPM_BUILD_ROOT%{_mandir}

cp -r examples* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/labltk/{labltktop,pp}

cp -p support/META $RPM_BUILD_ROOT%{_libdir}/ocaml/labltk

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes README.mlTk
%attr(755,root,root) %{_libdir}/ocaml/stublibs/dlllabltk.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/labltk
%attr(755,root,root) %{_bindir}/ocamlbrowser
%dir %{_libdir}/ocaml/labltk
%{_libdir}/ocaml/labltk/META
%{_libdir}/ocaml/labltk/*.mli
%{_libdir}/ocaml/labltk/*.cma
%{_libdir}/ocaml/labltk/*.cmi
%{_libdir}/ocaml/labltk/*.cmo
%{_libdir}/ocaml/labltk/liblabltk.a
%if %{with ocaml_opt}
%{_libdir}/ocaml/labltk/*.cmx
%{_libdir}/ocaml/labltk/frxlib.a
%{_libdir}/ocaml/labltk/frxlib.cmxa
%{_libdir}/ocaml/labltk/jpflib.a
%{_libdir}/ocaml/labltk/jpflib.cmxa
%{_libdir}/ocaml/labltk/labltk.a
%{_libdir}/ocaml/labltk/labltk.cmxa
%endif
%attr(755,root,root) %{_libdir}/ocaml/labltk/tkcompiler
%{_examplesdir}/%{name}-%{version}
