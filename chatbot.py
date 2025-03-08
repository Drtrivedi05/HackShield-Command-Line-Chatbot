import os
import random
import nltk
import time
from nltk.chat.util import Chat, reflections

# Chatbot Name
CHATBOT_NAME = "HackShield"

# List of Cybersecurity Jokes
cyber_jokes = [
    "Why don\'t hackers use elevators? Because they prefer to take the root! 😆",
    "Why did the computer go to therapy? Because it had too many issues! 😂",
    "Why was the cybersecurity expert so calm? Because he had two-factor authentication for his emotions! 🔐🤣",
    "Why did the hacker break up with his girlfriend? She kept changing her passwords! 😜",
    "What did the phishing email say to the victim? 'You've won a free trip to Malwareland!' 🎣🐟",
    "Why do programmers prefer dark mode? Because the light attracts too many bugs! 🌑🐛"
]

patterns = [
    # Greetings & Exit
    (r'hi|hello|hey|hii|hye|hola|yo', [f'Hello! I am {CHATBOT_NAME}. How can I help you today']),
    (r'how are you', [f'I am {CHATBOT_NAME}, your cybersecurity assistant. I am always ready to help!']),
    (r'what are you doing', ['I am here to assist you with cybersecurity questions!']),
    (r'who created you', ['I was created to help people learn about cybersecurity!']),
    (r'where are you from', ['I live in cyberspace, protecting digital systems!']),
    (r'tell me a joke', [lambda: random.choice(cyber_jokes)]),  # Picks a random joke
    (r'thank you|thanks', ['You\'re welcome! Always happy to help!']),
    (r'bye|goodbye', ['Goodbye! Stay safe online!']),
    (r'exit', [f'Thank you for using {CHATBOT_NAME}! Exiting in 5 seconds...']),

    # General Cybersecurity
    (r'what is cybersecurity', ['Cybersecurity is the practice of protecting systems, networks, and programs from cyber threats.']),
    (r'why is cybersecurity important', ['Cybersecurity helps prevent data breaches, cyberattacks, and identity theft.']),
    (r'what are the types of cybersecurity', ['Types include network security, application security, cloud security, and endpoint security.']),
    (r'what is CIA triad', ['The CIA triad stands for Confidentiality, Integrity, and Availability, the core principles of cybersecurity.']),

    # Network Security
    (r'what is network security', ['Network security involves securing network infrastructure from unauthorized access and threats.']),
    (r'what is a firewall', ['A firewall is a security device that monitors and controls incoming and outgoing traffic.']),
    (r'what is a proxy server', ['A proxy server acts as an intermediary between users and the internet for security and privacy.']),
    (r'what is a DMZ in networking', ['A DMZ (Demilitarized Zone) is a buffer zone between a trusted network and an untrusted one.']),
    (r'what are common network attacks', ['Common attacks include DoS, MITM, packet sniffing, and ARP poisoning.']),

    # Ethical Hacking
    (r'what is ethical hacking', ['Ethical hacking is the practice of testing security to identify vulnerabilities.']),
    (r'what is penetration testing', ['Penetration testing is simulating cyberattacks to find security weaknesses.']),
    (r'who are white hat hackers', ['White hat hackers use ethical hacking to improve security.']),
    (r'who are black hat hackers', ['Black hat hackers exploit vulnerabilities for malicious purposes.']),
    (r'who are grey hat hackers', ['Grey hat hackers work between ethical and unethical hacking.']),

    # Malware & Threats
    (r'what is malware', ['Malware is malicious software designed to damage or exploit systems.']),
    (r'what is a trojan horse', ['A trojan is malware that disguises itself as legitimate software.']),
    (r'what is a keylogger', ['A keylogger records keystrokes to steal sensitive information.']),
    (r'how does ransomware work', ['Ransomware encrypts files and demands payment for decryption.']),
    (r'what is a rootkit', ['A rootkit is hidden malware that allows unauthorized access to a system.']),

    # Phishing & Social Engineering
    (r'what is phishing', ['Phishing is a cyberattack that tricks users into revealing sensitive information.']),
    (r'how to prevent phishing', ['Avoid clicking unknown links, check URLs, and enable multi-factor authentication.']),
    (r'what is spear phishing', ['Spear phishing is a targeted phishing attack on a specific individual or organization.']),
    (r'what is vishing', ['Vishing is phishing conducted over phone calls.']),
    (r'what is smishing', ['Smishing is phishing through SMS messages.']),

    # Cryptography
    (r'what is cryptography', ['Cryptography is the practice of securing information through encryption.']),
    (r'what is symmetric encryption', ['Symmetric encryption uses a single key for encryption and decryption.']),
    (r'what is asymmetric encryption', ['Asymmetric encryption uses a public key for encryption and a private key for decryption.']),
    (r'what is hashing', ['Hashing converts data into a fixed-length string for integrity verification.']),
    (r'what is steganography', ['Steganography is hiding secret data within other files or media.']),

    # Security Practices
    (r'what is multi-factor authentication', ['MFA requires multiple verification methods for secure access.']),
    (r'how to create a strong password', ['Use uppercase, lowercase, numbers, and special characters.']),
    (r'what is social engineering', ['Social engineering manipulates people into revealing confidential information.']),
    (r'how can I secure my Wi-Fi', ['Use WPA3 encryption, change default credentials, and disable WPS.']),
    (r'what is a botnet', ['A botnet is a network of compromised devices controlled remotely for cyberattacks.']),

    # Cloud Security
    (r'what is cloud security', ['Cloud security protects cloud-based applications and data.']),
    (r'what is shared responsibility model', ['Cloud providers secure infrastructure, while users secure their data.']),
    (r'what is data encryption in the cloud', ['Data encryption protects cloud-stored data from unauthorized access.']),

    # Cybersecurity Careers
    (r'what are cybersecurity jobs', ['Cybersecurity careers include ethical hacker, security analyst, and forensic expert.']),
    (r'how to start a career in cybersecurity', ['Learn networking, get certifications, and gain hands-on experience.']),
    (r'what are the best cybersecurity certifications', ['Popular certifications include CEH, CISSP, and CompTIA Security+.']),

    # Emerging Threats
    (r'what is AI in cybersecurity', ['AI helps detect and prevent cyber threats using machine learning.']),
    (r'what is quantum cryptography', ['Quantum cryptography uses quantum mechanics to secure communications.']),
    (r'what is cyber warfare', ['Cyber warfare involves using digital attacks against governments or nations.']),

    # Cyber Law & Compliance
    (r'what is GDPR', ['GDPR is a European regulation for data protection and privacy.']),
    (r'what is HIPAA', ['HIPAA is a US law protecting healthcare data privacy.']),
    (r'what is PCI DSS', ['PCI DSS ensures secure handling of cardholder information.']),

    # Cyber Forensics
    (r'what is cyber forensics', ['Cyber forensics investigates digital crimes and security breaches.']),
    (r'what is a forensic image', ['A forensic image is an exact copy of digital evidence for investigation.']),
    (r'what are forensic tools', ['Tools include EnCase, Autopsy, and FTK for analyzing digital evidence.']),

    # Dark Web & Cybercrime
    (r'what is the dark web', ['The dark web is a hidden part of the internet accessible via Tor.']),
    (r'what is identity theft', ['Identity theft is stealing personal information for fraud.']),
    (r'how to report cybercrime', ['Report cybercrime to local authorities or cybersecurity agencies.']),

    # Cyber Attacks in India
    (r'how many cyberattacks happened in india', ['India witnessed over 13.91 lakh (1.39 million) cybersecurity incidents in 2022, as per CERT-In reports.']),
    (r'what are the most common cyberattacks in india', ['The most common attacks include phishing, ransomware, data breaches, DDoS attacks, and SIM swapping frauds.']),
    (r'what was the biggest cyberattack on an indian organization', ['One of the biggest attacks was on AIIMS (All India Institute of Medical Sciences) in 2022, where hackers demanded ₹200 crore in cryptocurrency.']),
    (r'which sectors in india are most vulnerable to cyberattacks', ['The banking, healthcare, government, and telecom sectors are the most targeted by cybercriminals.']),
    (r'what is the status of ransomware attacks in india', ['India is among the top 10 countries facing ransomware attacks, with over 80% of organizations reporting incidents in 2023.']),

    # Government Initiatives & Cybersecurity Laws
    (r'what is cert-in',['CERT-In (Indian Computer Emergency Response Team) monitors cyber threats, provides early warnings, and coordinates cybersecurity efforts in India.']),
    (r'what is the it act 2000',['The Information Technology (IT) Act 2000 is India\'s primary law for cybercrime, electronic transactions, and data protection.']),
    (r'what is the national cyber security policy',['The NCSP 2013 aims to protect critical infrastructure, develop cybersecurity skills, and encourage a secure cyberspace.']),
    (r'what is the digital personal data protection act 2023',['The Digital Personal Data Protection Act 2023 protects citizens\' personal data and regulates companies handling digital information.']),
    (r'what steps has the indian government taken to strengthen cybersecurity',['The government has implemented the National Cyber Security Strategy, made data breach reporting mandatory to CERT-In, launched the Cyber Surakshit Bharat initiative, created Cyber Swachhta Kendra for malware detection, and developed AI-based threat detection systems.']),

    # Cybercrime & Digital Arrests in India
    (r'how many cybercrime cases are reported in india annually',['Over 65,000+ cybercrime cases were reported in 2022, with fraud being the most common type of crime.']),
    (r'which city in india records the highest cybercrimes',['Hyderabad, Bengaluru, and Mumbai are among the top cities with the highest cybercrime cases.']),
    (r'what is the indian cyber crime coordination centre i4c',['The Indian Cyber Crime Coordination Centre (I4C) helps track and take action against cybercriminals, including digital arrests.']),
    (r'what was india\'s biggest digital arrest related to cybercrime',['In 2021, the Delhi Police arrested over 1,000 people involved in loan app scams and digital frauds.']),
    (r'how does india track cybercriminals',['Indian law enforcement agencies use AI-based tracking, call detail records (CDR), IP tracing, and digital forensic tools to track cybercriminals.']),

    # Cybersecurity Awareness & Best Practices in India
    (r'what is the cyber surakshit bharat initiative',['Cyber Surakshit Bharat is a government program launched in 2018 to educate officials and organizations about cyber hygiene and secure IT practices.']),
    (r'how can indian citizens report cyber fraud',['Citizens can report cybercrimes via:\n- Cybercrime helpline: 1930\n- Cybercrime portal: www.cybercrime.gov.in']),
    (r'what are the major cyber scams in india',['UPI frauds, fake KYC scams, OTP phishing, job scams, and cryptocurrency frauds are the most common cyber scams in India.']),
    (r'what is sim swapping fraud',['SIM swapping fraud is when hackers clone a victim\'s SIM card to gain access to bank accounts and OTPs, leading to financial fraud.']),
    (r'how can companies in india ensure cybersecurity compliance',['Companies should follow CERT-In\'s security guidelines, implement ISO 27001 cybersecurity standards, conduct regular cybersecurity audits, and ensure compliance with the Data Protection Act.']),


    # Default Response
    (r'(.*)', ['I am not sure I understand.', 'Could you please rephrase that', f'I am {CHATBOT_NAME}, and I can answer questions about cybersecurity.']),
]

chatbot = Chat(patterns, reflections)

def start_chat():
    print(f"Hello! I am {CHATBOT_NAME}, your cybersecurity chatbot. You can type 'exit' to leave.")
    while True:
        user_input = input("You: ").strip().lower()
        
        if user_input == "exit":
            print(f"{CHATBOT_NAME}: Thank you for using {CHATBOT_NAME}! Exiting in 5 seconds...")
            time.sleep(5)  # Wait for 3 seconds before exiting
            os._exit(0)  # Forcefully close the CMD
            break
        
        response = chatbot.respond(user_input)
        print(f"{CHATBOT_NAME}: {response}")

start_chat()
