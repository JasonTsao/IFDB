from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from models import *
from django.http import HttpResponse, HttpResponseRedirect

from datetime import datetime, timedelta
import time
import json
import ast


def newProfile(request):
	rtn_dict = {"success": False, "msg": ""}

	list_to_save = ['hello', 'goodbye', 'noway']
	new_profile = Profile()
	new_profile.friends = list_to_save
	new_profile.save()

	return HttpResponse(json.dumps(rtn_dict), content_type="application/json")


def getProfiles(request):
	rtn_dict = {"success": False, "msg": ""}
	profiles_array = []
	profiles_ids = []

	profiles = Profile.objects.all()

	for profile in profiles:
		profiles_ids.append(profile.id)
		profiles_array.append(profile.friends)

	rtn_dict['profiles'] = profiles_array
	rtn_dict['profile_ids'] = profiles_ids
	return HttpResponse(json.dumps(rtn_dict), content_type="application/json")