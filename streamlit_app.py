# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie!:cup_with_straw:")
st.write(
  "Choose the fruits you want in your Custom Smoothie!"
)

from snowflake.snowpark.functions import col

name_on_order = st.text_input("Name of the Smoothie :")
st.write("The Name of the Smoothie will be", name_on_order)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredient_list=st.multiselect(
    'Choose Upto 5 Ingredients:',my_dataframe,max_selections=5
    
)
if ingredient_list:
     #st.write(ingredient_list)
     #st.text(ingredient_list)

     ingredients_string= ''

     for fruit_chosen in ingredient_list:
        ingredients_string+=fruit_chosen+' '
         
     #st.write(ingredients_string)
     my_insert_stmt="""INSERT INTO smoothies.public.ORDERS(INGREDIENTS,NAME_ON_ORDER)
     VALUES('"""+ingredients_string+"""','"""+name_on_order+"""')"""

     time_to_insert = st.button('Submit Order')

     if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered!,{name_on_order}", icon="✅")
    
        
#st.dataframe(data=my_dataframe, use_container_width=True)
