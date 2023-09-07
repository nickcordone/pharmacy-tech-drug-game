import streamlit as st
import random
import json
from streamlit_js_eval import streamlit_js_eval

# Define a function to generate and return the data
@st.cache_data 
def generate_data(file_path):
    with open(file_path) as f:
        return json.load(f)

file_path = "dict.json"
data = generate_data(file_path)

#create a function to generate data and ensure cache is used to not randomize the data until it is needed
@st.cache_data
def generate_combination():
    main_categories = list(data.keys())

    if not main_categories:
        st.write("No main categories found in the data.")
    else:
        # Randomly select a main category
        selected_main_category = random.choice(main_categories)
        st.write("Main Category: ", selected_main_category)

        # this will generate a random subcategory if it exsits, else it will just use the main category name
        subcategory = list()

        for subcategory_data in data[selected_main_category]:
            if subcategory_data == "Generic & Brand Name Category":
                subcategory.append(selected_main_category)
            else:
                subcategory.append(subcategory_data)
            
        subcategory = random.choice(subcategory)
        st.write("Subcategory: ", subcategory)

    # This is to generate the generic and brand names from the main/subcategories and if there is no subcategory just get the keys/values
    try:
        generic_brand_category = data[selected_main_category][subcategory]["Generic & Brand Name Category"]

        generic_names = list(generic_brand_category.keys())

        brand_names = list(generic_brand_category.values())
    except KeyError:
        generic_brand_category = data[selected_main_category]["Generic & Brand Name Category"]
        
        generic_names = list(generic_brand_category.keys())

        brand_names = list(generic_brand_category.values())

    return selected_main_category, subcategory, generic_brand_category, generic_names, brand_names

# Call the function to get multiple variables
result = generate_combination()

# Create a centered container for your content
# centered_container = st.container()
# with centered_container:
# list out the variables
if result is not None:
    selected_main_category, subcategory, generic_brand_category, generic_names, brand_names = result

# function to get a random value for if we get a generic or brand name
@st.cache_data()
def randomize_generic_or_brand():
    g_or_b = random.choice(range(0, 2))  # 0 = Generic, 1 = Brand
    return g_or_b

random_value = randomize_generic_or_brand()

# get the generic value so it won't change until we clear the cache
@st.cache_data()
def randomize_generic_name():
    generic = random.choice(range(0, len(generic_names)))
    return generic

# get the brand value so it won't change until we clear the cache
@st.cache_data()
def randomize_brand_name():
    brand = random.choice(range(0, len(brand_names)))
    return brand

# begining of session state
state = st.session_state

def clear_text():
    st.session_state["text"] = ""

if "correct_guesses" not in state:
    state.correct_guesses = list()

if 'count' not in st.session_state:
    st.session_state.count = 0

if 'wrong' not in st.session_state:
    st.session_state.wrong = 0

if 'give_up' not in st.session_state:
    st.session_state.give_up = False

if 'disabled' not in st.session_state:
    st.session_state.disabled = False

# end of session state

if random_value == 0:
    # get the generic name of the random value
    generic = generic_names[randomize_generic_name()]
    # give the user the drug they need to guess
    st.write("Generic Name:", generic)
    # grab the index of the generic name
    generic_names_index = generic_names.index(generic)
    # if we get a generic name, user needs to guess the brand name
    brand_guess = st.text_input("Enter Brand Name Guess", key="text", disabled=st.session_state.disabled)
    if brand_names[generic_names_index] == brand_guess:
        # clear the cache
        st.cache_data.clear()
        # add the correct guess to the list of correct answers
        state.correct_guesses.append(generic)
        # keep count of correct answers
        st.session_state.count += 1
        # tell the user they got the correct answer
        st.write(f"{brand_guess} was the correct answer!")
        st.session_state.wrong = 0
        # call the function again to get a new random value
        st.button("Go Next", on_click=clear_text)
    else:
        # create a counter of incorrect guesses
        st.session_state.wrong += 1
        # tell the user they got the incorrect answer
        if brand_guess == "":
            st.write("#")
        elif st.session_state.wrong <= 1:
            st.write("#")
        else:
            st.write(f"{brand_guess} was the incorrect answer!")
        # 5 will be first letter
        if st.session_state.wrong >= 5:
            st.write(f"The first letter is {brand_names[generic_names_index][0]}")
        # 10 shows the length of the answer
        if st.session_state.wrong >= 10:
            st.write(f"The length of the brand name drug is {len(brand_names[generic_names_index])} letters/characters")
        # 15 lets the user go next, if they do choose to give up no points will be given
        if st.session_state.wrong >= 15:
            if st.button("Give up?", on_click=clear_text):
                st.write(f"The brand name was {brand_names[generic_names_index]}")
                st.cache_data.clear()
                st.session_state.wrong = 0
                st.button("Go Next, No Points", on_click=clear_text)
            st.markdown(''':red[*ONCE CLICKED EVEN IF YOU GUESS THE CORRECT ANSWER, YOU WILL NOT BE GIVEN A POINT*] ''')
else:
    # get the brand name of the random value
    brand = brand_names[randomize_brand_name()]
    # give the user the drug they need to guess
    st.write("Brand Name:", brand)
    # grab the index of the brand name
    brand_names_index = brand_names.index(brand)
    # if we get a brand name, user needs to guess the generic name
    generic_guess = st.text_input("Enter Generic Name Guess", key="text", disabled=st.session_state.disabled)
    if generic_names[brand_names_index] == generic_guess:
        # clear the cache
        st.cache_data.clear()
        # add the correct guess to the list of correct answers
        state.correct_guesses.append(generic_names[brand_names_index])
        # keep count of correct answers
        st.session_state.count += 1
        # tell the user they got the correct answer
        st.write(f"{generic_guess} was the correct answer!")
        # call the function again to get a new random value
        st.session_state.wrong = 0
        st.button("Go Next", on_click=clear_text)
    else:
        # create a counter of incorrect guesses
        st.session_state.wrong += 1
        # tell the user they got the incorrect answer
        if generic_guess =="":
            st.write("#")
        elif st.session_state.wrong <= 1:
            st.write("#")
        else:
            st.write(f"{generic_guess} was the incorrect answer!")
        # 5 will be first letter
        if st.session_state.wrong >= 5:
            st.write(f"The first letter is {generic_names[brand_names_index][0]}")
        # 10 shows the length of the answer
        if st.session_state.wrong >= 10:
            st.write(f"The length of the generic name drug is {len(generic_names[brand_names_index])} letters/characters")
        # 15 lets the user go next, if they do choose to give up no points will be given
        if st.session_state.wrong >= 15:
            if st.button("Give up?", on_click=clear_text):
                st.write(f"The generic name was {generic_names[brand_names_index]}")
                st.cache_data.clear()
                st.session_state.wrong = 0
                st.button("Go Next, No Points", on_click=clear_text)
            st.markdown(''':red[*ONCE CLICKED EVEN IF YOU GUESS THE CORRECT ANSWER, YOU WILL NOT BE GIVEN A POINT*] ''')

col1, col2 = st.columns([.25, .25])

# allows the user to stop and see how many correct answers were guessed
with col1:
    st.write("#")
    st.write("#")
    st.write("#")
    if st.button("Stop"):
        st.session_state.disabled = True
        st.session_state.wrong = 0
        st.write(f"You got {st.session_state.count} correct answers!")
    st.write("#")
    st.write("#")
    st.write("#")
    st.write("> 5 guesses gives the first letter of the correct answer")
    st.write("> 10 guesses gives the length of the correct answer")
    st.write("> 15 guesses gives the option to give up, with no points given")

# button to allow the user start over
with col2:
    st.write("#")
    st.write("#")
    st.write("#")
    if st.button("Start Over"):
        streamlit_js_eval(js_expressions="parent.window.location.reload()")

# fix the size of the text input box
st.markdown("""
            <style>
            [data-testid="stTextInput"]{
            width: 50%;
            }
            </style>
            
            """, unsafe_allow_html=True)
