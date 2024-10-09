def get_validated_input(prompt, valid_choices):
    asset_choice = input(prompt)

    while asset_choice not in valid_choices:
        asset_choice = input(f"Opção inválida. Por favor, selecione uma das opções disponíveis {valid_choices}: ")
    return asset_choice

def get_asset_selection_global():
    print("Selecione o grupo de ativos para análise:")
    print("(1) Ações Brasileiras")
    print("(2) Fundos Imobiliários Brasileiros")
    print("(3) Criptomoedas")
    print("(4) Cancelar operação")
    return get_validated_input("Digite sua escolha (1, 2, 3, ou 4): ", ['1', '2', '3', '4'])

def get_asset_selection_personal():
    print("Selecione a opção:")
    print("(1) Analisar meus Ativos")
    print("(2) Ver meus Ativos")
    print("(3) Ver minhas Transações")
    print("(4) Cancelar operação")
    return get_validated_input("Digite sua escolha (1, 2, 3, ou 4): ", ['1', '2', '3', '4'])
