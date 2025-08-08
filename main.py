import streamlit as st
import pickle
import locale
from sklearn.linear_model import LinearRegression

# ──────────────────────────────────────────────────────────────────────────────
# Locale setup: try a real UTF-8 locale, else fall back and fake an INR currency
# ──────────────────────────────────────────────────────────────────────────────
try:
    # try the usual UTF-8 locale
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
except locale.Error:
    # if that fails, at least switch to the system default (often "C")
    try:
        locale.setlocale(locale.LC_ALL, '')
    except locale.Error:
        pass
    # now grab whatever conv we have, tweak it for Indian rupees, and monkey-patch
    _conv = locale.localeconv().copy()
    _conv.update({
        'int_curr_symbol': 'INR ',
        'currency_symbol': '₹',
        'mon_decimal_point': '.',
        'mon_thousands_sep': ',',
        'mon_grouping': [3, 3, 0],
        'p_cs_precedes': 1,
        'n_cs_precedes': 1,
        'p_sep_by_space': 0,
        'n_sep_by_space': 0,
        'p_sign_posn': 1,
        'n_sign_posn': 1
    })
    locale.localeconv = lambda: _conv
# ──────────────────────────────────────────────────────────────────────────────

# load your model and params
model = pickle.load(open('model.pickle', 'rb'))
params = pickle.load(open('params.pickle', 'rb'))

st.set_page_config(
    page_title='Bengaluru House Price Prediction',
    page_icon=':house:'
)

st.title('Bengaluru House Price Prediction')
st.subheader('Predict the price of a house in Bengaluru using Machine Learning')

total_sq_feet = st.number_input(
    'Total Square Feet',
    placeholder='Enter the total square feet area of the house',
    min_value=300, max_value=100000
)
number_bathrooms = st.number_input(
    'Number of Bathrooms',
    placeholder='Enter the number of bathrooms in the house',
    min_value=1, max_value=20
)
number_bedrooms = st.number_input(
    'Number of Bedrooms',
    placeholder='Enter the number of bedrooms in the house',
    min_value=1, max_value=20
)
location = st.selectbox('Choose the location of the house', params['columns'])

if st.button('Predict', type='primary'):
    features = [0] * (len(params['columns']) + params['prefix'])
    features[0] = total_sq_feet
    features[1] = number_bathrooms
    features[2] = number_bedrooms
    features[params['prefix'] + params['columns'].index(location)] = 1

    price = model.predict([features])[0] * 100_000
    if price <= 0:
        st.error('The location you have chosen does not have any houses with the entered features')
    else:
        # this will now work even if the container has no en_US locale
        price_str = locale.currency(price, grouping=True)
        st.success(f'The predicted price of the house is {price_str}')

