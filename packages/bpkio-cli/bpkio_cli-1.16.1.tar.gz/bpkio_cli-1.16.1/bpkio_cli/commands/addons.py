import os

from bpkio_cli.core.config_provider import CONFIG
import click
import cloup


plugin_folder = CONFIG.get("path", section="addons")


class AddonGroup(click.Group):
    def list_commands(self, ctx):
        if not os.path.isdir(plugin_folder):
            click.secho(f"Plugin folder {plugin_folder} does not exist", fg="red")
            return []

        rv = []
        for filename in os.listdir(plugin_folder):
            if filename.endswith(".py") and filename != "__init__.py":
                rv.append(filename[:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        ns = {}
        fn = os.path.join(plugin_folder, name + ".py")
        with open(fn) as f:
            code = compile(f.read(), fn, "exec")
            eval(code, ns, ns)
        return ns[name]


@cloup.command(cls=AddonGroup, help="Other functionality provided through plugins")
def addons():
    pass
