from flask import Flask , render_template,request, url_for, jsonify, json

import requests

app = Flask(__name__)

# Just added basic routes
@app.route('/')
def Home():
  # Requests NYT Bestseller 'combined print and ebook fiction' list (there's a lot of lists we can request)
  requestUrl = "https://api.nytimes.com/svc/books/v3/lists/current/Combined%20Print%20and%20E-Book%20Fiction.json?api-key=Jn4QJ3QZomcadk6kUzr7GKmJubrMVB6y"
  requestHeaders = {
    "Accept": "application/json"
  }
  response = requests.get(requestUrl, headers=requestHeaders)

  # Turn json into a python dictionary
  response_dict = json.loads(response.text)

  # Get only book list info from response_dict
  book_dict = response_dict["results"]["books"]

  # Arrays that will hold featured list data (title, author, cover url)
  featured_title = []
  featured_author = []
  featured_cover = []

  # Get only necessary data for featured list from book_dict
  for i in book_dict:
    featured_title.append(i["title"])
    featured_author.append(i["author"])
    featured_cover.append(i["book_image"])    

  length = len(featured_title)

  # Send featured list data to Home.html
  return render_template('Home.html', length = length,
                                      cover_url = featured_cover, 
                                      featured_title = featured_title, 
                                      featured_author = featured_author)


@app.route('/bookshelf')
def BookShelf():
  return render_template('Bookshelf.html')

@app.route('/account')
def Account():
  return render_template('Account.html')

@app.route('/genres')
def Genres():
  return render_template('genres.html')

@app.route('/romance')
def Romance():
      
  #Requests Open Library API for genres
  request_url = "https://openlibrary.org/subjects/romance.json?"
  request_headers = {
    "Accept": "application/json"
  }
  response = requests.get(request_url, headers=request_headers)
  response_dict = json.loads(response.text)
  book_dict = response_dict["works"]

  romance_title = []
  romance_author = []
  romance_genre = []
  
  for i in book_dict:
    romance_title.append(i["title"])
    romance_genre.append(i["subject"])
    romance_author.append(i["authors"])
    
  length = len(romance_title)
  
  return render_template('romance.html', length = length, 
                                         romance_title = romance_title, 
                                         romance_genre = romance_genre,
                                         romance_author = romance_author)

@app.route('/thriller')
def Thriller():
    #Requests Open Library API for genres
  request_url = "https://openlibrary.org/subjects/thriller.json?"
  request_headers = {
    "Accept": "application/json"
  }
  response = requests.get(request_url, headers=request_headers)
  response_dict = json.loads(response.text)
  book_dict = response_dict["works"]

  thriller_title = []
  thriller_author = []
  thriller_genre = []
  
  for i in book_dict:
    thriller_title.append(i["title"])
    thriller_genre.append(i["subject"])
    thriller_author.append(i["authors"])
    
  length = len(thriller_title)
  
  return render_template('thriller.html', length = length, 
                                         thriller_title = thriller_title, 
                                         thriller_genre = thriller_genre,
                                         thriller_author = thriller_author)

@app.route('/nonfiction')
def Nonfiction():
  return render_template('nonfiction.html')

@app.route('/horror')
def Horror():
  return render_template('horror.html')

@app.route('/ya')
def YoungAdult():
  return render_template('young_adult.html')

@app.route('/comedy')
def Comedy():
  return render_template('comedy.html')

# @app.route('/BookSearchList', methods = ['GET'])
# def BookSearchList():

#   title = request.args.get('BookTitle')
#   print("---- GET TEST ----")
#   print(title)

#   return render_template('BookSearchList.html')



@app.route('/BookSearchList', methods = ['GET','POST'])
def BookSearchList():

  # This route method is almost 'POST' method (I guess ?)
  if request.method == 'POST':
  
    # Get the user input from the form
    BookTitle = request.form.get('BookTitle')

    # Changed URL format for fetching ..
    # (ex: Harry potter -> Harry+potter)
    url_BookTitle = BookTitle.replace(" ", "+")
    
    # Source from : openlibrary.org 
    response = requests.get(f'http://openlibrary.org/search.json?title={url_BookTitle}&limit=10')

    # The response need to be convert to JSON format
    response = response.json()
    results = response['docs']

    # Set the array of the lists that I want to get
    book_title = []
    author_name = []
    cover_id = []
    isbn = []
    
    count = 0

    # Get the most recent books data from the results length (cover,title,author)
    # Loop untill the length of results
    for i in range(len(results)):
           
      if 'title' in results[i] and 'author_name' in results[i] and 'cover_i' in results[i]:

        cover_id.append(results[i]['cover_i'])
        book_title.append(results[i]['title'])
        author_name.append(results[i]['author_name'])
        # Since there are lots of isbn get the first one
        isbn.append(results[i]['isbn'][0])

        count+=1
      # else:
      #   break

    # Send the all data to the BookSearchList.html  
  return render_template('BookSearchList.html', count = count,
                                                isbn = isbn,
                                                cover_id = cover_id, 
                                                book_title = book_title, 
                                                author_name = author_name)

if __name__ == '__main__':

  # Added for debugging 
  app.run(debug=True)
  # If this is not working then, try this...
  # flask --app server.py --debug run
