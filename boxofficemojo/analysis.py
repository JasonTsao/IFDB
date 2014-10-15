from django.http import HttpResponse

from models import BOMMovieData

import json

def evaluateBoxOfficeResults(request):
	rtn_dict = {"success": False}
	try:
		bom_data = BOMMovieData.objects.all()
		for movie in bom_data:
			print movie
			movie_data = json.loads(movie.movie_data)
			for k in movie_data:
				print k
	except Exception, e:
		rtn_dict["error"] = "{}".format(e)
	return HttpResponse(json.dumps(rtn_dict), "application/json")