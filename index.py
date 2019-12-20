

from flask import Flask, request, jsonify, render_template
import os
import dialogflow
import requests
import json
import pusher

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


#adityatest1
@app.route('/foo', methods=['POST']) 
def foo():
    data = request.json
    return jsonify(data)
#aditya

#adityatest2
@app.route("/somethingfoo", methods=["POST"])
def do_something():
    data = request.get_json()
    return jsonify(data)
#adityatest2



#adityatest2 this is being used in dialogflow
@app.route("/get_movie_detail1", methods=["POST"])
def get_movie_detail1():
#def do_something():
    data = request.get_json()
    #movie = data['username']
    #movie = data['movie']

    # this is for intent movie
    movie = data['queryResult']['parameters']['movie']
    #below is for intent moviename
    #movie = data['queryResult']['parameters']['any']

    #movie = data['queryResult']

    api_key = os.getenv('OMDB_API_KEY')

    movie_detail = requests.get('http://www.omdbapi.com/?t={0}&apikey={1}'.format(movie, api_key)).content
    movie_detail = json.loads(movie_detail)

    response =  """
            Title : {0}
            Released: {1}
            Actors: {2}
            Plot: {3}
    """.format(movie_detail['Title'], movie_detail['Released'], movie_detail['Actors'], movie_detail['Plot'])

    reply = {
        "fulfillmentText": response,
    }



    #return jsonify(movie_detail)
    return jsonify(reply)
#adityatest2



#aditya
@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    fulfillment_text = detect_intent_texts(project_id, "unique", message, 'en')
    response_text = { "message":  fulfillment_text }

    return jsonify(response_text)
#aditya



#aditya
    @app.route('/get_movie_detail', methods=['POST'])
    def get_movie_detail():
        #return jsonify({'You sent':"Hello world"})
        data = request.get_json(silent=True)
        movie = data['queryResult']['parameters']['movie']
        api_key = os.getenv('OMDB_API_KEY')

        movie_detail = requests.get('http://www.omdbapi.com/?t={0}&apikey={1}'.format(movie, api_key)).content
        movie_detail = json.loads(movie_detail)
        response =  """
            Title : {0}
            Released: {1}
            Actors: {2}
            Plot: {3}
        """.format(movie_detail['Title'], movie_detail['Released'], movie_detail['Actors'], movie_detail['Plot'])

        reply = {
            "fulfillmentText": response,
        }

        return jsonify(reply)       

        
        #return jsonify({'You sent':data})
        

        
 

        #return jsonify({'You sent':data}), 201
#aditya




   





#aditya
def detect_intent_texts(project_id, session_id, text, language_code):
     session_client = dialogflow.SessionsClient()
     session = session_client.session_path(project_id, session_id)

     if text:
         text_input = dialogflow.types.TextInput(
             text=text, language_code=language_code)
         query_input = dialogflow.types.QueryInput(text=text_input)
         response = session_client.detect_intent(
             session=session, query_input=query_input)

         return response.query_result.fulfillment_text
    
#aditya













 # run Flask app
if __name__ == "__main__":
     app.run()    
