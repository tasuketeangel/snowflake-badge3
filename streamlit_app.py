# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
from snowflake.snowpark.functions import when_matched, when_not_matched

import requests

# Write directly to the app
st.title(f"Customize your smoothie")
st.write(
  """Replace this example with your own code!
  **And if you're new to Streamlit,** check
  out our easy-to-follow guides at
  [docs.streamlit.io](https://docs.streamlit.io).
  """
)

r = requests.get("https://smoothiefroot.com")
st.text(r)

name_on_order = st.text_input('Name on smth')
st.write('THe name will be:', name_on_order)


session = get_active_session()


from requests.adapters import HTTPAdapter, Retry

s = requests.Session()

retries = Retry(total=5,
                backoff_factor=0.1,
                status_forcelist=[ 500, 502, 503, 504 ])

s.mount('http://my.smoothiefroot.com/api/fruit/apples', HTTPAdapter(max_retries=retries))

smoothiefroot_response = s.get('http://my.smoothiefroot.com/api/fruit/apples')

st.text(smoothiefroot_response)

#my_dataframe = session.table("smoothies.public.fruit_options").select('FRUIT_NAME')
#st.dataframe(data=my_dataframe, use_container_width=True)

my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()

st.write(my_dataframe)

editable_df = st.data_editor(my_dataframe)

submt = st.button('sub')

if submt:
    st.success('clickedme')

    og_dataset = session.table("smoothies.public.orders")
    edited_dataset = session.create_dataframe(editable_df)
    og_dataset.merge(edited_dataset
                     , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                     , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                    )
