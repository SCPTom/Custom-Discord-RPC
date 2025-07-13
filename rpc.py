from pypresence import Presence
import time
import ctypes





class RPC:
    def __init__(self):
        self._state = ""
        self._details = ""
        self._largeImage = ""
        self._largeText = ""
        self._smallImage = ""
        self._smallText = ""
        self.Client = None
        self.client_id = ""

        self.connected = False

    def initRPC(self):
        print("RPC_DEBUG: Attempting to initialize RPC...")
        try:
            self.Client = Presence(self.client_id, pipe=0)
            print("RPC_DEBUG: Presence object created. Attempting to connect...")
            self.Client.connect()
            self.connected = True
            print("RPC_DEBUG: Successfully connected to Discord RPC.")
            return True
        except Exception as e:
            ctypes.windll.user32.MessageBoxW(0, "RPC connection failed.", "Error", 0x10)
            print(f"[ERROR] initRPC: Failed to connect to Discord RPC. Error: {e}", file=sys.stderr) 
            print("RPC_DEBUG: Please ensure Discord is running and you have a valid Client ID.", file=sys.stderr)
            self.connected = False
            return False


    def updateRPC(self):
        try:
            self.Client.update(
                state=self._state,
                details=self._details,
                start=int(time.time()),
                large_image=self._largeImage,
                large_text=self._largeText,
                small_image=self._smallImage,
                small_text=self._smallText,
            )
            return True
        except Exception as e:
            print(f"[ERROR] updateRPC: {e}")
            return False

    def closeRPC(self):
        if self.Client:
            self.Client.close()
            self.connected = False
            return True
        return False

    # --- Getters ---
    def getState(self):
        return self._state

    def getDetails(self):
        return self._details

    def getLargeImage(self):
        return self._largeImage

    def getLargeText(self):
        return self._largeText

    def getSmallImage(self):
        return self._smallImage

    def getSmallText(self):
        return self._smallText

    def getClientID(self):
        return self.client_id
    
    def getConnected(self):
        return self.connected

    # --- Setters ---
    def setState(self, state):
        self._state = state

    def setDetails(self, details):
        self._details = details

    def setLargeImage(self, image):
        self._largeImage = image

    def setLargeText(self, text):
        self._largeText = text

    def setSmallImage(self, image):
        self._smallImage = image

    def setSmallText(self, text):
        self._smallText = text

    def setClientID(self, client_id):
        self.client_id = client_id
