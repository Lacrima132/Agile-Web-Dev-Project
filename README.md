# Agile-Web-Dev-Project

**Forum Project for Agile Web Dev**

Bountify is a dynamic platform designed to facilitate mercenary and trade opportunities across a fictional galaxy. It aims to empower users by providing direct access to lucrative missions, trade deals, and a vibrant community of fellow adventurers.

## Key Features

- **Post and Accept Bounties**:  
  Users can post bounties for specific missions or tasks they need help with and accept bounties posted by others. This system encourages collaboration and competition among users, fostering a thriving marketplace for mercenary activities.

- **Buy and Sell Weapons**:  
  The platform offers a marketplace where users can buy and sell weapons and other essential gear needed for their missions. This allows users to equip themselves adequately for the challenges they will face.

- **Community Interaction**:  
  Bountify hosts a forum where users can interact, share experiences, and learn from each other. Whether discussing strategies, sharing stories, or forming alliances, the community aspect is central to the Bountify experience.

- **User Profiles and Reputation**:  
  Each user has a profile where they can showcase their achievements and build a reputation within the community. This reputation system helps users gain trust and recognition for their skills and accomplishments.

## Team Members

|      Name      | Student ID |  Github Username |
|----------------|------------|------------------|
| Daniel Loo     | 23157127   | Lacrima132       |
| Helen Yang     | 23072751   | trebbyyy         |
| Aaron Chin     | 23286189   | aaroooooon       |
| Isabella Rowe  | 23159504   | ipr17            |


## User Journey

- **Sign Up and Log In**:  
  New users can sign up and create a profile, while existing users can log in to access their accounts. The sign-up process is straightforward, requiring basic information and preferences.

- **Explore the Forum**:  
  Once logged in, users can browse the forum to see the latest posts, bounties, and trade offers. The forum is designed to be intuitive and engaging, making it easy for users to find opportunities that interest them.

- **Post Bounties and Trade Offers**:  
  Users can post their own bounties and trade offers, specifying details and requirements. This creates a dynamic environment where supply and demand meet, and users can find partners for their ventures.

- **Engage and Interact**:  
  The interaction doesn't stop at the forum. Users can comment on posts, send messages, and build relationships with other members of the community. This engagement is crucial for fostering a sense of belonging and collaboration.

## How to Launch the Website

    $ git clone https://github.com/Lacrima132/Agile-Web-Dev-Project.git
    
- Either use the call: 

    $ /.installer.sh

- Or manually input the lines in installer.sh into the terminal 

## How to Run Tests

- Ensure you are in the directory that holds the tests folder
- Ensure you have Google Chrome installed on your system (or in your virtual environment):

      $ google-chrome --version

- If it is not installed (google-chrome: command not found):

      $ wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
      $ sudo dpkg -i google-chrome-stable_current_amd64.deb
      $ sudo apt-get install -f

- Ensure the flask app is running 
- From a new terminal:

      $ python -m unittest discover -s tests