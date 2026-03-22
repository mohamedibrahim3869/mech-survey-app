import pandas as pd
import os

# Define common aliases for engineering columns
COLUMN_ALIASES = {
    'name': ['part name', 'item', 'description', 'mark', 'pos'],
    'length': ['length', 'len', 'l (mm)', 'l'],
    'width': ['width', 'w (mm)', 'w', 'breadth'],
    'thickness': ['thickness', 'thk', 't', 't (mm)', 'plate thk'],
    'material': ['material', 'mat', 'spec', 'grade'],
    'quantity': ['quantity', 'qty', 'count', 'nos']
}

def smart_load_survey(file_path):
    ext = os.path.splitext(file_path)[-1].lower()
    df = pd.read_excel(file_path) if ext in ['.xlsx', '.xls'] else pd.read_csv(file_path)
    
    # Clean column names
    df.columns = [str(c).strip().lower() for c in df.columns]
    
    mapping = {}
    # Try to find a match for each required field
    for internal_name, aliases in COLUMN_ALIASES.items():
        for col in df.columns:
            if col in aliases:
                mapping[col] = internal_name
                break
    
    # Rename the columns we found to our internal standard
    df = df.rename(columns=mapping)
    
    # Return only the columns we successfully mapped
    standard_cols = ['name', 'length', 'width', 'thickness', 'material', 'quantity']
    available_cols = [c for c in standard_cols if c in df.columns]
    
    return df[available_cols]
