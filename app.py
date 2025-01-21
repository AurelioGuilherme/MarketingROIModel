import streamlit as st
import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("MarketingROIModel")

# Load CSV from Data folder
#data_path = os.path.join("../Data", "MKT.csv")
data = pd.read_csv("Data/MKT.csv")
target = "sales"
# Select features
features = st.multiselect("Selecione as features para o modelo:", 
                          [col for col in data.columns if col != target])

if target and features:
        # Split data
        X = data[features]
        y = data[target]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train model
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Predictions
        y_pred = model.predict(X_test)

        # Evaluation
        col_1, col_2 = st.columns(2)
        with col_1:
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            st.write("### Métricas do Modelo:")
            st.write(f"**Mean Squared Error (MSE):** {mse:.4f}")
            st.write(f"**R² Score:** {r2:.4f}")

        with col_2:
            st.write("### Gráfico de Regressão:")
            if len(features) > 1:
                X_test_projection = X_test.dot(model.coef_)
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=X_test_projection, y=y_test, mode='markers', name='Dados reais'))
                fig.add_trace(go.Scatter(x=X_test_projection, y=y_pred, mode='lines', name='Linha de Regressão', line=dict(color='red')))
                fig.update_layout(title="Regressão Linear (Projeção em 2D)", xaxis_title="Projeção das Features", yaxis_title=target)
            else:
                projection_feature = features[0]
                fig = px.scatter(x=X_test[projection_feature], y=y_test, labels={"x": projection_feature, "y": target}, title="Regressão Linear")
                fig.add_scatter(x=X_test[projection_feature], y=y_pred, mode='lines', name='Linha de Regressão', line=dict(color='red'))
            st.plotly_chart(fig)

        # Predict return on investment
        st.write("### Previsão de Retorno:")
        investment_values = []
        for feature in features:
            investment = st.number_input(f"Insira o valor de investimento para {feature}:", min_value=0.0, step=0.2)
            investment_values.append(investment)

        if any(val > 0 for val in investment_values):
            predicted_return = model.predict([investment_values])[0]
            st.write(f"## Com os investimentos fornecidos, o retorno previsto é: **{predicted_return:.2f}**")
else:
    st.warning("Selecione a variável alvo e pelo menos uma feature para continuar.")