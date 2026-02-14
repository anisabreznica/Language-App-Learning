# 🌍 LearnLang - Advanced Multilingual Learning Ecosystem

LearnLang nuk është thjesht një fjalor, por një sistem i plotë menaxhimi të nxënies (LMS) i optimizuar për shpejtësi dhe përdorshmëri. Ky projekt demonstron integrimin e një backend-i solid me një frontend modern "Glassmorphism".

---

## 🇦🇱 Detajet e Projektit (Albanian)

### 🧠 Logjika e Funksionimit
Aplikacioni bazohet në **Session Management**. Kur një përdorues zgjedh një gjuhë në Homepage, kjo zgjedhje ruhet në server-side session. Kjo lejon që të gjitha faqet pasardhëse (mësimet, provimet dhe certifikata) të adaptohen automatikisht pa pasur nevojë për ricarikim të të dhënave bazë.

### 🛡️ Siguria dhe Databaza
* **SQLite3:** Përdoret një arkitekturë relacionale për të lidhur përdoruesit me rezultatet e tyre (`User ID` -> `Scores`).
* **Zhbllokimi i Provimeve:** Sistemet e provimeve janë të lidhura me njëri-tjetrin; nuk mund të hysh në Provimin 2 pa kaluar me sukses Provimin 1 (Logic-Gate).

---

## 🇺🇸 Technical Deep Dive (English)

### ⚙️ Dynamic Content Rendering
The application uses **Jinja2 Templating** to filter data from a master dictionary. 
* **Universal Dictionary:** Instead of having 3 separate databases for each language, we use a single JSON-like structure where each word key contains values for `sq`, `en`, and `de`.
* **Smart Exams:** Questions are not hardcoded. The system pulls 10 random items from the selected week's category, shuffles the options, and ensures the correct answer matches the user's "Primary Language".

### 📊 Progress Calculation
Progress is calculated in real-time using the formula:
$$Total \% = \frac{\sum \text{Passed Exams}}{\text{Total Available Exams}} \times 100$$
When the counter reaches 100%, a hidden DOM element (Certificate Section) is triggered via JavaScript.

---

## 🇩🇪 Technische Details (German)

### 🏗️ Architektur und Design
* **Frontend-Stil:** Das Design nutzt "Glassmorphism" – eine Kombination aus Unschärfe (Backdrop-filter) und Transparenz, um eine saubere, futuristische Benutzeroberfläche zu schaffen.
* **Responsive Design:** Die Anwendung ist vollständig für Mobilgeräte optimiert, mit speziellen Media-Queries für die Zertifikatsansicht (A4-Skalierung).

### 🎓 Automatisierte Zertifizierung
Das Zertifikat ist kein statisches Bild. Es ist ein dynamisches HTML/CSS-Dokument, das:
1. Den Namen des Schülers aus der Datenbank zieht.
2. Ein zufälliges Zertifikats-ID-Format generiert.
3. Die Sprache basierend auf der Lernsprache (`learn_lang`) anpasst.

---

## 🛠 Tech Stack Summary

| Feature | Technology | Usage |
| :--- | :--- | :--- |
| **Server** | Python 3.x | Backend Logic & Routing |
| **Framework** | Flask | Web Micro-framework |
| **Database** | SQLite | User Data & Score Persistence |
| **Auth** | Flask Session | User Authentication & Lang Preference |
| **UI/UX** | CSS Grid/Flexbox | Responsive & Modern Layout |

---

## 🚀 Installation & Expert Usage

1. **Environment Setup:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install flask