# Import python packages
import streamlit as st
import requests
import pandas as pd
from snowflake.snowpark.functions import col


# Write directly to the app
st.title(":cup_with_straw:Customize Your Smoothie!:cup_with_straw:")
st.write(
  """Choose the fruit you want in your custom Smoothie"""
)


cnx = st.connection("snowflake")
session = cnx.session()
#session = get_active_session()

name_on_order = st.text_input('Name on Smoothie:')

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
pd_df=my_dataframe.to_pandas()

ingredients_list = st.multiselect(
    'Choose upto 5 ingredients:',
    my_dataframe)


    #st.write(ingredients_list)
    #st.text(ingredients_list)

if ingredients_list:   
     ingredients_string = ''
    
     for fruit_chosen in ingredients_list:
         ingredients_string += fruit_chosen + ' '

         search_on=pd_df.loc[pd_df['FRUIT_NAME']== fruit_chosen, 'SEARCH_ON'].iloc[0]
         st.write('The search value for ' , fruit_chosen,' is ', search_on,'.')
        
         st.subheader(fruit_chosen+ ': Nutrition Information')
         smoothiefroot_response= requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
         sf_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)

        
        #st.text(smoothiefroot_response.json())

     
     my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('"""+ ingredients_string + """','"""+ name_on_order+"""')"""

     #st.write(my_insert_stmt)
     time_to_submit= st.button('Submit Order',type="primary")
    
     if time_to_submit:
         session.sql(my_insert_stmt).collect()
         st.success('Your Smoothie is ordered!', icon="✅")


#smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
#st.text(smoothie froot_response.json())
