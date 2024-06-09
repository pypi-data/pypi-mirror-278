"""
Partly implementation from: 
https://codeberg.org/imbev/simplematrixbotlib/src/branch/master/simplematrixbotlib/auth.py
"""

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
import dotenv
import base64
import json
import os

class Creds:
    """
    A class to store and handle login credentials.

    ...

    Attributes
    ----------
    homeserver : str
        The homeserver for the bot to connect to. Begins with "https://".

    username : str
        The username for the bot to connect as.

    password : str
        The password for the bot to connect with.

    """

    def __init__(self,
                 homeserver,
                 username=None,
                 password=None,
                 login_token=None,
                 access_token=None,
                 session_stored_file='session.txt',
                 device_name: str='mxbt') -> None:
        """
        Initializes the simplematrixbotlib.Creds class.

        Parameters
        ----------
        homeserver : str
            The homeserver for the bot to connect to. Begins with "https://".

        username : str, optional
            The username for the bot to connect as. This is necessary if password is used instead of login_token.

        password : str, optional
            The password for the bot to connect with. Can be used instead of login_token. One of the password, login_token, or access_token must be provided.

        login_token : str, optional
            The login_token for the bot to connect with. Can be used instead of password. One of the password, login_token, or access_token must be provided.

        access_token : str, optional
            The access_token for the bot to connect with. Can be used instead of password. One of the password, login_token, or access_token must be provided.

        session_stored_file : str, optional
            Location for the bot to read and write device_id and access_token. The data within this file is encrypted and decrypted with the password parameter using the cryptography package. If set to None, session data will not be saved to file.

        device_name : str, optional
            Name display in the list of sessions. Useful to identified the device.
        """

        self.homeserver = homeserver
        self.username = username
        self.password = password
        self.login_token = login_token
        self.access_token = access_token
        self._session_stored_file = session_stored_file
        self.device_name = device_name
        self.device_id = ""

        if self.password:
            self._key = self.fernet_key_from_pass(self.password)
        elif self.login_token:
            self._key = self.fernet_key_from_pass(self.login_token)
        elif self.access_token:
            self._key = self.fernet_key_from_pass(self.access_token)
        else:
            raise ValueError(
                "password or login_token or access_token is required")

    def fernet_key_from_pass(self, value: str, unique: bool=False) -> bytes:
        password = bytes(value, 'utf-8')
        if unique:
            salt = os.urandom(16)
        else:
            salt = b'0\xc03T\xb8\x9a\xf9\xcb\xf4\xf8\xc7\x00a\xd6\xa7M'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return base64.urlsafe_b64encode(kdf.derive(password))

    def fernet_decrypt(self, token, key):
        f = Fernet(key)
        data = str(f.decrypt(token))
        if data[0:2] == "b'":
            data = data[2:-1]
        return data

    @classmethod
    def from_env(cls, filepath: str=".env", **kwargs) -> "Creds":
        """
        Initialize class using .env file.
        You can provide any custom options with format:
            name = ENV_VAR_NAME
        """
        dotenv.load_dotenv(filepath)
        data = dict()
        for key, value in kwargs.items():
            data[key] = os.environ.get(value)
        return cls(**data)

    @classmethod
    def from_json(cls, filepath: str) -> "Creds":
        data = json.load(open(filepath, "r"))
        return cls(
            data['homeserver'],
            data['username'],
            data['password']
        )

    def session_read_file(self) -> None:
        """
        Reads and decrypts the device_id and access_token from file

        """
        if self._session_stored_file:
            try:
                with open(self._session_stored_file, 'r') as f:
                    encrypted_session_data = bytes(f.read()[2:-1], 'utf-8')
                    file_exists = True

            except FileNotFoundError:
                file_exists = False

            if file_exists:
                decrypted_session_data = self.fernet_decrypt(
                    encrypted_session_data,
                    self._key)[3:-2].replace('\'', '').replace(' ',
                                                               '').split(",")

                self.device_id = decrypted_session_data[0]
                self.access_token = decrypted_session_data[1]

                if not self.device_id or not self.access_token or (
                        self.device_id == "") or (self.access_token == ""):
                    raise ValueError(
                        f"Can't load credentials: device ID '{self.device_id}' or access token '{self.access_token}' were not properly saved. "
                        f"Reset your session by deleting {self._session_stored_file} and the crypto store if encryption is enabled."
                    )

        else:
            file_exists = False

        if not file_exists:
            self.device_id = None

    def session_write_file(self) -> None:
        """
        Encrypts and writes to file the device_id and access_token.
        """

        if not self._session_stored_file:
            print('device_id and access_token will not be saved')
            return

        if not (self.device_id and self.access_token):
            raise ValueError(
                f"Can't save credentials: missing device ID '{self.device_id}' or access token '{self.access_token}'"
            )
        elif (self.device_id == "") or (self.access_token == ""):
            raise ValueError(
                f"Can't save credentials: empty device ID '{self.device_id}' or access token '{self.access_token}'"
            )

        session_data = str([self.device_id, self.access_token])

        encrypted_session_data = Fernet(
            self._key
        ).encrypt(
            session_data.encode()
        )

        with open(self._session_stored_file, 'w') as f:
            f.write(str(encrypted_session_data))

