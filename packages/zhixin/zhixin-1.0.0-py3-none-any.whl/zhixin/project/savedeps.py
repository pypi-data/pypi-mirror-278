import os

from zhixin.compat import ci_strings_are_equal
from zhixin.package.meta import PackageSpec
from zhixin.project.config import ProjectConfig
from zhixin.project.exception import InvalidProjectConfError


def pkg_to_save_spec(pkg, user_spec):
    assert isinstance(user_spec, PackageSpec)
    if user_spec.external:
        return user_spec
    return PackageSpec(
        owner=pkg.metadata.spec.owner,
        name=pkg.metadata.spec.name,
        requirements=user_spec.requirements
        or (
            ("^%s" % pkg.metadata.version)
            if not pkg.metadata.version.build
            else pkg.metadata.version
        ),
    )


def save_project_dependencies(
    project_dir, specs, scope, action="add", environments=None
):
    config = ProjectConfig.get_instance(os.path.join(project_dir, "zhixin.ini"))
    config.validate(environments)
    for env in config.envs():
        if environments and env not in environments:
            continue
        config.expand_interpolations = False
        candidates = []
        try:
            candidates = _ignore_deps_by_specs(config.get("env:" + env, scope), specs)
        except InvalidProjectConfError:
            pass
        if action == "add":
            candidates.extend(spec.as_dependency() for spec in specs)
        if candidates:
            result = []
            for item in candidates:
                item = item.strip()
                if item and item not in result:
                    result.append(item)
            config.set("env:" + env, scope, result)
        elif config.has_option("env:" + env, scope):
            config.remove_option("env:" + env, scope)
    config.save()


def _ignore_deps_by_specs(deps, specs):
    result = []
    for dep in deps:
        ignore_conditions = []
        depspec = PackageSpec(dep)
        if depspec.external:
            ignore_conditions.append(depspec in specs)
        else:
            for spec in specs:
                if depspec.owner:
                    ignore_conditions.append(
                        ci_strings_are_equal(depspec.owner, spec.owner)
                        and ci_strings_are_equal(depspec.name, spec.name)
                    )
                else:
                    ignore_conditions.append(
                        ci_strings_are_equal(depspec.name, spec.name)
                    )
        if not any(ignore_conditions):
            result.append(dep)
    return result
