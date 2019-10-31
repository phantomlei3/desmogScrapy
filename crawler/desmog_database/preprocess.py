import requests

# take files of organization and convert it into url
# test.txt url and mark inaccessible urls with (not working)
def preprocess_organization_name_to_url(filename):
    output_file = ""
    output = open(output_file, "w")

    with open(filename) as file:
        for line in file:
            name = line.strip().lower()
            processed_name = name.replace("'", "").replace(" ", "-")
            url = "https://www.desmogblog.com/" + processed_name
            accessible = test_url(url)
            if accessible:
                output.write(url + "\n")
            else:
                output.write(name + "(not working)" + "\n")

def test_url(url):
    return requests.head(url).status_code == 200

if __name__ == '__main__':
    with open("desmog_organization_links.txt") as file:
        for line in file:
            if not test_url(line.strip()):
                print(False)

