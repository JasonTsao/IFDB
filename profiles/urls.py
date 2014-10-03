from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required


urlpatterns = patterns("profiles.views",
                url(r"^new$", "newProfile"),
                url(r"^get$", "getProfiles"),
)