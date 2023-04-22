import gdown

url = 'https://docs.google.com/spreadsheets/d/16aIJ6DJtZ7YX1N56d1HVvJJ45iiW_jTf5n0n1U7grKU/export?format=csv'
output = 'code.csv'
gdown.download(url, output, quiet=False)