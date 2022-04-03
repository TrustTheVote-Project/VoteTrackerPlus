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

"""How to manage a VTP specific contest"""

import json

class Contest:
    """A wrapper around the rules of engagement regarding a specific contest"""

    # Legitimate Contest keys.  Note 'selection', 'uid', and 'cloak'
    # are not legitimate keys for blank ballots
    _keys = ['candidates', 'question', 'tally', 'win-by', 'max', 'write-in',
                 'selection', 'uid', 'cloak']

    # A simple numerical n digit uid
    _uids = {}
    _nextuid = 0

    @staticmethod
    def set_uid(a_contest_blob, ggo):
        """Will add a contest uid (only good within the context of this
        specific election) to the supplied contest.
        """
#        import pdb; pdb.set_trace()
        name = next(iter(a_contest_blob))
        if 'uid' in a_contest_blob[name]:
            raise IndexError(f"The uid of contest {name} is already set")
        a_contest_blob[name]['uid'] = str(Contest._nextuid).rjust(4, '0')
        if Contest._nextuid not in Contest._uids:
            Contest._uids[Contest._nextuid] = {}
        Contest._uids[Contest._nextuid]['name'] = name
        Contest._uids[Contest._nextuid]['ggo'] = ggo
        Contest._nextuid += 1

    @staticmethod
    def check_syntax(a_contest_blob, filename):
        """
        Will check the synatx of a contest somewhat and conveniently
        return the contest name
        """
        name = next(iter(a_contest_blob))
        ### ZZZ - sanity check the name
        for key in a_contest_blob[name]:
            if key not in Contest._keys:
                if filename:
                    raise KeyError(f"File ({filename}): "
                                   f"the specified key ({key}) is not a valid Contest key")
                raise KeyError(f"The specified key ({key}) is not a valid Contest key")
        return name

    def __init__(self, a_contest_blob, ggo, contests_index):
        """Construct the object placing the contest info in an attribute
        while recording the meta data
        """
        self.name = Contest.check_syntax(a_contest_blob, '')
        self.contest = a_contest_blob[self.name]
        self.ggo = ggo
        self.index = contests_index
        # set defaults
        if 'max' not in self.contest:
            if self.contest['tally'] == 'plurality':
                self.contest['max'] = 1
        # Some constructor time sanity checks
        if 'max' in self.contest and self.contest['max'] < 1:
            raise ValueError(f"Illegal value for max ({self.contest['max']}) "
                                 "- must be greater than 0")

    def __str__(self):
        """Return the contest contents as a print-able json string - careful ..."""
        contest_dict = { key: self.contest[key] for key in Contest._keys if key in self.contest }
        contest_dict.update({'name': self.name, 'ggo': self.ggo})
        return json.dumps(contest_dict, sort_keys=True, indent=4, ensure_ascii=False)

    def get(self, name):
        """Generic getter - can raise KeyError"""
        # Return the choices
        if name == 'choices':
            if 'candidates' in self.contest:
                return self.contest['candidates']
            if 'question' in self.contest:
                return self.contest['question']
        # Return contest 'meta' data
        if name in ['name', 'ggo', 'index', 'contest']:
            return getattr(self, name)
        # Else return contest data
        return getattr(self, 'contest')[name]

# EOF
