import pandas as pd
import ast

def load_and_process_data(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath)

    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Convert Support and Resistance columns from string to lists
    df['Support'] = df['Support'].apply(ast.literal_eval)
    df['Resistance'] = df['Resistance'].apply(ast.literal_eval)

    # Safely compute min and max only for non-empty lists
    df['support_min'] = df['Support'].apply(lambda x: min(x) if x else None)
    df['support_max'] = df['Support'].apply(lambda x: max(x) if x else None)
    df['resistance_min'] = df['Resistance'].apply(lambda x: min(x) if x else None)
    df['resistance_max'] = df['Resistance'].apply(lambda x: max(x) if x else None)

    # Add is_bullish and Trend columns for chatbot logic
    df['is_bullish'] = df['close'] > df['open']
    df['Trend'] = df.apply(lambda row: 'Bullish' if row['close'] > row['open'] else 'Bearish', axis=1)

    return df
