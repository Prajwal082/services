from services.identity.azidentity import Azidentity

az = Azidentity()

print(az.get_access_token('.default'))

print(az.list_secrets('https://akv-prajwal.vault.azure.net/'))

print(az.get_secret('https://akv-prajwal.vault.azure.net/','general-spn-secret'))