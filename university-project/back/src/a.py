from passlib.context import CryptContext
import os

# Your existing CryptContext
crypt_context = CryptContext(schemes=["sha256_crypt", "md5_crypt"])


# Function to hash the amount with a random salt
def hash_amount_with_password(amount, password):
    # Convert the amount to a string before hashing
    amount_str = str(amount)

    # Generate a random salt for the sha256_crypt scheme
    salt = crypt_context.schemes["sha256_crypt"].using().gen_salt()

    # Use the CryptContext to hash the amount with the random salt and user's password
    hashed_amount = crypt_context.hash(amount_str + salt, scheme="sha256_crypt")

    return hashed_amount


# Function to unhash the amount with user's password
def unhash_amount_with_password(hashed_amount, password):
    # Verify the hashed amount using the user's password
    try:
        original_amount = float(crypt_context.verify(password, hashed_amount))
        return original_amount
    except ValueError:
        # Handle the case where the hash verification fails
        raise ValueError("Hash verification failed")


# Example usage
user_password = "user_password"  # Replace this with the user's actual password
amount = 100.50
hashed_amount = hash_amount_with_password(amount, user_password)

# Simulate the callback with the hashed amount
try:
    original_amount = unhash_amount_with_password(hashed_amount, user_password)
    print(f"Amount after unhashing: {original_amount}")
except ValueError as e:
    print(f"Error: {e}")
