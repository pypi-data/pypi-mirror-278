A plugin for django to quick start a website
# Live Demo
release soon
# Features

● Twitter Bootstrap based UI with theme support

● Better filter, date range, number range, etc.

● Full CRUD methods

● Built-in data export with xls, csv, xml and json format

# Get Started

    pip install fluke-yw

# Install Requires

    django>=1.9

# usage

    import fluke
    from fluke import views
    
    
    class BaseSetting(object):
        enable_themes = True
        use_bootswatch = True
    
    
    class GlobalSettings(object):
        site_title = "fluke"
        site_footer = "fluke"
        menu_style = "accordion"
    
    fluke.site.register(views.BaseAdminView, BaseSetting)
    fluke.site.register(views.CommAdminView, GlobalSettings)
    