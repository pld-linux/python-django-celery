#
# Conditional build:
%bcond_without	tests	# do not perform "make test"

%define 	module	django-celery
Summary:	django-celery provides Celery intergration for Django
Name:		python-%module
Version:	2.4.2
Release:	0.9
License:	BSD
Group:		Development/Languages
URL:		http://code.google.com/p/%{module}/
Source0:	http://pypi.python.org/packages/source/d/%{module}/%{module}-%{version}.tar.gz
# Source0-md5:	ac2e18cf0738b966d5bece53218e6423
BuildRequires:	python-modules
BuildRequires:	python-setuptools
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	sed >= 4.0
Requires:	python-django
Requires:	python-celery >= 2.4.2
Requires:	python-django-picklefield
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Provides Celery integration for Django; Using Django ORM and cache
backend for storing results, autodiscovery of task modules for
applications listed in INSTALLED_APPS, and more.

%prep
%setup -q -n %{module}-%{version}

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--optimize=2 \
	--skip-build \
	--root $RPM_BUILD_ROOT

%py_postclean

rm -rf $RPM_BUILD_ROOT%{py_sitescriptdir}/%{module}/tests
rm -rf $RPM_BUILD_ROOT%{py_sitescriptdir}/tests

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS LICENSE README docs
%attr(755,root,root)%{_bindir}/djcelerymon
%{py_sitescriptdir}/djcelery
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/django_celery-%{version}-*.egg-info/
%endif
