import os

class Config:
    #used against attacks, to generate tokens(signatures)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you_never_guess'