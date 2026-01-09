# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests



# Write directly to the app
st.title(f"Customize your smoothie")

name_on_order = st.text_input('Name on smth')
st.write('THe name will be:', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()


#session = get_active_session()


my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()

ingredients_list = st.multiselect(
    'Choose 0-5 ingr',
    my_dataframe
)
st.stop()


if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        st.subheader("nf")
        # nutrition (to pass hash)
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
        #st.text(smoothiefroot_response)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                values ('""" + ingredients_string +"""','""" + name_on_order + """')"""

    #st.write(my_insert_stmt)
    order_button = st.button("submit")

    st.write(my_insert_stmt)

    if order_button:
        session.sql(my_insert_stmt).collect()
    
        st.write(my_insert_stmt)
        st.stop()
        