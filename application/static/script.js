/* Function to generate categories for user selection based on genre selection (Fiction or Non-Fiction) */
function updateCategories() {
            /* Identify the two input filters to link up and assign the value of the genre to a variable */
            var genreSelect = document.getElementById("genre");
            var categorySelect = document.getElementById("category");
            var selectedGenre = genreSelect.value;

            /* Record the chosen genre for filtering purposes */
            document.getElementById("selected_genre").value = selectedGenre;

            /* Declare an empty string for the category dropdown menu */
            categorySelect.innerHTML = "";

            /* If statement to decide on which categories to show the user based on the selected genre */
            if (selectedGenre === "fiction") {
                var categories = [
                "Adventure",
                "Crime",
                "Dystopian",
                "Fantasy",
                "Graphic Novels",
                "Horror",
                "LGBTQ+",
                "Literary",
                "Mystery & Detective",
                "Romance",
                "Science Fiction",
                "Thriller"
                ];
            } else if (selectedGenre === "non-fiction") {
                var categories = [
                "Business",
                "Cooking",
                "Crafts",
                "Gardening",
                "Music",
                "Nature",
                "Philosophy",
                "Politics",
                "Religion",
                "Travel",
                "True Crime"
                ];
            }

            /* For loop to create an option for user to choose from in the dropdown menu */
            for (var i = 0; i < categories.length; i++) {
                var option = document.createElement("option");
                option.value = categories[i];
                option.text = categories[i];
                categorySelect.appendChild(option);
            }
        }

        /* Initialize the categories based on the default genre selection*/
        updateCategories();
