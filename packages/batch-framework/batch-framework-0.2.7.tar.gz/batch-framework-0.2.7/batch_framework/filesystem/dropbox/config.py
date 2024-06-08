import os
import requests
import webbrowser
import base64
import dropbox


class DropboxConfig:
    """
    Get OAuth2 Token
    """
    REFRESH_TOKEN_FILE = 'DROPBOX_REFRESH_TOKEN.ini'

    @property
    def refresh_token(self):
        if os.getenv('DROPBOX_REFRESH_TOKEN') is not None:
            return os.getenv('DROPBOX_REFRESH_TOKEN')
        elif os.path.exists(DropboxConfig.REFRESH_TOKEN_FILE):
            with open(DropboxConfig.REFRESH_TOKEN_FILE, 'r') as f:
                token = f.read()
                try:
                    dbx = dropbox.Dropbox(
                        app_key=self.app_key,
                        app_secret=self.app_secret,
                        oauth2_refresh_token=token
                    )
                    dbx.files_list_folder('')
                except dropbox.exceptions.AuthError:
                    token = self.__obtain_refresh_token()
            return token
        else:
            token = self.__obtain_refresh_token()
            return token

    def __obtain_refresh_token(self):
        url = f'https://www.dropbox.com/oauth2/authorize?client_id={self.app_key}&' \
            f'response_type=code&token_access_type=offline'
        webbrowser.open(url)
        access_token = input('dropbox_access_token:\n')
        refresh_token = self._get_refresh_token(access_token)
        with open(DropboxConfig.REFRESH_TOKEN_FILE, 'w') as f:
            f.write(refresh_token)
        return refresh_token

    def _get_refresh_token(self, access_code_generated):
        auth = base64.b64encode(f'{self.app_key}:{self.app_secret}'.encode())
        headers = {
            'Authorization': f"Basic {auth}",
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = f'code={access_code_generated}&grant_type=authorization_code'
        response = requests.post('https://api.dropboxapi.com/oauth2/token',
                                 data=data,
                                 auth=(self.app_key, self.app_secret),
                                 headers=headers)
        data = response.json()
        if 'refresh_token' in data:
            return data['refresh_token']

    @property
    def app_key(self):
        return os.getenv('DROPBOX_APP_KEY')

    @property
    def app_secret(self):
        return os.getenv('DROPBOX_APP_SECRET')
