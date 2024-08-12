# SkillSwap

SkillSwap is an innovative web application that facilitates skill exchange and collaborative learning. It connects individuals who are eager to learn from experts in specific fields with those who possess expertise in those areas. The core of SkillSwap’s value lies in its ability to offer valuable learning opportunities for free, in exchange for sharing your own knowledge and skills.

![SS1](https://github.com/VishRMehta/AI-Community-Skill-Swap/blob/master/Screenshot%202024-08-12%20at%2002.10.50.png)
![SS2](https://github.com/VishRMehta/AI-Community-Skill-Swap/blob/master/Screenshot%202024-08-12%20at%2002.11.14.png)

## Key Features

**Expert-Learner Matching**: Uses advanced AI techniques to match users based on skill compatibility and geographical proximity, ensuring meaningful and effective connections.

**Customizable Profiles**: Users can create detailed profiles, showcasing their skills and expertise, and specify areas they wish to learn more about.

**Intelligent Recommendations**: Employs machine learning algorithms to suggest optimal connections, facilitating efficient and relevant exchanges.

## How It Works:

**For Learners**: Gain free access to expert knowledge in areas of interest by offering your own skills in return. Whether you want to learn a new programming language, improve your design skills, or explore any other field, SkillSwap connects you with the right experts.

**For Experts**: Share your expertise with eager learners and gain insights from them. It’s a great way to give back, stay updated with industry trends, and network with like-minded professionals.


SkillSwap is designed to empower both learners and experts, fostering a community of knowledge sharing and personal growth. It’s more than just a platform—it’s a gateway to professional development and skill enhancement, driven by a culture of mutual benefit and collaboration.

## Features

- **User Profiles**: Create and update profiles with personal information, location, and skills.
- **AI-Driven Matchmaking**: 
  - **Skill Similarity**: Uses TF-IDF vectorization and cosine similarity to measure skill compatibility.
  - **Geographical Proximity**: Calculates distances between locations to adjust similarity scores.
  - **Combined Similarity**: Merges skill and geographical similarities to provide optimal match suggestions.
- **Search and Filter**: Search and filter profiles based on various criteria like name, location, and skills.
- **Responsive Design**: Optimized for both desktop and mobile devices.

## Technologies Used

- **Frontend**: React.js, CSS
- **Backend**: Django, Django REST Framework
- **Database**: PostgreSQL
- **AI/ML**: Scikit-learn, Pandas, Geopy
- **Deployment**: AWS Elastic Beanstalk, Docker

## Getting Started

### Prerequisites

- Node.js and npm (for frontend)
- Python and pip (for backend)
- Docker (optional, for containerized development)
- AWS CLI (for deployment)

### Frontend Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/skill_swap.git
   cd skill_swap/frontend
   npm install
   npm start
   ```
2. **Backend Setup**
   ```bash
   cd skill_swap/backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```
3. **Deployment on Docker**
   ```bash
   docker-compose up --build
   ```
   The frontend will be available at http://localhost:3000
   The backend will be available at http://localhost:8000
   
5. **Deployment on AWS**
   ```bash
   npm run build (in frontend folder)
   eb init
   eb deploy
   eb status
   eb logs
   ```
