from util import Singleton


class ClientManager(Singleton):
    clients = []

    def find(self, uuid):
        for element in self.clients:
            if element.uuid == uuid:
                return element

        return None

    def find_users(self, uuid):
        result = []

        for element in self.clients:
            if element.__class__.__name__ == 'UserClient':
                if element.target_id == uuid:
                    result.append(element)

        return result

    def delete(self, uuid):
        for element in self.clients:
            if element.uuid == uuid:
                self.clients.remove(element)

    def all(self):
        return self.clients


class Client:
    id = ''
    type = ''
    uuid = ''

    def __init__(self, client_id, client_type, uuid):
        self.id = client_id  # socket session id
        self.type = client_type  # bridge, user
        self.uuid = uuid  # base62 identifier

        ClientManager.instance().clients.append(self)


class BridgeClient(Client):
    def __init__(self, client_id, uuid):
        super().__init__(client_id, 'bridge', uuid)


class UserClient(Client):
    target_id = ''

    def __init__(self, client_id, uuid, target_id):
        self.target_id = target_id

        super().__init__(client_id, 'user', uuid)
