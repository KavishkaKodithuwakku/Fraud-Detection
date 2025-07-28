import streamlit as st
import pandas as pd
import joblib


model = joblib.load("fraud_detection_xgb.pkl")


st.title("Fraud Detection App")

st.markdown("Please enter the transaction details and use the predict button")

st.divider()

transaction_type = st.selectbox("Transaction Type", ["PAYMENT", "TRANSFER", "CASH_OUT", "DEBIT", "CREDIT"  ])
amount = st.number_input("Amount", min_value=0.0, value=1000.0)
oldbalanceOrg = st.number_input("Old Balance (Sender)", min_value=0.0, value=10000.0)
newbalanceOrig = st.number_input("New Balance (Sender)", min_value=0.0, value=9000.0)
OldbalanceDest = st.number_input("Old Balance (Reciever)", min_value=0.0, value=0.0)
newbalanceDest = st.number_input("New Balance (Reciever)", min_value=0.0, value=0.0)

if st.button("Predict"):
    input_data = pd.DataFrame({
        "type": [transaction_type],
        "amount": [amount],
        "oldbalanceOrg": [oldbalanceOrg],
        "newbalanceOrig": [newbalanceOrig],
        "oldbalanceDest": [OldbalanceDest],
        "newbalanceDest": [newbalanceDest]
    })

    input_data["balanceDiffOrg"] = input_data["oldbalanceOrg"] - input_data["newbalanceOrig"]
    input_data["balanceDiffDest"] = input_data["newbalanceDest"] - input_data["oldbalanceDest"]
    input_data["zero_after_transfer"] = (
        (input_data["type"].isin(["TRANSFER", "CASH_OUT"])) &
        (input_data["oldbalanceOrg"] > 0) &
        (input_data["newbalanceOrig"] == 0)
    ).astype(int)

    prediction = model.predict(input_data)

    st.subheader(f"Prediction: '{int(prediction)}'")

    if prediction[0] == 1:
        st.error("The transaction can be fraud.")
    else:
        st.success("The transaction looks likes  is not fraud")
