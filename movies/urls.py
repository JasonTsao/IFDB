from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required


urlpatterns = patterns("movies.utils",
                url(r"^remove$", "removeMovies"),
                url(r"^get$", "getMovies"),
)