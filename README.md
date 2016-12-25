# onthefly
Change Django Settings on Custom admin page at "RUNTIME".

# Installation

```bash
pip install django-onthefly
```

# Configuration

##### adminplus configuration (INSTALLED_APPS)

Replace 'django.contrib.admin' with 'django.contrib.admin.apps.SimpleAdminConfig'
Add 'adminplus' after SimpleAdminConfig

```bash
'django.contrib.admin.apps.SimpleAdminConfig',
# ...
'adminplus',
# ...
```

##### onthefly configuration (INSTALLED_APPS)

Add 'onthefly' at the bottom of the list.

##### Final INSTALLED_APPS

```bash
INSTALLED_APPS = (
    'django.contrib.admin.apps.SimpleAdminConfig', (instead of 'django.contrib.admin')
    # ...
    'adminplus',
    # ...
    # ...
    'onthefly'
    )
```

##### You need to change urls.py like below as well

```bash
    # urls.py
    from django.contrib import admin
    from adminplus.sites import AdminSitePlus

    admin.site = AdminSitePlus()
    admin.autodiscover()

    urlpatterns = [
        # ...
        # Include the admin URL conf as normal.
        (r'^admin', include(admin.site.urls)),
        # ...
    ]
```

# Usage
go to django admin panel and see Onthefly Settings on bottom of the page as Custom Views
Add, Delete or Change settings at runtime.


# TODOs
##### 1- Add new backends apart from Redis
##### 2- Exception fallback to prevent unstabilities while changing settings at runtime
##### 3- More if you 'd like to contribute!

# CONTRIBUTE
##### All contributions are very welcomed!

# SCREENSHOT
![ScreenShot](https://raw.github.com/baranbartu/onthefly/master/screenshot.png)


