function updateCategories() {
            var genreSelect = document.getElementById("genre");
            var categorySelect = document.getElementById("category");
            var selectedGenre = genreSelect.value;

            document.getElementById("selected_genre").value = selectedGenre;

            categorySelect.innerHTML = "";

            if (selectedGenre === "fiction") {
                var categories = [
                "Classics",
                "Crime",
                "Dystopian",
                "Fantasy",
                "Graphic Novels",
                "Historical",
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

            for (var i = 0; i < categories.length; i++) {
                var option = document.createElement("option");
                option.value = categories[i];
                option.text = categories[i];
                categorySelect.appendChild(option);
            }
        }

        // Initialize the categories based on the default genre selection
        updateCategories();