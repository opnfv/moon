from django.utils.translation import ugettext_lazy as _

import horizon


class Moon(horizon.Dashboard):
    name = _("Moon")
    slug = "moon"
    panels = ('model','policy','pdp',)  # Add your panels here.
    default_panel = 'model'  # Specify the slug of the default panel.


horizon.register(Moon)
