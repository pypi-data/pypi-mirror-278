from aleksis.core.util.apps import AppConfig


class DefaultConfig(AppConfig):
    name = "aleksis.apps.cursus"
    verbose_name = "AlekSIS — Cursus"
    dist_name = "AlekSIS-App-Cursus"

    urls = {
        "Repository": "https://edugit.org/AlekSIS/onboarding//AlekSIS-App-Cursus",
    }
    licence = "EUPL-1.2+"
    copyright_info = (([2023], "Jonathan Weth", "dev@jonathanweth.de"),)
