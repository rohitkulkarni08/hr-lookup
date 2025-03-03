import os
import openai
import json
import re
import pandas as pd

openai.api_key = os.getenv("OPENAI_API_KEY")

class EmployeeQuerySystem:
    def __init__(self, schema_file, employee_file, progress_file, project_file):
        self.schema_doc = self.load_schema(schema_file)
        self.employee_fact_table = self.load_and_clean_data(employee_file)
        self.progress_table_fact = self.load_and_clean_data(progress_file)
        self.project_table_dim = self.load_and_clean_data(project_file)
        self.progress_table = self.aggregate_table(self.progress_table_fact, 'EmployeeID')
        self.project_table = self.aggregate_table(self.project_table_dim, 'EmployeeID')
    
    def load_schema(self, schema_file):
        with open(schema_file, 'r') as file:
            return file.read()
    
    def load_and_clean_data(self, file_path):
        df = pd.read_csv(file_path)
        df.columns = df.columns.str.replace(' ', '')
        return df
    
    def aggregate_table(self, df, groupby_column):
        return df.groupby(groupby_column).agg(lambda x: list(x)).reset_index()
    
    def question_processing_prompt(self, question):
        return f"""Your task is to analyze the provided question, identify the specific information being requested, and retrieve the relevant table and field(s) from the schema document to answer accurately. Always include EmployeeID and EmployeeName from the employee_fact_table to enable necessary joins.
        
        Ensure the output is strictly JSON formatted.
        If the requested information does not exist, set `status` to `not_found`.
        
        Question:
        {question}
        
        Schema Document:
        {self.schema_doc}
        """
    
    def json_parser(self, gpt_output):
        if gpt_output.startswith("```json"):
            gpt_output = gpt_output[7:]
        if gpt_output.endswith("```"):
            gpt_output = gpt_output[:-3]
        
        try:
            return json.loads(gpt_output.strip())
        except json.JSONDecodeError as e:
            print("JSONDecodeError:", e)
            return {}
    
    def question_processing_gpt4_output(self, question):
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": self.question_processing_prompt(question)}],
            max_tokens=512,
            temperature=0
        )
        return self.json_parser(response["choices"][0]["message"]["content"])
    
    def question_answering_gpt4_output(self, question, data_dict):
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": self.question_answering_prompt(question, data_dict)}],
            max_tokens=512,
            temperature=0
        )
        return response["choices"][0]["message"]["content"]
    
    def question_answering_prompt(self, question, data_dict):
        return f"""Analyze the given question and provide a natural, structured response using the provided table data.
        If no data is available, inform the user clearly.
        
        Question:
        {question}
        
        Data Dictionary:
        {data_dict}
        """
    
    def handle_question(self, question_text):
        table_dict = self.question_processing_gpt4_output(question_text)
        
        if table_dict.get("status") == "found":
            result_df = None

            for table in table_dict["tables"]:
                table_name = table["table_name"]
                fields = table["fields"]

                df_to_join = getattr(self, table_name)[fields]

                if result_df is None:
                    result_df = df_to_join
                else:
                    result_df = pd.merge(
                        result_df,
                        df_to_join,
                        on='EmployeeID',
                        how='left'
                    )

            df_json = result_df.to_json(orient="records")
            df_dict = json.loads(df_json)
            answer = self.question_answering_gpt4_output(question_text, df_dict)
            answer = ' '.join(answer.replace("\\n", "\n").split())
        else:
            answer = table_dict.get("message", "The requested information is not available.")

        print("\nResponse:", answer, '\n')

def main():
    system = EmployeeQuerySystem('database_schema.txt', 'employee_fact_table.csv', 'progress_table.csv', 'project_table.csv')
    print("Employee Query System (Type 'stop' to end)")
    while True:
        question_text = input("Ask your question: ")
        if question_text.lower() == 'stop':
            break
        system.handle_question(question_text)

if __name__ == "__main__":
    main()
