import jwt
import base64
public = "-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCzq7HbMx8ea370AxU2NhP2uzip\nUgqJgp8FDMWqESMrgGlG60Of8tvLJcu+tEdBFOFSHRZmmk7wm/SdzC+0u+GDgTTq\nnrMH9sT6ScveMuCemLsOACpWK0Z8F7ojACMKBgr6/3dVLs1XwSTtr95k3Zf0oGMb\nAMEI3R3wWGhe0+uWCwIDAQAB\n-----END PUBLIC KEY-----"
print(jwt.encode({"name": "motemote","priv": "admin"}, key=public, algorithm='HS256'))