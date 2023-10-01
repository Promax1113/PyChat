import hashlib, os

def pass_check(username, password):
    if not os.path.isfile(f"{os.getcwd()}/user_data/{username}.hash"):
        os.mkdir(f"{os.getcwd()}/user_data/")
        with open(f"{os.getcwd()}/user_data/{username}.hash", 'w') as f:
            f.write(hashlib.sha256(password).hexdigest())
            f.close()
        return 200
    else:
        with open(f"{os.getcwd()}/user_data/{username}.hash", "r") as f:
            saved_hash = f.readline()
        if saved_hash == hashlib.sha256(password).hexdigest(): return 200
        else: return 401