import urllib.request
import sys
import time

RELIABLE_IMAGE_MAP = {
    "Aamir Khan": "https://upload.wikimedia.org/wikipedia/commons/6/65/Aamir_Khan_at_the_success_bash_of_Secret_Superstar.jpg",
    "Gabbar Singh": "https://upload.wikimedia.org/wikipedia/en/3/3c/Gabbar_Singh_(Amjad_Khan).jpg",
    "Sholay": "https://upload.wikimedia.org/wikipedia/en/thumb/5/52/Sholay-poster.jpg/400px-Sholay-poster.jpg",
    "3 Idiots": "https://upload.wikimedia.org/wikipedia/en/thumb/d/df/3_idiots_poster.jpg/400px-3_idiots_poster.jpg",
    "Alia Bhatt": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/10/Alia_Bhatt_at_Berlinale_2022_Ausschnitt.jpg/500px-Alia_Bhatt_at_Berlinale_2022_Ausschnitt.jpg",
    "Priyanka Chopra": "https://upload.wikimedia.org/wikipedia/commons/4/45/Priyanka_Chopra_at_Bulgary_launch%2C_2024_%28cropped%29.jpg",
    "Rajinikanth": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/Rajinikanth_in_2019.jpg/500px-Rajinikanth_in_2019.jpg",
    "Kareena Kapoor": "https://upload.wikimedia.org/wikipedia/commons/2/29/Kareena_Kapoor_Khan_in_2023_%281%29_%28cropped%29.jpg",
    "Hrithik Roshan": "https://upload.wikimedia.org/wikipedia/commons/9/92/Hrithik_Roshan_in_2024_%28cropped%29.jpg",
    "Akshay Kumar": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Akshay_Kumar_National_Award_for_Padman_%28cropped%29.jpg/500px-Akshay_Kumar_National_Award_for_Padman_%28cropped%29.jpg",
    "Katrina Kaif": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Katrina_Kaif_at_the_Bharat_audio_launch.jpg/500px-Katrina_Kaif_at_the_Bharat_audio_launch.jpg",
    "Ranveer Singh": "https://upload.wikimedia.org/wikipedia/commons/3/32/Ranveer_Singh_in_2023_%281%29_%28cropped%29.jpg",
    "Ranbir Kapoor": "https://upload.wikimedia.org/wikipedia/commons/a/a0/Ranbir_Kapoor_snapped_at_Kalina_airport.jpg",
    "Anushka Sharma": "https://upload.wikimedia.org/wikipedia/commons/e/e6/Anushka_Sharma_promoting_Zero.jpg",
    "Varun Dhawan": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Varun_Dhawan_at_Mehboob_Studios_in_2025_%28cropped%29.jpg/500px-Varun_Dhawan_at_Mehboob_Studios_in_2025_%28cropped%29.jpg",
    "Madhuri Dixit": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Madhuri_Dixit_in_November_2022.jpg/500px-Madhuri_Dixit_in_November_2022.jpg",
    "Sridevi": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Sridevi.jpg/500px-Sridevi.jpg",
    "Kajol": "https://upload.wikimedia.org/wikipedia/commons/4/41/Kajol_snapped_promoting_Maa_%28cropped%29.jpg",
    "Rishi Kapoor": "https://upload.wikimedia.org/wikipedia/commons/a/a7/Rishi_Kapoor_in_2016.jpg",
    "Dev Anand": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Dev_Anand_interacting_with_the_Press_at_the_36th_International_Film_Festival_of_India_%E2%80%93_2005_in_Panaji%2C_Goa_on_November_26%2C_2005.jpg/500px-Dev_Anand_interacting_with_the_Press_at_the_36th_International_Film_Festival_of_India_%E2%80%93_2005_in_Panaji%2C_Goa_on_November_26%2C_2005.jpg",
    "Lagaan": "https://upload.wikimedia.org/wikipedia/en/b/b6/Lagaan.jpg",
    "Dangal": "https://upload.wikimedia.org/wikipedia/en/9/99/Dangal_Poster.jpg",
    "Bahubali": "https://upload.wikimedia.org/wikipedia/en/5/5f/Baahubali_The_Beginning_poster.jpg",
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://www.wikipedia.org/'
}

print("Checking all image URLs...\n")
failed = []
ok = []
for name, url in RELIABLE_IMAGE_MAP.items():
    attempt_error = None
    for attempt in range(1, 4):
        try:
            req = urllib.request.Request(url, headers=headers)
            res = urllib.request.urlopen(req, timeout=15)
            code = res.getcode()
            if code == 200:
                ok.append(name)
                print(f"  OK  [{code}] {name}")
                attempt_error = None
                break
            else:
                attempt_error = f"HTTP {code}"
                print(f" RETRY [{attempt}] [{code}] {name}")
        except Exception as e:
            attempt_error = str(e)
            if '429' in str(e) and attempt < 3:
                print(f" RETRY [{attempt}] {name} due to 429")
            else:
                print(f" FAIL [ERR] {name} -> {e}")
                break
        time.sleep(2)
    if attempt_error:
        failed.append((name, url, attempt_error))

print(f"\n=== Summary: {len(ok)} OK, {len(failed)} FAILED ===")
for name, url, err in failed:
    print(f"  FAILED: {name}")
    print(f"    URL: {url}")
    print(f"    ERR: {err}")
