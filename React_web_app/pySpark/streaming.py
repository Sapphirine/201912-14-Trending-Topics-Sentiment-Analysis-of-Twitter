#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import socket
import json


# In[2]:


# Credentials
ACCESS_TOKEN = '1103131265899859971-RGxzlNgIkBCrvG6mBNoiDhMUbKERnU'     # your access token
ACCESS_SECRET = 'zKTNPrULGWqmQ09Xai9oouG7hsu5TLQC6lpEgAnOAg1Bd'    # your access token secret
CONSUMER_KEY = 'tArVehMnAEeBhYNrptt058msw'     # your API key
CONSUMER_SECRET = 'CE5bZNrluNMuDL1zP1NzZkmtn7lanXxqIHpfRbUXEnWmKLe5i1'  # your API secret key

tags = ['Jakarta', 'Tokyo', '東京', 'London', 'São Paulo', 'New York', 'NYC', 'Paris', 'Los Angeles', 
        'LA', 'Chicago', 'Singapore', 'Istanbul', 'Osaka', '大阪', 'Toronto', 'Madrid', 'Seoul', '서울', 'Miami',
        'Atlanta', 'Houston']


# In[3]:


class TweetsListener(StreamListener):
    """
    tweets listener object
    """
    def __init__(self, csocket):
        self.client_socket = csocket
    def on_data(self, data):
        try:
            msg = json.loads( data )
            print('TEXT:{}\n'.format(msg['text']))
            toSend = json.dumps({'text': msg['text'], 'id': msg['id_str']})+'\n'
            self.client_socket.send( toSend.encode('utf-8') )
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            return False
        # return True
    def on_error(self, status):
        print(status)
        return False

def sendData(c_socket, tags):
    """
    send data to socket
    """
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    twitter_stream = Stream(auth, TweetsListener(c_socket))
    twitter_stream.filter(track=tags)


# In[4]:


class twitter_client:
    def __init__(self, TCP_IP, TCP_PORT):
      self.s = s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.s.bind((TCP_IP, TCP_PORT))

    def run_client(self, tags):
      try:
        self.s.listen(1)
        while True:
          print("Waiting for TCP connection...")
          conn, addr = self.s.accept()
          print("Connected... Starting getting tweets.")
          sendData(conn, tags)
          conn.close()
      except KeyboardInterrupt:
        exit


# In[ ]:


if __name__ == '__main__':
    client = twitter_client("localhost", 9001)
    client.run_client(tags)

