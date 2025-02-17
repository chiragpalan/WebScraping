
import pandas as pd
from collections import defaultdict

def build_transition_matrix(df, order=1):
    """
    Build a transition matrix (as nested dictionaries) from the data.

    Parameters:
      df (DataFrame): Input DataFrame with columns ['Client_ID', 'Product', 'Date_Acct_Open'].
      order (int): Order of the Markov model (e.g., 1 for first-order, 2 for second-order, etc.)

    Returns:
      dict: A transition matrix where keys are tuples of previous products and values are 
            dictionaries mapping the next product to its probability.
    """
    # Convert the Date_Acct_Open column to datetime format
    df['Date_Acct_Open'] = pd.to_datetime(df['Date_Acct_Open'])
    
    # Sort the DataFrame by Client_ID and Date_Acct_Open to ensure proper sequence order
    df_sorted = df.sort_values(by=['Client_ID', 'Date_Acct_Open'])
    
    # Dictionary to hold sequences for each client (key: previous products tuple, value: list of next products)
    sequences = defaultdict(list)
    
    # Group by Client_ID and extract product sequences
    for client, group in df_sorted.groupby('Client_ID'):
        products = list(group['Product'])
        # Loop over the products so that each sequence has length equal to 'order'
        for i in range(len(products) - order):
            # Take a slice of length 'order' as the previous products
            prev_products = tuple(products[i:i + order])
            # The product immediately following the sequence is the next product
            next_product = products[i + order]
            sequences[prev_products].append(next_product)
    
    # Build raw transition counts: For each sequence, count how many times each next product appears.
    transition_counts = defaultdict(lambda: defaultdict(int))
    for prev_products, next_products in sequences.items():
        for next_product in next_products:
            transition_counts[prev_products][next_product] += 1
    
    # Normalize counts row-wise to convert counts into probabilities.
    transition_matrix = {}
    for prev_products, transitions in transition_counts.items():
        total = sum(transitions.values())
        # For each previous products tuple, convert counts to probabilities
        transition_matrix[prev_products] = {p: count / total for p, count in transitions.items()}
    
    return transition_matrix

def recommend_next_product(prev_products, transition_matrix, order=1):
    """
    Recommend the next product given a sequence of previous products.

    Parameters:
      prev_products (tuple or list): The sequence of previous products (length should equal the model order).
      transition_matrix (dict): The transition matrix built from the training data.
      order (int): The order of the Markov model.

    Returns:
      str or None: The recommended next product, or None if no recommendation can be made.
    """
    # Ensure the input is a tuple
    prev_products = tuple(prev_products)
    
    # 1. If an exact sequence match exists in the transition matrix, use it:
    if prev_products in transition_matrix:
        return max(transition_matrix[prev_products], key=transition_matrix[prev_products].get)
    
    # 2. Fallback: Try using a lower-order sequence (reduce the history)
    for i in range(1, order):
        reduced_seq = prev_products[i:]  # Remove the first element(s)
        if reduced_seq in transition_matrix:
            return max(transition_matrix[reduced_seq], key=transition_matrix[reduced_seq].get)
    
    # 3. Global Fallback: Recommend the most common next product overall
    all_transitions = defaultdict(float)
    for transitions in transition_matrix.values():
        for product, prob in transitions.items():
            all_transitions[product] += prob
    if all_transitions:
        return max(all_transitions, key=all_transitions.get)
    
    # 4. If no data is available, return None
    return None

# ---------------------
# Sample Data
data = [
    ['C1', 'A101', 'SA', '2023-01-01'],
    ['C1', 'A102', 'FD', '2023-06-01'],
    ['C1', 'A103', 'CC', '2023-10-01'],
    ['C2', 'A201', 'SA', '2023-02-01'],
    ['C2', 'A202', 'CC', '2023-09-01'],
    ['C2', 'A203', 'MF', '2023-12-01'],
    ['C3', 'A301', 'SA', '2023-03-01'],
    ['C3', 'A302', 'SA', '2023-07-01'],
    ['C3', 'A303', 'MF', '2023-11-01']
]

df = pd.DataFrame(data, columns=['Client_ID', 'Account_ID', 'Product', 'Date_Acct_Open'])

# ---------------------
# Set the desired order (e.g., 2 for a second-order model)
order = 2

# Build the transition matrix using the provided data
transition_matrix = build_transition_matrix(df, order)

# Print the transition matrix for inspection
print("Transition Matrix (Probabilities):")
for key, value in transition_matrix.items():
    print(f"{key} -> {value}")

# ---------------------
# Example Recommendations
print("\nRecommendations:")
print("Recommendation for (SA, FD):", recommend_next_product(('SA', 'FD'), transition_matrix, order))
print("Recommendation for (SA, CC):", recommend_next_product(('SA', 'CC'), transition_matrix, order))
print("Recommendation for (SA, SA):", recommend_next_product(('SA', 'SA'), transition_matrix, order))
print("Recommendation for (FD, CC):", recommend_next_product(('FD', 'CC'), transition_matrix, order))
