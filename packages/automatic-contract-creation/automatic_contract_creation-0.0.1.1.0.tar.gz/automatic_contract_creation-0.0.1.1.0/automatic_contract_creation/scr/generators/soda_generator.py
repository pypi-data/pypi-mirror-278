from automatic_contract_creation.scr.generators.contract_variable import ContractVariable
import re
from typing import Optional

class SODAGenerator(ContractVariable):
    def __init__(self, connection_name: str, **creds):
        super().__init__(connection_name, **creds)

    def generate_soda_yaml(self, table_name, dtypes, where_clause, checks_config_dict: dict, col_check):
        soda_yaml = f"""dataset: {table_name}
        """
        if where_clause:
            soda_yaml +=f"""
filter_sql: | 
    {where_clause}
    """
        soda_yaml+=f"""
columns:"""

        for nm_col in dtypes['column_name']:
            column_info = f"""
- name: {nm_col}
  data_type: {dtypes[dtypes['column_name'] == nm_col]['data_type'].values[0]}"""

            if nm_col in col_check:
                column_info += """
  checks:"""

                for check_type, check_config in checks_config_dict.items():
                    if check_type != 'regex_columns' and nm_col in check_config.get('columns', []):
                        if check_type == 'duplicate_count' or check_type == 'missing_count':
                            column_info += f"""
  - type: {check_type}"""
                        if check_type == 'invalid_count':
                            column_info += f"""
  - type: {check_type}"""
                            if 'valid_min' in list(check_config['valid_format_dict'][nm_col].keys()):
                                column_info += f"""
    valid_min: {check_config['valid_format_dict'][nm_col]['valid_min']}
    valid_max: {check_config['valid_format_dict'][nm_col]['valid_max']}"""

                            if 'valid_regex' in list(check_config['valid_format_dict'][nm_col]):
                                column_info += f"""
    valid_regex_sql: '{check_config['valid_format_dict'][nm_col]['valid_regex']}'"""

                            if 'valid_values' in list(check_config['valid_format_dict'][nm_col].keys()):
                                column_info += f"""
    valid_values: {check_config['valid_format_dict'][nm_col]['valid_values']}"""

                        column_info += f"""
    must_be: 0"""

            column_info += "\n"
            soda_yaml += column_info

        return soda_yaml


    def generate_soda_contracts(self, query: str, parameters: Optional[dict] = None):
        table_name = re.search(r'from\s+(?:[\w\-\."])+\.(\w+)\b', query).group(1)
        where_clause = re.search(r'\bWHERE\b\s*(.*?)(?=\sGROUP\sBY|\s*LIMIT|\s*$)', query, re.IGNORECASE)
        where_clause = where_clause.group(1) if where_clause else None
        checks_config_dict, dtypes, col_check = self.get_checks_config(query, parameters)

        soda_yaml = self.generate_soda_yaml(table_name, dtypes, where_clause, checks_config_dict, col_check)
        yaml_file = f'{table_name}_contract.yml'
        with open(yaml_file, "w", encoding='utf-8') as log_file:
            log_file.write(str(soda_yaml) + '\n')
        # print(soda_yaml)
