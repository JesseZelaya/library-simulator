# Author: Jesse Zelaya
# Date: 7/3/2020
# Description: Library simulator involving multiple classes


class LibraryItem:
    """main class of library item"""
    def __init__(self, library_item_id, title):
        """initializes variables
           location- 'ON_SHELF, ON_HOLD_SHELF, CHECKED_OUT' """
        self._library_item_id = library_item_id
        self._title = title
        self._checked_out_by = None
        self._requested_by = None
        self._location = "ON_SHELF"
        self._date_checked_out = None

    def get_library_item_id(self):
        """returns library_item_id"""
        return self._library_item_id

    def get_title(self):
        """returns title"""
        return self._title

    def set_checked_out_by(self, person):
        """sets who checked out the item"""
        self._checked_out_by = person

    def get_checked_out_by(self):
        """returns person who checked out item"""
        return self._checked_out_by

    def set_requested_by(self, person):
        """sets who requested item"""
        self._requested_by = person

    def get_requested_by(self):
        """returns person who requested item"""
        return self._requested_by

    def get_location(self):
        """returns location"""
        return self._location

    def set_location(self, location_input):
        """sets location 'ON_SHELF, ON_HOLD_SHELF, CHECKED_OUT' """
        self._location = location_input

    def set_date_checked_out(self, date):
        """sets date item was checked out on"""
        self._date_checked_out = date

    def get_date_checked_out(self):
        """returns date item was checked out"""
        return self._date_checked_out


class Book(LibraryItem):
    """book item inherits from LibraryItem class"""
    def __init__(self, library_item_id, title, author):
        super().__init__(library_item_id, title)
        self._author = author
        self._check_out_length = 21

    def get_check_out_length(self):
        return self._check_out_length

    def get_author(self):
        """returns author name"""
        return self._author


class Album(LibraryItem):
    """album item inherits from LibraryItem class"""
    def __init__(self, library_item_id, title, artist):
        super().__init__(library_item_id, title)
        self._artist = artist
        self._check_out_length = 14

    def get_check_out_length(self):
        return self._check_out_length

    def get_artist(self):
        return self._artist


class Movie(LibraryItem):
    """album item inherits from LibraryItem class"""

    def __init__(self, library_item_id, title, director):
        super().__init__(library_item_id, title)
        self._director = director
        self._check_out_length = 7

    def get_check_out_length(self):
        return self._check_out_length

    def get_director(self):
        return self._director


class Patron:
    """patron class defines a library patron for the simulator"""
    def __init__(self, patron_id, name):
        self._patron_id = patron_id
        self._name = name
        self._checked_out_items = {}
        self._fine_amount = 0

    def get_fine_amount(self):
        """returns fine amount"""
        return self._fine_amount

    def get_patron_id(self):
        """return patron ID"""
        return self._patron_id

    def get_name(self):
        """returns name"""
        return self._name

    def get_checked_out_items(self):
        #print('HI')
        return self._checked_out_items

    def set_checked_out_items(self, libItem):
        self._checked_out_items[libItem.get_library_item_id()] = libItem

    def remove_checked_out_items(self, libId):
        try:
            self._checked_out_items[libId]
        except KeyError:
            return None
        else:
            del self._checked_out_items[libId]

    def add_library_item(self, libItem):
        """adds library item to checked_out_items"""
        key = libItem.get_library_item_id()
        self._checked_out_items[key] = libItem

    def remove_library_item(self, lib_id):
        """removes item from checked out items using id"""
        try:
            self._checked_out_items[lib_id]
        except KeyError:
            print("item not in list to remove")
            return None
        else:
            del self._checked_out_items[lib_id]

    def get_library_item(self, lib_id):
        """returns checked out item"""
        try:
            self._checked_out_items[lib_id]
        except KeyError:
            #print("Item not in list")
            return None
        else:
            return self._checked_out_items[lib_id]

    def amend_fine(self, fee):
        """changes value to """
        self._fine_amount += fee


class Library:
    """represents main library"""
    def __init__(self):
        """
        : holdings: LibraryItems collection
        : members: Patron collection
        : current_date: date from time library was created
        """
        self._holdings = {}
        self._members = {}
        self._current_date = 0

    def add_library_item(self, libItem):
        """adds a library item to holdings"""
        self._holdings[libItem.get_library_item_id()] = libItem

    def get_library_item_from_id(self, libId):
        """gets library item from id"""
        try:
            self._holdings[libId]
        except KeyError:
            return None
        else:
            return self._holdings[libId]

    def add_patron(self, patron):
        self._members[patron.get_patron_id()] = patron

    def get_patron_from_id(self, patronId):
        try:
            self._members[patronId]
        except KeyError:
            return None
        else:
            return self._members[patronId]

    def check_out_library_item(self, patronId, libraryId):
        """uses patron id and library id to check out and update items"""
        if self.get_patron_from_id(patronId) is None:
            return "patron not found"

        if self.get_library_item_from_id(libraryId) is None:
            return "item not found"
        # create objects to use in method
        item = self.get_library_item_from_id(libraryId)
        person = self.get_patron_from_id(patronId)

        if item.get_location() == "CHECKED_OUT":
            return "item already checked out"
        elif item.get_requested_by() is not None or item.get_location() == "ON_HOLD_SHELF":
            return "item on hold by other patron"
        # update requested by if it was on hold for this Patron
        else:
            item.set_checked_out_by(person)
            item.set_date_checked_out(self._current_date)
            item.set_location("CHECKED_OUT")

        if item.get_requested_by() is person:
            item.set_requested_by(None)
        person.set_checked_out_items(item)
            #return "right"

        return "check out successful"

    def return_library_item(self, libId):
        """returns library item and updates as needed"""
        if self.get_library_item_from_id(libId) is None:
            return "item not found"
        item = self.get_library_item_from_id(libId)
        if item.get_location() == "ON_SHELF":
            return "item already in library"
        person = item.get_checked_out_by()
        person.remove_library_item(libId)

        if item.get_requested_by() is not None:
            item.set_location("ON_HOLD_SHELF")
        else:
            item.set_location("ON_SHELF")
        item.set_checked_out_by(None)
        return "return successful"

    def request_library_item(self, patronId, libId):
        """handles requests for library items and updates as needed"""
        if self.get_patron_from_id(patronId) is None:
            return "patron not found"
        if self.get_library_item_from_id(libId) is None:
            return "item not found"

        person = self.get_library_item_from_id(patronId)
        item = self.get_library_item_from_id(libId)

        if item.get_requested_by() is not None:
            return "item already on hold"

        else:
            item.set_requested_by(person)

        if item.get_location() == "ON_SHELF":
            item.set_location("ON_HOLD_SHELF")

        return "request successful"

    def pay_fine(self, patronId, money):
        """controls paying fines"""
        if self.get_patron_from_id(patronId) is None:
            return "patron not found"
        person = self.get_patron_from_id(patronId)
        person.amend_fine(-money)
        return "payment successful"

    def increment_current_date(self):
        self._current_date += 1
        if self._members != {}:
            for key in self._members:
                person = self._members[key]
                if person.get_checked_out_items() != {}:
                    for key2 in person.get_checked_out_items():
                        item = person.get_checked_out_items()[key2]
                        if type(item) is Book and (self._current_date - item.get_date_checked_out() > 21):
                            self._members[key].amend_fine(.1)
                        elif type(item) is Album and (self._current_date - item.get_date_checked_out() > 14):
                            self._members[key].amend_fine(.1)
                        elif type(item) is Movie and (self._current_date - item.get_date_checked_out() > 7):
                            self._members[key].amend_fine(.1)



#

b1 = Book("345", "Phantom Tollbooth", "Juster")
a1 = Album("456", "...And His Orchestra", "The Fastbacks")
m1 = Movie("567", "Laputa", "Miyazaki")
print(b1.get_author())
print(a1.get_artist())
print(m1.get_director())

p1 = Patron("abc", "Felicity")
p2 = Patron("bcd", "Waldo")
p3 = Patron("dd", "jo")

lib = Library()
lib.add_library_item(b1)
lib.add_library_item(a1)
lib.add_patron(p1)
lib.add_patron(p2)
lib.add_patron(p3)

lib.check_out_library_item("bcd", "456")
loc = a1.get_location()
lib.request_library_item("abc", "456")
lib.check_out_library_item("dd", "456")

lib.return_library_item("456")
lib.check_out_library_item("bcd", "456")
print(p1.get_checked_out_items())
# for i in range(57):
#     lib.increment_current_date()  # 57 days pass
# p2_fine = p2.get_fine_amount()
# print(p2_fine)
# lib.pay_fine("bcd", p2_fine)
# print(p2.get_fine_amount())
# lib.return_library_item("456")
# lib.check_out_library_item("abc", "456")
# print(p1.get_checked_out_items())



#
#




