#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os, shutil

class MysqlConnectorCConan(ConanFile):
    name = "mysql-connector-c"
    version = "6.1.11"
    url = "https://github.com/bincrafters/conan-mysql-connector-c"
    description = "A MySQL client library for C development."
    license = "http://www.gnu.org/licenses/old-licenses/gpl-2.0.html"
    generators = "cmake"
    exports_sources = ["CMakeLists.txt", "LICENSE"]
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"

    def source(self):
        source_url = "http://dev.mysql.com/get/Downloads/Connector-C"
        archive_name = self.name + "-" + self.version + "-src"
        ext = "tar.gz"
        tools.get("{0}/{1}.{2}".format(source_url, archive_name, ext))
        os.rename(archive_name, "sources")
        
        sources_cmake = os.path.join("sources", "CMakeLists.txt")
        sources_cmake_orig = os.path.join("sources", "CMakeListsOriginal.txt")
        
        os.rename(sources_cmake, sources_cmake_orig)
        os.rename("CMakeLists.txt", sources_cmake)

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
        self.cpp_info.bindirs = ['lib']
