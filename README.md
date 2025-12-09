# 🦉 **AI Scheduling Assistant**
**AI-Powered Semester Planning for University Students**

OwlSchedule is an intelligent academic planning assistant that helps university students build optimized semester schedules through a conversational interface.  
Students describe their preferences in natural language, and the system generates valid schedules based on real course data, academic progress, and custom constraints.

🔗 **Live Demo:** https://owl-xmrt.onrender.com/


## **Overview**

OwlSchedule streamlines course planning by combining:

- AI language understanding  
- Constraint-based scheduling  
- Academic progress tracking  
- A modern and friendly UI  

Students can request things like:

- Preferred days (M/W/F, T/Th)  
- No morning or no evening classes  
- GenEds they want to take  
- Professors to avoid  
- Credit minimum/maximum  
- Online vs. in-person mode  

The system then generates multiple schedule options, allows refinement, and saves the confirmed schedule to the student’s academic profile.


## **Features**

- AI Chat Interface — Natural-language schedule requests  
- Multiple schedule generation using **OR-Tools suite**
- Clean UI for schedule comparison**  
- Persistent conversation memory stored per user  
- Supabase-powered authentication and profile storage  
- Automatic academic progress tracking
- Online/offline course mode detection
- Fully deployed on Render (frontend + API services) 


## **Tech Stack**

### **Frontend**
- Vue 3 (Composition API)  
- Vue Router  
- TailwindCSS  
- Axios  

### **Backend**
OwlSchedule uses two separate backend services:

1. **Data API (FastAPI + Supabase)**  
   - Manages academic profiles  
   - Stores confirmed schedules  
   - Saves chat history  

2. **AI + Scheduling Engine**  
   - Handles dialog generation  
   - Runs scheduling with Google OR-Tools  
   - Applies university constraints to build valid schedules  

### **Other Tools**
- Supabase Auth + Postgres  
- Google Gemini API  
- Render cloud hosting  


## **How the System Works (Conceptually)**

- When the student sends a message, it is forwarded to the AI service.  
- The AI interprets the student's preferences and current academic info, and generates updated constraints.  
- The scheduling engine uses those constraints to create valid schedule combinations.  
- The Data API stores:
  - user profiles  
  - conversation history  
  - confirmed schedules  
  - updated academic progress  

This creates a smooth loop where the student can refine preferences until they’re satisfied, then save the newly-generated schedule for future reference.


## **Running Locally**

### **Frontend**
```python
cd frontend-static
npm install
npm run dev
```
### **Backend**
```python
pip install -r requirements.txt
uvicorn main:app --reload
```
### **ENV files**
```python
SUPABASE_URL=
SUPABASE_KEY=
AI_API_KEY=
```

## **Contributors**
Kseniya Chadovich - Project Lead & Full-Stack Developer

Kaen Zhang - Backend Developer & Database Engineer

Jingting Liu - Backend Developer (LLM Integration)

Fathima Hamna Mohamed Suhree - Frontend Developer & Supabase Auth

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.


## License

[MIT](https://choosealicense.com/licenses/mit/)

