import streamlit as st

# Dialog definition
@st.dialog("Data Protection Declaration")
def show_data_protection_dialog():
    st.markdown("""
**Data Protection Declaration**  
Anonymous research survey  

Lorenzo Pengue is the controller, i.e. the entity responsible for this processing activity,  
in accordance with the General Data Protection Regulation (GDPR). According to the GDPR, the  
controller is obliged to provide information to data subjects. Therefore, please take note of the  
following information:

This processing activity is carried out for the following purposes:

- anonymous research survey
- analysis of anonymous survey responses
- analysis of short audio recordings for laboratory studies
- scientific evaluation of sound perception

Lorenzo Pengue  
penguel00[at]univie.ac.at  

Contact person: Lorenzo Pengue  
is the controller responsible for this processing activity.

For the purpose of this processing activity, the University of Vienna processes the  
following categories of personal data:

- anonymous survey responses
- anonymous audio recordings without identifying information
- no names, e-mail addresses, IP addresses, or other identifiers are collected  

Legal foundation(s) of the processing activity:
- explicit consent of the data subject (Art. 6(1)(a) GDPR)
- research purposes
- statistical purposes

Data protection declaration Anonymous research survey, version 1.0 as of 10 December 2025  

The controller may not be able to comply with its obligations to you if you do not provide your anonymous survey data. This applies if the provision of data is necessary for participation in the research project.

If the Controller does not collect the data from you personally, it obtains them from the following source:

- Data are collected directly in the survey)

Your personal data will be disclosed to recipients outside the University of Vienna:  
No  

Your personal data will be transferred to recipients in a third country (EU or EEA country) or an international organization:  
No  

The University of Vienna will store your personal data for the following duration:
- Anonymous survey responses: until 31 December 2027
- Anonymous audio recordings: until 31 December 2027
- No personal identifiers are stored

As a data subject of this processing activity you have the following rights:
- right to access to personal data,
- right to rectification of personal data,
- right to erasure of personal data,
- right to restriction of processing,
- right to data portability and
- right to object to the further processing of your personal data, If the controller processes your data based on overriding legitimate interests or if the processing is necessary for academic or historical research purposes or statistical purposes.

In addition, you have the right to withdraw your consent to the processing of your personal data at any time without having to state a reason. Finally, you also have the possibility to lodge a complaint with the Austrian Data Protection Authority (www.dsb.gv.at) if you believe that the processing of your personal data is not permissible.

Vienna, 10 December 2025
    """)

