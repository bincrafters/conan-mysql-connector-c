#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os, shutil

class MysqlConnectorCConan(ConanFile):
    name = "mysql-connector-c"
    version = "6.1.11"
    url = "https://github.com/bincrafters/conan-mysql-connector-c"
    description = "Connector/C (libmysqlclient) is a MySQL client library for C development."
    license = "http://www.gnu.org/licenses/old-licenses/gpl-2.0.html"
    generators = "cmake", "txt"
    exports_sources = ["CMakeLists.txt", "LICENSE"]
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"

    def source(self):
        source_url = "http://dev.mysql.com/get/Downloads/Connector-C/"
        tools.get("{0}/mysql-connector-c-{1}-src.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version + "-src"
        os.rename(extracted_dir, "sources")
        shutil.move("sources/CMakeLists.txt", "sources/CMakeListsOriginal.cmake")
        shutil.copy("CMakeLists.txt", "sources/CMakeLists.txt")

    def build(self):
        cmake = CMake(self)

        if self.options.shared:
            cmake.definitions["DISABLE_SHARED"] = "OFF"
            cmake.definitions["DISABLE_STATIC"] = "ON"
        else:
            cmake.definitions["DISABLE_SHARED"] = "ON"
            cmake.definitions["DISABLE_STATIC"] = "OFF"

        if self.settings.compiler == "Visual Studio":
            if self.settings.compiler.runtime == "MD" or self.settings.compiler.runtime == "MDd":
                cmake.definitions["WINDOWS_RUNTIME_MD"] = "ON"

        cmake.configure(source_dir="sources")
        cmake.build()
        cmake.install()

    def package(self):
        pass

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
