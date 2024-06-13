from conan import ConanFile


class DeployConan(ConanFile):
    name = "deploy"
    settings = "os", "arch", "compiler", "build_type"
    description = "部署组件"
    url = "https://litebmc.com"
    homepage = ""
    generators = "CMakeDeps"
    package_type = "application"
    version = "0.0.1"
    license = "MulanPSL v2"

    def requirements(self):
    % for package in packages:
        self.requires("${package}")
    % endfor
        pass

    def configure(self):
% if len(pkg.get("requires", {})) > 0:
    % for conan in pkg["requires"].get("compile", []):
        % if conan.get("option") is not None:
            % for k, v in conan.get("option").items():
        self.options["${conan.get("conan").split("/")[0]}"].${k} = ${("\"" + v + "\"") if isinstance(v, str) else str(v)}
            % endfor
        % endif
    % endfor
<%test_requires=pkg["requires"].get("test", [])%>\
    % if len(test_requires):
        % for conan in test_requires:
            % if conan.get("option") is not None:
                % for k, v in conan.get("option").items():
        self.options["${conan.get("conan").split("/")[0]}"].${k} = ${("\"" + v + "\"") if isinstance(v, str) else str(v)}
                % endfor
            % endif
        % endfor
    % endif
% endif
        pass

