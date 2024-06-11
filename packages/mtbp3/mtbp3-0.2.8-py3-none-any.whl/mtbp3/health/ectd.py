#  Copyright (C) 2023-2024 Y Hsu <yh202109@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public license as published by
#  the Free software Foundation, either version 3 of the License, or
#  any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details
#
#  You should have received a copy of the GNU General Public license
#  along with this program. If not, see <https://www.gnu.org/license/>

import pandas as pd
import os
from mtbp3.util.cdt import ListTree
import mtbp3
    
class ctoc_by_fda:
    def __init__(self, ectd_version="3.2.2", ctoc_version="2.3.3"):
        assert isinstance(ectd_version, str) and all(char.isdigit() or char == '.' for char in ectd_version), "Version must be a string with integers and dots"
        assert isinstance(ctoc_version, str) and all(char.isdigit() or char == '.' for char in ctoc_version), "Version must be a string with integers and dots"
        self.ectd_version = ectd_version
        self.ctoc_version = ctoc_version
        self.folder_name = mtbp3.get_data(f'supp_ectd/fda_ectd{ectd_version}_ctocv{ctoc_version}.txt')
        self.ctoc = self.__load_list()

    def __load_list(self):
        #file_path = f'./mtbp3/data/supp_ectd/fda_ectd{self.ectd_version}_ctocv{ctoc_version}.txt'
        file_path = self.folder_name
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                lines = file.readlines()
            lines = [line.strip() for line in lines if line.strip()]
            return lines
        else:
            print(f"eCTD Version {self.ectd_version} with CTOC Version {self.ctoc_version} not found.")
            return []

    def show_ctoc_tree(self, module=None, to_right=False):
        if not (isinstance(module, int) and 1 <= module <= 5):
            module = 1

        filtered_ctoc = [item for item in self.ctoc if item.startswith(str(module))]
        tree = ListTree(lst=filtered_ctoc, infmt='dotspace')
        return tree.list_tree(to_right=to_right)

    def find_section_given_words(self, words):
        if not isinstance(words, str) or not words:
            raise ValueError("str must be a nonempty string")
        return [row for row in self.ctoc if words in row]

if __name__ == "__main__":
    pass
