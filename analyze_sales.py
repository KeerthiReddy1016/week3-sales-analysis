
from pathlib import Path
import pandas as pd

# Paths
DATA_PATH = Path('data/sales.csv')   # adjust if your file is elsewhere
REPORT_PATH = Path('REPORT.md')

def load_data(path: Path) -> pd.DataFrame:
    """Load the CSV and return a DataFrame. Raises if not found."""
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {path.resolve()}")
    df = pd.read_csv(path, parse_dates=['date'])
    return df

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Basic cleaning: fill missing prices, drop non-positive quantities."""
    if 'unit_price' in df.columns:
        df['unit_price'] = df['unit_price'].fillna(df['unit_price'].median())
    if 'quantity' in df.columns:
        df = df[df['quantity'] > 0].copy()
    df['total'] = df['quantity'] * df['unit_price']
    return df

def analyze(df: pd.DataFrame):
    """Compute simple stats and produce a small summary report string."""
    total_sales = df['total'].sum()
    product_totals = df.groupby('product', as_index=False)['total'].sum().sort_values('total', ascending=False)

    lines = []
    lines.append(f"Total sales: {total_sales:.2f}")
    lines.append("") 
    lines.append("Revenue by product:")
    for _, row in product_totals.iterrows():
        lines.append(f"- {row['product']}: {row['total']:.2f}")

    # best product
    best = product_totals.iloc[0] if len(product_totals) > 0 else None
    if best is not None:
        lines.append("")
        lines.append(f"Best selling product: {best['product']} ({best['total']:.2f})")

    return "\n".join(lines)

def main():
    df = load_data(DATA_PATH)           # <- this defines df
    print("Loaded data (first 5 rows):")
    print(df.head(), "\n")

    df = clean_data(df)
    summary = analyze(df)

    REPORT_PATH.write_text(summary)
    print(f"Report saved to {REPORT_PATH.resolve()}")
    print("\nSummary:\n")
    print(summary)

if __name__ == '__main__':
  main()