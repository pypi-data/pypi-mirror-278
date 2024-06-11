#  Copyright (C) 2023 Y Hsu <yh202109@gmail.com>
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

import csv
import glob
import os
import re
import numpy as np
import pandas as pd
from mtbp3.util.lsr import LsrTree
import mtbp3

class Emt:
    """A class representing MedDRA terms.

    This class provides methods to interact with the Emt object,
    including listing files associated with the Emt.

    Attributes:
        folder_name (str): The folder name associated with the Emt.
        lsr (LsrTree): An instance of the LsrTree class for listing files.
        month (str): The month of the version published.
        year (str): The year of the version published.
    """

    def __init__(self, folder_name=''):
        """
        Initialize a new Emt object.

        Args:
            folder_name (str, optional): The folder name associated with the Emt.
                If not provided, the default folder name will be used.
        """
        if folder_name:
            self.folder_name = folder_name
            self.demo = False
        else:
            self.folder_name = mtbp3.get_data('test_emt/MedDRA')
            self.demo = True

        self.version_number = "00.0"
        self.version_number_us = "00_0"
        self.readme_file = None
        self.year = ""
        self.month = ""
        self.language = ""
        self.mdhier = None
        self.llt = None
        self.smq_list = None
        self.smq_content = None
        self.fmq_list = None
        self.fmq_list_unique = None
        self.fmq_list_default = None

        meddra_release_file = os.path.join(self.folder_name, 'MedAscii', 'meddra_release.asc')
        if os.path.isfile(meddra_release_file):
            with open(meddra_release_file, 'r') as file:
                reader = csv.reader(file, delimiter='$')
                header = next(reader)
                self.version_number = header[0]
                self.version_number_us = self.version_number.replace(".", "_")
                self.language = header[1]
        else:
            raise FileNotFoundError("meddra_release.asc file not found.")

        pattern = os.path.join(self.folder_name, '!!readme_[1-3][0-9]_[0-1]_English.txt')
        files = glob.glob(pattern, recursive=False)
        if len(files) == 1:
            self.readme_file = files[0]
        else:
            raise ValueError("Readme file not found or multiple files found.")

        with open(self.readme_file, 'r') as file:
            lines = file.readlines()[-3:]
            for line in lines:
                match = re.search(r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\b \d{4}', line)
                if match:
                    self.month, self.year = match.group().split()
                    break

    def expected_file_lists(self):
        """
        Get the three lists of files associated with the Emt.

        Returns:
            tuple: A tuple containing three lists of file names.
        """
        support_doc_files = [
            f"!!readme_{self.version_number_us}_English.txt",
            f"detail_report_{self.version_number_us}_English.pdf",
            f"dist_file_format_{self.version_number_us}_English.pdf",
            f"intguide_{self.version_number_us}_English.pdf",
            f"SMQ_intguide_{self.version_number_us}_English.pdf",
            f"SMQ_spreadsheet_{self.version_number_us}_English.xlsx",
            f"version_report_{self.version_number_us}_English.xlsx",
            f"whatsnew_{self.version_number_us}_English.pdf",
        ]
        med_ascii_files = [
            "hlgt.asc", "hlgt_hlt.asc", "hlt.asc", "hlt_pt.asc", "intl_ord.asc",
            "llt.asc", "mdhier.asc", "meddra_history_english.asc", "meddra_release.asc", 
            "pt.asc", "smq_content.asc", "smq_list.asc", "soc.asc", "soc_hlgt.asc"
        ]
        med_ascii_files = ["/MedAscii/" + file for file in med_ascii_files] 
        seq_ascii_files = [
            "hlgt.seq", "hlgt_hlt.seq", "hlt.seq", "hlt_pt.seq", "intl_ord.seq",
            "llt.seq", "mdhier.seq", "pt.seq", "soc.seq", "soc_hlgt.seq"
        ]
        seq_ascii_files = ["/SeqAscii/" + file for file in seq_ascii_files] 
        return support_doc_files, med_ascii_files, seq_ascii_files

    def find_files(self):
        """
        Find all expected files associated with the Emt.

        Returns:
            list: A list of missing file names.
        """
        lsr = LsrTree(self.folder_name, outfmt="list")
        lsr_files = lsr.list_files()
        support_doc_files, med_ascii_files, seq_ascii_files = self.expected_file_lists()

        missing_files = []
        for file in support_doc_files + med_ascii_files + seq_ascii_files:
            if file not in lsr_files:
                missing_files.append(file)

        if not missing_files:
            mdhierasc = os.path.join(self.folder_name, 'MedAscii', 'mdhier.asc')
            #self.mdhier = pd.read_csv(mdhierasc, delimiter='$', header=None, dtype=str)
            self.mdhier = pd.read_csv(mdhierasc, delimiter='$', header=None)
            nsoc = len(self.mdhier[7].unique())
            return [], f"All files found. Version: {self.version_number}; Year: {self.year}; Month: {self.month}; Language: {self.language}. N_SOC: {nsoc}."
        else:
            return missing_files, f"{len(missing_files)} files not found."

    def load_llt(self, unique=True):
        if self.llt is None:
            ids=[0,1,2,9]
            tmp = pd.read_csv(os.path.join(self.folder_name, 'MedAscii', 'llt.asc'), delimiter='$', header=None)
            self.llt = tmp[ids]
        if unique:
            self.llt = self.llt.drop_duplicates().reset_index(drop=True)


    def list_files(self):
        """
        List all files associated with the Emt.

        Returns:
            list: A list of file names.
        """
        lsr = LsrTree(self.folder_name, outfmt="tree", with_counts=True)
        lsr_files = lsr.list_files()
        return lsr_files

    def find_soc(self, terms=[], ignore_case=False):
            """
            Find all unique SOC (System Organ Class) terms.

            Args:
                terms (list, optional): The specific SOC name(s) to filter the results. Defaults to an empty list.
                ignore_case (bool, optional): Flag to indicate whether to ignore case sensitivity when filtering terms. Defaults to False.

            Returns:
                list: A list of unique SOC terms. If terms is provided, it returns the corresponding ids.

            Raises:
                AssertionError: If terms is not a list.
            """
            return self.find_term_wi_level(terms, ignore_case=ignore_case, level=1)

    def find_hlgt(self, terms=[], ignore_case=False):
            """
            Find all unique HLGT terms.

            Args:
                terms (list, optional): The specific HLGT name(s) to filter the results. Defaults to an empty list.
                ignore_case (bool, optional): Flag to indicate whether to ignore case sensitivity when filtering terms. Defaults to False.

            Returns:
                list: A list of unique HLGT terms. If terms is provided, it returns the corresponding ids.

            Raises:
                AssertionError: If terms is not a list.
            """
            return self.find_term_wi_level(terms, ignore_case=ignore_case, level=2)

    def find_hlt(self, terms=[], ignore_case=False):
            """
            Find all unique HLT terms.

            Args:
                terms (list, optional): The specific HLT name(s) to filter the results. Defaults to an empty list.
                ignore_case (bool, optional): Flag to indicate whether to ignore case sensitivity when filtering terms. Defaults to False.

            Returns:
                list: A list of unique HLT terms. If terms is provided, it returns the corresponding ids.

            Raises:
                AssertionError: If terms is not a list.
            """
            return self.find_term_wi_level(terms, ignore_case=ignore_case, level=3)

    def find_pt(self, terms=[], ignore_case=False):
            """
            Find all unique PT terms.

            Args:
                terms (list, optional): The specific PT name(s) to filter the results. Defaults to an empty list.
                ignore_case (bool, optional): Flag to indicate whether to ignore case sensitivity when filtering terms. Defaults to False.

            Returns:
                list: A list of unique PT terms. If terms is provided, it returns the corresponding ids.

            Raises:
                AssertionError: If terms is not a list.
            """
            return self.find_term_wi_level(terms, ignore_case=ignore_case, level=4)

    def find_llt(self, terms=[], ignore_case=False, llt_current_only=True):
            """
            Find all unique LLT terms.

            Args:
                terms (list, optional): The specific LLT name(s) to filter the results. Defaults to an empty list.
                ignore_case (bool, optional): Flag to indicate whether to ignore case sensitivity when filtering terms. Defaults to False.

            Returns:
                list: A list of unique LLT terms. If terms is provided, it returns the corresponding ids.

            Raises:
                AssertionError: If terms is not a list.
            """
            self.load_llt()
            return self.find_term_wi_level(terms=terms, ignore_case=ignore_case, level=5, llt_current_only=llt_current_only)

    def all_str_digit(self, lst=[]):
        """
        Check if all elements in a given list are strings containing only digits.

        Args:
            fin (list): The list to check.

        Returns:
            bool: True if all elements in the list are strings containing only digits, False otherwise.
        """
        if not isinstance(lst, list):
            return False
        return all(isinstance(element, int) or element is None for element in lst)

    def assert_terms(self, input, remove_none=False):
        """
        Assert that the input is either a string or a list.
        If the input is a string, it is converted to a length one list.
        All elements in the list are converted to strings and empty elements are removed.

        Args:
            input (str or list): The input to be validated.

        Returns:
            list: The validated list.

        Raises:
            AssertionError: If the input is neither a string nor a list.
        """
        range_8_int = [10000000, 99999999]
        less_term_warning = "Warning: Some input terms might be removed due to format"
        if isinstance(input, int):
            if range_8_int[0] <= input <= range_8_int:
                return [input]
            else:
                if remove_none:
                    print(less_term_warning)
                    return []
                else:
                    return [None]

        if isinstance(input, str):
            if len(input) == 8 and input.isdigit() and input[0] != '0':
                return [int(input)]
            else:
                return [input]

        if not isinstance(input, (list, pd.core.series.Series, np.ndarray)):
            raise ValueError("Input must be a list, pandas Series, or numpy array.")
        if len(input) == 0:
            return []

        len0 = len(input)


        if all(isinstance(element, int) or (element is None) or (element is np.nan) for element in input):
            out = [element if (range_8_int[0] <= element <= range_8_int[1]) else None for element in input]
        else:
            if all((isinstance(element, str) and ((len(element) == 8 and element.isdigit()) or len(element) == 0)) or (element is None) or (element is np.nan) for element in input):
                out = [int(element) if (len(element) == 8 and element.isdigit() and element[0] != '0') else None for element in input]
            else:
                out = [element if (element is not np.nan) else None for element in input]
        if remove_none:
            out = [element for element in out if element is not None]
        if len(out) != len0:
            print(less_term_warning)
        return out

    def find_term_wi_level(self, terms=[], ignore_case=False, level=1, llt_current_only=True):
        """
        Find all unique terms.

        Args:
            terms (list, optional): The specific SOC name(s) to filter the results. Defaults to an empty list.
            ignore_case (bool, optional): Flag to indicate whether to ignore case sensitivity when filtering terms. Defaults to False.
            level (int, optional): The level of the SOC hierarchy to consider. Defaults to 1.

        Returns:
            list: A list of unique terms. If terms is provided, it returns the corresponding ids.

        Raises:
            AssertionError: If terms is not a list.

        """
        assert level in range(1, 6), "level should be between 1 and 5"
        ignore_case = ignore_case if isinstance(ignore_case, bool) and ignore_case else False
        if level < 5:
            id0 = 4-level 
            id1 = 8-level
            subset = self.mdhier[[id0, id1]].drop_duplicates().reset_index(drop=True)
        else:
            id0 = 0 
            id1 = 1
            self.load_llt()
            if llt_current_only:
                subset = self.llt[self.llt[9]=='Y'][[id0,id1]]
            else:
                subset = self.llt[[id0,id1]]

        terms = self.assert_terms(terms)

        if terms:
            if self.all_str_digit(lst=terms):
                out = pd.merge(pd.DataFrame(terms), subset, left_on=0, right_on=id0)[id1].tolist()
            else:
                terms_df = pd.DataFrame(terms)
                if ignore_case:
                    terms_df['lower0'] = terms_df[0].str.lower()
                    subset['lowerid1'] = subset[id1].str.lower()
                    out = pd.merge(terms_df, subset, left_on='lower0', right_on='lowerid1', how='left', sort=False)[id0].tolist()
                else:
                    out = pd.merge(terms_df, subset, left_on=0, right_on=id1, how='left', sort=False)[id0].tolist()
        else:
            out = subset[id1].tolist()
        return out

    def find_pt_given_soc(self, soc=[], primary_soc_only=False, ignore_case=False):
        """
        Find all PTs (Preferred Terms) given a SOC (System Organ Class) name.

        Args:
            soc (str or list): The name of the SOC or a list of SOC names.
            primary_soc_only (bool, optional): If True, only return PTs associated with the primary SOC. 
                                                Defaults to False.

        Returns:
            pandas.DataFrame: A DataFrame containing the PTs associated with the given SOC. 
                                Each row represents a PT and contains the PT code and PT name.
        """

        df = self.mdhier
        if df.empty:
            return pd.DataFrame(columns=['pt_id', 'pt', 'primary'])
        soc = self.assert_terms(soc, remove_none=True)
        if self.all_str_digit(lst=soc):
            soc_id = soc
        else:
            soc_id = self.find_soc(soc, ignore_case=ignore_case)

        if primary_soc_only:
            subset_df = df[(df[3].isin(soc_id)) & (df[11] == 'Y')][[0, 4, 3, 7]].reset_index(drop=True)
            subset_df.columns = ['pt_id', 'pt', 'soc_id', 'soc']
        else:
            subset_df = df[df[3].isin(soc_id)][[0, 4, 3, 7, 11]].reset_index(drop=True)
            subset_df.columns = ['pt_id', 'pt', 'soc_id', 'soc', 'primary']
            
        return subset_df


    def find_llt_given_pt(self, pt=[], ignore_case=False, llt_current_only=True):
        """
        Find all LLTs (Lowest Level Terms) given a PT (Preferred Term) name or a list of PT names.

        Args:
            pt (str or list): The name of the PT or a list of PT names.

        Returns:
            pandas.DataFrame: A DataFrame containing the LLTs associated with the given PT(s). 
                                Each row represents an LLT and contains the LLT code and LLT name.
        """
        self.load_llt()
        df = self.llt
        df.columns = ['llt_id', 'llt', 'pt_id', 'llt_currency']
        if llt_current_only:
            df = df[df['llt_currency'] == 'Y']
        
        pt = self.assert_terms(pt, remove_none=True)

        if self.all_str_digit(lst=pt):
            pt_id = pt
        else:
            pt_id = self.find_pt(pt, ignore_case=ignore_case)

        subset_df = df[df['pt_id'].isin(pt_id)]
        subset_df['pt'] = self.find_pt(subset_df['pt_id'])
        
        return subset_df

    def find_llt_given_soc(self, soc=[], primary_soc_only=False, ignore_case=False, llt_current_only=True):
        """
        Find all LLTs (Lowest Level Terms) given a SOC (System Organ Class) name.

        Args:
            soc_name (str): The name of the SOC.
            primary_soc_only (bool, optional): If True, only return LLTs associated with the primary SOC. 
                                                Defaults to False.

        Returns:
            pandas.DataFrame: A DataFrame containing the LLTs associated with the given SOC. 
                                Each row represents an LLT and contains the LLT code and LLT name.
        """
        pt_df = self.find_pt_given_soc(soc=soc, primary_soc_only=primary_soc_only, ignore_case=ignore_case)
        llt_df = self.find_llt_given_pt(pt=pt_df['pt_id'], ignore_case=ignore_case, llt_current_only=llt_current_only)
        return llt_df.merge(pt_df, on='pt_id')

    def find_soc_given_pt(self, pt=[], primary_only=True, ignore_case=False):
        """
        Find the SOC (System Organ Class) given a list of PT (Preferred Term) names.

        Args:
            pt (list): A list of PT names.

        Returns:
            str: The name of the primary SOC.

        Raises:
            AssertionError: If pt is not a list.
        """
        df = self.mdhier
        pt = self.assert_terms(pt, remove_none=True)

        if self.all_str_digit(lst=pt):
            pt_id = pt
        else:
            pt_id = self.find_pt(pt, ignore_case=ignore_case)

        pt_soc = df[[0,4, 3,7, 11]]
        pt_soc.columns=['pt_id', 'pt', 'soc_id','soc','primary']
        if primary_only:
            pt_soc = pt_soc[pt_soc['primary'] == 'Y']

        out = pd.DataFrame(pt_id)
        out.columns = ['pt_id']
        
        out = out.merge(pt_soc, on='pt_id', how='left')

        return out

    def load_smq(self):
        if self.smq_list is None:
            try:
                tmp = pd.read_csv(os.path.join(self.folder_name, 'MedAscii', 'smq_list.asc'), delimiter='$', header=None)
                tmp = tmp.iloc[:, :-1]
                tmp.columns = ['smq_id', 'smq', 'smq_level', 'smq_description', 'smq_source', 'smq_note', 'MedDRA_version', 'smq_status', 'smq_algorithm']
                self.smq_list = tmp
            except pd.errors.EmptyDataError:
                self.smq_list = None
        if self.smq_content is None:
            try:
                tmp = pd.read_csv(os.path.join(self.folder_name, 'MedAscii', 'smq_content.asc'), delimiter='$', header=None)
                tmp = tmp.iloc[:, :-3]
                tmp.columns = ['smq_id', 'term_id', 'term_level', 'term_scope', 'term_category', 'term_weight', 'term_status']
                tmp['term_level'] = tmp['term_level'].astype(str)
                tmp.loc[tmp['term_level'] == '4', 'term_level'] = 'pt'
                tmp.loc[tmp['term_level'] == '5', 'term_level'] = 'llt'
                tmp.loc[tmp['term_level'] == '0', 'term_level'] = 'smq'
                self.smq_content = tmp
            except pd.errors.EmptyDataError:
                self.smq_content = None

    def find_smq(self, terms=[], with_detail=False, ignore_case=False):
        """
        Find all unique SMQ (Standard MedDRA Queries) terms.

        Args:
            terms (list, optional): The specific SMQ name(s) to filter the results. Defaults to an empty list.
            ignore_case (bool, optional): Flag to indicate whether to ignore case sensitivity when filtering terms. Defaults to False.

        Returns:
            list: A list of unique SMQ terms. If terms is provided, it returns the corresponding ids.

        Raises:
            AssertionError: If terms is not a list.
        """
        self.load_smq()
        if self.smq_list is None:
            return 'smq file not found'

        df = self.smq_list

        terms = self.assert_terms(terms)

        if len(terms) == 0:
            return df['smq'].tolist()

        if not with_detail:
            if self.all_str_digit(terms):
                return df[df['smq_id'].isin(terms)]['smq'].tolist()
            else:
                if ignore_case:
                    out = df[df['smq'].str.lower().isin([term.lower() for term in terms])]['smq_id'].tolist()
                else: 
                    out=df[df['smq'].isin(terms)]['smq_id'].tolist()
                return out
        else:
            if self.all_str_digit(terms):
                out = df[df['smq_id'].isin(terms)]
            else:
                if ignore_case:
                    out = df[df['smq'].str.lower().isin([term.lower() for term in terms])]
                else:
                    out = df[df['smq'].isin(terms)]
            return out

    def find_terms_given_smq(self, smq=[], ignore_case=False, active_only=True, narrow_only=True, llt_only=False, llt_current_only=True):
        """
        Find all terms related an SMQ (Standard MedDRA Query) name or a list of SMQ names.

        Args:
            smq (str or list): The name of the SMQ or a list of SMQ names.
            ignore_case (bool, optional): Flag to indicate whether to ignore case sensitivity when filtering terms. Defaults to False.

        Returns:
            pandas.DataFrame: A DataFrame containing the terms associated with the given SMQ(s). 
        """
        self.load_smq()
        df = self.smq_content

        smq = self.assert_terms(smq)
        if len(smq) == 0:
            return []
        if len(smq) > 1:
            print("Warning: Only the first element of smq will be used.")
            smq = smq[0]

        smq_details = self.find_smq(terms=smq, with_detail=True, ignore_case=ignore_case) 

        if narrow_only:
            keep_columns = ['term_id', 'term_level', 'term_status']
            if active_only:
                subset_df = df[(df['smq_id'].isin(smq_details['smq_id'])) & (df['term_scope'] == 2) & (df['term_status'] == 'A')]
            else:
                subset_df = df[(df['smq_id'].isin(smq_details['smq_id'])) & (df['term_scope'] == 2) ]
            out = self.find_terms_given_smq_sub(subset_df, keep_columns, llt_only=llt_only, llt_current_only=llt_current_only)
        else:
            if active_only:
                subset_df = df[(df['smq_id'].isin(smq_details['smq_id'])) & (df['term_status']=='A')]
            else:
                subset_df = df[(df['smq_id'].isin(smq_details['smq_id']))]

            
            if subset_df['term_category'].eq('A').all():
                keep_columns = ['term_id', 'term_level', 'term_status']
                out = self.find_terms_given_smq_sub(subset_df, keep_columns, llt_only=llt_only, llt_current_only=llt_current_only)
            elif set(subset_df['term_category'].unique()) == {'A', 'S'}:
                keep_columns = ['term_id', 'term_level', 'term_status']
                out = pd.DataFrame()
                for _ in range(5):
                    subset_df0 = subset_df[(subset_df['term_category'] == 'A')]
                    subset_df1 = subset_df[(subset_df['term_category'] == 'S')]
                    out1 = self.find_terms_given_smq_sub(subset_df0, keep_columns, llt_only=llt_only, llt_current_only=llt_current_only)
                    out1['term_associated_smq_level'] = _ + 1
                    out = pd.concat([out, out1], ignore_index=True)

                    if not subset_df1.empty:
                        unique_smq_ids = subset_df1['smq_id'].unique().tolist()
                        if active_only:
                            subset_df = df[(df['smq_id'].isin(unique_smq_ids)) & (df['term_status']=='A')]
                        else:
                            subset_df = df[(df['smq_id'].isin(unique_smq_ids))]
                    else:
                        break
            else:
                if 'Weight' in str(smq_details['smq_algorithm']):
                    keep_columns = ['term_id', 'term_level', 'term_status', 'term_category', 'term_weight']
                else:
                    keep_columns = ['term_id', 'term_level', 'term_status', 'term_category']
                out = self.find_terms_given_smq_sub(subset_df, keep_columns, llt_only=llt_only, llt_current_only=llt_current_only)
        return out

    def find_terms_given_smq_sub(self, subset_df, keep_columns, llt_only, llt_current_only):
        llt_df = subset_df.loc[subset_df['term_level'] == 'llt', keep_columns]
        llt_df['term'] = self.find_llt(llt_df['term_id'])
        pt_df = subset_df.loc[subset_df['term_level'] == 'pt', keep_columns]

        if llt_only:
            llt_df2 = self.find_llt_given_pt(pt_df['term_id'], llt_current_only=llt_current_only)
            llt_df2 = llt_df2.drop(columns=[2])
            llt_df2.columns = keep_columns
            out = pd.concat([llt_df, llt_df2], ignore_index=True)
        else:
            pt_df['term'] = self.find_pt(pt_df['term_id'])
            out = pd.concat([llt_df, pt_df], ignore_index=True)
        out.reset_index(drop=True, inplace=True)
        return out

    def load_fmq_default(self):
        if self.fmq_list_default is None:
            try:
                tmp = pd.read_csv(os.path.join(mtbp3.get_data('test_emt/FMQ'), "FMQ_Consolidated_List.csv"), delimiter=',', header=0)
                tmp = tmp.iloc[:, :-1]
                tmp.columns = ['fmq', 'pt', 'fmq_pt', 'classification']
                self.fmq_list_default = tmp
            except pd.errors.EmptyDataError:
                self.fmq_list_default = None

    def load_fmq(self):
        if self.fmq_list is None:
            self.load_fmq_default()
            self.fmq_list = self.fmq_list_default

    def find_fmq_file(self, file_path=""):
        if file_path=="": 
            self.load_fmq_default()
            self.fmq_list = self.fmq_list_default
            return f"Default FMQ table found. Table size: {str(self.fmq_list.shape)}"
        elif file_path and file_path.endswith(".csv") and os.path.isfile(file_path):
            try:
                tmp = pd.read_csv(file_path, delimiter=',', header=0)
                tmp = tmp.iloc[:, :-1]
                tmp.columns = ['fmq', 'pt', 'fmq_pt', 'classification']
                self.fmq_list = tmp
            except pd.errors.EmptyDataError:
                self.fmq_list_default = None
            return f"Specified FMQ CSV file found. Table size: {str(self.fmq_list.shape)}"
        else:
            return os.path.isfile(file_path)

    def save_fmq_consolidated_list_csv(self, folder_path=""):
        """
        Save the CSV file in the specified folder.

        Args:
            folder_path (str): The path of the folder where the CSV file should be saved.
        """
        if not os.path.isdir(folder_path):
            print("Error: Invalid folder path.")
            return
        
        self.load_fmq_default()
        new_file_path = os.path.join(folder_path, "FMQ_Consolidated_List.csv")
        self.fmq_list_default.to_csv(new_file_path, index=False)

    def find_fmq(self, fmq=[], narrow_only=True):
        """
        Find all unique FMQ (FDA Medical Queries) terms.

        Args:
            fmq (list, optional): The specific FMQ name(s) to filter the results. Defaults to an empty list.

        Returns:
            list: A list of unique FMQ terms. If fmq is provided, it returns the corresponding ids.

        Raises:
            AssertionError: If fmq is not a list.
        """
        self.load_fmq()
        fmq = self.assert_terms(fmq)

        if len(fmq) == 0:
            return list(self.fmq_list['fmq'].unique())
        else:
            assert isinstance(fmq, list), "fmq should be a list"
            tmp = self.fmq_list['fmq'].unique()
            return [e in tmp for e in fmq]

    def find_terms_given_fmq(self, fmq=[], ignore_case=False, narrow_only=True):
        """
        Find all terms related to an FMQ (FDA Medical Query) name or a list of FMQ names.

        Args:
            fmq (str or list): The name of the FMQ or a list of FMQ names.
            ignore_case (bool, optional): Flag to indicate whether to ignore case sensitivity when filtering terms. Defaults to False.

        Returns:
            pandas.DataFrame: A DataFrame containing the terms associated with the given FMQ(s). 
        """
        self.load_fmq()
        fmq0 = self.assert_terms(fmq)
        if len(fmq0) == 0:
            return pd.DataFrame()
        elif len(fmq0) == 1:
            fmq = fmq0
        elif len(fmq0) > 1:
            fmq = list(set(fmq0))
        else:
            raise AssertionError("fmq0 should be a list")

        df = self.fmq_list
        df = df.drop('fmq_pt', axis=1)

        if len(fmq) > 0:
            if ignore_case:
                df = df[df['fmq'].str.lower().isin([x.lower() for x in fmq])]
            else:
                df = df[df['fmq'].isin(fmq)]

        if narrow_only:
            df = df[df['classification'] == 'Narrow']
        return df


    def show_fmq_tree(self, fmq=[], with_soc=False, ignore_case=False, to_right=False):
        pt_df = self.find_terms_given_fmq(fmq=fmq, narrow_only=False, ignore_case=ignore_case)

        if with_soc:
            if self.demo:
                soc_list = self.find_soc()
                pt_given_soc = self.find_pt_given_soc(soc=soc_list[:3], primary_soc_only=True)
                pt_given_soc_sample = pt_given_soc.sample(n=len(pt_df), replace=True, axis=0)
                soc_df = self.find_soc_given_pt(pt=pt_given_soc_sample['pt_id'], primary_only=True, ignore_case=ignore_case)
                pt_df['soc'] = soc_df['soc']
            else:
                soc_df = self.find_soc_given_pt(pt=pt_df['pt'], primary_only=True, ignore_case=ignore_case)
                pt_df = pt_df.merge(soc_df[['pt','soc']], on='pt', how='left')

            pt_df = pt_df.sort_values(by=['fmq', 'classification', 'soc'])
            pt_df['ord2'] = pt_df.groupby(['fmq'])['pt'].transform(lambda x: x.factorize()[0] + 1)
            pt_df['ord2'] = pt_df['ord2'].astype(str).str.zfill(len(str(pt_df['ord2'].max())))

            if to_right:
                pt_df['fmq_class'] = 'FMQ/'+pt_df['fmq'] + '/' + pt_df['classification'] + ' [Classification]/'
                pt_df['fmq_class_soc'] = 'FMQ/'+pt_df['fmq'] + '/' + pt_df['classification'] + ' [Classification]/' + pt_df['soc'] + ' [SOC]/'
                pt_df['fmq_class_soc_pt'] = 'FMQ/'+pt_df['fmq'] + '/' + pt_df['classification'] + ' [Classification]/' + pt_df['soc'] + ' [SOC]/' + pt_df['pt'] + ' [PT' + pt_df['ord2'] + ']'
            else:
                pt_df['fmq_class'] = 'FMQ/'+pt_df['fmq'] + '/[Classification] ' + pt_df['classification'] + '/'
                pt_df['fmq_class_soc'] = 'FMQ/'+pt_df['fmq'] + '/[Classification] ' + pt_df['classification'] + '/[SOC] ' + pt_df['soc'] + '/'
                pt_df['fmq_class_soc_pt'] = 'FMQ/'+pt_df['fmq'] + '/[Classification] ' + pt_df['classification'] + '/[SOC] ' + pt_df['soc'] + '/[PT' + pt_df['ord2'] + '] ' + pt_df['pt']

            list0 = [f"FMQ/{fmq}/" for fmq in pt_df['fmq'].unique().tolist()]
            list1 = pt_df['fmq_class'].unique().tolist()
            lists = pt_df['fmq_class_soc'].unique().tolist()
            list2 = pt_df['fmq_class_soc_pt'].unique().tolist()
            tree = mtbp3.util.cdt.ListTree(lst = ['FMQ/']+list0+list1+lists+list2)
            return tree.list_tree(to_right=to_right)
        else:
            pt_df = pt_df.sort_values(by=['fmq', 'classification'])
            pt_df['ord2'] = pt_df.groupby(['fmq'])['pt'].transform(lambda x: x.factorize()[0] + 1)
            pt_df['ord2'] = pt_df['ord2'].astype(str).str.zfill(len(str(pt_df['ord2'].max())))
            list0 = [f"FMQ/{fmq}/" for fmq in pt_df['fmq'].unique().tolist()]

            if to_right:
                pt_df['fmq_class'] = 'FMQ/'+pt_df['fmq'] + '/' + pt_df['classification'] + ' [Classification]/'
                pt_df['fmq_class_pt'] = 'FMQ/'+pt_df['fmq'] + '/' + pt_df['classification'] + ' [Classification]/' + pt_df['pt'] + ' [PT' + pt_df['ord2'] + ']'
            else:
                pt_df['fmq_class'] = 'FMQ/'+pt_df['fmq'] + '/[Classification] ' + pt_df['classification'] + '/'
                pt_df['fmq_class_pt'] = 'FMQ/'+pt_df['fmq'] + '/[Classification] ' + pt_df['classification'] + '/[PT' + pt_df['ord2'] + '] ' + pt_df['pt']

            list1 = pt_df['fmq_class'].unique().tolist()
            list2 = pt_df['fmq_class_pt'].unique().tolist()
            tree = mtbp3.util.cdt.ListTree(lst = ['FMQ/']+list0+list1+list2)
            return tree.list_tree(to_right=to_right)

if __name__ == "__main__":
    pass
    #emt = Emt()
    #print(emt.find_files())
    #print(emt.find_fmq_file(file_path=""))
    #fmq_list = emt.find_fmq()
    #out=emt.show_fmq_tree(fmq=fmq_list[:2], with_soc=True, ignore_case=True, to_right=True)
    #print('\n'.join(out))


