import os

def main():
    readme_path = os.path.join(os.path.dirname(__file__), '..', '..', 'README.md')
    readme_path = os.path.abspath(readme_path)
    try:
        with open(readme_path, 'r') as file:
            print(file.read())
    except FileNotFoundError:
        print("README.md file not found")

if __name__ == '__main__':
    main()
