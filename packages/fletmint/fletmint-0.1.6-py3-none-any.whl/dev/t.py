"""
import xml.etree.ElementTree as ET
import csv


def parse_kml_to_csv(kml_file, csv_file):
    # Define namespaces to handle prefixes in the KML file
    namespaces = {"kml": "http://www.opengis.net/kml/2.2"}

    # Parse the KML file
    tree = ET.parse(kml_file)
    root = tree.getroot()

    # Open the CSV file for writing with a specified delimiter
    with open(csv_file, mode="w", newline="") as file:
        writer = csv.writer(file, delimiter=";")  # Change delimiter to semicolon
        # Loop through each placemark in the KML file
        for placemark in root.findall(".//kml:Placemark", namespaces):
            # Find the LineString element
            linestring = placemark.find(".//kml:LineString/kml:coordinates", namespaces)
            if linestring is not None:
                # Split the coordinates string into individual coordinates
                coordinates = linestring.text.strip().split()
                # Loop through each coordinate string
                for coord in coordinates:
                    # Split each coordinate string into longitude, latitude, and elevation
                    lon, lat, elev = coord.split(",")
                    # Convert elevation to integer to remove any decimals
                    elev = int(float(elev))  # Converts to float first, then to integer
                    # Write to CSV file
                    writer.writerow([lat, lon, elev])


from pathlib import Path

# Path to your KML file
kml_file_path = "C:\\Users\\edoar\\Documents\\contours.kml"
# Path to your desired output CSV file
csv_file_path = "C:\\Users\\edoar\\Documents\\contours-ext-3.csv"

# Call the function with the paths
parse_kml_to_csv(kml_file_path, csv_file_path)
"""
import requests

cookies = {
    "_ga": "GA1.1.1794906617.1715765326",
    "disclaimer": "eyJpdiI6InhtSmVuYmE1bEFVOVVZdWVnYVFqZ1E9PSIsInZhbHVlIjoiMUUwajRRaXhua0ZXS1hieW1vSll3Zz09IiwibWFjIjoiY2Q4MTU3ZWY4ZjBmYjMzOGMyMDRlM2I3OTE1ZGIzNWMxMzZmM2ExMzhmMmNhYTA5YmY0MWNkNWFhZWQ2ODdmMiJ9",
    "XSRF-TOKEN": "eyJpdiI6ImMyR2syRFZ2WFRqOVlZWFNBQVlreUE9PSIsInZhbHVlIjoiYXA2eVFxQmhcL2RQV1ordm9zdnBraDAxNlh5MVI1Z01zTlJZdm1DVnlnZjZOVmtGWHd1VTVKR1V2SGx6U2JJRTJtdWxtOGlZclRabmt4TkY2M0pRYW13PT0iLCJtYWMiOiI3NWNlOWU2ZmI5NDkwYjQ4YTZlMTc0NWZkZjM0Y2FlMmJmNmQ1Mjc3NjhkZDJjOGM4YmFmYmI3MGQ3YmQ0YTMxIn0%3D",
    "erome_session": "eyJpdiI6InhyNWxHdFRIcit0azJlanhTbWpObWc9PSIsInZhbHVlIjoidzljU3N3XC9LZ3hRNXNTMDZFZjUwbnpiMisrUHhqUEZBRWY1RVZtcDgwY1g1M2s2YUVKSWNPVFJEZkd0eXE2SUtQXC9ETE1BXC9ESTR1RFRFc1IrbTk0RFE9PSIsIm1hYyI6ImQwNDY2NGJiMWQ5NmVhMDBjOTczNGIzNTZhOTI5NTIwMWYzZjcyZTcyM2ExZGUwZjYzOTA2YzNkNjNjMzBjZmMifQ%3D%3D",
    "_ga_6S5PBWQ8CG": "GS1.1.1715765325.1.1.1715765369.0.0.0",
}

headers = {
    "Accept": "*/*",
    "Accept-Language": "it,it-IT;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    # 'Cookie': '_ga=GA1.1.1794906617.1715765326; disclaimer=eyJpdiI6InhtSmVuYmE1bEFVOVVZdWVnYVFqZ1E9PSIsInZhbHVlIjoiMUUwajRRaXhua0ZXS1hieW1vSll3Zz09IiwibWFjIjoiY2Q4MTU3ZWY4ZjBmYjMzOGMyMDRlM2I3OTE1ZGIzNWMxMzZmM2ExMzhmMmNhYTA5YmY0MWNkNWFhZWQ2ODdmMiJ9; XSRF-TOKEN=eyJpdiI6ImMyR2syRFZ2WFRqOVlZWFNBQVlreUE9PSIsInZhbHVlIjoiYXA2eVFxQmhcL2RQV1ordm9zdnBraDAxNlh5MVI1Z01zTlJZdm1DVnlnZjZOVmtGWHd1VTVKR1V2SGx6U2JJRTJtdWxtOGlZclRabmt4TkY2M0pRYW13PT0iLCJtYWMiOiI3NWNlOWU2ZmI5NDkwYjQ4YTZlMTc0NWZkZjM0Y2FlMmJmNmQ1Mjc3NjhkZDJjOGM4YmFmYmI3MGQ3YmQ0YTMxIn0%3D; erome_session=eyJpdiI6InhyNWxHdFRIcit0azJlanhTbWpObWc9PSIsInZhbHVlIjoidzljU3N3XC9LZ3hRNXNTMDZFZjUwbnpiMisrUHhqUEZBRWY1RVZtcDgwY1g1M2s2YUVKSWNPVFJEZkd0eXE2SUtQXC9ETE1BXC9ESTR1RFRFc1IrbTk0RFE9PSIsIm1hYyI6ImQwNDY2NGJiMWQ5NmVhMDBjOTczNGIzNTZhOTI5NTIwMWYzZjcyZTcyM2ExZGUwZjYzOTA2YzNkNjNjMzBjZmMifQ%3D%3D; _ga_6S5PBWQ8CG=GS1.1.1715765325.1.1.1715765369.0.0.0',
    "Pragma": "no-cache",
    "Range": "bytes=0-",
    "Referer": "https://www.erome.com/",
    "Sec-Fetch-Dest": "video",
    "Sec-Fetch-Mode": "no-cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
    "sec-ch-ua": '"Chromium";v="124", "Microsoft Edge";v="124", "Not-A.Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
}

response = requests.get(
    "https://v55.erome.com/2573/KBIB4Vn5/o5t5uZL1_720p.mp4",
    cookies=cookies,
    headers=headers,
)

with open("video.mp4", "wb") as file:
    file.write(response.content)
