#!/usr/bin/env python3.5

import os
import sys
import subprocess
import glob


os.putenv("LANG", "C")

TMP_DIR = "/tmp/debian-moon"
INIT_dir = os.path.split(os.path.abspath(sys.argv[0]))[0]

print("init dir: {}".format(INIT_dir))

_run = subprocess.run(["mkdir", "-p", TMP_DIR])
if _run.returncode != 0:
    exit("\033[31mCannot create tmp dir\033[m")

os.chdir(TMP_DIR)

_run = subprocess.run(["sudo", "-E", "apt-get", "install", "-y", "git"])
if _run.returncode != 0:
    exit("\033[31mCannot install Git\033[m")

print("\033[32mCloning Debian version\033[m")
_run = subprocess.run(["git", "clone", "https://anonscm.debian.org/git/openstack/keystone.git"])
if _run.returncode != 0:
    os.chdir(os.path.join(TMP_DIR, "keystone"))
    _run = subprocess.run(["git", "pull"])
    if _run.returncode != 0:
        print("\033[31mCannot clone ou pull debian version\033[m")

os.chdir(TMP_DIR)

print("\033[32mCloning Moon project\033[m")
_run = subprocess.run(["git", "clone", "https://git.opnfv.org/moon"])
if _run.returncode != 0:
    os.chdir(os.path.join(TMP_DIR, "moon"))
    _run = subprocess.run(["git", "pull"])
    if _run.returncode != 0:
        print("\033[31mCannot clone Moon project\033[m")

os.chdir(TMP_DIR)

_run = subprocess.run(["cp",
                       "-r",
                       os.path.join(TMP_DIR, "keystone", "debian"),
                       os.path.join(TMP_DIR, "moon", "keystone-moon")])

print("\033[32mBuilding Moon project\033[m")
os.chdir(os.path.join(TMP_DIR, "moon", "keystone-moon"))

mandatory_deb_pkg = """dh-apparmor 
dh-systemd 
openstack-pkg-tools 
python-all python-pbr 
python-sphinx
python-bashate
python-keystonemiddleware
python-ldap
python-ldappool
python-memcache
python-migrate
python-mock
python-msgpack
python-oslo.cache
python-oslo.concurrency
python-oslo.config
python-oslo.context
python-oslo.db
python-oslo.i18n
python-oslo.log
python-oslo.messaging
python-oslo.policy
python-oslo.serialization
python-oslo.service
python-oslo.utils
python-oslosphinx
python-oslotest
python-os-testr
python-passlib
python-paste
python-pastedeploy
python-pycadf
python-pymongo
python-pysaml2
python-pysqlite2
python-routes
python-sqlalchemy
python-stevedore
python-testscenarios
python-testtools
python-unittest2
python-webob
python-webtest
subunit
testrepository
python-coverage
python-dogpile.cache
python-eventlet
python-hacking
python-oslo.cache
python-oslo.concurrency
python-oslo.config
python-oslo.db
python-oslo.log
python-oslo.messaging
python-oslo.middleware
python-tempest-lib
python-oauthlib
python-pam"""

_command = ["sudo", "-E", "apt-get", "install", "-y"]
_command.extend(mandatory_deb_pkg.split())
_run = subprocess.run(_command)

os.putenv("DEB_BUILD_OPTIONS", "nocheck")

changelog = open(os.path.join(TMP_DIR, "moon", "keystone-moon", "debian", "changelog"), "rt")
changelog_str = changelog.read()
# print(changelog_str.splitlines()[0])
current_version = changelog_str.splitlines()[0].split("(")[1].split(")")[0]
changelog.close()
changelog = open(os.path.join(TMP_DIR, "moon", "keystone-moon", "debian", "changelog"), "wt")
changelog.write("""keystone ({version}) UNRELEASED; urgency=medium

  * integration of the Moon platform.

 -- Thomas Duval <thomas.duval@orange.com>  {date}

""".format(
    version=current_version+"-moon",
    date=subprocess.Popen(["date"], stdin=None, stdout=subprocess.PIPE).communicate()[0].decode("utf-8").strip()))
changelog.write(changelog_str)
changelog.close()

keystone_install_file = open(os.path.join(TMP_DIR, "moon", "keystone-moon", "debian", "keystone.install"), "a")
keystone_install_file.write("etc/policies         /etc/keystone\n")


# _run = subprocess.run(["dpkg-buildpackage", "-b", "-us"])
_run = subprocess.run(["dpkg-buildpackage", "-b", "-us"])

print("\033[32mResults:\033[m")
subprocess.run(["pwd", ])
subprocess.run(["mkdir", "-p", "/tmp/deb"])

files = glob.glob(os.path.join(TMP_DIR, "moon", "*.deb"))
for _file in files:
    subprocess.run(["mv", "-v", _file, "/tmp/deb/"])
