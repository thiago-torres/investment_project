def get_user_asset_selection():
    print("Select the group of assets for analysis:")
    print("(1) Brazilian Assets")
    print("(2) Brazilian REITs")
    print("(3) Cryptocurrencies")
    print("(4) Cancel")
    asset_choice = input("Enter your choice (1, 2, 3, or 4): ")

    while asset_choice not in ['1', '2', '3', '4']:
        asset_choice = input("Invalid choice. Please select one of the available options (1, 2, 3, or 4): ")

    return asset_choice