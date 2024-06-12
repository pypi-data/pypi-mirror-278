from NEMO.decorators import customization
from NEMO.views.customization import CustomizationBase


@customization(key="publications", title="Publications")
class PublicationsCustomization(CustomizationBase):
    variables = {
        "publications_enable_landing_carousel": "",
        "publications_carousel_latest_display_count": "10",
        "publications_carousel_latest_display_order": '["-creation_time"]',
        "publications_carousel_interval_time": "5",
    }
