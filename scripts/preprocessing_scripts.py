import pandas as pd
from google_play_scraper import reviews

def accumulate_reviews(app_id=None, target=400):
    """
        Fetch Google Play Store reviews for a given app until a target count is reached.

        This function repeatedly requests reviews for the specified app and accumulates 
        unique entries based on `reviewId`. It continues fetching until the total number 
        of unique reviews reaches the desired `target`.

        Parameters
        ----------
        app_id : str, optional
            The Google Play Store application ID to fetch reviews for.
        target : int, optional
            The number of unique reviews to collect. Defaults to 400.

        Returns
        -------
        list
            A list of dictionaries, where each dictionary represents a single review 
            returned by the Google Play Store API.

        Notes
        -----
        Duplicate reviews are filtered using their `reviewId`. Additional requests 
        are made as needed until the target count is met.
        """
    seein_ids = set()
    all_reviews = []
    while len(all_reviews) < target:
        bank_reviews, _ = reviews(app_id=app_id, count=target, lang='en', country='us')
        for review in bank_reviews:
            if review.get('reviewId') not in seein_ids:
                seein_ids.add(review.get('reviewId'))
                if len(all_reviews)<target:
                    all_reviews.append(review)
                else:
                    break
    return all_reviews


    


def preprocessing_data(bank_name = None, data_frame=None):
    """
    Prepare and standardize review data for analysis.

    This function renames specific columns to standardized names, adds 
    metadata such as the bank name and source, and converts the review 
    date to a plain date (without time).

    Parameters
    ----------
    bank_name : str, optional
        The name of the bank associated with the reviews.
    data_frame : pandas.DataFrame, optional
        The DataFrame containing raw review data. Expected to include the 
        columns 'content', 'at', and 'score'.

    Returns
    -------
    pandas.DataFrame
        The processed DataFrame with renamed columns, added metadata, and 
        a normalized date field.
    """
    data_frame = data_frame.rename(columns = {'content':'review', 'at':'date', 'score':'rating'})
    data_frame['bank'] = bank_name
    data_frame['source'] = 'Google Play'
    data_frame['date'] = data_frame['date'].dt.date
    return data_frame

    