import pandas as pd
from collections import defaultdict

class MarkovModel:
    def __init__(self, order=1):
        """
        Initialize the Markov Model with a specified order.
        :param order: Order of the Markov Model (1 for first-order, 2 for second-order, etc.)
        """
        self.order = order
        self.transition_matrix = defaultdict(lambda: defaultdict(int))

    def fit(self, df):
        """
        Train the Markov Model on the given data.
        :param df: Pandas DataFrame with columns ['Client_ID', 'Product', 'Date_Acct_Open']
        """
        # Convert date column to datetime
        df['Date_Acct_Open'] = pd.to_datetime(df['Date_Acct_Open'])

        # Sort by Client_ID and Date_Acct_Open
        df = df.sort_values(by=['Client_ID', 'Date_Acct_Open'])

        # Create sequences of product take-up per customer
        sequences = defaultdict(list)

        for client, group in df.groupby('Client_ID'):
            products = list(group['Product'])
            for i in range(len(products) - self.order):
                prev_products = tuple(products[i:i + self.order])
                next_product = products[i + self.order]
                sequences[prev_products].append(next_product)

        # Count transitions
        for prev_products, next_products in sequences.items():
            for next_product in next_products:
                self.transition_matrix[prev_products][next_product] += 1

        # Normalize to create probabilities
        for prev_products, transitions in self.transition_matrix.items():
            total = sum(transitions.values())
            self.transition_matrix[prev_products] = {p: count / total for p, count in transitions.items()}

    def recommend(self, prev_products):
        """
        Recommend the next product based on the given sequence of previous product take-ups.
        :param prev_products: Tuple of previous products (length should match the model's order)
        :return: Recommended product or fallback option
        """
        prev_products = tuple(prev_products)

        # Check if the exact sequence exists
        if prev_products in self.transition_matrix:
            return max(self.transition_matrix[prev_products], key=self.transition_matrix[prev_products].get)

        # Fallback: Use lower-order Markov model if sequence is not found
        for i in range(1, self.order):
            reduced_seq = prev_products[i:]
            if reduced_seq in self.transition_matrix:
                return max(self.transition_matrix[reduced_seq], key=self.transition_matrix[reduced_seq].get)

        # Fallback: Recommend the most common first product
        all_transitions = defaultdict(int)
        for transitions in self.transition_matrix.values():
            for product, count in transitions.items():
                all_transitions[product] += count

        if all_transitions:
            return max(all_transitions, key=all_transitions.get)
        
        return None  # No recommendation if data is insufficient

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

# Train a second-order Markov model
markov = MarkovModel(order=2)
markov.fit(df)

# Example Recommendations
print("Recommendation for (SA, FD):", markov.recommend(('SA', 'FD')))
print("Recommendation for (SA, CC):", markov.recommend(('SA', 'CC')))
print("Recommendation for (SA, SA):", markov.recommend(('SA', 'SA')))
print("Recommendation for (FD, CC):", markov.recommend(('FD', 'CC')))
