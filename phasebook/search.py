from flask import Blueprint, request, jsonify

from .data.search_data import USERS


bp = Blueprint("search", __name__, url_prefix="/search")


@bp.route("")
def search():
    try:
        # Parse query parameters
        query_params = request.args.to_dict()

        # Call the search_users function
        results = search_users(**query_params)

        # Sort the results based on the specified priority
        sorted_results = sort_search_results(results)

        # Return the results as JSON
        return jsonify(sorted_results), 200
    except Exception as e:
        # Handle any exceptions and return an error response
        return jsonify({"error": str(e)}), 500



def search_users(id=None, name=None, age=None, occupation=None):
    """Search users database

    Parameters:
        args: a dictionary containing the following search parameters:
            id: string
            name: string
            age: string
            occupation: string

    Returns:
        a list of users that match the search parameters
    """

    # Implement search here!
    results = []

    for user in USERS:
        # Check if the user matches the specified search parameters
        if id is not None and (user.get('id') == id):
            results.append(user)
            continue

        if name is not None and name.lower() in user.get('name', '').lower():
            results.append(user)

        if age is not None and ('age' in user and int(age) - 1 <= user.get('age', 0) <= int(age) + 1):
            results.append(user)

        if occupation is not None and occupation.lower() in user.get('occupation', '').lower():
            results.append(user)

    # Remove duplicates from results
    unique_results = [dict(t) for t in {tuple(d.items()) for d in results}]

    return unique_results

#Bonus Challenge
def sort_search_results(results):
    # Sort the results based on the specified priority
    sorted_results = sorted(results, key=lambda x: (
        x.get('id', ''),
        x.get('name', ''),
        abs(x.get('age', 0)),
        x.get('occupation', '')
    ), reverse=False)

    return sorted_results