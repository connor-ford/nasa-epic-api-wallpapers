import requests, os
from time import sleep

# config
image_type = "natural" # natural, enhanced, aerosol, cloud
wallpaper_path = "C:\\Users\\connor\\Documents\\wallpapers"

# ensure internet connection
while True:
    try:
        response = requests.get("https://www.google.com", timeout=5)
        print("Connected to internet.")
        break
    except requests.ConnectionError:
        print("Not connected to internet. Retrying in 5 seconds...")
        sleep(5)

# try to get list of images and handle exception if occurs.
try:
    response = requests.get(f"https://epic.gsfc.nasa.gov/api/{image_type}")
except requests.exceptions.RequestException as errex:
    print("Request Exception")
    print(errex)
    exit(1)

response = response.json()

# if no new images available, exit
ls = os.listdir(wallpaper_path)
if len(response) == len(ls) and response[0]["image"] + ".png" in ls:
    print("Images already up to date.")
    exit(0)

print(f"{len(response)} new images found.")

# delete old images
if (len(ls)):
    print(f"Removing {len(ls)} old images... ", end="")
    for old_image in ls:
        os.remove(f"{wallpaper_path}\{old_image}")
    print("Done.")

# download new images
for item in response:
    date = item["date"].split(" ")[0].split("-")

    print(
        "Downloading {0}... ".format(item["image"]),
        end="",
    )

    try:
        img_data = requests.get(
            f"https://epic.gsfc.nasa.gov/archive/{image_type}/{date[0]}/{date[1]}/{date[2]}/png/{item['image']}.png"
        )
    except requests.exceptions.RequestException as errex:
        print("Request Exception")
        print(errex)
        exit(1)

    with open(f"{wallpaper_path}/{item['image']}.png", "wb") as handler:
        handler.write(img_data.content)

    print("Done.")

print(f"{len(response)} images downloaded.")
