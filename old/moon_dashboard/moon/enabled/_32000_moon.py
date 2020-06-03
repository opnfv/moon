# The name of the dashboard to be added to HORIZON['dashboards']. Required.
DASHBOARD = 'moon'

# If set to True, this dashboard will not be added to the settings.
DISABLED = False

# A list of AngularJS modules to be loaded when Angular bootstraps.
ADD_ANGULAR_MODULES = ['moon']

# Automatically discover static resources in installed apps
AUTO_DISCOVER_STATIC_FILES = True

# A list of applications to be added to INSTALLED_APPS.
ADD_INSTALLED_APPS = [
    'openstack_dashboard.dashboards.moon',
]

# A list of scss files to be included in the compressed set of files
ADD_SCSS_FILES = ['moon/scss/moon.scss']
