from aleksis.core.util.apps import AppConfig


class DefaultConfig(AppConfig):
    name = "aleksis.apps.kolego"
    verbose_name = "AlekSIS — Kolego"
    dist_name = "AlekSIS-App-Kolego"

    urls = {
        "Repository": "https://edugit.org/AlekSIS/onboarding//AlekSIS-App-Kolego",
    }
    licence = "EUPL-1.2+"
    copyright_info = (([2023], "Jonathan Weth", "dev@jonathanweth.de"),)
