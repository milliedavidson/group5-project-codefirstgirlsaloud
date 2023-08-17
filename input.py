def format_category_for_search(category): # Function to format categories (otherwise they are fed in with spaces, etc
    if category == "Fantasy":
        formatted_category = "bestselling+fantasy" # Do we add bestselling across the board?
        return formatted_category

    elif category == "Science Fiction": # Do we instead code a function that removes all white spaces from categories?
        formatted_category = "sciencefiction"
        return formatted_category

    else:
        return category


# Is this function necessary? There's a chance it is but requires some testing to see.
