from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv('/app/backend/.env')

MONGO_URL = os.getenv("MONGO_URL")
client = MongoClient(MONGO_URL)
db = client["college_admission"]

db.colleges.delete_many({})

colleges_data = [
    # ===== IITs =====
    {"name":"IIT Bombay","location":"Mumbai","state":"Maharashtra","type":"IIT","nirf_rank":1,"branches":["Computer Science","Electrical","Mechanical","Civil","Chemical","Aerospace"],"fees_per_year":2.5,"hostel_fees":0.5,"total_fees":12.0,"placement_avg":21.5,"placement_highest":1.8,"facilities_rating":9.8,"campus_size":"550 acres","notable_alumni":["Sundar Pichai","Parag Agrawal","Nandan Nilekani"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":1,"closing_rank":66},{"year":2024,"branch":"Computer Science","category":"OBC","opening_rank":20,"closing_rank":25},{"year":2024,"branch":"Computer Science","category":"SC","opening_rank":3,"closing_rank":5},{"year":2024,"branch":"Computer Science","category":"ST","opening_rank":1,"closing_rank":2},
       {"year":2023,"branch":"Computer Science","category":"General","opening_rank":1,"closing_rank":63},{"year":2023,"branch":"Computer Science","category":"OBC","opening_rank":18,"closing_rank":23},
       {"year":2022,"branch":"Computer Science","category":"General","opening_rank":1,"closing_rank":60},{"year":2021,"branch":"Computer Science","category":"General","opening_rank":1,"closing_rank":58},
       {"year":2024,"branch":"Electrical","category":"General","opening_rank":150,"closing_rank":450},{"year":2024,"branch":"Mechanical","category":"General","opening_rank":600,"closing_rank":950},
     ]},
    {"name":"IIT Delhi","location":"Delhi","state":"Delhi","type":"IIT","nirf_rank":2,"branches":["Computer Science","Electrical","Mechanical","Civil","Chemical","Mathematics & Computing"],"fees_per_year":2.5,"hostel_fees":0.4,"total_fees":11.6,"placement_avg":20.8,"placement_highest":1.5,"facilities_rating":9.7,"campus_size":"525 acres","notable_alumni":["Vinod Khosla","Sachin Bansal","Arvind Kejriwal"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":67,"closing_rank":115},{"year":2024,"branch":"Computer Science","category":"OBC","opening_rank":26,"closing_rank":42},
       {"year":2023,"branch":"Computer Science","category":"General","opening_rank":64,"closing_rank":108},{"year":2022,"branch":"Computer Science","category":"General","opening_rank":61,"closing_rank":105},{"year":2021,"branch":"Computer Science","category":"General","opening_rank":59,"closing_rank":100},
       {"year":2024,"branch":"Mathematics & Computing","category":"General","opening_rank":116,"closing_rank":180},{"year":2024,"branch":"Electrical","category":"General","opening_rank":200,"closing_rank":550},
     ]},
    {"name":"IIT Madras","location":"Chennai","state":"Tamil Nadu","type":"IIT","nirf_rank":1,"branches":["Computer Science","Electrical","Mechanical","Civil","Chemical","Aerospace"],"fees_per_year":2.5,"hostel_fees":0.35,"total_fees":11.4,"placement_avg":19.5,"placement_highest":1.2,"facilities_rating":9.8,"campus_size":"617 acres","notable_alumni":["Raghuram Rajan","Kris Gopalakrishnan"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":116,"closing_rank":184},{"year":2024,"branch":"Computer Science","category":"OBC","opening_rank":43,"closing_rank":70},
       {"year":2023,"branch":"Computer Science","category":"General","opening_rank":109,"closing_rank":176},{"year":2022,"branch":"Computer Science","category":"General","opening_rank":106,"closing_rank":170},{"year":2021,"branch":"Computer Science","category":"General","opening_rank":103,"closing_rank":165},
       {"year":2024,"branch":"Electrical","category":"General","opening_rank":300,"closing_rank":680},
     ]},
    {"name":"IIT Kanpur","location":"Kanpur","state":"Uttar Pradesh","type":"IIT","nirf_rank":4,"branches":["Computer Science","Electrical","Mechanical","Civil","Chemical","Aerospace"],"fees_per_year":2.5,"hostel_fees":0.4,"total_fees":11.6,"placement_avg":18.9,"placement_highest":1.0,"facilities_rating":9.5,"campus_size":"1055 acres","notable_alumni":["Narayana Murthy","Roman Saini"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":185,"closing_rank":280},{"year":2024,"branch":"Computer Science","category":"OBC","opening_rank":71,"closing_rank":110},
       {"year":2023,"branch":"Computer Science","category":"General","opening_rank":177,"closing_rank":265},{"year":2022,"branch":"Computer Science","category":"General","opening_rank":170,"closing_rank":255},{"year":2021,"branch":"Computer Science","category":"General","opening_rank":165,"closing_rank":250},
       {"year":2024,"branch":"Electrical","category":"General","opening_rank":400,"closing_rank":850},
     ]},
    {"name":"IIT Kharagpur","location":"Kharagpur","state":"West Bengal","type":"IIT","nirf_rank":5,"branches":["Computer Science","Electrical","Mechanical","Civil","Chemical","Mining","Aerospace"],"fees_per_year":2.5,"hostel_fees":0.3,"total_fees":11.2,"placement_avg":17.8,"placement_highest":0.95,"facilities_rating":9.4,"campus_size":"2100 acres","notable_alumni":["Vinod Gupta","Aparajita Datta"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":281,"closing_rank":420},{"year":2024,"branch":"Computer Science","category":"OBC","opening_rank":111,"closing_rank":165},
       {"year":2023,"branch":"Computer Science","category":"General","opening_rank":266,"closing_rank":398},{"year":2022,"branch":"Computer Science","category":"General","opening_rank":258,"closing_rank":385},{"year":2021,"branch":"Computer Science","category":"General","opening_rank":250,"closing_rank":375},
       {"year":2024,"branch":"Electrical","category":"General","opening_rank":500,"closing_rank":1100},
     ]},
    {"name":"IIT Roorkee","location":"Roorkee","state":"Uttarakhand","type":"IIT","nirf_rank":6,"branches":["Computer Science","Electrical","Mechanical","Civil","Chemical","Architecture"],"fees_per_year":2.5,"hostel_fees":0.35,"total_fees":11.4,"placement_avg":16.5,"placement_highest":0.85,"facilities_rating":9.3,"campus_size":"365 acres","notable_alumni":["Binny Bansal","Ajit Doval"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":421,"closing_rank":600},{"year":2024,"branch":"Computer Science","category":"OBC","opening_rank":166,"closing_rank":235},
       {"year":2023,"branch":"Computer Science","category":"General","opening_rank":399,"closing_rank":570},{"year":2022,"branch":"Computer Science","category":"General","opening_rank":385,"closing_rank":550},{"year":2021,"branch":"Computer Science","category":"General","opening_rank":370,"closing_rank":535},
       {"year":2024,"branch":"Electrical","category":"General","opening_rank":700,"closing_rank":1350},
     ]},
    {"name":"IIT Hyderabad","location":"Hyderabad","state":"Telangana","type":"IIT","nirf_rank":8,"branches":["Computer Science","Electrical","Mechanical","Civil","Chemical"],"fees_per_year":2.5,"hostel_fees":0.4,"total_fees":11.6,"placement_avg":16.0,"placement_highest":0.80,"facilities_rating":9.2,"campus_size":"576 acres","notable_alumni":["Tech leaders","Researchers"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":601,"closing_rank":900},{"year":2024,"branch":"Computer Science","category":"OBC","opening_rank":236,"closing_rank":350},
       {"year":2023,"branch":"Computer Science","category":"General","opening_rank":575,"closing_rank":860},{"year":2022,"branch":"Computer Science","category":"General","opening_rank":555,"closing_rank":830},{"year":2021,"branch":"Computer Science","category":"General","opening_rank":540,"closing_rank":810},
       {"year":2024,"branch":"Electrical","category":"General","opening_rank":1000,"closing_rank":1800},
     ]},
    {"name":"IIT Guwahati","location":"Guwahati","state":"Assam","type":"IIT","nirf_rank":7,"branches":["Computer Science","Electrical","Mechanical","Civil","Chemical"],"fees_per_year":2.5,"hostel_fees":0.35,"total_fees":11.4,"placement_avg":15.5,"placement_highest":0.75,"facilities_rating":9.1,"campus_size":"706 acres","notable_alumni":["Tech entrepreneurs"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":901,"closing_rank":1300},{"year":2024,"branch":"Computer Science","category":"OBC","opening_rank":351,"closing_rank":510},
       {"year":2023,"branch":"Computer Science","category":"General","opening_rank":860,"closing_rank":1250},{"year":2022,"branch":"Computer Science","category":"General","opening_rank":830,"closing_rank":1200},{"year":2021,"branch":"Computer Science","category":"General","opening_rank":810,"closing_rank":1180},
       {"year":2024,"branch":"Electrical","category":"General","opening_rank":1400,"closing_rank":2500},
     ]},
    {"name":"IIT BHU","location":"Varanasi","state":"Uttar Pradesh","type":"IIT","nirf_rank":10,"branches":["Computer Science","Electrical","Mechanical","Civil","Chemical","Mining"],"fees_per_year":2.5,"hostel_fees":0.35,"total_fees":11.4,"placement_avg":15.0,"placement_highest":0.72,"facilities_rating":9.0,"campus_size":"1300 acres","notable_alumni":["Lal Bahadur Shastri"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":1301,"closing_rank":1800},{"year":2024,"branch":"Computer Science","category":"OBC","opening_rank":511,"closing_rank":700},
       {"year":2023,"branch":"Computer Science","category":"General","opening_rank":1250,"closing_rank":1720},{"year":2022,"branch":"Computer Science","category":"General","opening_rank":1200,"closing_rank":1660},{"year":2021,"branch":"Computer Science","category":"General","opening_rank":1160,"closing_rank":1600},
       {"year":2024,"branch":"Electrical","category":"General","opening_rank":2000,"closing_rank":3200},
     ]},
    {"name":"IIT Indore","location":"Indore","state":"Madhya Pradesh","type":"IIT","nirf_rank":12,"branches":["Computer Science","Electrical","Mechanical","Civil"],"fees_per_year":2.5,"hostel_fees":0.4,"total_fees":11.6,"placement_avg":14.5,"placement_highest":0.68,"facilities_rating":8.9,"campus_size":"510 acres","notable_alumni":["Young entrepreneurs"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":1801,"closing_rank":2600},{"year":2023,"branch":"Computer Science","category":"General","opening_rank":1721,"closing_rank":2480},{"year":2022,"branch":"Computer Science","category":"General","opening_rank":1661,"closing_rank":2380},{"year":2021,"branch":"Computer Science","category":"General","opening_rank":1601,"closing_rank":2300},
     ]},

    # ===== NITs =====
    {"name":"NIT Trichy","location":"Tiruchirappalli","state":"Tamil Nadu","type":"NIT","nirf_rank":9,"branches":["Computer Science","Electronics","Electrical","Mechanical","Civil","Chemical","Instrumentation"],"fees_per_year":1.5,"hostel_fees":0.3,"total_fees":7.2,"placement_avg":12.5,"placement_highest":0.45,"facilities_rating":8.9,"campus_size":"800 acres","notable_alumni":["Karthik Subbaraj"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":1850,"closing_rank":4820},{"year":2024,"branch":"Computer Science","category":"OBC","opening_rank":1200,"closing_rank":2950},{"year":2024,"branch":"Computer Science","category":"SC","opening_rank":380,"closing_rank":850},{"year":2024,"branch":"Computer Science","category":"ST","opening_rank":150,"closing_rank":320},
       {"year":2023,"branch":"Computer Science","category":"General","opening_rank":1780,"closing_rank":4650},{"year":2022,"branch":"Computer Science","category":"General","opening_rank":1720,"closing_rank":4500},{"year":2021,"branch":"Computer Science","category":"General","opening_rank":1680,"closing_rank":4400},
       {"year":2024,"branch":"Electronics","category":"General","opening_rank":5000,"closing_rank":9200},{"year":2024,"branch":"Electrical","category":"General","opening_rank":9500,"closing_rank":14800},
     ]},
    {"name":"NIT Warangal","location":"Warangal","state":"Telangana","type":"NIT","nirf_rank":10,"branches":["Computer Science","Electronics","Electrical","Mechanical","Civil","Chemical","Biotechnology"],"fees_per_year":1.5,"hostel_fees":0.25,"total_fees":7.0,"placement_avg":11.8,"placement_highest":0.42,"facilities_rating":8.8,"campus_size":"256 acres","notable_alumni":["Jayaprakash Narayan"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":2100,"closing_rank":5200},{"year":2024,"branch":"Computer Science","category":"OBC","opening_rank":1350,"closing_rank":3180},
       {"year":2023,"branch":"Computer Science","category":"General","opening_rank":2020,"closing_rank":5020},{"year":2022,"branch":"Computer Science","category":"General","opening_rank":1950,"closing_rank":4850},{"year":2021,"branch":"Computer Science","category":"General","opening_rank":1900,"closing_rank":4700},
       {"year":2024,"branch":"Electronics","category":"General","opening_rank":5500,"closing_rank":9800},
     ]},
    {"name":"NIT Surathkal","location":"Mangalore","state":"Karnataka","type":"NIT","nirf_rank":11,"branches":["Computer Science","Electronics","Electrical","Mechanical","Civil","Chemical","Information Technology"],"fees_per_year":1.5,"hostel_fees":0.28,"total_fees":7.12,"placement_avg":11.2,"placement_highest":0.38,"facilities_rating":8.7,"campus_size":"295 acres","notable_alumni":["Rajeev Suri"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":2500,"closing_rank":6200},{"year":2024,"branch":"Computer Science","category":"OBC","opening_rank":1580,"closing_rank":3750},
       {"year":2023,"branch":"Computer Science","category":"General","opening_rank":2400,"closing_rank":5980},{"year":2022,"branch":"Computer Science","category":"General","opening_rank":2350,"closing_rank":5800},{"year":2021,"branch":"Computer Science","category":"General","opening_rank":2300,"closing_rank":5650},
       {"year":2024,"branch":"Information Technology","category":"General","opening_rank":6500,"closing_rank":10200},
     ]},
    {"name":"NIT Rourkela","location":"Rourkela","state":"Odisha","type":"NIT","nirf_rank":16,"branches":["Computer Science","Electronics","Electrical","Mechanical","Civil","Chemical","Metallurgy"],"fees_per_year":1.4,"hostel_fees":0.25,"total_fees":6.6,"placement_avg":10.5,"placement_highest":0.35,"facilities_rating":8.5,"campus_size":"648 acres","notable_alumni":["Dilip Shanghvi"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":5500,"closing_rank":11200},{"year":2024,"branch":"Computer Science","category":"OBC","opening_rank":3200,"closing_rank":6800},
       {"year":2023,"branch":"Computer Science","category":"General","opening_rank":5320,"closing_rank":10850},{"year":2022,"branch":"Computer Science","category":"General","opening_rank":5150,"closing_rank":10500},{"year":2021,"branch":"Computer Science","category":"General","opening_rank":5000,"closing_rank":10200},
       {"year":2024,"branch":"Electronics","category":"General","opening_rank":11500,"closing_rank":17200},
     ]},
    {"name":"NIT Calicut","location":"Kozhikode","state":"Kerala","type":"NIT","nirf_rank":13,"branches":["Computer Science","Electronics","Electrical","Mechanical","Civil","Chemical"],"fees_per_year":1.45,"hostel_fees":0.3,"total_fees":7.0,"placement_avg":10.8,"placement_highest":0.38,"facilities_rating":8.6,"campus_size":"625 acres","notable_alumni":["K. Radhakrishnan"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":4200,"closing_rank":9500},{"year":2024,"branch":"Computer Science","category":"OBC","opening_rank":2500,"closing_rank":5800},
       {"year":2023,"branch":"Computer Science","category":"General","opening_rank":4050,"closing_rank":9180},{"year":2022,"branch":"Computer Science","category":"General","opening_rank":3920,"closing_rank":8900},{"year":2021,"branch":"Computer Science","category":"General","opening_rank":3800,"closing_rank":8650},
       {"year":2024,"branch":"Electronics","category":"General","opening_rank":9800,"closing_rank":15500},
     ]},
    {"name":"NIT Jaipur","location":"Jaipur","state":"Rajasthan","type":"NIT","nirf_rank":18,"branches":["Computer Science","Electronics","Electrical","Mechanical","Civil","Chemical"],"fees_per_year":1.4,"hostel_fees":0.26,"total_fees":6.64,"placement_avg":10.2,"placement_highest":0.35,"facilities_rating":8.4,"campus_size":"325 acres","notable_alumni":["Corporate executives"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":6800,"closing_rank":13500},{"year":2024,"branch":"Computer Science","category":"OBC","opening_rank":4200,"closing_rank":8200},
       {"year":2023,"branch":"Computer Science","category":"General","opening_rank":6600,"closing_rank":13100},{"year":2022,"branch":"Computer Science","category":"General","opening_rank":6400,"closing_rank":12800},{"year":2021,"branch":"Computer Science","category":"General","opening_rank":6200,"closing_rank":12500},
       {"year":2024,"branch":"Electronics","category":"General","opening_rank":14000,"closing_rank":21000},
     ]},
    {"name":"NIT Nagpur","location":"Nagpur","state":"Maharashtra","type":"NIT","nirf_rank":22,"branches":["Computer Science","Electronics","Electrical","Mechanical","Civil","Metallurgy"],"fees_per_year":1.4,"hostel_fees":0.25,"total_fees":6.6,"placement_avg":9.8,"placement_highest":0.32,"facilities_rating":8.3,"campus_size":"220 acres","notable_alumni":["Industry leaders"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":8200,"closing_rank":16500},{"year":2024,"branch":"Computer Science","category":"OBC","opening_rank":5100,"closing_rank":10200},
       {"year":2023,"branch":"Computer Science","category":"General","opening_rank":7900,"closing_rank":16000},{"year":2022,"branch":"Computer Science","category":"General","opening_rank":7700,"closing_rank":15500},
     ]},
    {"name":"NIT Kurukshetra","location":"Kurukshetra","state":"Haryana","type":"NIT","nirf_rank":24,"branches":["Computer Science","Electronics","Electrical","Mechanical","Civil","Information Technology"],"fees_per_year":1.4,"hostel_fees":0.24,"total_fees":6.56,"placement_avg":9.5,"placement_highest":0.30,"facilities_rating":8.2,"campus_size":"300 acres","notable_alumni":["Government officials"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":9500,"closing_rank":18200},{"year":2024,"branch":"Computer Science","category":"OBC","opening_rank":5900,"closing_rank":11500},
       {"year":2023,"branch":"Computer Science","category":"General","opening_rank":9200,"closing_rank":17600},{"year":2022,"branch":"Computer Science","category":"General","opening_rank":8900,"closing_rank":17000},
     ]},
    {"name":"NIT Silchar","location":"Silchar","state":"Assam","type":"NIT","nirf_rank":28,"branches":["Computer Science","Electronics","Electrical","Mechanical","Civil"],"fees_per_year":1.3,"hostel_fees":0.22,"total_fees":6.08,"placement_avg":8.5,"placement_highest":0.25,"facilities_rating":7.9,"campus_size":"625 acres","notable_alumni":["Engineers"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":15000,"closing_rank":28000},{"year":2024,"branch":"Computer Science","category":"OBC","opening_rank":9500,"closing_rank":17500},
       {"year":2023,"branch":"Computer Science","category":"General","opening_rank":14500,"closing_rank":27000},{"year":2022,"branch":"Computer Science","category":"General","opening_rank":14000,"closing_rank":26000},
     ]},
    {"name":"NIT Durgapur","location":"Durgapur","state":"West Bengal","type":"NIT","nirf_rank":25,"branches":["Computer Science","Electronics","Electrical","Mechanical","Civil","Metallurgy"],"fees_per_year":1.35,"hostel_fees":0.23,"total_fees":6.32,"placement_avg":9.2,"placement_highest":0.28,"facilities_rating":8.1,"campus_size":"187 acres","notable_alumni":["PSU professionals"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":11200,"closing_rank":22000},{"year":2024,"branch":"Computer Science","category":"OBC","opening_rank":7000,"closing_rank":13800},
       {"year":2023,"branch":"Computer Science","category":"General","opening_rank":10800,"closing_rank":21200},{"year":2022,"branch":"Computer Science","category":"General","opening_rank":10400,"closing_rank":20500},
     ]},
    {"name":"NIT Bhopal","location":"Bhopal","state":"Madhya Pradesh","type":"NIT","nirf_rank":30,"branches":["Computer Science","Electronics","Electrical","Mechanical","Civil"],"fees_per_year":1.3,"hostel_fees":0.22,"total_fees":6.08,"placement_avg":8.8,"placement_highest":0.26,"facilities_rating":8.0,"campus_size":"650 acres","notable_alumni":["Engineers"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":13500,"closing_rank":25500},{"year":2024,"branch":"Computer Science","category":"OBC","opening_rank":8500,"closing_rank":16000},
       {"year":2023,"branch":"Computer Science","category":"General","opening_rank":13000,"closing_rank":24500},{"year":2022,"branch":"Computer Science","category":"General","opening_rank":12500,"closing_rank":23500},
     ]},
    {"name":"NIT Jamshedpur","location":"Jamshedpur","state":"Jharkhand","type":"NIT","nirf_rank":32,"branches":["Computer Science","Electronics","Electrical","Mechanical","Civil","Metallurgy"],"fees_per_year":1.25,"hostel_fees":0.20,"total_fees":5.8,"placement_avg":8.2,"placement_highest":0.24,"facilities_rating":7.8,"campus_size":"340 acres","notable_alumni":["Steel industry pros"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":17500,"closing_rank":32000},{"year":2024,"branch":"Computer Science","category":"OBC","opening_rank":11000,"closing_rank":20000},
       {"year":2023,"branch":"Computer Science","category":"General","opening_rank":17000,"closing_rank":31000},{"year":2022,"branch":"Computer Science","category":"General","opening_rank":16500,"closing_rank":30000},
     ]},
    {"name":"NIT Patna","location":"Patna","state":"Bihar","type":"NIT","nirf_rank":26,"branches":["Computer Science","Electronics","Electrical","Mechanical","Civil"],"fees_per_year":1.28,"hostel_fees":0.21,"total_fees":5.96,"placement_avg":8.6,"placement_highest":0.25,"facilities_rating":7.9,"campus_size":"28 acres","notable_alumni":["Entrepreneurs"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":14200,"closing_rank":27000},{"year":2024,"branch":"Computer Science","category":"OBC","opening_rank":8900,"closing_rank":16800},
       {"year":2023,"branch":"Computer Science","category":"General","opening_rank":13800,"closing_rank":26000},{"year":2022,"branch":"Computer Science","category":"General","opening_rank":13400,"closing_rank":25000},
     ]},
    {"name":"NIT Allahabad","location":"Prayagraj","state":"Uttar Pradesh","type":"NIT","nirf_rank":21,"branches":["Computer Science","Electronics","Electrical","Mechanical","Civil","Information Technology"],"fees_per_year":1.38,"hostel_fees":0.24,"total_fees":6.48,"placement_avg":9.5,"placement_highest":0.31,"facilities_rating":8.2,"campus_size":"220 acres","notable_alumni":["IAS officers"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":10200,"closing_rank":19500},{"year":2024,"branch":"Computer Science","category":"OBC","opening_rank":6400,"closing_rank":12200},
       {"year":2023,"branch":"Computer Science","category":"General","opening_rank":9800,"closing_rank":18800},{"year":2022,"branch":"Computer Science","category":"General","opening_rank":9400,"closing_rank":18200},
     ]},
    {"name":"NIT Agartala","location":"Agartala","state":"Tripura","type":"NIT","nirf_rank":42,"branches":["Computer Science","Electronics","Electrical","Mechanical","Civil"],"fees_per_year":1.2,"hostel_fees":0.18,"total_fees":5.52,"placement_avg":6.5,"placement_highest":0.18,"facilities_rating":7.2,"campus_size":"500 acres","notable_alumni":["Regional engineers"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":28000,"closing_rank":48000},{"year":2023,"branch":"Computer Science","category":"General","opening_rank":27000,"closing_rank":46000},
     ]},
    {"name":"NIT Hamirpur","location":"Hamirpur","state":"Himachal Pradesh","type":"NIT","nirf_rank":38,"branches":["Computer Science","Electronics","Electrical","Mechanical","Civil"],"fees_per_year":1.25,"hostel_fees":0.20,"total_fees":5.8,"placement_avg":7.0,"placement_highest":0.20,"facilities_rating":7.5,"campus_size":"300 acres","notable_alumni":["IT professionals"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":20000,"closing_rank":38000},{"year":2023,"branch":"Computer Science","category":"General","opening_rank":19000,"closing_rank":36000},
     ]},
    {"name":"NIT Srinagar","location":"Srinagar","state":"Jammu & Kashmir","type":"NIT","nirf_rank":44,"branches":["Computer Science","Electronics","Electrical","Mechanical","Civil"],"fees_per_year":1.2,"hostel_fees":0.15,"total_fees":5.4,"placement_avg":6.0,"placement_highest":0.16,"facilities_rating":7.0,"campus_size":"240 acres","notable_alumni":["Regional leaders"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":32000,"closing_rank":55000},{"year":2023,"branch":"Computer Science","category":"General","opening_rank":30000,"closing_rank":52000},
     ]},
    {"name":"NIT Raipur","location":"Raipur","state":"Chhattisgarh","type":"NIT","nirf_rank":36,"branches":["Computer Science","Electronics","Electrical","Mechanical","Civil"],"fees_per_year":1.25,"hostel_fees":0.20,"total_fees":5.8,"placement_avg":7.5,"placement_highest":0.22,"facilities_rating":7.6,"campus_size":"350 acres","notable_alumni":["Engineers"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":18000,"closing_rank":34000},{"year":2023,"branch":"Computer Science","category":"General","opening_rank":17500,"closing_rank":33000},
     ]},

    # ===== IIITs =====
    {"name":"IIIT Hyderabad","location":"Hyderabad","state":"Telangana","type":"IIIT","nirf_rank":7,"branches":["Computer Science","Electronics","Computational Engineering"],"fees_per_year":3.5,"hostel_fees":0.4,"total_fees":15.6,"placement_avg":16.5,"placement_highest":0.75,"facilities_rating":9.2,"campus_size":"62 acres","notable_alumni":["Pavan Sondur","Gaurav Mittal"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":180,"closing_rank":750},{"year":2024,"branch":"Computer Science","category":"OBC","opening_rank":90,"closing_rank":380},
       {"year":2023,"branch":"Computer Science","category":"General","opening_rank":165,"closing_rank":710},{"year":2022,"branch":"Computer Science","category":"General","opening_rank":155,"closing_rank":680},{"year":2021,"branch":"Computer Science","category":"General","opening_rank":150,"closing_rank":660},
       {"year":2024,"branch":"Electronics","category":"General","opening_rank":800,"closing_rank":1850},
     ]},
    {"name":"IIIT Bangalore","location":"Bangalore","state":"Karnataka","type":"IIIT","nirf_rank":15,"branches":["Computer Science","Electronics"],"fees_per_year":3.8,"hostel_fees":0.45,"total_fees":17.0,"placement_avg":15.2,"placement_highest":0.62,"facilities_rating":8.9,"campus_size":"25 acres","notable_alumni":["Startup founders"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":850,"closing_rank":2100},{"year":2024,"branch":"Computer Science","category":"OBC","opening_rank":480,"closing_rank":1280},
       {"year":2023,"branch":"Computer Science","category":"General","opening_rank":800,"closing_rank":2020},{"year":2022,"branch":"Computer Science","category":"General","opening_rank":770,"closing_rank":1950},
     ]},
    {"name":"IIIT Delhi","location":"Delhi","state":"Delhi","type":"IIIT","nirf_rank":17,"branches":["Computer Science","Electronics","Computer Science & Design"],"fees_per_year":3.2,"hostel_fees":0.4,"total_fees":14.4,"placement_avg":14.8,"placement_highest":0.58,"facilities_rating":8.8,"campus_size":"25 acres","notable_alumni":["Product leaders at FAANG"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":950,"closing_rank":2350},{"year":2024,"branch":"Computer Science","category":"OBC","opening_rank":520,"closing_rank":1420},
       {"year":2023,"branch":"Computer Science","category":"General","opening_rank":900,"closing_rank":2250},{"year":2022,"branch":"Computer Science","category":"General","opening_rank":870,"closing_rank":2180},
     ]},
    {"name":"IIIT Allahabad","location":"Prayagraj","state":"Uttar Pradesh","type":"IIIT","nirf_rank":20,"branches":["Computer Science","Information Technology","Electronics"],"fees_per_year":2.8,"hostel_fees":0.35,"total_fees":12.6,"placement_avg":12.5,"placement_highest":0.42,"facilities_rating":8.5,"campus_size":"100 acres","notable_alumni":["Tech entrepreneurs"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":2800,"closing_rank":6500},{"year":2024,"branch":"Computer Science","category":"OBC","opening_rank":1650,"closing_rank":3950},
       {"year":2023,"branch":"Computer Science","category":"General","opening_rank":2700,"closing_rank":6300},{"year":2022,"branch":"Computer Science","category":"General","opening_rank":2620,"closing_rank":6100},
       {"year":2024,"branch":"Information Technology","category":"General","opening_rank":6800,"closing_rank":12200},
     ]},
    {"name":"IIIT Gwalior","location":"Gwalior","state":"Madhya Pradesh","type":"IIIT","nirf_rank":35,"branches":["Computer Science","Information Technology","Electronics"],"fees_per_year":2.5,"hostel_fees":0.3,"total_fees":11.2,"placement_avg":10.0,"placement_highest":0.35,"facilities_rating":8.0,"campus_size":"60 acres","notable_alumni":["Software engineers"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":5500,"closing_rank":12000},{"year":2023,"branch":"Computer Science","category":"General","opening_rank":5200,"closing_rank":11500},
     ]},
    {"name":"IIIT Lucknow","location":"Lucknow","state":"Uttar Pradesh","type":"IIIT","nirf_rank":40,"branches":["Computer Science","Information Technology"],"fees_per_year":2.2,"hostel_fees":0.25,"total_fees":9.8,"placement_avg":8.5,"placement_highest":0.28,"facilities_rating":7.8,"campus_size":"50 acres","notable_alumni":["IT professionals"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":8000,"closing_rank":16000},{"year":2023,"branch":"Computer Science","category":"General","opening_rank":7500,"closing_rank":15000},
     ]},
    {"name":"IIIT Kottayam","location":"Kottayam","state":"Kerala","type":"IIIT","nirf_rank":45,"branches":["Computer Science","Electronics"],"fees_per_year":2.0,"hostel_fees":0.25,"total_fees":9.0,"placement_avg":7.5,"placement_highest":0.22,"facilities_rating":7.5,"campus_size":"60 acres","notable_alumni":["Engineers"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":12000,"closing_rank":22000},{"year":2023,"branch":"Computer Science","category":"General","opening_rank":11500,"closing_rank":21000},
     ]},
    {"name":"IIIT Sri City","location":"Chittoor","state":"Andhra Pradesh","type":"IIIT","nirf_rank":43,"branches":["Computer Science","Electronics"],"fees_per_year":2.0,"hostel_fees":0.25,"total_fees":9.0,"placement_avg":7.2,"placement_highest":0.20,"facilities_rating":7.4,"campus_size":"80 acres","notable_alumni":["Tech professionals"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":14000,"closing_rank":26000},{"year":2023,"branch":"Computer Science","category":"General","opening_rank":13500,"closing_rank":25000},
     ]},

    # ===== EAMCET COLLEGES (TS & AP) =====
    {"name":"JNTU Hyderabad","location":"Hyderabad","state":"Telangana","type":"EAMCET","nirf_rank":55,"branches":["Computer Science","Electronics","Electrical","Mechanical","Civil","Information Technology"],"fees_per_year":0.35,"hostel_fees":0.15,"total_fees":2.0,"placement_avg":5.5,"placement_highest":0.18,"facilities_rating":7.5,"campus_size":"280 acres","notable_alumni":["Engineers","Government officials"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":500,"closing_rank":5500},{"year":2024,"branch":"Computer Science","category":"OBC","opening_rank":2000,"closing_rank":8000},
       {"year":2023,"branch":"Computer Science","category":"General","opening_rank":480,"closing_rank":5200},{"year":2022,"branch":"Computer Science","category":"General","opening_rank":460,"closing_rank":5000},
       {"year":2024,"branch":"Electronics","category":"General","opening_rank":6000,"closing_rank":15000},
     ]},
    {"name":"Osmania University","location":"Hyderabad","state":"Telangana","type":"EAMCET","nirf_rank":60,"branches":["Computer Science","Electronics","Electrical","Mechanical","Civil"],"fees_per_year":0.3,"hostel_fees":0.12,"total_fees":1.68,"placement_avg":4.8,"placement_highest":0.15,"facilities_rating":7.3,"campus_size":"1600 acres","notable_alumni":["Politicians","Scientists"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":1200,"closing_rank":8000},{"year":2024,"branch":"Computer Science","category":"OBC","opening_rank":3500,"closing_rank":12000},
       {"year":2023,"branch":"Computer Science","category":"General","opening_rank":1100,"closing_rank":7500},{"year":2022,"branch":"Computer Science","category":"General","opening_rank":1000,"closing_rank":7200},
     ]},
    {"name":"CBIT Hyderabad","location":"Hyderabad","state":"Telangana","type":"EAMCET","nirf_rank":48,"branches":["Computer Science","Electronics","Electrical","Mechanical","Civil","Information Technology"],"fees_per_year":1.8,"hostel_fees":0.3,"total_fees":8.4,"placement_avg":7.5,"placement_highest":0.25,"facilities_rating":8.2,"campus_size":"28 acres","notable_alumni":["IT professionals","Entrepreneurs"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":200,"closing_rank":2800},{"year":2024,"branch":"Computer Science","category":"OBC","opening_rank":800,"closing_rank":5500},
       {"year":2023,"branch":"Computer Science","category":"General","opening_rank":180,"closing_rank":2600},{"year":2022,"branch":"Computer Science","category":"General","opening_rank":160,"closing_rank":2500},
       {"year":2024,"branch":"Electronics","category":"General","opening_rank":3000,"closing_rank":8500},
     ]},
    {"name":"VNR VJIET Hyderabad","location":"Hyderabad","state":"Telangana","type":"EAMCET","nirf_rank":52,"branches":["Computer Science","Electronics","Electrical","Mechanical","Civil","Information Technology"],"fees_per_year":1.7,"hostel_fees":0.28,"total_fees":7.92,"placement_avg":6.8,"placement_highest":0.22,"facilities_rating":8.0,"campus_size":"20 acres","notable_alumni":["Software engineers"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":300,"closing_rank":3500},{"year":2024,"branch":"Computer Science","category":"OBC","opening_rank":1000,"closing_rank":6500},
       {"year":2023,"branch":"Computer Science","category":"General","opening_rank":280,"closing_rank":3300},{"year":2022,"branch":"Computer Science","category":"General","opening_rank":260,"closing_rank":3100},
     ]},
    {"name":"Vasavi College of Engineering","location":"Hyderabad","state":"Telangana","type":"EAMCET","nirf_rank":58,"branches":["Computer Science","Electronics","Electrical","Mechanical","Civil","Information Technology"],"fees_per_year":1.5,"hostel_fees":0.25,"total_fees":7.0,"placement_avg":6.2,"placement_highest":0.20,"facilities_rating":7.8,"campus_size":"15 acres","notable_alumni":["Tech professionals"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":400,"closing_rank":4200},{"year":2024,"branch":"Computer Science","category":"OBC","opening_rank":1500,"closing_rank":7800},
       {"year":2023,"branch":"Computer Science","category":"General","opening_rank":380,"closing_rank":4000},{"year":2022,"branch":"Computer Science","category":"General","opening_rank":360,"closing_rank":3800},
     ]},
    {"name":"Mahatma Gandhi IT (MGIT)","location":"Hyderabad","state":"Telangana","type":"EAMCET","nirf_rank":65,"branches":["Computer Science","Electronics","Electrical","Mechanical","Information Technology"],"fees_per_year":1.3,"hostel_fees":0.22,"total_fees":6.08,"placement_avg":5.5,"placement_highest":0.18,"facilities_rating":7.5,"campus_size":"12 acres","notable_alumni":["IT professionals"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":800,"closing_rank":6000},{"year":2024,"branch":"Computer Science","category":"OBC","opening_rank":2500,"closing_rank":10000},
       {"year":2023,"branch":"Computer Science","category":"General","opening_rank":750,"closing_rank":5700},{"year":2022,"branch":"Computer Science","category":"General","opening_rank":700,"closing_rank":5400},
     ]},
    {"name":"BVRIT Hyderabad","location":"Hyderabad","state":"Telangana","type":"EAMCET","nirf_rank":70,"branches":["Computer Science","Electronics","Mechanical","Information Technology"],"fees_per_year":1.4,"hostel_fees":0.25,"total_fees":6.6,"placement_avg":5.8,"placement_highest":0.18,"facilities_rating":7.6,"campus_size":"18 acres","notable_alumni":["Software developers"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":600,"closing_rank":5000},{"year":2023,"branch":"Computer Science","category":"General","opening_rank":550,"closing_rank":4700},
     ]},
    {"name":"CVR College of Engineering","location":"Hyderabad","state":"Telangana","type":"EAMCET","nirf_rank":72,"branches":["Computer Science","Electronics","Electrical","Mechanical","Civil"],"fees_per_year":1.2,"hostel_fees":0.20,"total_fees":5.6,"placement_avg":5.2,"placement_highest":0.15,"facilities_rating":7.4,"campus_size":"15 acres","notable_alumni":["Engineers"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":1500,"closing_rank":8500},{"year":2023,"branch":"Computer Science","category":"General","opening_rank":1400,"closing_rank":8000},
     ]},
    # AP EAMCET Colleges
    {"name":"JNTU Kakinada","location":"Kakinada","state":"Andhra Pradesh","type":"EAMCET","nirf_rank":62,"branches":["Computer Science","Electronics","Electrical","Mechanical","Civil","Information Technology"],"fees_per_year":0.35,"hostel_fees":0.12,"total_fees":1.88,"placement_avg":4.5,"placement_highest":0.14,"facilities_rating":7.2,"campus_size":"200 acres","notable_alumni":["Engineers","Academics"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":800,"closing_rank":7000},{"year":2024,"branch":"Computer Science","category":"OBC","opening_rank":2500,"closing_rank":10000},
       {"year":2023,"branch":"Computer Science","category":"General","opening_rank":750,"closing_rank":6500},{"year":2022,"branch":"Computer Science","category":"General","opening_rank":700,"closing_rank":6200},
     ]},
    {"name":"JNTU Anantapur","location":"Anantapur","state":"Andhra Pradesh","type":"EAMCET","nirf_rank":68,"branches":["Computer Science","Electronics","Electrical","Mechanical","Civil"],"fees_per_year":0.35,"hostel_fees":0.12,"total_fees":1.88,"placement_avg":4.0,"placement_highest":0.12,"facilities_rating":7.0,"campus_size":"250 acres","notable_alumni":["Regional engineers"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":2000,"closing_rank":12000},{"year":2023,"branch":"Computer Science","category":"General","opening_rank":1800,"closing_rank":11000},
     ]},
    {"name":"Andhra University","location":"Visakhapatnam","state":"Andhra Pradesh","type":"EAMCET","nirf_rank":56,"branches":["Computer Science","Electronics","Electrical","Mechanical","Civil"],"fees_per_year":0.4,"hostel_fees":0.12,"total_fees":2.08,"placement_avg":5.0,"placement_highest":0.15,"facilities_rating":7.4,"campus_size":"400 acres","notable_alumni":["Scientists","Politicians"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":600,"closing_rank":5000},{"year":2024,"branch":"Computer Science","category":"OBC","opening_rank":2000,"closing_rank":8500},
       {"year":2023,"branch":"Computer Science","category":"General","opening_rank":550,"closing_rank":4700},{"year":2022,"branch":"Computer Science","category":"General","opening_rank":520,"closing_rank":4500},
     ]},
    {"name":"SVNIT Surat","location":"Surat","state":"Gujarat","type":"NIT","nirf_rank":19,"branches":["Computer Science","Electronics","Electrical","Mechanical","Civil","Chemical"],"fees_per_year":1.45,"hostel_fees":0.28,"total_fees":6.92,"placement_avg":10.0,"placement_highest":0.34,"facilities_rating":8.4,"campus_size":"310 acres","notable_alumni":["Industry leaders"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":7500,"closing_rank":14800},{"year":2023,"branch":"Computer Science","category":"General","opening_rank":7200,"closing_rank":14200},{"year":2022,"branch":"Computer Science","category":"General","opening_rank":7000,"closing_rank":13800},
     ]},
    {"name":"NIT Goa","location":"Goa","state":"Goa","type":"NIT","nirf_rank":40,"branches":["Computer Science","Electronics","Electrical","Mechanical"],"fees_per_year":1.3,"hostel_fees":0.22,"total_fees":6.08,"placement_avg":8.0,"placement_highest":0.22,"facilities_rating":7.8,"campus_size":"200 acres","notable_alumni":["Engineers"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":16000,"closing_rank":30000},{"year":2023,"branch":"Computer Science","category":"General","opening_rank":15000,"closing_rank":28000},
     ]},
    {"name":"NIT Puducherry","location":"Puducherry","state":"Tamil Nadu","type":"NIT","nirf_rank":46,"branches":["Computer Science","Electronics","Electrical","Mechanical","Civil"],"fees_per_year":1.2,"hostel_fees":0.18,"total_fees":5.52,"placement_avg":7.0,"placement_highest":0.19,"facilities_rating":7.3,"campus_size":"180 acres","notable_alumni":["Engineers"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":22000,"closing_rank":40000},{"year":2023,"branch":"Computer Science","category":"General","opening_rank":21000,"closing_rank":38000},
     ]},
    {"name":"SRM University","location":"Chennai","state":"Tamil Nadu","type":"EAMCET","nirf_rank":33,"branches":["Computer Science","Electronics","Electrical","Mechanical","Civil","Information Technology","Aerospace"],"fees_per_year":3.0,"hostel_fees":0.5,"total_fees":14.0,"placement_avg":8.5,"placement_highest":0.42,"facilities_rating":8.5,"campus_size":"250 acres","notable_alumni":["Tech professionals"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":1000,"closing_rank":15000},{"year":2023,"branch":"Computer Science","category":"General","opening_rank":900,"closing_rank":14000},
     ]},
    {"name":"VIT Vellore","location":"Vellore","state":"Tamil Nadu","type":"EAMCET","nirf_rank":14,"branches":["Computer Science","Electronics","Electrical","Mechanical","Civil","Information Technology"],"fees_per_year":2.8,"hostel_fees":0.45,"total_fees":13.0,"placement_avg":9.5,"placement_highest":0.45,"facilities_rating":8.7,"campus_size":"320 acres","notable_alumni":["Startup founders","FAANG engineers"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":500,"closing_rank":10000},{"year":2023,"branch":"Computer Science","category":"General","opening_rank":450,"closing_rank":9500},
     ]},
    {"name":"BITS Pilani Hyderabad","location":"Hyderabad","state":"Telangana","type":"IIIT","nirf_rank":8,"branches":["Computer Science","Electronics","Electrical","Mechanical","Civil","Chemical"],"fees_per_year":5.0,"hostel_fees":0.6,"total_fees":22.4,"placement_avg":16.0,"placement_highest":0.70,"facilities_rating":9.0,"campus_size":"200 acres","notable_alumni":["Tech leaders"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":300,"closing_rank":2000},{"year":2023,"branch":"Computer Science","category":"General","opening_rank":280,"closing_rank":1900},{"year":2022,"branch":"Computer Science","category":"General","opening_rank":260,"closing_rank":1800},
     ]},
    {"name":"Manipal Institute of Technology","location":"Manipal","state":"Karnataka","type":"EAMCET","nirf_rank":25,"branches":["Computer Science","Electronics","Electrical","Mechanical","Civil","Information Technology"],"fees_per_year":4.0,"hostel_fees":0.5,"total_fees":18.0,"placement_avg":9.0,"placement_highest":0.40,"facilities_rating":8.6,"campus_size":"600 acres","notable_alumni":["Satya Nadella (attended nearby)"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":800,"closing_rank":12000},{"year":2023,"branch":"Computer Science","category":"General","opening_rank":750,"closing_rank":11000},
     ]},
    {"name":"Chaitanya Bharathi IT (CBIT Kurnool)","location":"Kurnool","state":"Andhra Pradesh","type":"EAMCET","nirf_rank":75,"branches":["Computer Science","Electronics","Mechanical"],"fees_per_year":1.0,"hostel_fees":0.18,"total_fees":4.72,"placement_avg":4.5,"placement_highest":0.12,"facilities_rating":7.0,"campus_size":"10 acres","notable_alumni":["Engineers"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":5000,"closing_rank":20000},{"year":2023,"branch":"Computer Science","category":"General","opening_rank":4500,"closing_rank":18000},
     ]},
    {"name":"Anurag University","location":"Hyderabad","state":"Telangana","type":"EAMCET","nirf_rank":80,"branches":["Computer Science","Electronics","Mechanical","Information Technology"],"fees_per_year":1.5,"hostel_fees":0.22,"total_fees":6.88,"placement_avg":5.0,"placement_highest":0.15,"facilities_rating":7.3,"campus_size":"25 acres","notable_alumni":["IT professionals"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":2000,"closing_rank":12000},{"year":2023,"branch":"Computer Science","category":"General","opening_rank":1800,"closing_rank":11000},
     ]},
    {"name":"VNRVJIET Women's Engineering","location":"Hyderabad","state":"Telangana","type":"EAMCET","nirf_rank":73,"branches":["Computer Science","Electronics","Information Technology"],"fees_per_year":1.6,"hostel_fees":0.25,"total_fees":7.4,"placement_avg":5.8,"placement_highest":0.18,"facilities_rating":7.5,"campus_size":"12 acres","notable_alumni":["Women engineers"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":1000,"closing_rank":8000},{"year":2023,"branch":"Computer Science","category":"General","opening_rank":900,"closing_rank":7500},
     ]},
    {"name":"GRIET Hyderabad","location":"Hyderabad","state":"Telangana","type":"EAMCET","nirf_rank":78,"branches":["Computer Science","Electronics","Electrical","Mechanical","Information Technology"],"fees_per_year":1.3,"hostel_fees":0.22,"total_fees":6.08,"placement_avg":5.0,"placement_highest":0.15,"facilities_rating":7.3,"campus_size":"15 acres","notable_alumni":["Software professionals"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":1200,"closing_rank":9000},{"year":2023,"branch":"Computer Science","category":"General","opening_rank":1100,"closing_rank":8500},
     ]},
    {"name":"Sreenidhi Institute of Science & Tech","location":"Hyderabad","state":"Telangana","type":"EAMCET","nirf_rank":82,"branches":["Computer Science","Electronics","Mechanical","Information Technology"],"fees_per_year":1.4,"hostel_fees":0.22,"total_fees":6.48,"placement_avg":4.8,"placement_highest":0.14,"facilities_rating":7.2,"campus_size":"20 acres","notable_alumni":["Engineers"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":2500,"closing_rank":14000},{"year":2023,"branch":"Computer Science","category":"General","opening_rank":2300,"closing_rank":13000},
     ]},
    {"name":"NIT Karnataka (NITK)","location":"Surathkal","state":"Karnataka","type":"NIT","nirf_rank":11,"branches":["Computer Science","Electronics","Electrical","Mechanical","Civil","Chemical","Information Technology"],"fees_per_year":1.5,"hostel_fees":0.28,"total_fees":7.12,"placement_avg":11.5,"placement_highest":0.40,"facilities_rating":8.7,"campus_size":"300 acres","notable_alumni":["Industry leaders"],
     "historical_cutoffs":[
       {"year":2024,"branch":"Computer Science","category":"General","opening_rank":2400,"closing_rank":6000},{"year":2024,"branch":"Computer Science","category":"OBC","opening_rank":1500,"closing_rank":3650},
       {"year":2023,"branch":"Computer Science","category":"General","opening_rank":2300,"closing_rank":5800},{"year":2022,"branch":"Computer Science","category":"General","opening_rank":2200,"closing_rank":5600},
       {"year":2024,"branch":"Information Technology","category":"General","opening_rank":6200,"closing_rank":11500},
     ]},
]

result = db.colleges.insert_many(colleges_data)
print(f"Seeded {len(result.inserted_ids)} colleges!")

db.colleges.create_index([("name", 1)])
db.colleges.create_index([("location", 1)])
db.colleges.create_index([("branches", 1)])
db.colleges.create_index([("total_fees", 1)])
db.colleges.create_index([("type", 1)])

print(f"Total colleges: {db.colleges.count_documents({})}")
types = db.colleges.aggregate([{"$group": {"_id": "$type", "count": {"$sum": 1}}}])
for t in types:
    print(f"  {t['_id']}: {t['count']}")
