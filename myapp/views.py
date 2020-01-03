import json

from django.shortcuts import render
from django.http import HttpResponseRedirect
import requests

app_name = "Neuromorpho App"

# Index page
def index(request):
    context = {
        'app_name': app_name
    }
    return render(request, 'index.html', context)

# Fetching records
def fetch(request):
	if request.method == 'POST':
		data = request.POST.copy()
		query_param = data.get('query_param')
		query_val = data.get('query_val')
		size = data.get('size')
		page = data.get('page')
		sort_param = data.get('sort_param')
		order = data.get('order')
		print(type(query_param))
		print(type(query_val))
		print(type(size))
		print(type(page))
		print(type(sort_param))
		print(type(order))

		fetch_url = "http://neuromorpho.org/api/neuron/select?q="+query_param+":"+query_val+"&page="+page+"&size="+size+"&sort="+sort_param+","+order
		print(str(fetch_url))

		success = 1

		res = requests.get(fetch_url)
		res_json = res.json()

		# print(res_json['status'])

		if("status" in res_json):
			success = -1

		if(success == 1):
			with open('data/output.json', 'w') as data_file:
				json.dump(res_json, data_file)
		
		context = {
		    'app_name': app_name,
		    'view_name': 'Fetch New Records',
		    'success': success,
		    'fetch_url': fetch_url
		}	

		print("success is "+str(success))	

		return render(request, 'fetch.html', context)

	context = {
	'app_name': app_name,
	'view_name': 'Fetch New Records'
	}
	return render(request, 'fetch.html', context)

# Displaying records
def display(request):
    with open('data/output.json', 'r') as d:
        data = json.load(d)
    context = {
        'app_name' : app_name,
        'data': data["_embedded"]["neuronResources"],
        'view_name': 'Display Records'
    }
    print(data)
    return render(request, 'display.html', context)


# Deleting record
def delete(request):
	success = 0

	if request.method == 'POST':
		data = request.POST.copy()
		neuron_id = data.get('neuron')
		success = -1

		with open('data/output.json', 'r') as data_file:
		    data = json.load(data_file)

		for elem in data["_embedded"]["neuronResources"]:
		    if(elem["neuron_id"] == int(neuron_id)):
		        data["_embedded"]["neuronResources"].remove(elem)
		        print(elem)
		        success = 1

		with open('data/output.json', 'w') as data_file:
		    json.dump(data, data_file)
		
		context = {
		    'app_name': app_name,
		    'view_name': 'Delete Record',
		    'success': success,
		    'del_id': neuron_id
		}	

		print("success is "+str(success))	

		return render(request, 'delete.html', context)	

	context = {
	    'app_name': app_name,
	    'view_name': 'Delete Record',
	    'success': success
	}

	print("success is "+str(success))	

	return render(request, 'delete.html', context)
