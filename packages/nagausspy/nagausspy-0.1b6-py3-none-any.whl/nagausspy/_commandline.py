# nagausspy: NaFoMat tools for editing Gaussian Files
# Copyright (C) 2024  Hadrián Montes, NaFoMat

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from typing import List
class CommandLine(object):
    """
    Stores the info about the command line of ht egaussian log file

    Attributes
    ----------
    keywords : list(Keyword)
        List with all the keyword of the command line.
    """

    def __init__(self, line=""):
        self.keywords: List[Keyword] = [Keyword(key) for key in line.split()]

    def __str__(self):
        return "# " + " ".join(str(i) for i in self.keywords)

    __repr__ = __str__

    def __getitem__(self, keywordname: str) -> 'Keyword':
        for key in self.keywords:
            if key.keyword == keywordname:
                return key
        raise IndexError

    def add_keyword(self, keywordstr: str):
        """
        Adds a new keyword to the command line

        Parameters
        ----------
        keywordstr : string
            String with the definition of the keyword an its modifiers
            as would appear un the .com file.

        """
        keyword = Keyword(keywordstr)
        try:
            _ = self[keyword.keyword]
        except IndexError:
            self.keywords.append(keyword)
            return

        text = "Keyword {} already in the command line"
        text = text.format(keyword.keyword)
        raise RuntimeError(text)

    def remove_keyword(self, keyword: str):
        """
        Removes one keyword from the command line.

        Parameters
        ----------
        keyword : string
            Name of the keyword to remove

        """
        keyword = self[keyword]
        self.keywords.remove(keyword)

class Keyword(object):
    """
    Stores a gaussian keyword and its modifiers
    """

    def __init__(self, keyword_str: str):
        self._string = keyword_str

        self._keyword = None
        self._modifiers = ModifierSet()
        self._format_string()

    def __str__(self):
        out = self.keyword
        if len(self.modifiers) == 1:
            out += "={}".format(list(self.modifiers)[0])
        elif len(self.modifiers) >= 2:
            out += "=({})".format(",".join(str(i) for i in self.modifiers))
        return out

    __repr__ = __str__

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        if self.keyword != other.keyword:
            return False
        if self.modifiers != other.modifiers:
            return False
        return True

    def __getitem__(self, modifiername: str) -> 'Modifier':
        for modifier in self.modifiers:
            if modifier.name == modifiername:
                return modifier
        text = ("Modifier {} is not in the keyword").format(modifiername)
        raise IndexError(text)

    def _format_string(self):
        splitted = self._string.split("=")
        self._keyword = splitted[0]

        if len(splitted) >= 2:
            self._format_modifiers("=".join(splitted[1:]))

    def _format_modifiers(self, modifiers):
        # Remove the parenthesis
        modifiers = modifiers.replace("(", "").replace(")", "")

        # split the modifiers by commas and it to the set of keywords
        for modifier in modifiers.split(","):
            self._modifiers.add(Modifier(modifier))

    def add_modifier(self, modifierstr: str):
        """
        Adds a new modfier to the keyword.

        Parameters
        ----------
        modifierstr : string
            String with the modfier as would be written in the .com file.
        """
        self.modifiers.add(Modifier(modifierstr))

    def remove_modifier(self, modifiername: str):
        """
        Removes a modifier from the keyword.

        Parameters
        ----------
        modifiername : string
            The name of the modifier to remove

        """
        modifier = self[modifiername]
        self.modifiers.remove(modifier)

    @property
    def keyword(self) -> str:
        """
        The main part of the keyword
        """
        return self._keyword

    @property
    def modifiers(self) -> 'ModifierSet':
        """
        A set with the modifiers that apply to the main keyword. Any
        change to this set will reflect on the Keyword object.

        """
        return self._modifiers

    __repr__ = __str__

class ModifierSet(set):
    """
    Stores an indexable set
    """

    # def __init__(self, values=()):
    #     super(ModifierSet, self).__init__(values)

    def __getitem__(self, index: int) -> 'Modifier':
        if index >= len(self):
            raise IndexError

        return tuple(self)[index]

class Modifier(object):
    """
    Stores a modifier and its value (if any).
    """

    def __init__(self, modifier_string: str):
        self._name = None
        self._val = None

        self._parse(modifier_string)

    def _parse(self, modifier_string: str):
        splitted = modifier_string.split("=")
        if len(splitted) == 1:
            self._name = splitted[0].strip()

        elif len(splitted) == 2:
            self._name = splitted[0].strip()
            self._val = splitted[1].strip()

        else:
            text = ("Invalid modifier for keyword {}").format(modifier_string)
            raise ValueError(text)

    def __repr__(self):
        out = str(self.name)
        if self.value is not None:
            out += "={}".format(self.value)
        return out

    __str__ = __repr__

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        if self.name != other.name:
            return False
        if self.value != other.value:
            return False
        return True

    @property
    def name(self) -> str:
        """
        The name of the modifier. This item is not modifiable
        """
        return self._name

    @property
    def value(self):
        """
        The value of the modifier (if any). This value can be midifed
        only if it has a non None value.
        """
        return self._val

    @value.setter
    def value(self, value):
        if self._val is not None:
            self._val = value
        else:
            text = ("The modifier {} seems to be a non-valuable one. If you are"
                    " sure a value can be placed in this modifier, remove it "
                    "from the list an add it as a new one.").format(self.name)
            raise ValueError(text)
