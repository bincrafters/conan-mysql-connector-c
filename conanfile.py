#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import glob
import os



class MysqlConnectorCConan(ConanFile):
    name = "mysql-connector-c"
    version = "6.1.11"
    url = "https://github.com/bincrafters/conan-mysql-connector-c"
    description = "A MySQL client library for C development."
    topics = ("conan", "mysql", "sql", "connector", "database")
    homepage = "https://dev.mysql.com/downloads/connector/c/"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "GPL-2.0"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt", "patches/*.patch"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False],
               "with_ssl": [True, False],
               "with_zlib": [True, False]}
    default_options = {'shared': False,
                       'with_ssl': True,
                       'with_zlib': True}
    _source_subfolder = "source_subfolder"

    def requirements(self):
        if self.options.with_ssl:
            self.requires.add("OpenSSL/1.1.1a@conan/stable")

        if self.options.with_zlib:
            self.requires.add("zlib/1.2.11@conan/stable")

    def source(self):
        sha256 = "c8664851487200162b38b6f3c8db69850bd4f0e4c5ff5a6d161dbfb5cb76b6c4"
        source_url = "http://dev.mysql.com/get/Downloads/Connector-C"
        archive_name = self.name + "-" + self.version + "-src"
        ext = "tar.gz"
        tools.get("{0}/{1}.{2}".format(source_url, archive_name, ext), sha256=sha256)
        os.rename(archive_name, self._source_subfolder)

        sources_cmake = os.path.join(self._source_subfolder, "CMakeLists.txt")
        sources_cmake_orig = os.path.join(self._source_subfolder, "CMakeListsOriginal.txt")

        os.rename(sources_cmake, sources_cmake_orig)
        os.rename("CMakeLists.txt", sources_cmake)

    def build(self):
        for filename in glob.glob("patches/*.patch"):
            self.output.info('applying patch "%s"' % filename)
            tools.patch(base_path=self._source_subfolder, patch_file=filename)

        cmake = CMake(self)

        cmake.definitions["DISABLE_SHARED"] = not self.options.shared
        cmake.definitions["DISABLE_STATIC"] = self.options.shared

        if self.settings.compiler == "Visual Studio":
            if self.settings.compiler.runtime == "MD" or self.settings.compiler.runtime == "MDd":
                cmake.definitions["WINDOWS_RUNTIME_MD"] = True

        if self.options.with_ssl:
            cmake.definitions["WITH_SSL"] = "system"

        if self.options.with_zlib:
            cmake.definitions["WITH_ZLIB"] = "system"

        cmake.configure(source_dir=self._source_subfolder)
        cmake.build()
        cmake.install()

    def package(self):
        pass

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.bindirs = ['lib']
