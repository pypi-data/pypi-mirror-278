import pandas as pd
from perseo.main import milisec
import sys
from .template import Template

class Toolkit:

    def import_your_data_from_csv(self, input_data):
      try:
          data = pd.read_csv(input_data)

          return data
      except FileNotFoundError:
          print(f'File not found: {input_data}')
          return None
      except pd.errors.EmptyDataError:
          print(f'The CSV file is empty: {input_data}')
          return None
      except pd.errors.ParserError:
          print(f'Error parsing the CSV file: {input_data}')
          return None
      
    ## Check the status of the columns
    def check_status_column_names(self, data):
        column_names = ['model', 'pid', 'event_id', 'value', 'age', 'value_datatype', 'valueIRI', 'activity', 'unit', 'input', 'target', 'protocol_id', 'frequency_type', 'frequency_value', 'agent', 'startdate', 'enddate', 'comments']

        check_column_in_data = set(data.columns).issubset(column_names)
        
        if not check_column_in_data:
            sys.exit('Your CSV template contains column names that are not part of the accepted for the Toolkit. Accepted column names: {}'.format(column_names))
            
        for name in column_names:
            if name not in data.columns:
                data[name] = pd.Series(dtype=object)
                
        data = data.where(pd.notnull(data), None)

        return data
        
    ## Add ontological columns
    def add_columns_from_template(self,data):        
        print('Transforming and Validating....')

        data = data.where(pd.notnull(data), None)

        temp = Template.template_model
        final_df = pd.DataFrame()

        for row in data.iterrows():
            milisec_point = milisec()

            # Tag each row with the new of the model 
            new_row = {milisec_point : {'model': row[1]['model']}}

            # Include columns related to ontological terms:
            for cde in temp.items():
                if cde[0] == new_row[milisec_point]['model']:
                    new_row[milisec_point].update(cde[1])

            # Include columns from input CSV table:
            new_row[milisec_point].update({title: val for title, val in row[1].items() if val is not None})

            # Concate rows:
            final_row_df = pd.DataFrame(new_row[milisec_point], index=[1])
            if not final_row_df.empty and not final_row_df.isna().all().all():
                final_df = pd.concat([final_df, final_row_df], ignore_index=True)

        final_df = final_df.reset_index(drop=True)
        final_df = final_df.where(pd.notnull(final_df), None)
        return final_df

      
    def transform_shape_based_on_config(self, configuration, data):
        
        # Import static template for all CDE terms:
        temp = Template.template_model
        
        # Empty objects:
        final_df = pd.DataFrame()
        row_df = {}

        # Iterate each row from data input
        # check each YAML object from configuration file to set the parameters
        for row in data.iterrows():

            for config in configuration.items():

                # Create a unique stamp per new row to about them to colapse:
                milisec_point = milisec()

                row_df.update({milisec_point: {'model':config[1]['cde']}})
                
                # Add YAML template static information
                for cde in temp.items():
                    if cde[0] == row_df[milisec_point]['model']:
                        row_df[milisec_point].update(cde[1])

                # Relate each YAML parameter with original data input
                for element in config[1]['columns'].items():
                    for r in row[1].index:
                        if r == element[1]:
                            dict_element = {element[0]:row[1][r]}
                            row_df[milisec_point].update(dict_element)
                            
                # Store formed element into the final table:
                final_row_df = pd.DataFrame(row_df[milisec_point], index=[1])
                if not final_row_df.empty and not final_row_df.isna().all().all():
                    final_df = pd.concat([final_df, final_row_df], ignore_index=True)
        final_df = final_df.reset_index(drop=True)

        final_df = final_df.where(pd.notnull(final_df), None)
        return final_df

    ## Value edition
    def value_edition(self, data):
        not_null_data = pd.notnull(data)

        for index, row in data.iterrows():
            if not_null_data.loc[index, 'value']:
                value = data.loc[index, 'value']
                if row['value_datatype'] == 'xsd:string':
                    data.at[index, 'value_string'] = value
                elif row['value_datatype'] == 'xsd:float' and row['model'] not in ['Medication']:
                    data.at[index, 'value_float'] = value
                elif row['value_datatype'] == 'xsd:integer' and row['model'] not in ['Medication']:
                    data.at[index, 'value_integer'] = value
                elif row['value_datatype'] == 'xsd:date':
                    data.at[index, 'value_date'] = value
                elif row['model'] in ['Medication']:
                    data.at[index, 'concentration_value'] = value

            if 'valueIRI' in data.columns and not_null_data.loc[index, 'valueIRI']:
                value_iri = data.loc[index, 'valueIRI']
                
                if row['model'] in ['Sex', 'Status', 'Diagnosis', 'Phenotype', 'Clinical_trial', 'Body_measurement']:
                    data.at[index, 'attribute_type'] = value_iri
                    
                elif row['model'] in ['Imaging']:
                    data.at[index, 'output_id'] = value_iri
                    
                elif row['model'] in ['Genotype']:
                    data.at[index, 'output_type'] = value_iri

            if 'target' in data.columns and not_null_data.loc[index, 'target']:
                target = data.loc[index, 'target']
                    
                if row['model'] in ['Symptoms_onset', 'Lab_measurement', 'Surgical', 'Imaging', 'Questionnaire', 'Genotype']:
                    data.at[index, 'target_type'] = target

            if 'input' in data.columns and not_null_data.loc[index, 'input']:
                input_value = data.loc[index, 'input']
                
                if row['model'] in ['Genotype', 'Lab_measurement', 'Imaging', 'Biobank']:
                    data.at[index, 'input_type'] = input_value

            if 'agent' in data.columns and not_null_data.loc[index, 'agent']:
                agent = data.loc[index, 'agent']
                
                if row['model'] in ['Biobank', 'Clinical_trial']:
                    data.at[index, 'agent_id'] = agent
                    
                elif row['model'] in ['Medication', 'Surgery']:
                    data.at[index, 'substance_id'] = agent
                
                elif row['model'] in ['Genotype']:
                    data.at[index, 'attribute_type'] = agent

            if 'activity' in data.columns and not_null_data.loc[index, 'activity']:
                activity = data.loc[index, 'activity']
                
                if row['model'] in ['Disability', 'Lab_measurement', 'Imaging', 'Surgery', 'Genotype']:
                    data.at[index, 'specific_process_type'] = activity
                    
                elif row['model'] in ['Medication']:
                    data.at[index, 'activity_type'] = activity

            if 'unit' in data.columns and not_null_data.loc[index, 'unit']:
                unit_value = data.loc[index, 'unit']
                
                if row['model'] in ['Body_measurement', 'Lab_measurement']:
                    data.at[index, 'unit_type'] = unit_value
                    
                elif row['model'] in ['Medication']:
                    data.at[index, 'concentration_unit_type'] = unit_value
                    
        return data   

    # Time edition
    def time_edition(self, data):
        
        data = data.where(pd.notnull(data), None)

        for index, row in data.iterrows():
            ## From startdate to enddate
            
            if type(row['enddate']) == float or row['enddate'] == None: #TODO work on nan values to filter them better
                data.at[index, 'enddate'] = row['startdate']
                
        return data

    #Clean rows with no value
    
    def clean_empty_rows(self, data):
        
        data = data.where(pd.notnull(data), None)
        columns_to_check = ['value', 'valueIRI', 'activity', 'target', 'agent']

        for row in data.iterrows():
            if all(row[1][col] is None for col in columns_to_check):
                if row[1]['model'] not in ['Biobank', 'Consent_used', 'Consent_contacted']: 
                    data = data.drop(row[0])
        return data
    
    def delete_extra_columns(self, data):
        columns_to_delete = ['value', 'valueIRI', 'target', 'agent', 'input', 'activity', 'unit']
        
        for column in columns_to_delete:
            if column in data.columns:
                del data[column]

        return data
    
    def unique_id_generation(self,data):
        data['uniqid'] = ''

        for i in data.index:
            data.at[i, 'uniqid'] = milisec()
        
        return data

    def whole_quality_control(self,input_data):

        imported_file = self.import_your_data_from_csv(input_data)
        
        if imported_file is not None:
            print('CSV file imported successfully.')
        else:
            print('CSV file import failed. Please check the file path and format.')

        columns_names_conformation = self.check_status_column_names(imported_file)
        
        table_with_template_addition = self.add_columns_from_template(columns_names_conformation)

        table_with_value_edited = self.value_edition(table_with_template_addition)

        table_with_time_corrected = self.time_edition(table_with_value_edited)

        table_with_blanks_cleaned = self.clean_empty_rows(table_with_time_corrected)

        table_extra_column_deleted = self.delete_extra_columns(table_with_blanks_cleaned)

        table_with_uniqid = self.unique_id_generation(table_extra_column_deleted)

        if table_with_uniqid is not None:
            print('CSV data transformation done.')
        else:
            sys.exit('CSV file quiality control failed. Please check the columns names, every required column is not present')

        return table_with_uniqid
      
      
    def yaml_quality_control(self,input_data,configuration):

        imported_file = self.import_your_data_from_csv(input_data)
        if imported_file is not None:
            print('CSV file imported successfully.')
        else:
            print('CSV file import failed. Please check the file path and format.')

        # columns_names_conformation = self.check_status_column_names(imported_file)
        # if columns_names_conformation is not None:
        #     print('Every CSV columns present.')
        # else:
        #     sys.exit('CSV file quiality control failed. Please check the columns names, every required column is not present')

        table_with_template_addition = self.transform_shape_based_on_config(configuration=configuration, data=imported_file)

        table_with_value_edited = self.value_edition(table_with_template_addition)

        table_with_time_corrected = self.time_edition(table_with_value_edited)

        table_with_blanks_cleaned = self.clean_empty_rows(table_with_time_corrected)

        table_extra_column_deleted = self.delete_extra_columns(table_with_blanks_cleaned)

        table_with_uniqid = self.unique_id_generation(table_extra_column_deleted)

        if table_with_uniqid is not None:
            print('CSV data transformation done.')
        else:
            print('CSV data transformation failed. Something went wrong during transformation.')

        return table_with_uniqid
