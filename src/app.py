import streamlit as st
import pickle
import pandas as pd


@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


@st.cache
def load_model():
    return pickle.load(open('model.pkl', 'rb'))


def main():
    st.title("Dos Attack Predictor")
    model = load_model()
    input_type = st.sidebar.selectbox("Input Type", ["Manual", "File"])
    if (input_type == "Manual"):
        df = get_inputs("Manual")
        if (df is not None) and (st.checkbox("Predict")):
            try:
                model_prediction = model.predict(df)
                print(model_prediction)
                if (model_prediction == 1):
                    st.warning("Dos attack detected!")
                elif (model_prediction == 0):
                    st.success("No dos attack detected!")
                st.balloons()
            except Exception as e:
                st.write(e)
    elif(input_type == "File"):
        df = get_inputs("File")
        if (df is not None) and (st.checkbox("Predict")):
            try:
                model_prediction = model.predict(df)
                df["prediction"] = model_prediction
                df["prediction"] = df["prediction"].map(
                    {0: "Benign", 1: "DosAttack"})
                csv = convert_df(df)
                st.download_button(
                    label="Download Predicted-data as CSV",
                    data=csv,
                    file_name='dos_prediction.csv',
                    mime='text/csv',
                )
                st.balloons()
            except Exception as e:
                st.write(e)


def get_inputs(input_type: str):
    if input_type == "File":
        st.sidebar.text("File Inputs")
        file = st.file_uploader("Upload File", type=["csv"])
        if file is not None:
            return pd.read_csv(file)
    elif input_type == "Manual":
        st.sidebar.text("Manual Inputs")
        protocol = st.number_input("protocol")
        flow_duration = st.number_input("flow_duration")
        total_forward_packets = st.number_input("total_forward_packets")
        total_backward_packets = st.number_input("total_backward_packets")
        total_forward_packets_length = st.number_input(
            "total_forward_packets_length")
        total_backward_packets_length = st.number_input(
            "total_backward_packets_length")
        forward_packet_length_mean = st.number_input(
            "forward_packet_length_mean")
        backward_packet_length_mean = st.number_input(
            "backward_packet_length_mean")
        forward_packets_per_second = st.number_input(
            "forward_packets_per_second")
        backward_packets_per_second = st.number_input(
            "backward_packets_per_second")
        forward_iat_mean = st.number_input("forward_iat_mean")
        backward_iat_mean = st.number_input("backward_iat_mean")
        flow_iat_mean = st.number_input("flow_iat_mean")
        flow_packets_per_seconds = st.number_input("flow_packets_per_seconds")
        flow_bytes_per_seconds = st.number_input("flow_bytes_per_seconds")
        return [[protocol, flow_duration, total_forward_packets, total_backward_packets, total_forward_packets_length, total_backward_packets_length, forward_packet_length_mean, backward_packet_length_mean, forward_packets_per_second, backward_packets_per_second, forward_iat_mean, backward_iat_mean, flow_iat_mean, flow_packets_per_seconds, flow_bytes_per_seconds]]


if __name__ == '__main__':
    main()
