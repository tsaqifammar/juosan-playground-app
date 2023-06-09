from django.views.decorators.http import require_http_methods
from django.http import HttpRequest, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from core.lib.solver import Solver
from core.lib.validate import validate_solution
import os, json
import time

# Create your views here.
@require_http_methods(["GET"])
def index(request: HttpRequest):
  file_path = os.path.join(os.path.dirname(__file__), 'static', 'core', 'janko_instances.json')
  f = open(file_path)
  instances = json.load(f)
  f.close()

  return render(request, "core/index.html", {
    "example_instances": instances
  })

@require_http_methods(["POST"])
def solve(request: HttpRequest):
  body = json.loads(request.body.decode('utf-8'))

  for key in ["m", "n", "r", "N", "R"]:
    if not (key in body):
      return HttpResponseBadRequest("The keys m, n, r, N, and R must all be included.")

  solver = Solver(**body)
  start = time.time()
  val = solver.solve()
  print(f"{time.time() - start} seconds solve execution time.")

  return JsonResponse(val)

@require_http_methods(["POST"])
def validate(request: HttpRequest):
  body = json.loads(request.body.decode('utf-8'))

  for key in ["m", "n", "r", "N", "R", "S"]:
    if not (key in body):
      return HttpResponseBadRequest("The keys m, n, r, N, R, and S must all be included.")

  res = validate_solution(**body)

  return JsonResponse(res)
