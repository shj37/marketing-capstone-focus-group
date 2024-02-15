# streamlit run focus_group_data_app.py
import streamlit as st
import pandas as pd

# Load the Excel file
@st.cache_data
def load_data(file_path):
    return pd.read_excel(file_path)

def main():
    st.set_page_config(page_title="Focus Group Script Analysis")
    st.header("Focus Group Script Analysis")

    st.markdown("<p>Created by <span style='text-align: center; font-style: italic;'>Shijun Ju</span></p>", unsafe_allow_html=True)

    # Create a file uploader widget
    uploaded_file = st.sidebar.file_uploader("Upload Excel file", type=["xlsx"])

    # If a file is uploaded
    if uploaded_file is not None:
        df = load_data(uploaded_file)

        # Create a selectbox for selecting values from one column
        selected_objective = st.sidebar.selectbox('Select Research OBJECTIVE', df['objective'].unique())

        # Filter DataFrame based on the selected value
        filtered_df = df[df['objective'] == selected_objective]

        # Create a multiselect for selecting values from another column
        selected_questions = st.sidebar.multiselect('Select Research QUESTIONs', filtered_df['question'].unique())

        submitted = st.sidebar.button("Show Results")

        submitted_all_objectives = st.sidebar.button("Show ALL Objectives")

        submitted_all = st.sidebar.button("Show ALL Scripts")

        if submitted_all_objectives:
            objectives = df['objective'].unique()
            for obj in objectives:
                if "To " in obj:
                    st.markdown(f"#### Research Objective: {obj}")

        if submitted_all:
            current_moderator_question = ""
            current_research_question = ""
            current_objective = ""
            for index, row in df.iterrows():
                if current_objective != row['objective']:
                    if len(current_objective) > 0:
                        st.markdown("<hr>", unsafe_allow_html=True)

                    st.markdown(f"### Research Objective: {row['objective']}")
                    current_objective = row['objective']

                if current_research_question != row['question']:
                    if len(current_research_question) > 0:
                        st.markdown("<hr>", unsafe_allow_html=True)

                    st.markdown(f"#### Research Question: {row['question']}")
                    current_research_question = row['question']

                if current_moderator_question != row['moderator']:
                    if len(current_moderator_question) > 0:
                        st.markdown("<hr>", unsafe_allow_html=True)
                    st.write("**Moderator:**", row['moderator'])
                    current_moderator_question = row['moderator']

                st.write(f"**{row['name']}:**", row['answer'])

        if submitted:
            # Filter DataFrame based on the selected values
            filtered_df = filtered_df[filtered_df['question'].isin(selected_questions)]

            # Display values from other columns based on selections made
            if not filtered_df.empty:
                #st.write(filtered_df[['name', 'answer']])
                st.markdown(f"### Research Objective: {selected_objective}")

                current_moderator_question = ""
                current_research_question = ""

                for index, row in filtered_df.iterrows():
                    if current_research_question != row['question']:
                        if len(current_research_question) > 0:
                            st.markdown("<hr>", unsafe_allow_html=True)

                        st.markdown(f"#### Research Question: {row['question']}")
                        current_research_question = row['question']

                    if current_moderator_question != row['moderator']:
                        if len(current_moderator_question) > 0:
                            st.markdown("<hr>", unsafe_allow_html=True)
                        st.write("**Moderator:**", row['moderator'])
                        current_moderator_question = row['moderator']

                    st.write(f"**{row['name']}:**", row['answer'])
            else:
                st.write('Select Objective, then Questions.')
        else:
            st.write('Select Objective, then Questions.')

if __name__ == "__main__":
    main()
