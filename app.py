import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Set page config
st.set_page_config(
    page_title="Biolume: ALLGEN TRADING Inventory System",
    page_icon=":shopping_bags:",
)

# Google Sheets credentials
SCOPES = ["https://docs.google.com/spreadsheets/d/1oKiXawV6KXYuZt94oyHXxTuaXkSBDh9uEF02DpngToU", "https://www.googleapis.com/auth/drive"]
CREDS = ServiceAccountCredentials.from_json_keyfile_dict({
    "type": "service_account",
    "project_id": "biolume-is",
    "private_key_id": "0cdb2828674625dc1719a93f5338fdb8a5416bc5",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCdDuDRHV3YAm0t\nDouzC8PHfzXzEA1mFZco+qpsGnjN0XkdwlNFxmvnlWp9o8qd4+NUlUFLR3N3cHqE\nBcN2ilT6LZKaHGdwdPd6C/uBNjWuLwpuNCuOoeRTHnFLkJqnYmQytgfB7Kzz2qQG\n/wzx9xOZPOR9oEUG4NcZr9ISk40xfRUqDvjpImZCaYO68Dd2Q/SFRQnudlAlQHiz\nZhrwdsvkfV6o85K89Eh2msFJEZ/6uvZTNHd2JR1seLOPN30hcpOLhx02bb+kRcUH\n7bjX5rFscd0A30UAB6q9Gz5KMVD6j6/dfw0wj8DuGco3/FyJ5MfciK4j/XLBeA2F\nz60hX40LAgMBAAECggEAAx2McBl5BxPlPoOPWdnd5FMtqsiiu2eqO/Hc94/+3XZO\nRLzaEgRBl7JrDlr1ZfRjSgY76VZdf/0HMR88JVnRHbVRtyThGGX5kr4yGvoMTow4\nVL9MLeQgN1XfQXR43OEiw67AsKQVOjEYF9tvUk1oYh3HGobXV6+WFLhcHmo23sho\nckOTo1u5ESBnYx4kq9H2QQGfI2oJPJ+uayTv/FigQaOCgxYQdMtOPBGl98wWKoz5\nHV45Wj9s9lfkqNCQ14OcT7VTShbVHJZFU/swZspCdV68ggBPzn0/JGxSgZMPphx6\nlQjgLaNZfOnqbrYMdt3/+4moG45EkJ7JZUHmXgX3IQKBgQDMB0IkvHis0rGwZkeL\nqAAoCUJJnKzf5ZMeagmCJY7Eg5EwF+LZjvnzOkl+Udg42uJSp6LRLI0J9ifEVX/3\nuzAaZtFzk/oFY4lZHQoN2cre2uUXmXa//hdVR/yJOgdVRZvS8WHk8f2X3xCIkbt8\nsDQZ3UDzBRvfmJb/GRTqyEJqBwKBgQDFEK279znJz4bjLcK03xNXUkmddQBy4C+C\nsK0c30QR9desFhJji8KZGa6Yih48EdZXlzgaxeVs6SaYcJ0zdrZMYQokoT8cCoHB\nVSA+sGQLWva9YbuosJldyxV3P+eTgCbtKnLG3P11abz6ojhfRrGxogJ73dKVveFy\nc/UfT5iT3QKBgC5Imz2gL7Ps2/hLS4Gn69kpOItgamskNjqZDW0jvf5gZkhFsuVt\npNADcfag9G75YIwlkS7ob1pKJ/1G9A+rvB7RIkSY1gfw65B2oPhBZt8lQwEWhDTL\nnFlxSh2LN2ylrNKuhWmdZ8zTAnoorSJ9CmSvp3M5vnf7so1OEEuugDpzAoGBALzR\n9VXUVee71CgbMaPy1uplaynW8N4hVwSnWsf+WY/H+qXl5CrDwGrIA9YfCUdPZAw7\nVcO5eNH5OET6KnYkOhpHJNviMMEihB+F/EZ05vdGaoMdgRzqUZlgPKotbiuTsDiw\n4pcPKkB1V2DjTJZl+18Tt8ON0PgvnzP2TZl5v911AoGBALs3D+04D3LkqMVf03pC\nVxnntet75KyytN8GEpsTU4m69LTd1c03iUZCgBjxz1rZ5OSmECC9O0S0aDO4yWDY\nyMu2kav+/hKsMjIXC1NHMKe+97OOdCRmMQM97QdPdFYuwFTZ5wXpcJZvLWqdkqAf\nAV78I1KyEU1UDvducsA3/pBZ\n-----END PRIVATE KEY-----\n",
    "client_email": "gsheets-python-access@biolume-is.iam.gserviceaccount.com",
    "client_id": "101809676500595177681",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/gsheets-python-access%40biolume-is.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}, SCOPES)

# Initialize Google Sheets client
def init_gsheets():
    client = gspread.authorize(CREDS)
    sheet = client.open("Inventory").sheet1  # Replace with your Google Sheet name
    return sheet

# Load product data from Google Sheets
@st.cache_data
def load_product_data():
    sheet = init_gsheets()
    data = sheet.get_all_records()
    product_data = pd.DataFrame(data)
    product_data = product_data.dropna(subset=["Product Name", "Price", "Product Category"])
    return product_data

# Load inventory data from Google Sheets
def load_inventory_data():
    sheet = init_gsheets()
    data = sheet.get_all_records()
    return pd.DataFrame(data)

# Save inventory data to Google Sheets
def save_inventory_data(inventory_df):
    sheet = init_gsheets()
    sheet.clear()
    sheet.update([inventory_df.columns.values.tolist()] + inventory_df.values.tolist())

# User credentials
user_credentials = {
    "admin": {"username": "admin", "password": "1234", "role": "admin"},
    "viewer1": {"username": "viewer1", "password": "1234", "role": "viewer"},
    "viewer2": {"username": "viewer2", "password": "1234", "role": "viewer"},
    "viewer3": {"username": "viewer3", "password": "1234", "role": "viewer"},
}

# Main App
def main():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in user_credentials and user_credentials[username]["password"] == password:
            st.session_state.user_role = user_credentials[username]["role"]
            st.session_state.username = username
            st.success(f"Logged in as {st.session_state.user_role}.")
        else:
            st.error("Invalid username or password.")

    if "user_role" in st.session_state:
        role = st.session_state.user_role
        if role == "admin":
            inventory_system()
        elif role == "viewer":
            viewer_system()

# Inventory Management (Admin)
def inventory_system():
    st.title(":shopping_bags: Inventory Tracker")
    product_data = load_product_data()
    inventory_df = load_inventory_data()

    with st.sidebar:
        st.subheader("Add Products")
        selected_products = st.multiselect("Select Products", product_data["Product Name"].unique())

        if selected_products:
            product_entries = []
            for product in selected_products:
                product_details = product_data[product_data["Product Name"] == product].iloc[0]
                st.write(f"**{product}** - ${product_details['Price']:.2f} ({product_details['Product Category']})")
                quantity = st.number_input(f"Quantity for {product}", min_value=1, value=1)
                discount = st.number_input(f"Discount for {product} (%)", min_value=0, value=0)
                product_entries.append({
                    "Product Name": product,
                    "Product Category": product_details["Product Category"],
                    "Price": product_details["Price"],
                    "Quantity": quantity,
                    "Discount": discount,
                })

            st.subheader("Invoice Details")
            action = st.text_input("Action", "Sale")
            bill_no = st.text_input("Bill No.")
            party_name = st.text_input("Party Name")
            address = st.text_area("Address")
            city = st.text_input("City")
            state = st.text_input("State")
            contact_number = st.text_input("Contact Number")
            gst = st.text_input("GST")
            date = st.date_input("Date")

            if st.button("Add to Inventory"):
                for entry in product_entries:
                    entry.update({
                        "Action": action, "Bill No.": bill_no, "Party Name": party_name,
                        "Address": address, "City": city, "State": state, "Contact Number": contact_number,
                        "GST": gst, "Date": date
                    })
                new_entries_df = pd.DataFrame(product_entries)
                if not new_entries_df.empty:
                    inventory_df = pd.concat([inventory_df, new_entries_df], ignore_index=True)
                    save_inventory_data(inventory_df)
                    st.success(f"Added {len(product_entries)} product(s) to inventory!")

    st.subheader("Inventory Table")
    edited_df = st.data_editor(
        inventory_df,
        num_rows="dynamic",
        column_config={"Price": st.column_config.NumberColumn(format="$%.2f")},
        key="inventory_editor",
    )

    if st.button("Save Changes"):
        save_inventory_data(edited_df)
        st.success("Inventory updated successfully!")

    # **Product-wise Sales Summary**
    st.subheader("Product-wise Sales Summary")
    sales_df = inventory_df.groupby("Product Name").agg(
        Total_Quantity=("Quantity", "sum"),
        Total_Sale_Value=("Price", "sum")
    ).reset_index()
    sales_df["Total_Sale_Value"] = sales_df["Total_Quantity"] * sales_df["Total_Sale_Value"]
    st.write(sales_df)

    # **Date-wise Sales Summary**
    st.subheader("Date-wise Sales Summary")
    date_sales_df = inventory_df.groupby("Date").agg(
        Total_Quantity=("Quantity", "sum"),
        Total_Sale_Value=("Price", "sum")
    ).reset_index()
    date_sales_df["Total_Sale_Value"] = date_sales_df["Total_Quantity"] * date_sales_df["Total_Sale_Value"]
    st.write(date_sales_df)

    st.subheader("Sales Trends")
    st.line_chart(date_sales_df.set_index("Date")["Total_Sale_Value"])

# Viewer Dashboard
def viewer_system():
    st.title(":shopping_bags: Inventory Viewer")
    inventory_df = load_inventory_data()

    st.subheader("Product-wise Sales Summary")
    sales_df = inventory_df.groupby("Product Name").agg(
        Total_Quantity=("Quantity", "sum"),
        Total_Sale_Value=("Price", "sum")
    ).reset_index()
    sales_df["Total_Sale_Value"] = sales_df["Total_Quantity"] * sales_df["Total_Sale_Value"]
    st.write(sales_df)

    st.subheader("Date-wise Sales Summary")
    date_sales_df = inventory_df.groupby("Date").agg(
        Total_Quantity=("Quantity", "sum"),
        Total_Sale_Value=("Price", "sum")
    ).reset_index()
    date_sales_df["Total_Sale_Value"] = date_sales_df["Total_Quantity"] * date_sales_df["Total_Sale_Value"]
    st.write(date_sales_df)

    st.subheader("Sales Trends")
    st.line_chart(date_sales_df.set_index("Date")["Total_Sale_Value"])

if __name__ == "__main__":
    main()
