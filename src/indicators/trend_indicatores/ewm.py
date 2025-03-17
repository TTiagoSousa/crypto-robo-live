def calculate_ewm(df, ema_lengths):
    
    # Cálculo das EMAs (EWM) com adjust=False
    for length in ema_lengths:
        df[f'ewm{length}'] = df['close'].ewm(span=length, adjust=False).mean()
    
    return df