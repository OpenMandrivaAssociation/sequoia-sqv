%global debug_package %{nil}

%define libname %mklibname sequoia-sqv

Name:		sequoia-sqv
Version:	1.3.0
Release:	1
Source0:	https://gitlab.com/sequoia-pgp/sequoia-sqv/-/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:    %{name}-%{version}-vendor.tar.gz
Summary:	A simple signature verification program
URL:		https://gitlab.com/sequoia-pgp/sequoia-sqv
License:	GPL-2
Group:		System/Libraries
BuildRequires:	cargo
BuildRequires:	pkgconfig(nettle)
BuildRequires:	pkgconfig(gmp)

%description
%summary

%package -n %{libname}
Summary:    %summary
Group:      System/Libraries
Provides:   %{libname} = %{EVRD}

%description -n %{libname}
%summary

%prep
%autosetup -n %{name}-v%{version}-aef381070150a5bc076d178017bc4d375834fc11 -p1
tar -zxf %{SOURCE1}
mkdir -p .cargo
cat >> .cargo/config.toml << EOF
[source.crates-io]
replace-with = "vendored-sources"

[source."git+https://github.com/SoftbearStudios/bitcode.git?rev=5f25a59"]
git = "https://github.com/SoftbearStudios/bitcode.git"
rev = "5f25a59"
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"

EOF

%build
cargo build --release --frozen --features 'crypto-nettle'

%install
install -Dm 755 target/release/sqv -t %{buildroot}%{_bindir}/
install -Dm 644 target/release/build/sequoia-sqv-65cb67d5b438c143/out/shell-completions/sqv.bash %{buildroot}/%{_datadir}/bash-completion/completions/sqv.bash
install -Dm 644 target/release/build/sequoia-sqv-65cb67d5b438c143/out/shell-completions/_sqv %{buildroot}/%{_datadir}/zsh/site-functions/_sqv
install -Dm 644 target/release/build/sequoia-sqv-65cb67d5b438c143/out/shell-completions/sqv.fish %{buildroot}/%{_datadir}/fish/vendor_completions.d/sqv.fish
install -Dm 644 target/release/build/sequoia-sqv-65cb67d5b438c143/out/man-pages/sqv.1 %{buildroot}/%{_mandir}/sqv.1
 install -Dm 644 README.md %{buildroot}%{_datadir}/doc/%{name}/README.md

%files -n %{libname}
%{_bindir}/sqv
%{_datadir}/bash-completion/completions/*
%{_datadir}/fish/vendor_completions.d/*
%{_datadir}/zsh/site-functions/*
%{_mandir}/sqv.1
%{_datadir}/doc*
