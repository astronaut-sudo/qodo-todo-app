# To Do App Created by Qodo

**Architecture:**
- Frontend: Vue 3, with Ant Design Vue (for Antd icons/components)
- Backend: Python (FastAPI), SQLite for storage
- JWT-based user authentication
- Bonus: Password hashing, user-friendly error messages, and persistent session for logged-in user

**Get Started:**

BACKEND:
- Open a terminal and cd into the repo
- Navigate to backend directory using:
```
cd backend
```
- Install relevant libraries:
```
pip install -r requirements.txt
```
- Activate the Python virtual environment using:
```
source venv/bin/activate
```
- Start the FastAPI server:
```
uvicorn main:app --reload
```
If you run into errors with the uvicorn installation, you can also try:
```
python -m uvicorn main:app --reload
```
- The API will run at http://localhost:8000/

FRONTEND:
- Open a new terminal
- Go to frontend directory:
```
cd frontend
```
- Install dependencies once (if not done):
```
npm install
```
- Start the Vue dev server:
```
npm run dev
```
- Visit the frontend in your browser (default: http://localhost:5173/)

**Prompt:**
If you're curious, you can see the prompt I sent here (unless you also have access to it using logs):
```
Please create a usable To Do list app for me. Here are the requirements:
- Vue frontend, using Antd design icons for ease.
- SQLite backend to keep things simple
- Allow the user to log into their account, or create an account.
- Default page once logged in includes a text bar to enter a to do item, and the list of to do items below it.
- Allow the user to select medium, low, or high priority for a to-do item, and display it in three parts vertically next to each other.
- Allow user to select Not started, In progress, and completed as options for the progress of task. This should be viewed in each of the 3 priority verticals horizontally, or in a way that complies to an ease in UX.
- Add a separate page with a menu item to look at completed tasks. Don't show completed tasks on the same page.
- Add something that saves the time to the task.
- Add anything else you think i'm missing for a to-do list app (but mention it to me here)

After this, give me instructions to run the app locally and in a production environment!
```


**Screenshots:**

All screenshots are under the screenshots/ folder!
