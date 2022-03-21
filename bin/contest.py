#  VoteTrackerPlus
#   Copyright (C) 2022 Sandy Currier
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License along
#   with this program; if not, write to the Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""How to manage a specific contest"""

class Contest:
    """A wrapper around the rules of engagement regarding a specific contest"""

    # Legitimate Contest keys
    _keys = ['candidates', 'question', 'tally', 'win-by', 'max',
                 'selection']

    @staticmethod
    def check_syntax(a_contest_blob):
        """
        Will check the synatx of a contest somewhat and conveniently
        return the name
        """
        name = next(iter(a_contest_blob))
        ### ZZZ - sanity check the name
        for key in a_contest_blob[name]:
            if key not in Contest._keys:
                raise KeyError(f"The specified key ({key}) is not a valid Contest key")
        return name

    def __init__(self, a_contest_blob, ggo):
        """Boilerplate"""
        self.name = Contest.check_syntax(a_contest_blob)
        self.contest = a_contest_blob[self.name]
        self.ggo = ggo
        self.selection = []
        # set defaults
        if 'max' not in self.contest:
            self.contest['max'] = 1
        # Some constructor time sanity checks
        if self.contest['max'] < 1:
            raise ValueError(f"Illegal value for max ({self.contest['max']}) "
                                 "- must be greater than 0")

    def get(self, name):
        """Generic getter - can raise KeyError"""
        if name == 'choices':
            if 'candidates' in self.contest:
                return self.contest['candidates'].keys()
            if 'question' in self.contest:
                return self.contest['question'].keys()
        return self.contest[name]

    def select(self, offset):
        """Will select (add) a contest choice"""
        if offset > len(self.contest):
            raise ValueError(f"The choice offset ({offset}) is greater "
                             f"than the number of choices ({len(self.contest)})")
        if offset in self.selection:
            raise ValueError(f"The selction ({offset}) is being selected again")
        if offset < 0:
            raise ValueError(f"Only positive offsets are supported ({offset})")
        self.selection.append(offset)

# EOF
