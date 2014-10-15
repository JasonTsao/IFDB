from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required


urlpatterns = patterns("boxofficemojo.utils",
                url(r"^run$", "syncBoxOfficeMojoData"),
)

urlpatterns += patterns("boxofficemojo.analysis",
				url(r"^analysis$", "evaluateBoxOfficeResults")
)