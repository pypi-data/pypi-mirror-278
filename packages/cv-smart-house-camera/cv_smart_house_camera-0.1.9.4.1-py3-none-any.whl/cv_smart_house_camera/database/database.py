import firebase_admin
from firebase_admin import credentials, firestore


cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "cv-smarthouse",
  "private_key_id": "db7a30b68e2941ef9c20857ccfc34dd9b5665053",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDXVxeunS3OKSfe\nZpywZtoN+BYeHF0ZzF6lDmYBJ4RO65y2WXPGDOWFsf5aTie3kpgaMtG68LK6Ug3q\nWh1x+/VGMM/rkDX/PgeRttH93a8R2VVGsjA9aIVc8x3wfrBg3xbVa9PUJ5iGkL6o\nPSY+6BBWtEz1b38eGNIGdDBNUHkX4cI3zXn9KTtP8jc8cT6JOHrCDrNRJu5Ihgh2\n5jNDbh9NrMcmMbC+5UsO8nSkl2IsLqVf0ePebIfju2y1whhB0VOL2myfQaKeGs84\n17ALca2eyEZxvTGNzBd1Mb3cVgdQp2hQz38goCZQNlm1uGpBq5ODQglnWoyJCm6P\nlnL3hZTbAgMBAAECggEAQgGjtDXguv9Zha3tXJMCRuLjILKwBP7kifKKaNMslqZZ\nAHoV50C/wAXpwdOQEBCCyBEIwaUTG9KYClw6B1zkd3Hx4bJwIr9oQY2I+6iOh8mW\n/pcS+1fE/VNWO4gR13e6f4vQQAktEx5eGqK3zPOEQpd8uYTGMbsI8cp+ncxLefp8\n+IsoLB1hEKN2txDFadR3lCB/I4rY5MpH3PKI6YrrqWygC/eLHZC2UU33Mn465rJb\nskpNQkax1fFOzAWamOSp/PAbcIepPeswWYhqBPWiAXtIPDxHkArtg1AcjcEObXvQ\nz+k4z3Nle3Rszv5QDg33GlND9oaObQVYs58PipQulQKBgQDxM5KgLigAThe16K+B\nLhuTvaavTW6ObSZ79LuXEmjdG5AZaM/2ViFkha2HdEL2DDuAWCAwBLN3iMJZ4HET\nA1FL6gOx88Ppbpq00om4yvgLruasi+qXxWNVGZGLxQ5LWGT33Ls58VLUeHPIKZ6S\nlNPL54J+BNoouBZ7r+8n3OgV9wKBgQDkjVST0TcVK9ZFEZKyaGmRspJ/3oJRHgBA\nDN6DcUG/+IUeieV7uNeG9Xv/fTgiBYquJj8538BQRosJK151BLRbSUuDX6VvdNU4\nfAXN8e8vujOVm/rIrNuPLtFRTuERxaBF5+/xGAeRgwQmcdQVVjls9ZrnJdXXwbBh\nF/HuPVAvPQKBgQDQAR6wXj2GzdGqwUggyedkSEfno4n073IhsZLYnDqseymQkA/P\nqsVPT+yvBHb+gtwJOXZAkr1GFz0rjt9UeybvpZacLtDDjOuDhpDYOMkiIimxoVOk\noMehytP2SfCiz077ZXJcbJ12t415j1K9q/TeQf8JuBt+xAo3jihbIylOTwKBgQDQ\nRscbiZ3jyjYSbSg9Mw95eb0tj808NNXPiKrCJ9TeJ5DQOqQJMnIeh9k/A5LC1kAB\n4dLeX7w2q4KKkZ4bj3T4d3u8Nc5iGpswRT1Y5y+sU8gsf59zfqr6+ZRAv1w1wN4E\nto+fKuHCxh1jF3pJE3FzjQJjwMP2QYkFgjezfuZylQKBgF7egnf7GBhc3IQOp3yZ\npmdSdXrTiqznOtH1phbze5Fv4Zt93Dwd+OFDzrjX+khQbMFRT9QrfUAzwfEHCHWl\nrGFrLwn3bHKoFuoVfBaY8mR/KAle9R/GC1EGfmlxoJoeIWA1LDSL1ZHcT/VoaD1S\n/4MqdOAbAO6lvtlN4O0d1cve\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-kwy7w@cv-smarthouse.iam.gserviceaccount.com",
  "client_id": "106274326479450229163",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-kwy7w%40cv-smarthouse.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
})
firebase_admin.initialize_app(cred)

db = firestore.client()

def crud_factory(camera:str, module_name:str):
    base_path = f"{camera}/{module_name}/"

    def read(document_path):
        return read_record(base_path + document_path)
    
    def update(document_path, value):
        return update_record(base_path + document_path, value)

    def delete(document_path):
        return delete_record(base_path + document_path)

    def create(document_path, value):
        return create_record(base_path + document_path, value)

    def list(collection_path):
        return read_all_records(base_path + collection_path)
    


    return {
        "read": lambda document_path: read(document_path),
        "update": lambda document_path, value: update(document_path, value),
        "delete": lambda document_path: delete(document_path),
        "create": lambda document_path, value: create(document_path, value),
        "list": lambda collection_path: list(collection_path)
    }


def update_record(document_path, value):
    response = db.document(document_path)
    if response.get().exists:
        response.update(field_updates=value)
    else:
        response.set(document_data=value)

def delete_record(document_path,):
    response = db.document(document_path)
    if response.get().exists:
        response.delete()
    else:
        return None

def create_record(document_path, value):
    response = db.document(document_path)
    response.set(document_data=value)

def read_record(document_path):
    response = db.document(document_path)
    if response.get().exists:
        return response.get().to_dict()
    else:
        return None
    
def read_all_records(collection_path):
    users_ref = db.collection(collection_path)
    docs = users_ref.stream()
    result = []

    for doc in docs:
        print(f'{doc.id} => {doc.to_dict()}')
        result.append(doc.to_dict())
    
    return result

if(__name__ == "__main__"):
    # Test the database functions
    crud = crud_factory("camera", "offer")
    crud["create"]("test_collection/test_record", {"test": "test"})
    print(crud["read"]("test_collection/test_record"))
    crud["update"]("test_collection/test_record", {"test": "test2"})
    print(crud["list"]("test_collection"))
    crud["delete"]("test_collection/test_record")
    


