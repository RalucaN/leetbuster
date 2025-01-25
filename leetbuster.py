import pandas as pd
import time
from modules.identifier import analyze_text
from modules.normalizer import normalize
from modules.resolver import extract_final_text


class LeetBuster:
    def __init__(self, verbose=False):
        self.verbose = verbose

    def process(self, input_data, text_column='text'):
        start_time = time.time()

        if isinstance(input_data, str):
            result = self._process_single(input_data)
        elif isinstance(input_data, list):
            result = self._process_multiple(input_data)
        elif isinstance(input_data, pd.DataFrame):
            result = self._process_dataframe(input_data, text_column)
        else:
            raise ValueError("Input must be a string, list of strings, or pandas DataFrame")

        print(f'Total processing time: {time.time() - start_time:.2f} seconds')

        return result

    def _process_single(self, text):
        leets, _ = analyze_text(text, self.verbose)
        candidates = {key: list(normalize(key)) for key in leets}
        return extract_final_text([text], [candidates])[0]

    def _process_multiple(self, texts):
        list_of_candidates = []
        for text in texts:
            leets, _ = analyze_text(text, self.verbose)
            candidates = {key: list(normalize(key)) for key in leets}
            list_of_candidates.append(candidates)
        return extract_final_text(texts, list_of_candidates)

    def _process_dataframe(self, df, text_column):
        if text_column not in df.columns:
            raise ValueError(f"DataFrame must contain a '{text_column}' column")
        
        texts = df[text_column].tolist()
        results = self._process_multiple(texts)
        
        df_result = df.copy()
        df_result['resolved_text'] = results
        return df_result
    


if __name__ == "__main__":
    leet_buster = LeetBuster(verbose=True)

    # Process a single string
    single_result = leet_buster.process("w0rld!")
    print("Single string result:", single_result)
    single_result = leet_buster.process("H3ll0 w0rld!")
    print("Single string result:", single_result)

    # Process a list of strings
    list_result = leet_buster.process(["H3ll0 w0rld!", "1337 sp34k"])
    print("List result:", list_result)

    # Process a DataFrame with a custom column name
    df = pd.DataFrame({'message': ["H3ll0 w0rld!", "1337 sp34k"]})
    df_result = leet_buster.process(df, text_column='message')
    print("DataFrame result:")
    print(df_result)
