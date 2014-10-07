from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required


urlpatterns = patterns("profiles.utils",
                url(r"^new$", "newProfile"),
                url(r"^get$", "getProfiles"),
                url(r"^remove$", "removeProfiles"),
                url(r"^collaborat_links/get$", "getCollborationLinks"),
                url(r"^collaborat_links/remove$", "removeCollborationLinks"),
                url(r"^movies/get$", "getMovies"),
                url(r"^movies/remove$", "removeMovies"),
)