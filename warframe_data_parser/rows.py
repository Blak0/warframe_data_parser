import re
from abc import ABC, abstractmethod


row_classes_prefixes = [
    'MissionSignature',
    'RelicSignature',
    'Rotation',
    'Item',
]


def get_row_class_from_markup(markup):
    for prefix in row_classes_prefixes:
        row_class = globals()[f'{prefix}Row']
        if row_class(markup).does_markup_fit():
            return row_class
    return NoneRow


class Row(ABC):
    def __init__(self, markup):
        self.markup = markup

    @abstractmethod
    def get_data(self):
        """
            Receive a tuple with extracted data
        """

    @abstractmethod
    def accept_parser(self, parser):
        """
        Accept visiting parser and dispatch the proper method for it
        
        NOTE:
        It should return from the method of the parser, because it may
        return reward and user will expect the Row subclass to pass it further.
        """

    def does_markup_fit(self):
        if self.get_data():
            return True
        return False

    def parse(self, regex):
        match = re.search(regex, self.markup)
        if match:
            return match.groups()


class MissionSignatureRow(Row):
    def get_data(self):
        """
        "(...) Veil/Flexa (Caches) (...)" -> ("Veil", "Flexa", "Caches")
        """
        planet = r'([a-zA-Z]+)'
        name = r'([\w -\']+)'
        kind = r'\((\D+)\)'
        pattern = rf'{planet}/{name} {kind}'

        return self.parse(pattern)

    def accept_parser(self, parser):
        return parser.do_for_mission_signature(*self.get_data())


class RelicSignatureRow(Row):
    def get_data(self):
        """
        "(...) Axi A1 Relic (Intact) (...)" -> ("Axi", "A1", "Intact")
        """
        kind = r'([a-zA-Z]+)'
        name = r'(\D\d)'
        refinement = r'(\D+)'
        pattern = rf'{kind} {name} Relic \({refinement}\)'

        return self.parse(pattern)

    def accept_parser(self, parser):
        return parser.do_for_relic_signature(*self.get_data())


class RotationRow(Row):
    def get_data(self):
        """
        "(...) Rotation B (...)" -> ("Rotation B", )
        """
        pattern = r'(Rotation .){1}'

        return self.parse(pattern)

    def accept_parser(self, parser):
        return parser.do_for_rotation(*self.get_data())


class ItemRow(Row):
    def get_data(self):
        """
        "(...) Hell's Chamber (...) Common (21.37%) (...)" -> ("Hell's Chamber", "Common", "21.37%")
        """
        item_name = r"([A-Za-z0-9 ,()']+)"
        rarity_string = r"([a-zA-Z]+)"
        percentage = r"(\d*\.\d*%)"
        pattern = rf"<td>{item_name}</td><td>{rarity_string} \({percentage}\)</td>"

        return self.parse(pattern)

    def accept_parser(self, parser):
        return parser.do_for_item(*self.get_data())


class NoneRow(Row):
    def get_data(self):
        """
        Results in nothing since this class represents insignificant row.
        """

    def accept_parser(self, parser):
        """
        No action is desirable if row is not recognised as useful.
        """
