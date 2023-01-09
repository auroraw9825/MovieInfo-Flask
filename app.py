from flask import Flask, request
app = Flask(__name__)
import requests
import json

@app.route('/trendingMovie', methods=['GET']) # use the route() decorator to tell Flask what URL should trigger our function.
def getTrendingMovie():
	response = requests.get('https://api.themoviedb.org/3/trending/movie/week?api_key=f9acad7a4b064909be30cfd5e0064bf4')
	trending_M = response.json()['results']
	res = dict()
	for i in range(5):
	# print(film['title'])
		movie = {}
		movie["title"] = trending_M[i]["title"]
		movie["backdrop_path"] = trending_M[i]["backdrop_path"]
		movie["release_year"] = trending_M[i]["release_date"][:4]
		res[str(i)] = movie
	# print(res)
	# print(response.status_code)
	# print(response.text)
	# use a dictionary, and return the dic
	return json.dumps(res) #, 201 status code 201 means something is created successfully.


@app.route('/TVonAir', methods=['GET']) # use the route() decorator to tell Flask what URL should trigger our function.
def getTVair():
	response = requests.get('https://api.themoviedb.org/3/tv/airing_today?api_key=f9acad7a4b064909be30cfd5e0064bf4')
	trending_M = response.json()['results']
	res = dict()
	for i in range(5):
	# print(film['title'])
		movie = {}
		movie["name"] = trending_M[i]["name"]
		movie["backdrop_path"] = trending_M[i]["backdrop_path"]
		movie["first_air_date"] = trending_M[i]["first_air_date"][:4]
		res[str(i)] = movie
	return json.dumps(res) #, 201 status code 201 means something is created successfully.


@app.route('/searchMovie', methods=['GET'])
def searchMovie():
	keyword = request.args.get("keyword")
	response = requests.get('https://api.themoviedb.org/3/search/movie?api_key=f9acad7a4b064909be30cfd5e0064bf4&language=en-US&query=' + keyword + '&page=1&include_adult=false')
	moviesFound = response.json()['results']
	l = min(len(moviesFound), 10)
	res = dict()
	for i in range(l):
		movie = {}
		movie["id"] = moviesFound[i].get("id", None)
		movie["title"] = moviesFound[i].get("title", None)
		movie["overview"] = moviesFound[i].get("overview", None)
		movie["poster_path"] = moviesFound[i].get("poster_path", None)
		movie["release_date"] = moviesFound[i].get("release_date", None)
		movie["vote_average"] = moviesFound[i].get("vote_average", None)
		movie["vote_count"] = moviesFound[i].get("vote_count", None)
		movie["genre_ids"] = moviesFound[i].get("genre_ids", None)# a list

		# response_m = requests.get('https://api.themoviedb.org/3/genre/movie/list?api_key=f9acad7a4b064909be30cfd5e0064bf4&language=en-US')
		# found = response_m.json()['genres']
		# genres  = dict() # make a dict that the key is id, value if the genre name
		# for j in range(len(found)):
		# 	k = found[j].get("id", None)
		# 	v=  found[j].get("name", None)
		# 	genres[k]  = v
		global genre_m
		genre_arr = []
		for a in moviesFound[i]["genre_ids"]:
			genre_arr.append(genre_m.get(a, ""))
		genre_str =  ", ".join(x for x in genre_arr)
		movie["genre_str"] = genre_str
		res[str(i)] = movie
		# print("id: ", movie["id"])
		# print("title", movie["title"])
	return json.dumps(res) #, 20


@app.route('/searchTV', methods=['GET'])
def searchTV():
	keyword = request.args.get("keyword")
	response = requests.get('https://api.themoviedb.org/3/search/tv?api_key=f9acad7a4b064909be30cfd5e0064bf4&language=en-US&page=1&query=' + keyword + '&include_adult=false')
	TVsFound = response.json()['results']
	l = min(len(TVsFound), 10)
	res = dict()
	for i in range(l):
		movie = {}
		movie["id"] = TVsFound[i].get("id", None)
		movie["title"] = TVsFound[i].get("name", None) # change the key to make it is the same as the Movie field.
		movie["overview"] = TVsFound[i].get("overview", None)
		movie["poster_path"] = TVsFound[i].get("poster_path", None)
		# if "first_air_date" in TVsFound[i]:
		movie["release_date"] = TVsFound[i].get("first_air_date", None)
		movie["vote_average"] = TVsFound[i].get("vote_average", None)
		movie["vote_count"] = TVsFound[i].get("vote_count", None)
		movie["genre_ids"] = TVsFound[i].get("genre_ids", None)

		# response_m = requests.get('https://api.themoviedb.org/3/genre/tv/list?api_key=f9acad7a4b064909be30cfd5e0064bf4&language=en-US')
		# found = response_m.json()['genres']
		# genres  = dict() # make a dict that the key is id, value if the genre name
		# for j in range(len(found)):
		# 	k = found[j].get("id", None)
		# 	v=  found[j].get("name", None)
		# 	genres[k]  = v
		global genre_t
		genre_arr = []
		for a in TVsFound[i]["genre_ids"]:
			genre_arr.append(genre_t.get(a, ""))
		genre_str =  ", ".join(x for x in genre_arr)
		movie["genre_str"] = genre_str
		res[str(i)] = movie
	return json.dumps(res) #, 20


@app.route('/multiSearch', methods=['GET'])
def multiSearch():
	keyword = request.args.get("keyword")
	response = requests.get('https://api.themoviedb.org/3/search/multi?api_key=f9acad7a4b064909be30cfd5e0064bf4&language=en-US&query=' + keyword + '&page=1&include_adult=false')
	found = response.json()['results']
	l = min(len(found), 10)
	res = dict()
	for i in range(l):
		media = found[i].get("media_type", None)
		if media == "movie":
			movie = {}
			movie["media_type"] = "movie"
			# print(found[i].get("title", None), "movie")
			movie["id"] = found[i].get("id", None)
			movie["title"] = found[i].get("title", None)
			movie["overview"] = found[i].get("overview", None)
			movie["poster_path"] = found[i].get("poster_path", None)
			movie["release_date"] = found[i].get("release_date", None)
			movie["vote_average"] = found[i].get("vote_average", None)
			movie["vote_count"] = found[i].get("vote_count", None)
			movie["genre_ids"] = found[i].get("genre_ids", None)
			# response_m = requests.get('https://api.themoviedb.org/3/genre/movie/list?api_key=f9acad7a4b064909be30cfd5e0064bf4&language=en-US')
			# genre_found = response_m.json()['genres']
			# genres  = dict() # make a dict that the key is id, value if the genre name
			# for j in range(len(genre_found)):
			# 	k = genre_found[j].get("id", None)
			# 	v=  genre_found[j].get("name", None)
			# 	genres[k]  = v
			global genre_m
			genre_arr = []
			for a in found[i]["genre_ids"]:
				genre_arr.append(genre_m.get(a, ""))
			genre_str =  ", ".join(x for x in genre_arr)
			movie["genre_str"] = genre_str
			res[str(i)] = movie
		elif media == "tv":
			movie = {}
			movie["media_type"] = "tv"
			# print(found[i].get("title", None), "tv")
			movie["id"] = found[i].get("id", None)
			movie["title"] = found[i].get("name", None)
			movie["overview"] = found[i].get("overview", None)
			movie["poster_path"] = found[i].get("poster_path", None)
			movie["release_date"] = found[i].get("first_air_date", None)
			movie["vote_average"] = found[i].get("vote_average", None)
			movie["vote_count"] = found[i].get("vote_count", None)
			movie["genre_ids"] = found[i].get("genre_ids", None)
			# response_m = requests.get('https://api.themoviedb.org/3/genre/tv/list?api_key=f9acad7a4b064909be30cfd5e0064bf4&language=en-US')
			# genre_found = response_m.json()['genres']
			# genres  = dict() # make a dict that the key is id, value if the genre name
			# for j in range(len(genre_found)):
			# 	k = genre_found[j].get("id", None)
			# 	v=  genre_found[j].get("name", None)
			# 	genres[k]  = v
			genre_arr = []
			for a in found[i]["genre_ids"]:
				genre_arr.append(genre_t.get(a, ""))
			genre_str =  ", ".join(x for x in genre_arr)
			movie["genre_str"] = genre_str
			res[str(i)] = movie
	return json.dumps(res) #, 20



@app.route('/movieDetails', methods=['GET'])
def movieDetails():
	# get movie details
	keyword = request.args.get("keyword")
	response = requests.get('https://api.themoviedb.org/3/movie/' + keyword + '?api_key=f9acad7a4b064909be30cfd5e0064bf4&language=en-US')
	moviesFound = response.json() # no ["result"] because there is only  one movie.

	movie = {}
	movie["id"] = moviesFound.get("id", None)
	movie["title"] = moviesFound.get("title", None)
	movie["runtime"] = moviesFound.get("runtime", None)
	movie["release_date"] = moviesFound.get("release_date", None)
	# movie["spoken_languages"] = moviesFound["spoken_languages"]
	l = []
	for i  in moviesFound["spoken_languages"]:
		l.append(i["english_name"])
	movie["spoken_languages"] = ", ".join(i for i in l)
	movie["vote_average"] = moviesFound.get("vote_average", None)
	movie["vote_count"] = moviesFound.get("vote_count", None)
	movie["poster_path"] = moviesFound.get("poster_path", None)
	movie["backdrop_path"] = moviesFound.get("backdrop_path", None)
	# movie["genres"] = moviesFound["genres"]
	# change the genre to a string
	s = []
	m_g = moviesFound.get("genres", None)
	for i in range(len(m_g)):
		s.append(m_g[i].get("name", None))
	movie["genres"] = ", ".join(i for i in s)

	# get movie credits (actors)
	response1 = requests.get('https://api.themoviedb.org/3/movie/' + keyword + '/credits?api_key=f9acad7a4b064909be30cfd5e0064bf4&language=en-US')
	creditsFound = response1.json() # no ["result"] because there is only  one movie.
	actors = creditsFound.get("cast", None) # a list
	l = min(len(actors), 8) # at most display 8 actors
	movie["cast"] = dict() # cast is a dictionary
	for i in range(l):
		t = dict()
		t["name"] = actors[i].get("name", None)
		t["profile_path"] = actors[i].get("profile_path", None)
		if "character" in actors[i]:
			t["character"] =actors[i]["character"]
		movie["cast"][str(i)] = t

	# get movie reviews
	response2 = requests.get('https://api.themoviedb.org/3/movie/' + keyword + '/reviews?api_key=f9acad7a4b064909be30cfd5e0064bf4&language=en-US&page=1')
	reviewsFound = response2.json() # no ["result"] because there is only  one movie.
	found = reviewsFound["results"]
	l = min(len(found), 5) # at most display 5 reviews
	movie["reviews"] = dict() # cast is a dictionary
	for i in range(l):
		t = dict()
		# if ("author_details" in found[i])  and ("username" in found[i]["author_details"]):
		t["username"] = found[i]["author_details"].get("username", None)
			# print("hello! got a username!")
		t["content"] = found[i].get("content", None)
		t["rating"] = found[i]["author_details"].get("rating", None)
		if "created_at" in found[i]:
			a = found[i]["created_at"]
			t["created_at"] = a[5:7] + "/" + a[8:10] + "/" + a[:4]
		movie["reviews"][str(i)] = t

	return json.dumps(movie) #, 20


# @app.route('/movieCredits', methods=['GET'])
# def movieCredits():
# 	keyword = request.args.get("keyword")
# 	response = requests.get('https://api.themoviedb.org/3/movie/' + keyword + '/credits?api_key=f9acad7a4b064909be30cfd5e0064bf4&language=en-US')
# 	creditsFound = response.json() # no ["result"] because there is only  one movie.
# 	actors = creditsFound["cast"] # a list
# 	l = min(len(actors), 8) # at most display 8 actors
# 	found = dict()
# 	for i in range(l):
# 		t = dict()
# 		t["name"] = actors[i]["name"]
# 		t["profile_path"] = actors[i]["profile_path"]
# 		t["character"] =actors[i]["character"]
# 		found[str(i)] = t
# 	print(found)
# 	return json.dumps(found) #, 20


@app.route('/tvDetails', methods=['GET'])
def tvDetails():
	# get tv details
	keyword = request.args.get("keyword")
	response = requests.get('https://api.themoviedb.org/3/tv/' + keyword + '?api_key=f9acad7a4b064909be30cfd5e0064bf4&language=en-US')
	moviesFound = response.json() # no ["result"] because there is only  one movie.

	movie = {}
	if("backdrop_path" in moviesFound):
		movie["backdrop_path"] = moviesFound["backdrop_path"]
	if("episode_run_time" in moviesFound):
		movie["episode_run_time"] = moviesFound["episode_run_time"]
	if("first_air_date" in moviesFound):
		movie["release_date"] = moviesFound["first_air_date"]
	# change the genre to a string
	if("genres" in moviesFound):
		s = []
		for i in range(len(moviesFound["genres"])):
			s.append(moviesFound["genres"][i]["name"])
		movie["genres"] = ", ".join(i for i in s)
	# print("genres: ", movie["genres"])
	if("id" in moviesFound):
		movie["id"] = moviesFound["id"]
	if("name" in moviesFound):
		movie["title"] = moviesFound["name"]
	if("number_of_seasons" in moviesFound):
		movie["number_of_seasons"] = moviesFound["number_of_seasons"]
	if("overview" in moviesFound):
		movie["overview"] = moviesFound["overview"]
	movie["poster_path"] = moviesFound.get("poster_path", None)

	# movie["spoken_languages"] = moviesFound["spoken_languages"]
	if("spoken_languages" in moviesFound):
		l = []
		for i  in moviesFound["spoken_languages"]:
			l.append(i["english_name"])
		movie["spoken_languages"] = ", ".join(i for i in l)
	if("vote_average" in moviesFound):
		movie["vote_average"] = moviesFound["vote_average"]
	if("vote_count" in moviesFound):
		movie["vote_count"] = moviesFound["vote_count"]
	

	# get tv credits (actors)
	response1 = requests.get('https://api.themoviedb.org/3/tv/' + keyword + '/credits?api_key=f9acad7a4b064909be30cfd5e0064bf4&language=en-US')
	creditsFound = response1.json() # no ["result"] because there is only  one movie.
	actors = creditsFound.get("cast", None) # a list
	if(actors!=None):
		l = min(len(actors), 8) # at most display 8 actors
		movie["cast"] = dict() # cast is a dictionary
		for i in range(l):
			t = dict()
			t["name"] = actors[i].get("name", None)
			t["profile_path"] = actors[i].get("profile_path", None)
			if "character" in actors[i]:
				t["character"] =actors[i].get("character", None)
			movie["cast"][str(i)] = t

	# get tv reviews
	response2 = requests.get('https://api.themoviedb.org/3/tv/' + keyword + '/reviews?api_key=f9acad7a4b064909be30cfd5e0064bf4&language=en-US&page=1')
	reviewsFound = response2.json() # no ["result"] because there is only  one movie.
	found = reviewsFound["results"]
	l = min(len(found), 5) # at most display 5 reviews
	movie["reviews"] = dict() # cast is a dictionary
	for i in range(l):
		t = dict()
		# if ("author_details" in found[i])  and ("username" in found[i]["author_details"]):
		t["username"] = found[i]["author_details"].get("username", None)
			# print("hello! got a username!"
		t["content"] = found[i].get("content", None)
		t["rating"] = found[i]["author_details"].get("rating", None)
		if "created_at" in found[i]:
			a = found[i]["created_at"]
			t["created_at"] = a[5:7] + "/" + a[8:10] + "/" + a[:4]
		movie["reviews"][str(i)] = t

	return json.dumps(movie) #, 20

genre_m = dict()
# @app.route('/movieGenre', methods=['GET'])
# def movieGenre():
response = requests.get('https://api.themoviedb.org/3/genre/movie/list?api_key=f9acad7a4b064909be30cfd5e0064bf4&language=en-US')
found = response.json()['genres']
# global genre_m  # make a dict that the key is id, value if the genre name
for j in range(len(found)):
	k = found[j].get("id", None)
	v=  found[j].get("name", None)
	genre_m[k]  = v
# return json.dumps(genre_m) #, 20

genre_t = dict()
# @app.route('/tvGenre', methods=['GET'])
# def tvGenre():
response1 = requests.get('https://api.themoviedb.org/3/genre/tv/list?api_key=f9acad7a4b064909be30cfd5e0064bf4&language=en-US')
found = response1.json()['genres']
# genres  = dict() # make a dict that the key is id, value if the genre name
for j in range(len(found)):
	k = found[j].get("id", None)
	v=  found[j].get("name", None)
	genre_t[k]  = v
# 	return json.dumps(genres) #, 20


@app.route('/', methods=['GET'])
def home():
	return app.send_static_file("HW6.html")

if __name__ == '__main__':
    app.run(debug=True)


# response = requests.get(url="https://api.themoviedb.org/3/trending/movie/week?api_key=97588ddc4a26e3091152aa0c9a40de22")
# # print(response.status_code)
# # print(response.text)
# response.json()
# trending_M = response.json()['results']
# res = []
# for i in range(5):
#     # print(film['title'])
# 	title = trending_M[i]["title"]
# 	backdrop_path = trending_M[i]["backdrop_path"]
# 	release_year = trending_M[i]["release_date"][:4]
# 	res.append([title, backdrop_path, release_year])
# print(res)
