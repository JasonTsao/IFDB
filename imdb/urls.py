from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required


urlpatterns = patterns("imdb.views",
                url(r"^get$", "scrapeSite"),
)

urlpatterns += patterns("imdb.utils",
				url(r"^omdb/get$", "omdbSearchByTitle"),
)