from models import Establishment
# from opentable import OpenTable
# from tripadvisor import TripAdvisor
# from expedia import Expedia
from booking import Booking
from maeva import Maeva
from campings import Campings
from hotels import Hotels
from googles import Google
from opentable import Opentable
from trustpilot import Trustpilot
from tripadvisor import Tripadvisor
from expedia import Expedia
from api import ERApi


__class_name__ = {
    'booking': Booking,
    'maeva': Maeva,
    'camping': Campings,
    'hotels': Hotels,
    'google': Google,
    'opentable': Opentable,
    'trustpilot': Trustpilot,
    'tripadvisor': Tripadvisor,
    'expedia': Expedia
}


class ListScraper:
    def __init__(self,):
        self.establishments = []
        self.ids = []
    
    def init(self):
        etabs = ERApi.get_all('establishments')
        self.ids = map(lambda x: x['id'], etabs)

        for item in self.ids:
            etab = Establishment(rid=item)
            etab.refresh()
            self.establishments.append(etab)

    def start(self):
        for item in self.establishments:
            print("Establishment: ", item.name)

            for site in item.websites.keys():
                if site in __class_name__.keys():
                    instance = __class_name__[site](url=item.websites[site], establishment=item.id)
                    print(instance.establishment)
                    # print(instance)
    #             if site == 'expedia':
    #                 # print("item url: ", item.websites[site])
    #                 # instance = Expedia(url=item.websites[site])
    #                 # instance.execute()
    #                 continue
    #             elif site == 'booking':
    #                 # print("item url: ", item.websites[site])
    #                 instance = Booking(url=item.websites[site])
    #                 instance.set_establishment(item.id)
    #                 instance.execute()
    #                 # continue
    # #             elif site == 'tripadvisor':
    # #                 # instance = TripAdvisor(url=item.websites[site])
    # #                 # instance.execute()
    # #                 continue
    # #             elif site == 'opentable':
    # #                 # print("Ici")
    # #                 # instance = OpenTable(url=item.websites[site])
    # #                 # instance.execute()
    # #                 continue
    # #             elif site == 'google':
    # #                 continue
    # #             elif site == 'trustpilot':
    # #                 continue
    #             elif site == 'camping':
    #                 continue
