import urequests
import uhashlib


class CLOta_files:
    def __init__(self, url=None, headers={}):
        """ OTA agent class.
        Args:
            url (str): URL serveur OTA: ex. 'http://ota_server.com:8085'
            headers (list, optional): Headers for urequests.
        """
        self.url = url
        self.headers = headers
        self.files = self._getFilesToUpdate( url )

    def _getFilesToUpdate(self, url):
        files=[]
        urluf = "{}/{}".format(url, 'ota?ask_files=updated')
        # 1) Pour la première connexion au serveur OTA 
        # #timeout: 1sec pour connexion 5 sec pour lecture fichier
        dt={'timeout': 1 }
        payload = urequests.get( urluf, headers={} )
        code = payload.status_code
        if( code == 200 ):
            lines=payload.text.splitlines()
            for line in lines:
                files.append( line )
        return files

    def _check_hash(self, x, y):
        x_hash = uhashlib.sha1(x.encode())
        y_hash = uhashlib.sha1(y.encode())

        x = x_hash.digest()
        y = y_hash.digest()

        if str(x) == str(y):
            return True
        else:
            return False

    def _get_file(self, url):
        payload = urequests.get(url, headers=self.headers)
        code = payload.status_code

        if code == 200:
            return payload.text
        else:
            return None

    def _check_all(self):
        changes = []

        for file in self.files:
            latest_version = self._get_file(self.url + "/" + file)
            if latest_version is None:
                continue

            try:
                with open(file, "r") as local_file:
                    local_version = local_file.read()
            except:
                local_version = ""

            if not self._check_hash(latest_version, local_version):
                changes.append(file)

        return changes

    def fetch(self):
        """Check if newer version is available.

        Returns:
            True - if is, False - if not.
        """
        if not self._check_all():
            return False
        else:
            return True

    def update(self):
        """Replace all changed files with newer one.

        Returns:
            True - if changes were made, False - if not.
        """
        changes = self._check_all()

        for file in changes:
            with open(file, "w") as local_file:
                local_file.write(self._get_file(self.url + "/" + file))

        #-- LIBERER le SERVEUR
        urluf = "{}/{}".format(self.url, 'stop?exit=1')
        urequests.get( urluf, headers={} )
        if changes:
            return True
        else:
            return False