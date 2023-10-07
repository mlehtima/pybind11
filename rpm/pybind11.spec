# While the headers are architecture independent, the package must be
# built separately on all architectures so that the tests are run
# properly. See also
# https://fedoraproject.org/wiki/Packaging:Guidelines#Packaging_Header_Only_Libraries
%global debug_package %{nil}

Name:    pybind11
Version: 2.9.2
Release: 1
Summary: Seamless operability between C++11 and Python
License: BSD
URL:	 https://github.com/pybind/pybind11
Source0: %{name}-%{version}.tar.gz

# Patch out header path
#Patch1:  pybind11-2.8.1-hpath.patch

BuildRequires: make

# Needed to build the python libraries
BuildRequires: python3-devel
BuildRequires: python3-setuptools

#BuildRequires: eigen3-devel
BuildRequires: gcc-c++
BuildRequires: cmake

%global base_description \
pybind11 is a lightweight header-only library that exposes C++ types \
in Python and vice versa, mainly to create Python bindings of existing \
C++ code.

%description
%{base_description}

%package devel
Summary:  Development headers for pybind11
# https://fedoraproject.org/wiki/Packaging:Guidelines#Packaging_Header_Only_Libraries
Provides: %{name}-static = %{version}-%{release}
# For dir ownership
Requires: cmake

%description devel
%{base_description}

This package contains the development headers for pybind11.

%package -n     python3-%{name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-pybind11}

Requires: %{name}-devel%{?_isa} = %{version}-%{release}

%description -n python3-%{name}
%{base_description}

This package contains the Python 3 files.

%prep
%autosetup -p1 -n %{name}-%{version}/%{name}
#patch1 -p1 -b .hpath

%build
mkdir -p python3
# When -DCMAKE_BUILD_TYPE is set to Release, the tests in %%check might segfault.
# However, we do not ship any binaries, and therefore Debug
# build type does not affect the results.
# https://bugzilla.redhat.com/show_bug.cgi?id=1921199
%cmake -B python3 -DCMAKE_BUILD_TYPE=Debug -DPYTHON_EXECUTABLE=%{_bindir}/python3 -DPYBIND11_INSTALL=TRUE -DUSE_PYTHON_INCLUDE_DIR=FALSE %{!?with_tests:-DPYBIND11_TEST=OFF}
%make_build -C python3

%py3_build

%install
make DESTDIR=%{buildroot} INSTALL_ROOT=%{buildroot} install -C python3
PYBIND11_USE_CMAKE=true %py3_install "--install-purelib" "%{python3_sitearch}"

%files devel
%license LICENSE
%doc README.rst
%{_includedir}/pybind11/
%{_datadir}/cmake/pybind11/
%{_bindir}/pybind11-config

%files -n python3-%{name}
%{python3_sitearch}/%{name}/
%{python3_sitearch}/%{name}-*-py%{python3_version}.egg-info/
