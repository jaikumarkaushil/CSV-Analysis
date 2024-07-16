import streamlit as st
import pandas as pd

def read_csv(file):
    try:
        return pd.read_csv(file)
    except pd.errors.EmptyDataError:
        st.error("No columns to parse from file. The file may be empty or not properly formatted.")
        return None
    except Exception as e:
        st.error(f"Error reading the CSV file: {e}")
        return None

def filter_csv(df1, df2, col1, col2):
    # Check that the selected columns exist
    if col1 not in df1.columns or col2 not in df2.columns:
        st.error("Selected columns do not exist in the respective CSV files.")
        return None

    # Extract the mobile numbers
    mobile_numbers_to_remove = df2[col2]

    # Filter out entries from the first CSV
    filtered_df = df1[~df1[col1].isin(mobile_numbers_to_remove)]

    return filtered_df

def find_duplicates(df, column):
    # Find duplicate entries in the specified column
    duplicates = df[df.duplicated(subset=[column], keep=False)]
    # Filter out duplicates to get unique entries
    unique_df = df.drop_duplicates(subset=[column])
    return duplicates, unique_df

def main():
    st.title('CSV Filter based on Mobile Numbers')

    st.write("Upload the two CSV files to process. Select the column in each file containing the mobile numbers.")

    # File upload
    file1 = st.file_uploader("Upload the first CSV file", type="csv")
    file2 = st.file_uploader("Upload the second CSV file with data to filter out", type="csv")

    if file1 and file2:
        df1 = read_csv(file1)
        df2 = read_csv(file2)

        if df1 is not None and df2 is not None:
            # Select columns
            col1 = st.selectbox("Select the column with mobile numbers in the first CSV file", df1.columns)
            col2 = st.selectbox("Select the column with mobile numbers in the second CSV file", df2.columns)

            if st.button('Filter CSV'):
                filtered_df = filter_csv(df1, df2, col1, col2)
                
                if filtered_df is not None:
                    st.write("Filtered Data")
                    st.dataframe(filtered_df)

                    # Download the filtered data
                    csv = filtered_df.to_csv(index=False)
                    st.download_button(label="Download Filtered CSV", data=csv, mime='text/csv')
    
    st.title('Duplicate Entry Detector in CSV')

    st.write("Upload a CSV file and select the column to check for duplicate entries.")

    # File upload
    file = st.file_uploader("Upload the CSV file", type="csv")

    if file:
        df = pd.read_csv(file)

        if df is not None:
            # Select column
            column = st.selectbox("Select the column to check for duplicates", df.columns)

            if st.button('Find Duplicates'):
                duplicates, unique_df = find_duplicates(df, column)
                
                if not duplicates.empty:
                    st.write("Duplicate Entries")
                    st.dataframe(duplicates)
                else:
                    st.write("No duplicate entries found.")

                st.write("Filtered Data (No Duplicates)")
                st.dataframe(unique_df)

                # Download the filtered data
                csv = unique_df.to_csv(index=False)
                st.download_button(label="Download Filtered CSV", data=csv, mime='text/csv')

if __name__ == "__main__":
    main()
