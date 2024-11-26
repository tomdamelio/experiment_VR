import pkg_resources

installed_packages = pkg_resources.working_set
packages_list = sorted(["%s==%s" % (i.key, i.version) for i in installed_packages])
for package in packages_list:
    print(package)