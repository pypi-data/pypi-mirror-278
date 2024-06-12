import os
import shutil
import subprocess  # nosec

import click


_THIS_DIR = os.path.abspath(os.path.dirname(__file__))


@click.command()
def cli():
    """Install configuration files, IPython extensions, Jupyter extensions,
    and JavaScript/CSS assets for using a Docker image with Civis Platform
    Jupyter notebooks.
    """

    # make home areas and dirs
    for dr in [
        ("~", "work"),
        ("~", ".jupyter", "custom"),
        # folder that holds all the JS for notebook frontend extensions
        ("~", ".jupyter", "extensions"),
        ("~", ".jupyter", "custom", "fonts"),
        ("~", ".ipython", "profile_default"),
    ]:
        try:
            os.makedirs(os.path.expanduser(os.path.join(*dr)))
        except OSError:
            pass

    # enable civisjupyter extension
    for cmd in [
        "jupyter nbextension install --py civis_jupyter_ext",
        "jupyter nbextension enable --py civis_jupyter_ext",
    ]:
        subprocess.check_call(cmd, shell=True)  # nosec

    # copy code
    def _copy(src, dst):
        src = os.path.join(_THIS_DIR, *src)
        dst = os.path.expanduser(os.path.join(*dst))
        shutil.copy(src, dst)

    _copy(("assets", "jupyter_notebook_config.py"), ("~", ".jupyter"))
    _copy(("assets", "custom.css"), ("~", ".jupyter", "custom"))
    _copy(("assets", "custom.js"), ("~", ".jupyter", "custom"))
    for ext in ["eot", "woff", "svg", "ttf"]:
        _copy(
            ("assets", "fonts", "civicons.%s" % ext),
            ("~", ".jupyter", "custom", "fonts"),
        )
    _copy(("assets", ".bashrc"), ("~"))
    _copy(("assets", "ipython_config.py"), ("~", ".ipython", "profile_default"))
    _copy(("assets", "civis_client_config.py"), ("~", ".ipython"))

    # copy frontend extensions
    frontend_extensions = os.listdir(os.path.join(_THIS_DIR, "assets", "extensions"))
    for fe_ext in frontend_extensions:
        _copy(("assets", "extensions", fe_ext), ("~", ".jupyter", "extensions"))

    # install and enable nbextensions
    subprocess.check_call(
        "jupyter nbextension install ~/.jupyter/extensions", shell=True
    )  # nosec
    for extension in frontend_extensions:
        ext_name = os.path.splitext(extension)[0]
        cmd = "jupyter nbextension enable extensions/{}".format(ext_name)
        subprocess.check_call(cmd, shell=True)  # nosec
