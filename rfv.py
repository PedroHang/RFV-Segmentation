from io import BytesIO
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
     page_title="RFV Customer Segmentation Template",
     page_icon="   https://cdn-icons-png.flaticon.com/512/17436/17436453.png ",
     layout="wide"
)

def recencia_class(x, r, q_dict):
    """Classifica como melhor o menor quartil 
       x = valor da linha,
       r = recencia,
       q_dict = quartil dicionario   
    """
    if x <= q_dict[r][0.25]:
        return 'A'
    elif x <= q_dict[r][0.50]:
        return 'B'
    elif x <= q_dict[r][0.75]:
        return 'C'
    else:
        return 'D'

def freq_val_class(x, fv, q_dict):
    """Classifica como melhor o maior quartil 
       x = valor da linha,
       fv = frequencia ou valor,
       q_dict = quartil dicionario   
    """
    if x <= q_dict[fv][0.25]:
        return 'D'
    elif x <= q_dict[fv][0.50]:
        return 'C'
    elif x <= q_dict[fv][0.75]:
        return 'B'
    else:
        return 'A'

st.title("RFV Analysis App")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
     df_compras = pd.read_csv(uploaded_file, infer_datetime_format=True, parse_dates=['DiaCompra'])

     df_recencia = df_compras.groupby(by='ID_cliente', as_index=False)['DiaCompra'].max()
     df_recencia.columns = ['ID_cliente', 'DiaUltimaCompra']

     dia_atual = df_compras['DiaCompra'].max()

     df_recencia['Recencia'] = df_recencia['DiaUltimaCompra'].apply(lambda x: (dia_atual - x).days)

     df_recencia.drop('DiaUltimaCompra', axis=1, inplace=True)

     df_frequencia = df_compras[['ID_cliente', 'CodigoCompra']].groupby('ID_cliente').count().reset_index()
     df_frequencia.columns = ['ID_cliente', 'Frequencia']

     df_valor = df_compras[['ID_cliente', 'ValorTotal']].groupby('ID_cliente').sum().reset_index()
     df_valor.columns = ['ID_cliente', 'Valor']

     df_RF = df_recencia.merge(df_frequencia, on='ID_cliente')

     df_RFV = df_RF.merge(df_valor, on='ID_cliente')
     df_RFV.set_index('ID_cliente', inplace=True)

     quartis = df_RFV.quantile(q=[0.25, 0.5, 0.75])

     df_RFV['R_Quartile'] = df_RFV['Recencia'].apply(recencia_class, args=('Recencia', quartis))
     df_RFV['F_Quartile'] = df_RFV['Frequencia'].apply(freq_val_class, args=('Frequencia', quartis))
     df_RFV['M_Quartile'] = df_RFV['Valor'].apply(freq_val_class, args=('Valor', quartis))

     df_RFV['RFV_Score'] = (df_RFV.R_Quartile + df_RFV.F_Quartile + df_RFV.M_Quartile)

     dict_acoes = {
     'AAA': 'Send discount coupons, Ask them to recommend our product to a friend, Send free samples when launching a new product.',
     'DDD': 'Churn! customers who spent very little and made few purchases, do nothing',
     'DAA': 'Churn! customers who spent a lot and made many purchases, send discount coupons to try to recover them',
     'CAA': 'Churn! customers who spent a lot and made many purchases, send discount coupons to try to recover them'
     }

     df_RFV['acoes de marketing/crm'] = df_RFV['RFV_Score'].map(dict_acoes)

     fig = px.bar(df_RFV, x='RFV_Score', title='Client Tier Count', labels={'RFV_Score': 'Client Tier', 'count': 'Count'}, color_discrete_sequence=['limegreen'])
     fig.update_layout(xaxis={'categoryorder':'total descending'})
     st.plotly_chart(fig)

     st.markdown("---")

     col1, col2 = st.columns(2)


     with col1:
          st.markdown("### Marketing/CRM Actions")
          for key, value in dict_acoes.items():
               st.markdown(f"**{key}:** {value}")

     with col2:
         st.write("RFV with Quartiles", df_RFV.head())

     df_RFV['Highlight'] = df_RFV['RFV_Score'].apply(lambda x: 'Highlight' if x in ['AAA', 'DDD'] else 'Other')

     # Generate the pairplot
     fig = px.scatter_matrix(
     df_RFV,
     dimensions=['Recencia', 'Frequencia', 'Valor'],
     color='Highlight',
     symbol='RFV_Score',  # This adds different symbols for different RFV_Score values
     title="Pairplot of Recency, Frequency, and Value with Highlighted RFV Tiers",
     labels={'Recencia': 'Recency', 'Frequencia': 'Frequency', 'Valor': 'Value'}
     )

     # Customize the color scale to ensure the tiers are clearly visible
     fig.update_traces(diagonal_visible=False)

     # Update color and opacity to make 'Other' less prominent
     fig.update_traces(marker=dict(size=5, opacity=0.5), selector=dict(marker_color='rgba(128,128,128,0.5)'))
     fig.update_traces(marker=dict(size=10, opacity=1), selector=dict(marker_color='rgba(0,0,255,1)'))

     # Show the plot
     st.plotly_chart(fig)

     df_RFV.to_excel('./output/RFV.xlsx')

     st.success("RFV analysis completed. The result is saved as RFV.xlsx.")

     output = BytesIO()
     with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
          df_RFV.to_excel(writer, index=True, sheet_name='RFV')

     # Ensure the output is ready to be read by seeking to the beginning
     output.seek(0)

     # Add a download button to the Streamlit app
     st.download_button(
     label="Download RFV Excel file",
     data=output,
     file_name='RFV.xlsx',
     mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
     )