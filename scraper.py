from models import Establishment
# from opentable import OpenTable
# from tripadvisor import TripAdvisor
# from expedia import Expedia
from booking import Booking
from maeva import Maeva
from campings import Campings


__class_name__ = {
    'booking': Booking,
    'maeva': Maeva,
    'camping': Campings
}


class ListScraper:
    def __init__(self, ids):
        self.establishments = []
        self.ids = ids
    
    def init(self):
        for item in self.ids:
            etab = Establishment(rid=item)
            etab.refresh()
            self.establishments.append(etab)

    def start(self):
        for item in self.establishments:
            print("Establishment: ")
    #         # item.print()
            # print(item.name)
            # print(item.websites.keys())
            for site in item.websites.keys():
                # print(site, item.websites[site])
                if site in __class_name__.keys():
                    instance = __class_name__[site](url=item.websites[site])
                    print(instance)
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
