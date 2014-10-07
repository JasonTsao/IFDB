from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict

from models import *
from movies.models import *
from social.models import *
from django.http import HttpResponse, HttpResponseRedirect

from datetime import datetime, timedelta
import time
import json
import ast
