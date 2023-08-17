def format_category_for_search(category):
    if category == "Fantasy":
        formatted_category = "bestselling+fantasy"
        return formatted_category

    elif category == "Science Fiction":
        formatted_category = "sciencefiction"
        return formatted_category

    else:
        return category
