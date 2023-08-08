import cv2
import matplotlib.pyplot as plt
from faker import Faker
import random
import string
import json
import os

fake = Faker()

def create_name():
  first_name = fake.first_name()
  last_name = fake.last_name()

  return first_name, last_name

def create_date():
  possibilities = [f"{i:02}" for i in range(1, 99)]
  
  dd = random.choice(possibilities[:32])
  mm = random.choice(possibilities[:12])
  yy = random.choice(possibilities)

  return(dd+"."+mm+"."+yy)

def create_issuer():
  issuers = [
    "AUSTRIAN TRAFFIC DEPARTMENT",
    "DVLA",
    "RTD",
    "MINISTRY OF THE INTERIOR",
    "MINISTRY OF TRANSPORT",
    "TRANSPORT MALTA",
    "DEPARTMENT OF ROAD TRANSPORT",
    "NATIONAL TRANSPORT AUTHORITY",
    "DANISH ROAD DIRECTORATE",
    "MAANTEEAMET",
    "TRAFICOM",
    "NDLS",
    "RTSD"]
  
  issuer= random.sample(issuers, 1)
  string = ''.join(issuer)
  return string

def create_driver_id():
  driver_number = ''.join(random.choices('0123456789', k=9))

  return driver_number

def create_license_id():
  characters = string.digits + string.ascii_uppercase # Define the characters to choose from
  sequence_length = random.randint(8, 12) 
  random_sequence = ''.join(random.choices(characters, k=sequence_length))

  return random_sequence

def create_address_line_1():
  number = ''.join(random.choices('0123456789', k=3))
  st = fake.street_name()

  return number+" "+st

def create_address_line_2():
  state = fake.state()
  country = fake.country()
  postal = fake.postalcode()

  return state+" "+country+" "+postal

def create_categories():
    eu_driving_categories = ["AM", "A1", "A2", "A", "B1", "B", "BE", "C1", "C", "CE", "D1", "D1E"]

    num_categories = random.randint(1, 5)
    selected_categories = random.sample(eu_driving_categories, num_categories)

    return "/".join(selected_categories)

def add_text_to_image(image, text, position, font_size):
    
    # Choose a font and font scale
    font = cv2.FONT_HERSHEY_COMPLEX

    # Set font color as black
    font_color = (0,0,0)
    
    # Set position
    x, y = position

    # Font size
    size = font_size

    # Set default font thickness
    thickness = 1

    # Add the text to the image
    cv2.putText(image, text, (x, y), font, size, font_color, thickness, cv2.LINE_AA)

    # Return the modified image
    return image

def place_portrait(license, portrait, position):
    # Adjust size of the portrait to be placed
    portrait_resized = cv2.resize(portrait, (240, 350))

    # Set the position in which portrait should be centered
    x, y = position

    # Overlay the portrait on the image
    license[y:y + portrait_resized.shape[0], x:x + portrait_resized.shape[1]] = portrait_resized

    return license

# Determines paths for output files
output_licenses_dir = "licenses"
output_truth_table_dir = "jsons"

# (x, y) positions of each text field
last_name_position = (399, 179)  
first_name_position = (399, 210)
date_of_birth_pos = (399, 243)
date_of_issue_pos = (399, 277)
date_of_expiry_pos = (399, 309)
issuer_pos = (580, 277)
driver_id_pos = (580, 309)
license_id_pos = (399, 345)
address_1_pos = (399, 467)
address_2_pos = (399, 497)
categories_pos = (399, 566)
portrait_pos = (50, 220)

for j in range(5):
   
   # Creates data
   first_name, last_name = create_name()
   date_of_birth = create_date()
   date_of_issue = create_date()
   date_of_expiry = create_date()
   issuer = create_issuer()
   driver_id = create_driver_id()
   license_id = create_license_id()
   address_1 = create_address_line_1()
   address_2 = create_address_line_2()
   categories = create_categories()
   full_address = address_1 + " " + address_2 # this is for the truth table


   # Creates truth table
   data_dict = {
      "First Name": first_name,
      "Last Name": last_name,
      "Date of Birth": date_of_birth,
      "Date of Issue": date_of_issue,
      "Date of Expiry": date_of_expiry,
      "Issuing Agency": issuer,
      "Driver Number": driver_id,
      "License Number": license_id,
      "Address": full_address,
      "Categories": categories  
   }

   # Converts truth table to JSON and saves it
   json_output_path = os.path.join(output_truth_table_dir, f"generated_license_{j}.json")
   with open(json_output_path, "w") as json_file:
        json.dump(data_dict, json_file, indent=2)
    
   # Opens driver's license template
   license = cv2.imread("final_template.png")

   # Selects random portrait
   dataset_path = "faces"
   face_images = os.listdir(dataset_path) # Lists all portraits
   random_face_image = random.choice(face_images) # Choose random portrait
   portrait_path = os.path.join(dataset_path, random_face_image) # Loads portrait path
   portrait = cv2.imread(portrait_path)
   #mugshot = cv2.cvtColor(cv2.imread(mugshot_path), cv2.COLOR_BGR2RGB) # Loads portrait

   fields = [first_name, last_name, date_of_birth, date_of_issue, issuer, 
             date_of_expiry, driver_id, license_id, address_1, address_2, categories]
   
   locations = [first_name_position, last_name_position, date_of_birth_pos, date_of_issue_pos, 
                issuer_pos, date_of_expiry_pos, driver_id_pos, license_id_pos, address_1_pos,
                address_2_pos, categories_pos]
   
   font_sizes = [0.91, 0.91, 0.91, 0.82, 0.82, 0.82, 0.82, 0.91, 0.91, 0.91, 0.91]

   # Inserts text
   for i in range(len(fields)):
      license = add_text_to_image(license, fields[i], locations[i], font_sizes[i])
   
   # Inserts portrait
   license = place_portrait(license, portrait, portrait_pos)

   # Saves result
   output_path = os.path.join(output_licenses_dir, f"generated_license_{j}.png")
   cv2.imwrite(output_path, license)