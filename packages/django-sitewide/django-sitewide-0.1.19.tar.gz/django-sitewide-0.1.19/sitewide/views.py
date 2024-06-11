"""Sitewide Classes"""

import os
import tomllib

from django.views.generic import TemplateView
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from accounts.models import User
from .models import Setting

__ELEMENTS__ = []
__BASEATTRS__ = ["allow", "show"]
__MGRS__ = ["columns", "menus", "rows"]
__MGRATTRS__ = {
    "menus": ["icon", "id", "menus", "output", "url"], 
    "columns": ["id", "image","output", "rows", "url"],
    "rows": ["columns", "id", "image","output", "url"],
}
__PARTS__ = ["layout", "sidebar", "header", "footer"]
__PARTATTRS__ = {
    "layout": [
        "favicon",
        "footer",
        "header",
        "home",
        "image",
        "project",
        "settings",
        "sidebar",
        "user",
    ],
    "sidebar": ["state", "menus"],
    "header": ["icon", "menus"],
    "footer": ["columns", "rows"]
}

__DEFAULTS__ = {"home": "/", "show": True, "state": "sidebar_show"}


def get_attrs(part):
    """Return attributes associated with specified Sitewide Part"""
    if part in __PARTS__:
        return __BASEATTRS__ + __PARTATTRS__.get(part, [])
    if part in __MGRS__:
        return __BASEATTRS__ + __MGRATTRS__.get(part, [])
    raise AttributeError(f"Unrecognized Part: {part}")


def get_config():
    """Return the absolute path of a configuration file if the file exists.
    Otherwise return a default path"""

    default = "sitewide.toml"
    project_config_path = "/static/production/sitewide.toml"
    abspath = os.path.join(
        settings.BASE_DIR,
        project_config_path.lstrip(os.path.sep),
    )
    with open(abspath if os.path.exists(abspath) else default, "rb") as file:
        return tomllib.load(file)


def get_default(attr):
    """Return the default value of a specified attribute"""

    if attr in __DEFAULTS__:
        return __DEFAULTS__.get(attr)
    if attr in __PARTATTRS__:
        return __OBJS__.get(attr)(**{"id": attr, attr: {}})
    return __OBJS__.get(attr)()


class SitewidePartsManager:
    """A manager class for other sitewide objects"""

    def __init__(self, **kwargs):
        """Initialize List of Sitewide Objects"""

        if "id" not in kwargs:
            raise AttributeError("Part to be managed not specified")
        manage = kwargs.pop("id")
        if manage not in __MGRS__:
            raise AttributeError(f"Unexpected SitewidePart Manager: {manage}")
        self.manage = manage
        for entry in kwargs.pop(manage):
            self.entries.append(
                SitewidePart(**{"id": manage, "managed": True, manage: entry})
            )

    def __setattr__(self, name, value):
        """set the named attribute of Manager with value"""

        if value in __MGRS__ and name == "manage" and not hasattr(self, name):
            for attr, val in [(name, value), ("entries", [])]:
                super().__setattr__(attr, val)
        else:
            raise AttributeError(f"Unrecognized Attribute: '{name}'")


class SitewidePart:
    """Core or Common aspects of a Sitewide Object"""

    def __init__(self, **kwargs):
        """Initialize base properties"""

        identity = kwargs.get("id")
        self.identity = identity
        ctxdict = kwargs.pop(identity)
        for attr in self.__attrs:
            if attr in ctxdict:
                value = ctxdict.pop(attr)
                if attr in __PARTS__ or attr in __MGRS__:
                    setattr(
                        self,
                        attr,
                        __OBJS__.get(attr)(**{"id": attr, attr: value}),
                    )
                else:
                    setattr(self, attr, value)
            elif attr in __MGRS__:
                # Managers are optional
                continue
            else:
                setattr(self, attr, get_default(attr))

    def __setattr__(self, name, value):
        """Get the value of an attribute"""

        if (
            name == "identity"
            and not hasattr(self, name)
            and isinstance(value, str)
        ):
            # Still initializing, Sitewide Part not set before
            for attr, val in [
                (name, value),
                (
                    "_SitewidePart__attrs",
                    get_attrs(value),
                ),
            ]:
                super().__setattr__(attr, val)
        elif name in self.__attrs:
            if name == "user" and (value, AnonymousUser):
                pass
            elif not isinstance(value, __OBJS__.get(name)):
                raise TypeError(
                    f"Wrong value type {type(value)} for {name} property. "
                    + f"Expected {__OBJS__.get(name)}"
                )
            super().__setattr__(name, value)
        else:
            raise AttributeError(f"SitewidePart has no {name} attribute")


__OBJS__ = {
    "allow": list,
    "columns": SitewidePartsManager,  # list of rows, columns, and elements
    "elements": SitewidePartsManager,  # list of SitewideElement
    "favicon": str,
    "footer": SitewidePart,
    "header": SitewidePart,
    "home": str,
    "icon": str,
    "id": str,
    "image": str,
    "layout": str,
    "menus": SitewidePartsManager,  # list of SitewideMenuObject
    "project": str,
    "rows": SitewidePartsManager,  # list of rows, columns, and elements
    "settings": Setting,
    "show": bool,
    "sidebar": SitewidePart,
    "state": str,
    "output": str,
    "url": str,
    "user": User,
}


class Sitewide(SitewidePart):
    """Holds data for pages across a Django project"""

    def __init__(self, **kwargs):
        """Initialize sitewide"""

        config = get_config()
        config["layout"].update(kwargs)
        config.update({"id": "layout"})
        super().__init__(**config)


# Default Sitewide view.


class HomeView(TemplateView):
    """Sitewide's Home View"""

    template_name = "home.html"
    extra_context = {"pagetitle": "Home"}

    def get(self, request, *args, **kwargs):
        """Prepare to render view"""

        sitewide = Sitewide(user=self.request.user)
        self.extra_context["sitewide"] = sitewide
        return super().get(request, *args, **kwargs)
