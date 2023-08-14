import streamlit as st 
import pandas as pd   
import plotly.express as px 
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
import query
import time

st.set_page_config(page_title='Dashboard VM', page_icon='🌎', layout='wide')
st.subheader('🔔 Analisis descriptivo de seguros.')
st.markdown('##')

result = query.view_all_data()
df = pd.DataFrame(result, columns=['Policy','Expiry','Location','State','Region','Investment','Construction','BusinessType','Earthquake','Flood','Rating','id'])

st.sidebar.image('data/logo1.png', caption='Analisis Online')
st.sidebar.header('Aplicar filtros')
region = st.sidebar.multiselect(
    "Elija Región",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)
location = st.sidebar.multiselect(
    "Elija Localidad",
    options=df["Location"].unique(),
    default=df["Location"].unique()
)
construction = st.sidebar.multiselect(
    "Elija Construction",
    options=df["Construction"].unique(),
    default=df["Construction"].unique()
)
df_selection=df.query("Region == @region & Location == @location & Construction == @construction")
#st.dataframe(df_selection)

def Home():
    with st.expander('Tabular'):
        showData = st.multiselect('Filtro: ', df_selection.columns, default=[])
        st.write(df_selection[showData])
    total_investment = float(df_selection['Investment'].sum())
    investment_mode = float(df_selection['Investment'].mode())
    investment_mean = float(df_selection['Investment'].mean())
    investment_median = float(df_selection['Investment'].median())
    rating = float(df_selection['Rating'].sum())
    
    total1, total2, total3, total4, total5 = st.columns(5, gap='large')
    
    with total1:
        st.info('Total investment', icon='📌')
        st.metric(label='sum TZS', value=f'{total_investment:,.0f}')
    
    with total2:
        st.info('Mas frecuente', icon='📌')
        st.metric(label='moda TZS', value=f'{investment_mode:,.0f}')
        
    with total3:
        st.info('Promedio', icon='📌')
        st.metric(label='promedio TZS', value=f'{investment_mean:,.0f}')
        
    with total4:
        st.info('Ganancias centrales', icon='📌')
        st.metric(label='median TZS', value=f'{investment_median:,.0f}')
        
    with total5:
        st.info('Ratings', icon='📌')
        st.metric(label='rating TZS', value=numerize(rating), help=f""" Total Rating: {rating}  """)
        
    st.markdown("""---""")
    
def graphs():
    #total_investment = int(df_selection['Investment']).sum()
    #averageRating = int(round(df_selection['Rating']).mean(),2)
    
    #simple bar graph
    investment_by_business_type=(
        df_selection.groupby(by=['BusinessType']).count()[['Investment']].sort_values(by='Investment')
    )
    fig_investment = px.bar(
        investment_by_business_type,
        x='Investment',
        y = investment_by_business_type.index,
        orientation='h',
        title='<b> Inversion por tipo de negocio </b>',
        color_discrete_sequence=['#0083b8']*len(investment_by_business_type),
        template='plotly_white',
    )
    
    fig_investment.update_layout(
        plot_bgcolor = "rgba(0,0,0,0)",
        xaxis = (dict(showgrid=False))
    )
    
    # simple line graph
    investment_state = df_selection.groupby(
        by=["State"]).count()[["Investment"]]
    fig_state = px.line(
        investment_state,
        x=investment_state.index,
        y="Investment",
        orientation="v",
        title="<b> Investment by State </b>",
        color_discrete_sequence=["#0083b8"]*len(investment_state),
        template="plotly_white",
    )
    
    fig_state.update_layout(
        xaxis = dict(tickmode = 'linear'),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False))
    )
    
    left, right = st.columns(2)
    
    left.plotly_chart(fig_state, use_container_width=True)
    right.plotly_chart(fig_investment, use_container_width=True)


def Progressbar():
    st.markdown(
        """<style>.stProgress > div > div > div > div { background-image: linear-gradient(to right, #99ff99 , #FFFF00)}</style>""", unsafe_allow_html=True,)
    target = 3000000000
    current = df_selection["Investment"].sum()
    percent = round((current/target*100))
    mybar = st.progress(0)

    if percent > 100:
        st.subheader("Target Hecho !")
    else:
        st.write("Tienes ", percent, "% ", "de ", (format(target, 'd')), "TZS")
        for percent_complete in range(percent):
            time.sleep(0.1)
            mybar.progress(percent_complete+1, text=" Target Porcentaje")

def sideBar():
    with st.sidebar:
        selected = option_menu(
            menu_title="Menu Principal",
            options=["Home", "Progress"],
            icons=["house", "eye"],
            menu_icon="cast",
            default_index=0
        )
    if selected=="Home":
        #st.subheader(f'Pagina: {selected}')
        Home()
        graphs()
    if selected=="Progress":
        Progressbar()
        graphs()

sideBar()

# theme
hide_st_style = """ 

<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>
"""
