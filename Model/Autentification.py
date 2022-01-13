import bcrypt
import pickle

hashedPasswords = dict()

def checkPassword(username, password):
    file = open("noPasswordsHere.pkl", "rb")
    hashed = pickle.load(file)

    if username in hashed:
        if bcrypt.checkpw(password, hashed[username]):
            return True

    return False
