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

import numpy as np
import pandas as pd

def diff_2cols_in_1df(df, col1='ARM', col2='ACTARM', keep_diff_only=False):
    """
    Calculate the difference between two columns in a DataFrame.

    Args:
        df (pandas.DataFrame): The DataFrame containing the columns to compare.
        col1 (str): The name of the first column to compare. Default is 'ARM'.
        col2 (str): The name of the second column to compare. Default is 'ACTARM'.

    Returns:
        pandas.DataFrame or str: If there is a difference between the two columns, 
        a DataFrame is returned with the unique combinations of values in col1 and col2,
        along with a 'diff' column indicating whether the values are different ('True') or not ('').
        If there is no difference between the two columns, the string "The two columns are the same." is returned.
    """

    if not col1 or not col2:
        return "Both col1 and col2 must be provided."
    if not isinstance(df, pd.DataFrame):
        return "Input is not a DataFrame."
    if col1 not in df.columns:
        return f"Column '{col1}' does not exist in the DataFrame."
    if col2 not in df.columns:
        return f"Column '{col2}' does not exist in the DataFrame."
    if col1 == col2:
        return f"Columns should be different."
    
    diff = df[col1].ne(df[col2]).any()
    if diff:
        out = df.groupby([col1, col2], dropna=False).size().reset_index(name='count')
        out['diff'] = (out[col1] != out[col2]).map(lambda x: "" if x==False else "True")
        if keep_diff_only:
            out = out[out['diff']=='True']
            out = out.drop(columns=['diff'])
        else:
            out[col2] = out[col2].where(out['diff'] != '', '(same)')
            out = out.drop(columns=['diff'])
        return out
    else:
        return pd.DataFrame()
        
def diff_2cols_in_2df(df1, df2, col, gp):
    """
    Check if a column exists in both dataframes.

    Args:
        df1 (pandas.DataFrame): The first dataframe.
        df2 (pandas.DataFrame): The second dataframe.
        col (str): The column to check.
        gp (str): The group column.

    Returns:
        bool: True if the column exists in both dataframes, False otherwise.
    """
    if not isinstance(df1, pd.DataFrame) or not isinstance(df2, pd.DataFrame):
        return "Input is not a DataFrame."
    if not col or not isinstance(col, str):
        return "col should be a non-empty string."
    if not gp or not isinstance(gp, str):
        return "gp should be a non-empty string."
    if col not in df1.columns or col not in df2.columns:
        return f"Column '{col}' not found in both dataframes."
    if gp not in df1.columns or gp not in df2.columns:
        return f"Group '{gp}' not found in both dataframes."
    if gp == col:
        return "Columns 'gp' and 'col' should be different columns."
    if not df1[col].is_unique:
        return f"All values in column '{col}' of df1 should be unique."
    if not df2[col].is_unique:
        return f"All values in column '{col}' of df2 should be unique."

    df1 = df1[[col, gp]]
    df1.rename(columns={gp: f'{gp}1'}, inplace=True)
    df2 = df2[[col, gp]]
    df2.rename(columns={gp: f'{gp}2'}, inplace=True)
    df1['source1'] = 'True'
    df2['source2'] = 'True'

    merged_df = pd.merge(df1, df2, on=col, how='outer', indicator=True)
    
    summary = merged_df.groupby([f'{gp}1', f'{gp}2', 'source1', 'source2'], dropna=False).size().reset_index(name='count')
    summary.fillna('(missing)', inplace=True)
    return summary

def summarize_1nc_by_2group(df=None, column="", cutoff=None, group_col0="", group_col1="", to_cat=True):
    """
    Create a summary dataframe that shows the percentage of NaN values and values less than a cutoff point in a numerical column.

    Args:
        df (pandas.DataFrame): The input dataframe.
        column (str): The name of the numerical column.
        cutoff (float): The cutoff point.
        group_col0 (str): The first group column.
        group_col1 (str): The second group column.
        to_cat (bool): Whether to categorize the column based on the cutoff point.

    Returns:
        pandas.DataFrame: A summary dataframe with two columns: 'NaN Percentage' and 'Below Cutoff Percentage', pivoted by group_col1.

    Raises:
        ValueError: If the input is not a DataFrame or if the column is not a string or does not exist in the DataFrame.
        ValueError: If the group_col0 or group_col1 is not a string or does not exist in the DataFrame.
        ValueError: If the column is not a numerical column.

    """
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input is not a DataFrame.")
    if not column or not isinstance(column, str):
        raise ValueError("column should be a non-empty string.")
    if column not in df.columns:
        raise ValueError(f"Column '{column}' does not exist in the DataFrame.")
    
    # Convert column to numerical
    df[column+'_num'] = pd.to_numeric(df[column], errors='coerce').copy()
    tmp = diff_2cols_in_1df(df, col1=column, col2=column+'_num', keep_diff_only=True)
    df[column]=df[column+'_num'].copy()
    
    if not pd.api.types.is_numeric_dtype(df[column]):
        raise ValueError(f"Column '{column}' is not a numerical column.")
    if not group_col0 or not isinstance(group_col0, str):
        raise ValueError("group_col0 should be a non-empty string.")
    if group_col0 not in df.columns:
        raise ValueError(f"Column '{group_col0}' does not exist in the DataFrame.")
    if not group_col1 or not isinstance(group_col1, str):
        raise ValueError("group_col1 should be a non-empty string.")
    if group_col1 not in df.columns:
        raise ValueError(f"Column '{group_col1}' does not exist in the DataFrame.")
    
    if to_cat:
        if cutoff and cutoff > df[column].min() and cutoff < df[column].max() and df[column].max() != df[column].min():
            df['Ind'] = df.apply(lambda row: 1 if row[column] < cutoff else 0, axis=1)
            df['Indna'] = (~df[column].isna()).astype(int)
            summary_df = pd.DataFrame({'Total': df.groupby([group_col0, group_col1], dropna=False)['Indna'].sum()})
            summary_df['Count'] = df.groupby([group_col0, group_col1], dropna=False)['Ind'].sum()
        else:
            df['Ind'] = df[column].isna().astype(int)
            summary_df = pd.DataFrame({'Total': df.groupby([group_col0, group_col1], dropna=False)[column].size()})
            summary_df['Count'] = df.groupby([group_col0, group_col1], dropna=False)['Ind'].sum()

        summary_df['Percentage'] = summary_df.apply(lambda row: f"{row['Count']}/{row['Total']} ({(row['Count'] / row['Total']) * 100:.1f})", axis=1)
        out = summary_df.reset_index().pivot(index=group_col0, columns=group_col1, values='Percentage')
    else:
        summary_df = df.groupby([group_col0, group_col1])[column].agg(['mean', 'std']) 
        summary_df.columns = ['Mean', 'SD']
        summary_df['Mean_w_SD'] = summary_df.apply(lambda row: f"{row['Mean']:.1f} ({SD:.1f})", axis=1)
        out = summary_df.reset_index().pivot(index=group_col0, columns=group_col1, values='Mean_w_SD')

    return [out, tmp]

class ListTree:
    def __init__(self, lst=[], label=[], infmt='path'):
        self.lst = lst
        self.label = label
        self.infmt = infmt
        self.df = pd.DataFrame()
        self.prelst = pd.DataFrame()
        self.out = pd.DataFrame()
    
    def __list_tree_df(self):
        if not isinstance(self.lst, list):
            print('Input should be a list.')
            self.df = pd.DataFrame()
            return
        
        if not self.lst:
            print('Input should be a nonempty list.')
            self.df = pd.DataFrame()
            return
        
        if len(self.lst) <= 1:
            self.df = pd.DataFrame(self.lst, columns=['lst'])
            return
        
        if self.infmt == 'dotspace':
            df0 = pd.DataFrame([[line.split(' ', 1)[0]]+[line] for line in self.lst], columns=['c1', 'property'])
            df0['property'] = df0['property'].apply(lambda x: x.split(' ', 1)[1] if '.pseudo' in x else x)
            df0['lst'] = df0['c1'].str.replace('.', '/')
            df0['lst'] = df0['lst'].apply(lambda x: '/'.join([part.zfill(3) for part in x.split('/')]))
            df0['lst'] = df0['lst'].apply(lambda x: x + '/' if df0['lst'].str.contains(x+'/').any() else x)
            df0 = df0.drop('c1', axis=1)
            df0 = df0.sort_values('lst').reset_index(drop=True)
        else:
            df0 = pd.DataFrame(self.lst, columns=['lst'])
            if len(self.label) > 0:
                df0['property'] = self.label
            else:
                df0['property'] = ''

        df0['lst'] = df0['lst'].str.replace('^/', '', regex=True)
        df0['type'] = df0['lst'].apply(lambda x: True if x.endswith('/') else False)
        
        for index, row in df0.iterrows():
            r0, r1 = row['lst'].rsplit('/', 1)
            if r1 == "":
                if '/' in r0:
                    s0, s1 = r0.rsplit('/',1)
                    df0.loc[index, 't1'] = s0
                    df0.loc[index, 't0'] = s1
                else:
                    df0.loc[index, 't1'] = ""
                    df0.loc[index, 't0'] = r0
            else:
                df0.loc[index, 't1'] = r0
                df0.loc[index, 't0'] = r1
                
        df0 = df0.sort_values(by=['lst']).reset_index(drop=True)
        df0['level'] = df0['lst'].str.count('/') + 1
        df0['level'] = df0['level'] - df0['type']
        
        if df0['level'].min() > 0:
            df0['level'] = df0['level'] - df0['level'].min() + 1
        
        df0['row_index'] = df0.index
        df0 = df0[['lst', 'type', 't1', 't0', 'level', 'row_index', 'property']]
        
        self.df = df0.groupby(df0.columns.difference(['property', 'row_index']).tolist(), sort=False).agg({'row_index': 'max', 'property': lambda x: ''.join(x)}).reset_index().sort_values('row_index')
    
    def __list_tree_pre(self, to_right=False):
        self.__list_tree_df()
        if self.df.empty:
            self.prelst = self.df
            return self.prelst
        
        max_level = self.df['level'].max()
        prelst = pd.DataFrame("", index=self.df.index, columns=range(max_level))
        prelst = pd.DataFrame([['' for _ in range(self.df['level'].max())] for _ in range(len(self.df))])
        prelst = pd.concat([prelst, self.df[['t0','property','t1','type','level','row_index']]], axis=1).sort_values('row_index')
        prelst.reset_index(drop=True, inplace=True)
        prelst['row_index'] = prelst.index
        
        if to_right:
            pre = ['', '    ', '   │', ' ──┤', ' ──┘', '  ']
        else:
            pre = ['', '    ', '│   ', '├── ', '└── ', '  ']
        
        t1_list = prelst[prelst['type'] == True][['t1','level','t0']]
        
        if t1_list.empty:
            self.prelst = self.df['lst']
            return self.prelst
        
        for index, row in prelst.iterrows():
            if row['level'] > 0:
                prelst.loc[index, :(row['level'] - 1)] = [pre[1]] * (row['level'])
        
        for index, row in t1_list.iterrows():
            index_set = prelst[prelst['t1'] == row['t1']+'/'+row['t0']]['row_index']
            
            if row['t1'] == "":
                index_set = prelst[prelst['t1'] == row['t0']]['row_index']
            else:
                index_set = prelst[prelst['t1'] == row['t1']+'/'+row['t0']]['row_index']
            
            if not index_set.empty:
                min_row_index = index_set.min()
                max_row_index = index_set.max()
                prelst.loc[(min_row_index):(max_row_index), row['level']] = [pre[2]] * (max_row_index - min_row_index + 1)
                prelst.loc[index_set, row['level']] = [pre[3]] * len(index_set)
                prelst.loc[max_row_index, row['level']] = pre[4]
        
        if to_right:
            prelst['t0'] = prelst.apply(lambda row: row['t0'] if row['type'] == True else row['t0'], axis=1)
            prelst = prelst.loc[:, :'property']
            prelst = prelst.iloc[:, ::-1]
        else:
            prelst['t0'] = prelst.apply(lambda row: row['t0'] + ':' if row['type'] == True else row['t0'], axis=1)
            prelst = prelst.loc[:, :'property']

        if self.infmt == 'dotspace':
            prelst['t0'] = ''
        
        self.prelst = prelst
    
    def list_tree(self, to_right=False):
        self.__list_tree_pre(to_right=to_right)
        
        if self.prelst.empty:
            self.out = pd.DataFrame()
            return self.out
        
        out_joined = self.prelst.apply(lambda row: ''.join(row), axis=1)
        
        if to_right:
            max_length = out_joined.str.len().max()
            out_joined = out_joined.apply(lambda x: x.rjust(max_length))
        
        self.out = out_joined
        return self.out

if __name__ == "__main__":
    pass

