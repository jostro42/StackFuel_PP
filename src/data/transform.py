import re

import pandas as pd


def reformat_metacritic(
    df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Return the reformatted main table and critic repeats table.

    Select critic entries by highest review count and assign user information
    to the section platform. Leave the input DataFrame unchanged.
    """

    # --- Which info goes where? ---

    # 1. Define metadata to repeat on every platform row.
    #    Matches original column names (keys) to new ones for the new table format.
    #    Will be repeated for every platform row of a game entry.
    metadata = {
        "title": "title",
        "genres/0": "genre",
        "summary": "summary",
        "publisherName": "publisherName",
        "publisherUrl": "publisherUrl",
        "url": "url",
        "section": "original_platform",
        "releaseDate": "ReleaseDate",
    }

    # 2. How to extract the measures inside each "platformReviews/<index>/..." group.
    critic_fields = {
        "score": "metascore",
        "normalizedScore": "critic_normalized_score",  # normalized score gets its own new column
        "positiveCount": "critic_positive_count",
        "negativeCount": "critic_negative_count",
        "neutralCount": "critic_mixed_count",
        "reviewCount": "critic_total_count",
    }

    # 3. Same as (2), but for "userReviewSummary/..." variable group
    user_fields = {
        "positive": "user_positive_count",
        "negative": "user_negative_count",
        "neutral": "user_mixed_count",
        "reviewCount": "user_total_count",
    }

    # --- Preparation ---

    # 4. Get indices from the "platformReviews/<index>/..." variable group, and sort
    #    them into a integer list
    indices = sorted(
        int(match.group(1))
        for column in df.columns
        if (match := re.fullmatch(r"platformReviews/(\d+)/name", str(column)))
    )

    # 5. Some input validation
    # Are the column names unique?
    if not df.columns.is_unique:
        raise ValueError("The input DataFrame must have unique column names.")
    # Are there variables from "platformReview/<index>/.."group?
    if not indices:
        raise ValueError("No platformReviews/<index>/name columns were found.")

    # 6. Treat pandas nulls and empty strings as missing, while preserving zero.
    def is_missing(value):
        return pd.isna(value) or (isinstance(value, str) and not value.strip())

    # 7. Read review measures as numbers.
    #    Unavailable or nonnumeric values, such as 'tbd', become missing.
    def numeric(value):
        if is_missing(value):
            return pd.NA
        return pd.to_numeric(value, errors="coerce")

    # 8. Define the main output columns, including provenance for critic data.
    base_columns = [
        *metadata.values(),  # all new meta-data variable names
        "platform",  # the console the current row corresponds to
        *critic_fields.values(),  # all new critic_fields variable names
        "userscore",  # user score for the console iteration of the game
        *user_fields.values(),  # all new user_fields variable names
        "critic_sourceVar",  # var group supplying critic info
        "critic_review_url",  # console critic review web page
        "userscore_sourceVar",  # source variable for user score
        "user_review_sourceVar",  # source variable for user counts
    ]

    # --- Do the reformatting ---

    output_rows = []
    repeated_critic_rows = []

    test_df = df.copy()

    # 9. Process original rows sequentially
    for _, game in test_df.iterrows():
        # 10. Build a dictionary containing the platform and the corresponding index
        #     as found in the "platforReviews/.." var group
        platform_slots = {}
        for index in indices:
            platform = game[f"platformReviews/{index}/name"]

            if is_missing(platform):
                continue
            # if the platform key does not exist yet, create it together with an empty list as value.
            # append the index to that list
            platform_slots.setdefault(platform, []).append(index)

        # 11. Create one output row for each platform found in this game.
        for platform, slots in platform_slots.items():
            # 12. Create one output row for each platform found in the data for the game
            record = dict.fromkeys(
                base_columns, pd.NA
            )  # creates dict with all base columns filled with NAs

            # fills new data rows up with their respective content.
            # repeats game's metadata on this platform row
            for source, destination in metadata.items():
                record[destination] = game.get(source, pd.NA)

            record["platform"] = platform

            # 13. Use the one indexed observation for main critic fields that shows the highest
            #     critic review count. This ensures the most valid entry to enter the main data

            # get total critic-review counts for this platform's indexed entry
            review_counts = {
                index: numeric(game.get(f"platformReviews/{index}/reviewCount", pd.NA))
                for index in slots
            }

            # Select the entry with the highest count. Missing counts rank < 0.
            # Ties retain first indexed platform entry
            selected_index = max(
                slots,
                key=lambda index: (
                    float("-inf")
                    if is_missing(review_counts[index])
                    else review_counts[index]
                ),
            )

            selected_prefix = f"platformReviews/{selected_index}"

            for source, destination in critic_fields.items():
                record[destination] = numeric(
                    game.get(f"{selected_prefix}/{source}", pd.NA)
                )

            # retain source group and review url
            record["critic_sourceVar"] = selected_prefix
            record["critic_review_url"] = game.get(f"{selected_prefix}/url", pd.NA)

            # Indicate whether additional indexed observations exist.
            record["critic_observation_count"] = len(slots)

            # 14. Preserve every observation for repeated platforms in a separate table.
            #     Include all observations, including the one selected for the main table.
            if len(slots) > 1:
                for index in slots:
                    prefix = f"platformReviews/{index}"

                    observation = {
                        "title": game.get("title", pd.NA),
                        "url": game.get("url", pd.NA),
                        "platform": platform,
                        "source_index": index,
                        "selected_in_main": index == selected_index,
                        "critic_sourceVar": prefix,
                        "critic_review_url": game.get(f"{prefix}/url", pd.NA),
                    }

                    # Keep each observation's scores and counts together.
                    for source, destination in critic_fields.items():
                        observation[destination] = numeric(
                            game.get(f"{prefix}/{source}", pd.NA)
                        )

                    repeated_critic_rows.append(observation)

            # 15. Assign user information to the original section platform only.
            section = game.get("section", pd.NA)

            if not is_missing(section) and platform == section:
                record["userscore"] = numeric(game.get("userscore", pd.NA))
                record["userscore_sourceVar"] = "userscore"

                # Apply our provisional section-platform attribution.
                for source, destination in user_fields.items():
                    record[destination] = numeric(
                        game.get(f"userReviewsSummary/{source}", pd.NA)
                    )

                record["user_review_sourceVar"] = "userReviewsSummary"

            # 16. Retain the platform row even if all review metrics are missing.
            output_rows.append(record)

    # --- Finalize output data frames ---

    # 17. build main table and retain the converted nullable dtypes
    df_reformatted = pd.DataFrame(
        output_rows, columns=base_columns + ["critic_observation_count"]
    ).convert_dtypes()

    # 18. Define the review table's columns and build separate table of repeated
    #     critic observations
    review_columns = [
        "title",
        "url",
        "platform",
        "source_index",
        "selected_in_main",
        "critic_sourceVar",
        "critic_review_url",
        *critic_fields.values(),
    ]

    df_critic_repeats = pd.DataFrame(
        repeated_critic_rows,
        columns=review_columns,
    ).convert_dtypes()

    return df_reformatted, df_critic_repeats
