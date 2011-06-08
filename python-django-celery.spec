#
# Conditional build:
%bcond_without	tests	# do not perform "make test"

%define 	module	django-celery
Summary:	-
Name:		python-%module
Version:	2.2.4
Release:	0.1
License:	BSD
Group:		Development/Languages
URL:		http://code.google.com/p/%{module}/
Source0:	http://pypi.python.org/packages/source/d/%{module}/%{module}-%{version}.tar.gz
# Source0-md5:	08ea1ce14af8a09c8eeae7fcfcaefaae
#BuildRequires:	python-coverage
#BuildRequires:	python-devel
BuildRequires:	python-django
#BuildRequires:	python-nose
#BuildRequires:	python-pyflakes
#BuildRequires:	python-setuptools
#BuildRequires:	python-sqlite
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	sed >= 4.0
Requires:	python-django
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
When you run ./manage.py syncdb, Django will look for any new models
that have been defined, and add a database table to represent those
new models. However, if you make a change to an existing model,
./manage.py syncdb will not make any changes to the database.

This is where Django Evolution fits in. Django Evolution is an
extension to Django that allows you to track changes in your models
over time, and to update the database to reflect those changes.

%prep
%setup -q -n %{module}-%{version}
%{__sed} -i -e 's/^from ez_setup/#from ez_setup/' setup.py
%{__sed} -i -e 's/^use_setuptools()/#use_setuptools()/' setup.py

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
%{py_sitescriptdir}/%{module}
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/%{module}-%{version}-*.egg-info
%endif
