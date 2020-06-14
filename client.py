clients = []


class Client:
    id = ''
    type = ''

    def __init__(self, client_id, client_type):
        self.id = client_id  # base64
        self.type = client_type  # bridge, user

        clients.append(self)

    @staticmethod
    def find(client_id):
        for element in clients:
            if element.id == client_id:
                return element

        return None

    @staticmethod
    def delete(client_id):
        for element in clients:
            if element.id == client_id:
                clients.remove(element)

    @staticmethod
    def all():
        return clients


class BridgeClient(Client):
    def __init__(self, client_id):
        super().__init__(client_id, 'bridge')


class UserClient(Client):
    def __init__(self, client_id):
        super().__init__(client_id, 'user')
